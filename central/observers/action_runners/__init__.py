import logging
from ..models import (
    Action,
    RedisListRPushAction
)
from .base import ARunner
from .redis_list_rpush_runner import RedisListRPushRunner


logger = logging.getLogger(__name__)


async def action_runner_from(action: Action) -> ARunner:
    if type(action) == RedisListRPushAction:
        return RedisListRPushRunner(action)
    else:
        logger.warning(f'Action type {type(action)} not supported')