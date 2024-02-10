import logging
from central.telegram import api_client
from central.telegram.commands import commands
from central.telegram.errors import (
    InvalidCommandArgumentError,
    InvalidCommandError,
)
from central.telegram.models import TGMessage


logger = logging.getLogger(__name__)


async def on_command(msg: TGMessage):
    try:
        cmd = await commands.parse(msg)

        logger.debug('Executing command: %s', cmd.name)
        res = await cmd.execute()

        if res:
            await api_client.send_message(res)
    except InvalidCommandError as e:
        logger.debug('Invalid command: %s', e)
        # TODO Reply with a 'Sorry, what?' message
    except InvalidCommandArgumentError as e:
        logger.debug('Invalid command argument: %s', e)
        # TODO Reply with a 'Sorry, what?' message
    except Exception as e:
        logger.error('Error while executing command: %s', e)
