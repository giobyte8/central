import logging
from central.notif import notifier
from central.notif.models import Notif
from central.notif.notifier import NotifListener
from central.telegram import api_client
from central.telegram.models import TGResponseMsg
from central.telegram.repositories import (
    notif_subscriptions as notif_subs_repo
)


logger = logging.getLogger(__name__)


class TGNotifListener(NotifListener):
    """Notifications Listener to forward to telegram subscribers"""

    async def on_notification(self, notif: Notif) -> None:
        """Delivers given notification to all subscribed telegram chats

        Args:
            notif (Notif): Notification to deliver
        """
        chat_ids = await notif_subs_repo.get_all()
        logger.debug('Delivering notification to %d chats', len(chat_ids))

        for chat_id in chat_ids:
            # TODO Consider using markdown for title and content
            msg = TGResponseMsg(chat_id=chat_id, text=notif.content)
            await api_client.send_message(msg)


_notif_listener = TGNotifListener()


async def start() -> None:
    logger.debug('Starting TG notifications delivery service')
    await notifier.subscribe(_notif_listener)


async def stop() -> None:
    logger.debug('Stopping TG notifications delivery service')
    await notifier.unsubscribe(_notif_listener)
