import json
import logging
from central.utils import config as cfg
from central.services import redis_svc


logger = logging.getLogger(__name__)


async def enqueue(title: str, content: str) -> None:
    notif = { 'title': title, 'content': content }
    j_notif = json.dumps(notif)

    logger.debug('Enqueuing notification: %s', title)
    await redis_svc.list_rpush(cfg.queue_notif(), j_notif)
