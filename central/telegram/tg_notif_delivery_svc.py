import logging
from central.notif import notifier
from central.notif.models import Notif, NotifType
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
            parse_mode = None
            if notif.format is NotifType.MD:
                parse_mode = 'MarkdownV2'

            msg = TGResponseMsg(
                chat_id=chat_id,
                text=notif.content,
                parse_mode=parse_mode
            )
            await api_client.send_message(msg)


_notif_listener = TGNotifListener()


async def start() -> None:
    logger.debug('Starting TG notifications delivery service')
    await notifier.subscribe(_notif_listener)


async def stop() -> None:
    logger.debug('Stopping TG notifications delivery service')
    await notifier.unsubscribe(_notif_listener)
