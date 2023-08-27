import json
import central.utils.config as cfg
import logging
from central.notif.models import Notif
from central.services import redis_svc
from pydantic import ValidationError

logger = logging.getLogger(__name__)


async def on_notif_msg(msg: str):
    """Callback to be invoked upon notification message received from
    notifications queue

    Args:
        msg (str): Raw json notification from queue
    """
    logger.debug('Notification message received: %s', msg)

    try:
        j_notif = json.loads(msg)
        notif = Notif(**j_notif)

        print(f'Sending notif: { notif.title }')
    except ValidationError as e:
        logger.error('Invalid notification: %s', e)
    except json.JSONDecodeError as e:
        logger.error('Invalid JSON notification: %s', e)


async def start():
    await redis_svc.consume(cfg.queue_notif(), on_notif_msg)

