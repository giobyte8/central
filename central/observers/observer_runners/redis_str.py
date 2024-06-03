import logging
from .base import ORunner
from ..models import RedisStringObserver
from ...services import rd_svc


logger = logging.getLogger(__name__)


class RedisStrORunner(ORunner):
    def __init__(self, observer: RedisStringObserver):
        self.__observer = observer

    async def observe(self):
        """Observes current value of redis key and compares against
        last observed value. If value has changed, runs observer
        actions.

        Previous value is retrieved from redis key: '{key}.last'.
        If it doesn't exists (e.g: First observation) it will
        be set to current value and no actions will run.
        """
        logger.debug(f'Running observer: {self.__observer.name}')

        last_value_key = f'{self.__observer.key}.last'
        last_value = await rd_svc.str_get(last_value_key)
        curr_value = await rd_svc.str_get(self.__observer.key)

        if not last_value:
            logger.info(f'No previous value for: { self.__observer.name }')
            await rd_svc.str_set(last_value_key, curr_value)
            return

        if curr_value != last_value:
            logger.debug(f'Value changed from: { last_value } to { curr_value }')
            await self.run_actions()
            await rd_svc.str_set(last_value_key, curr_value)
        else:
            logger.debug(f'Value did not change: { last_value }')

    async def run_actions(self):
        """Runs observer actions."""
        logger.debug(f'Running observer actions: {self.__observer.name}')
