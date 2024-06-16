import logging
from typing import Any, Dict
from ...services import redis_svc
from ..models import RedisListRPushAction
from ..templates.str_template import StrTemplate
from .base import ARunner


logger = logging.getLogger(__name__)


class RedisListRPushRunner(ARunner):

    def __init__(self, action: RedisListRPushAction):
        self.action = action

    async def run(self, context: Dict[str, Any]) -> None:
        logger.info(f'Running redis_list_rpush action: { self.action.name }')

        msg = StrTemplate(self.action.msg_template).render(**context)
        await redis_svc.list_rpush(self.action.list_key, msg)
