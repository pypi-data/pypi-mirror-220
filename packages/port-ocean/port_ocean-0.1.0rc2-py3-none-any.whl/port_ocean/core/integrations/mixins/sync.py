import asyncio
from itertools import chain
from typing import Any, Awaitable

from loguru import logger

from port_ocean.clients.port.types import UserAgentType
from port_ocean.context.event import TriggerType, event_context, EventType
from port_ocean.context.ocean import ocean
from port_ocean.core.handlers.port_app_config.models import ResourceConfig
from port_ocean.core.integrations.mixins.events import EventsMixin
from port_ocean.core.integrations.mixins.handler import HandlerMixin
from port_ocean.core.models import Entity
from port_ocean.core.types import RawEntityDiff, EntityDiff, RESYNC_EVENT_LISTENER
from port_ocean.core.utils import validate_result, zip_and_sum
from port_ocean.exceptions.core import RawObjectValidationException, OceanAbortException
from port_ocean.utils import get_function_location


class SyncMixin(HandlerMixin, EventsMixin):
    def __init__(self) -> None:
        HandlerMixin.__init__(self)
        EventsMixin.__init__(self)

    async def register(
        self,
        entities: list[Entity],
        user_agent_type: UserAgentType,
    ) -> None:
        await self.entities_state_applier.upsert(entities, user_agent_type)
        logger.info("Finished registering change")

    async def unregister(
        self, entities: list[Entity], user_agent_type: UserAgentType
    ) -> None:
        await self.entities_state_applier.delete(entities, user_agent_type)
        logger.info("Finished unregistering change")

    async def sync(
        self,
        entities: list[Entity],
        user_agent_type: UserAgentType,
    ) -> None:
        entities_at_port = await ocean.port_client.search_entities(user_agent_type)

        await self.entities_state_applier.upsert(entities, user_agent_type)
        await self.entities_state_applier.delete_diff(
            {"before": entities_at_port, "after": entities}, user_agent_type
        )

        logger.info("Finished syncing change")


