import logging
from central.api.models import NotifSubscription, NotifDeliverySvc
from central.notif.errors import (
    NotifSubsInvalidError,
    NotifSubsAuthError,
)
from central.telegram import tg_notif_subs_svc as tg_nsubs_svc
from central.telegram.errors import (
    TGInitDataAuthError,
    TGInitDataParseError
)
from central.utils import config
from central.utils import crypto


logger = logging.getLogger(__name__)


async def create_subscription(sub: NotifSubscription):
    await _authenticate(sub)

    # Subscriptions service of each delivery service will take care of:
    #   1. Validate subscription data
    #   2. Prevent subscription duplication
    #   3. Create subscription and set uuid to object

    if sub.notif_delivery_svc == NotifDeliverySvc.TELEGRAM:
        try:
            sub_id = await tg_nsubs_svc.create_subscription(sub.servicePayload)
            sub.id = sub_id
        except TGInitDataAuthError:
            raise NotifSubsAuthError('TG Init data authentication failed')
        except TGInitDataParseError:
            raise NotifSubsInvalidError('TG Init data seems invalid')


async def _authenticate(sub: NotifSubscription) -> None:
    if not crypto.checkpw(sub.password, config.notif_feed_subs_pwd()):
        logger.warn(f'Invalid password in notifications subscription')
        raise NotifSubsAuthError('Password verification error')
