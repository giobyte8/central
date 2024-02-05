import logging
import uuid
from central.telegram import tg_init_data_svc as idata_svc
from central.telegram import unconfirmed_notif_subs_repo as unsubs_repo
from central.utils import config as cfg
from uuid import UUID


logger = logging.getLogger(__name__)


async def create_subscription(init_data: str) -> UUID:
    """Validates telegram init data and if it suceeds then creates an     \
        unconfirmed subscription to notifications feed.  Bot should       \
        confirm subscription in subsequent requests less than  10 mins    \
        from now, otherwise, unconfirmed subscription will expire.

    Args:
        init_data (str): Telegram init data

    Returns:
        UUID: Identifier of notifications subscription
    """
    await idata_svc.validate_init_data(init_data, cfg.tg_bot_token())

    # Generate uuid4 for new subscription
    sub_id = uuid.uuid4()

    await unsubs_repo.save(sub_id)
    return sub_id
