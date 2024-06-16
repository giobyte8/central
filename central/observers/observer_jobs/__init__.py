import logging
from typing import List
from ..action_runners import action_runner_from
from ..action_runners.base import ARunner
from ..configstores.base import ConfigStore
from ..models import Observer, RedisStringObserver
from .base import ObserverJob
from .redis_str import RedisStrObserverJob


logger = logging.getLogger(__name__)


async def observer_job_from(
    observer: Observer,
    cfg_store: ConfigStore
) -> ObserverJob:
    if type(observer) == RedisStringObserver:
        on_change_actions: List[ARunner] = []
        for action_name in observer.on_change:
            action = cfg_store.find_action(action_name)
            if action is not None:
                on_change_actions.append(await action_runner_from(action))

        return RedisStrObserverJob(observer, on_change_actions)
    else:
        logger.warning(f'Observer type {type(observer)} not supported')
