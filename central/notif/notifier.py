import asyncio
import json
import central.utils.config as cfg
import logging
from central.notif.models import Notif
from central.services import redis_svc
from pydantic import ValidationError
from typing import Awaitable, Callable


logger = logging.getLogger(__name__)


__listeners = set()


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

        # Notify every subscribed listener about notification
        for listener in __listeners:
            await listener(notif)
    except ValidationError as e:
        logger.error('Invalid notification: %s', e)
    except json.JSONDecodeError as e:
        logger.error('Invalid JSON notification: %s', e)


async def subscribe(listener: Callable[[Notif], Awaitable[None]]) -> None:
    """Subscribe listener to be notified whenever a new notification \
        arrives

    Args:
        listener (Callable[[Notif], Awaitable[None]]): An async func that \
            receives a notifications and returns None
    """
    __listeners.add(listener)


async def unsubscribe(listener: Callable[[Notif], Awaitable[None]]) -> None:
    """Removes given listener from list of subscribers

    Args:
        listener (Callable[[Notif], Awaitable[None]]): listener to remove
    """
    __listeners.discard(listener)


async def start():
    try:
        await redis_svc.consume(cfg.queue_notif(), on_notif_msg)
    except asyncio.CancelledError:
        logger.debug('Cancelling service: notifier')
    finally:
        # TODO: Any raised error derives in connection closed
        await stop()


async def stop():
    await redis_svc.stop()