class SyncRawMixin(HandlerMixin, EventsMixin):
    def __init__(self) -> None:
        HandlerMixin.__init__(self)
        EventsMixin.__init__(self)

    async def _on_resync(self, kind: str) -> list[dict[Any, Any]]:
        raise NotImplementedError("on_resync must be implemented")

    async def _calculate_raw(
        self, raw_diff: list[tuple[ResourceConfig, RawEntityDiff]]
    ) -> list[EntityDiff]:
        logger.info("Calculating diff in entities between states")
        return await asyncio.gather(
            *(
                self.entity_processor.parse_items(mapping, results)
                for mapping, results in raw_diff
            )
        )

    async def _resync_function_wrapper(
        self, fn: RESYNC_EVENT_LISTENER, kind: str
    ) -> list[dict[str, Any]]:
        try:
            results = await fn(kind)
            return validate_result(results)
        except RawObjectValidationException as error:
            raise OceanAbortException(
                f"Failed to validate raw data for returned data from {get_function_location(fn)}, error: {error}"
            ) from error
        except Exception as error:
            raise OceanAbortException(
                f"Failed to execute {get_function_location(fn)}, error: {error}"
            ) from error

    async def _get_resource_raw_results(
        self, resource_config: ResourceConfig
    ) -> tuple[list[dict[str, Any]], list[Exception]]:
        logger.info(f"Fetching {resource_config.kind} resync results")
        tasks: list[Awaitable[list[dict[Any, Any]]]] = []
        with logger.contextualize(kind=resource_config.kind):
            if self.__class__._on_resync != SyncRawMixin._on_resync:
                tasks.append(
                    self._resync_function_wrapper(self._on_resync, resource_config.kind)
                )

            fns = [
                *self.event_strategy["resync"][resource_config.kind],
                *self.event_strategy["resync"][None],
            ]

            tasks.extend(
                [
                    self._resync_function_wrapper(resync_function, resource_config.kind)
                    for resync_function in fns
                ]
            )

            logger.info(f"Found {len(tasks)} resync tasks for {resource_config.kind}")

            results_with_error: list[
                tuple[list[dict[Any, Any]], Exception]
            ] = await asyncio.gather(*tasks, return_exceptions=True)
            results: list[dict[Any, Any]] = list(
                chain.from_iterable(
                    [
                        result
                        for result, _ in results_with_error
                        if not isinstance(result, Exception)
                    ]
                )
            )

            errors = [
                error for _, error in results_with_error if isinstance(error, Exception)
            ]

            logger.info(
                f"Triggered {len(tasks)} tasks for {resource_config.kind}, failed: {len(errors)}"
            )
            return results, errors

    async def _register_resource_raw(
        self,
        resource: ResourceConfig,
        results: list[dict[Any, Any]],
        user_agent_type: UserAgentType,
    ) -> list[Entity]:
        objects_diff = await self._calculate_raw(
            [
                (
                    resource,
                    {
                        "before": [],
                        "after": results,
                    },
                )
            ]
        )

        entities_after: list[Entity] = objects_diff[0]["after"]
        await self.entities_state_applier.upsert(entities_after, user_agent_type)
        return entities_after

    async def _unregister_resource_raw(
        self,
        resource: ResourceConfig,
        results: list[dict[Any, Any]],
        user_agent_type: UserAgentType,
    ) -> list[Entity]:
        objects_diff = await self._calculate_raw(
            [
                (
                    resource,
                    {
                        "before": results,
                        "after": [],
                    },
                )
            ]
        )

        entities_after: list[Entity] = objects_diff[0]["before"]
        await self.entities_state_applier.delete(entities_after, user_agent_type)
        logger.info("Finished unregistering change")
        return entities_after

    async def _register_in_batches(
        self,
        resource_config: ResourceConfig,
        user_agent_type: UserAgentType,
        batch_work_size: int | None,
    ) -> tuple[list[Entity], list[Exception]]:
        results, errors = await self._get_resource_raw_results(resource_config)

        tasks = []

        batch_size = batch_work_size or len(results) or 1
        batches = [
            results[i : i + batch_size] for i in range(0, len(results), batch_size)
        ]
        for batch in batches:
            logger.info(f"Creating task for registering batch of {len(batch)} entities")
            tasks.append(
                self._register_resource_raw(resource_config, batch, user_agent_type)
            )

        registered_entities_results = await asyncio.gather(*tasks)
        entities: list[Entity] = sum(registered_entities_results, [])
        logger.info(
            f"Finished registering change for {len(results)} raw results for kind: {resource_config.kind}"
        )
        return entities, errors

    async def register_raw(
        self,
        kind: str,
        results: list[dict[Any, Any]],
        user_agent_type: UserAgentType,
    ) -> list[Entity]:
        logger.info(f"Registering state for {kind}")
        config = await self.port_app_config_handler.get_port_app_config()
        resource_mappings = [
            resource for resource in config.resources if resource.kind == kind
        ]

        return await asyncio.gather(
            *(
                self._register_resource_raw(resource, results, user_agent_type)
                for resource in resource_mappings
            )
        )

    async def unregister_raw(
        self,
        kind: str,
        results: list[dict[Any, Any]],
        user_agent_type: UserAgentType,
    ) -> list[Entity]:
        logger.info(f"Registering state for {kind}")
        config = await self.port_app_config_handler.get_port_app_config()
        resource_mappings = [
            resource for resource in config.resources if resource.kind == kind
        ]

        return await asyncio.gather(
            *(
                self._unregister_resource_raw(resource, results, user_agent_type)
                for resource in resource_mappings
            )
        )

    async def update_raw_diff(
        self,
        kind: str,
        raw_desired_state: RawEntityDiff,
        user_agent_type: UserAgentType,
    ) -> None:
        logger.info(f"Updating state for {kind}")
        config = await self.port_app_config_handler.get_port_app_config()
        resource_mappings = [
            resource for resource in config.resources if resource.kind == kind
        ]

        with logger.contextualize(kind=kind):
            logger.info(f"Found {len(resource_mappings)} resources for {kind}")

            objects_diff = await self._calculate_raw(
                [(mapping, raw_desired_state) for mapping in resource_mappings]
            )

            entities_before, entities_after = zip_and_sum(
                (
                    (entities_change["before"], entities_change["after"])
                    for entities_change in objects_diff
                )
            )

            await self.entities_state_applier.apply_diff(
                {"before": entities_before, "after": entities_after}, user_agent_type
            )

    async def sync_raw_all(
        self,
        _: dict[Any, Any] | None = None,
        trigger_type: TriggerType = "machine",
        user_agent_type: UserAgentType = UserAgentType.exporter,
        silent: bool = True,
    ) -> None:
        logger.info("Resync was triggered")

        async with event_context(EventType.RESYNC, trigger_type=trigger_type):
            app_config = await self.port_app_config_handler.get_port_app_config()

            entities_at_port = await ocean.port_client.search_entities(user_agent_type)

            creation_results: list[
                tuple[list[Entity], list[Exception]]
            ] = await asyncio.gather(
                *(
                    self._register_in_batches(
                        resource, user_agent_type, ocean.config.batch_work_size
                    )
                    for resource in app_config.resources
                )
            )
            flat_created_entities, errors = zip_and_sum(creation_results)

            if not errors:
                await self.entities_state_applier.delete_diff(
                    {"before": entities_at_port, "after": flat_created_entities},
                    user_agent_type,
                )

            message = f"Resync failed with {len(errors)}. Skipping delete phase due to incomplete state"
            error_group = ExceptionGroup(
                f"Resync failed with {len(errors)}. Skipping delete phase due to incomplete state",
                errors,
            )
            if not silent:
                raise error_group

            logger.error(message, exc_info=error_group)
