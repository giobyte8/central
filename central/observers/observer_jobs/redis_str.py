import logging
from typing import Any, Dict, List
from .base import ObserverJob
from ..action_runners.base import ARunner
from ..models import RedisStringObserver
from ...services import redis_svc


logger = logging.getLogger(__name__)


class RedisStrObserverJob(ObserverJob):
    def __init__(
        self,
        observer: RedisStringObserver,
        on_change_actions: List[ARunner]
    ):
        self.__observer = observer
        self.__on_change_actions = on_change_actions

    async def observe(self) -> None:
        """Observes current value of redis key and compares against
        last observed value. If value has changed, runs observer
        actions.

        Previous value is retrieved from redis key: '{key}.last'.
        If it doesn't exists (e.g: First observation) it will
        be set to current value and no actions will run.
        """
        logger.debug(f'Running observer: {self.__observer.name}')

        last_value_key = f'{self.__observer.key}.last'
        last_value = await redis_svc.str_get(last_value_key)
        curr_value = await redis_svc.str_get(self.__observer.key)

        if last_value is None:
            logger.info(f'No previous value for: { self.__observer.name }')

            if curr_value is not None:
                await redis_svc.str_set(last_value_key, curr_value)
            return

        if curr_value != last_value:
            logger.debug(f'Value changed from: { last_value } to { curr_value }')
            await self.run_actions(context={
                'redis_key_old_value': last_value,
                'redis_key_value': curr_value
            })
            await redis_svc.str_set(last_value_key, curr_value)

        else:
            logger.debug(f'Value did not change: { last_value }')

    async def run_actions(self, context: Dict[str, Any]) -> None:
        logger.debug(f'Running actions for observer: {self.__observer.name}')
        for a_runner in self.__on_change_actions:
            await a_runner.run(context)
