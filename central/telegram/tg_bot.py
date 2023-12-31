import logging
from central.telegram import tg_api, tg_cmd_svc
from central.telegram.tg_models import (
    TGMessage
)


logger = logging.getLogger(__name__)


async def start():
    """Starts to constantly poll updates so that users can keep
    a conversation with bot
    """
    await tg_api.poll_updates(on_message)


async def on_message(msg: TGMessage):
    logger.debug('Message received: %s', msg.text)

    if len(msg.text) > 1 and msg.text.startswith('/'):
        await tg_cmd_svc.on_command(msg)
    else:
        logger.info('Message received: %s', msg.text)



