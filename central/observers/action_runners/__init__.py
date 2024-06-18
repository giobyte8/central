import logging
from ..models import (
    Action,
    DockerCtrStartAction,
    DockerCtrStopAction,
    RedisListRPushAction,
    RenderTemplateAction,
)
from .base import ARunner
from .docker_ctr_start_runner import DockerCtrStartRunner
from .docker_ctr_stop_runner import DockerCtrStopRunner
from .redis_list_rpush_runner import RedisListRPushRunner
from .render_template_runner import RenderTemplateRunner


logger = logging.getLogger(__name__)


async def action_runner_from(action: Action) -> ARunner:
    if type(action) == RedisListRPushAction:
        return RedisListRPushRunner(action)

    elif type(action) == RenderTemplateAction:
        return RenderTemplateRunner(action)

    elif type(action) == DockerCtrStartAction:
        return DockerCtrStartRunner(action)

    elif type(action) == DockerCtrStopAction:
        return DockerCtrStopRunner(action)

    else:
        logger.warning(f'Action type {type(action)} not supported')