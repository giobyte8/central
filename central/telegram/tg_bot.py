import logging
from central.telegram import api_client, tg_cmd_svc
from central.telegram.models import (
    TGMessage
)


logger = logging.getLogger(__name__)


async def start():
    """Starts to constantly poll updates so that users can keep
    a conversation with bot
    """
    await api_client.poll_updates(on_message)


async def on_message(msg: TGMessage):
    if await _is_command(msg):
        await tg_cmd_svc.on_command(msg)
    else:
        logger.info('Non command message received: %s', msg.model_dump_json())


async def _is_command(msg: TGMessage) -> bool:
    if msg.text and msg.text.startswith('/'):
        return True
    if msg.web_app_data and msg.web_app_data.data.startswith('/'):
        return True

    return False
