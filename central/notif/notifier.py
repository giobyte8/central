import asyncio
import json
import central.utils.config as cfg
import logging
from abc import ABC, abstractmethod
from central.notif.models import Notif
from central.services import redis_svc
from central.services.redis_svc import MessageConsumer
from pydantic import ValidationError
from typing import Set


logger = logging.getLogger(__name__)


class NotifListener(ABC):
    """Abstract notifications listener. Should be implemented by \
        subscribers in order to get notifications as it arrives

    Args:
        ABC (_type_): _description_
    """

    @abstractmethod
    async def on_notification(self, notif: Notif):
        """Callback to be invoked upon notification arrival

        Args:
            notif (Notif): Notification object
        """
        pass


_listeners: Set[NotifListener] = set()


async def subscribe(listener: NotifListener) -> None:
    """Subscribe listener to be notified whenever a new notification \
        arrives

    Args:
        listener (NotifListener): An implementation of NotifListener \
            interface
    """
    _listeners.add(listener)


async def unsubscribe(listener: NotifListener) -> None:
    """Removes given listener from list of subscribers

    Args:
        listener (NotifListener): listener to remove
    """
    _listeners.discard(listener)



class NotifMsgConsumer(MessageConsumer):
    """Message consumer for notifications queue"""

    async def on_message(self, msg: str):
        logger.debug('Notification message received: %s', msg)

        try:
            j_notif = json.loads(msg)
            notif = Notif(**j_notif)

            # Notify every subscribed listener about notification
            for listener in _listeners:
                await listener.on_notification(notif)
        except ValidationError as e:
            logger.error('Invalid notification: %s', e)
        except json.JSONDecodeError as e:
            logger.error('Invalid JSON notification: %s', e)


async def start():
    try:
        consumer = NotifMsgConsumer()
        await redis_svc.consume(cfg.queue_notif(), consumer)
    except asyncio.CancelledError:
        logger.debug('Cancelling service: notifier')
    finally:
        # TODO: Any raised error derives in connection closed
        await stop()


async def stop():
    await redis_svc.stop()
