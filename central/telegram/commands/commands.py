import logging
from central.telegram.commands.base_command import Command
from central.telegram.commands.subscription import Subscription
from central.telegram.errors import InvalidCommandError
from central.telegram.models import TGMessage


logger = logging.getLogger(__name__)


async def parse(msg: TGMessage) -> Command:
    cmd_text = None
    if msg.text:
        cmd_text = msg.text
    elif msg.web_app_data:
        cmd_text = msg.web_app_data.data

    if not cmd_text:
        raise InvalidCommandError('No command text')

    cmd_parts = cmd_text.split()
    cmd_name  = await _resolve_cmd_name(cmd_parts[0])
    cmd_args  = cmd_parts[1:]

    if cmd_name == 'subscription':
        return Subscription(cmd_args, msg)


async def _resolve_cmd_name(cmd_name: str) -> str:
    if cmd_name in ['/sub', '/subscription']:
        return 'subscription'
    raise InvalidCommandError(f'Unsupported command: {cmd_name}')
