from central.services import redis_svc
from central.utils import config
from typing import Set


__subs_chats_key = config.rd_tg_notif_subscribed_chats()


async def save(chat_id: int) -> None:
    """Saves given chat_id to set of chats subscribed to notifications

    Args:
        chat_id (int): Telegram chat id
    """
    await redis_svc.set_add(__subs_chats_key, str(chat_id))


async def get_all() -> Set[int]:
    """Gets all chats subscribed to notifications

    Returns:
        set[int]: Set of chats subscribed to notifications
    """
    return await redis_svc.set_members(__subs_chats_key)
