import logging
from central.utils import config as cfg
from central.telegram import api_client
from central.telegram.models import (
    TGMessage,
    TGResponseMsg,
    TGInlineKeyboardMarkup,
    TGInlineKeyboardWebAppBtn,
    TGWebAppInfo,
)


logger = logging.getLogger(__name__)


_TG_APP_AUTH_URL = f'{ cfg.tg_web_apps_url() }/auth.html'


async def on_command(msg: TGMessage):
    cmdparts = msg.text.split()
    cmd = cmdparts[0][1:]
    args = cmdparts[1:]
    logger.debug(
        'Handling command: %s %s',
        cmd,
        args if len(args) > 0 else '')

    cmd = _resolve_alias(cmd)
    if cmd == 'subscribe':
        await _on_subscribe(msg)

    # Invalid command
    # TODO Consider reply with a help message
    else:
        pass


async def _on_subscribe(msg: TGMessage):
    response_text = (
        f'Hello { msg.chat.first_name }! \n'
        'Please authenticate to receive notifications')

    auth_btn = TGInlineKeyboardWebAppBtn(
        text='🔐 Authenticate',
        web_app=TGWebAppInfo(url=_TG_APP_AUTH_URL))

    inline_keyboard = TGInlineKeyboardMarkup(inline_keyboard=[[auth_btn]])
    response = TGResponseMsg(
        chat_id=msg.chat.id,
        text=response_text,
        reply_markup=inline_keyboard.model_dump_json())

    await api_client.send_message(response)


def _resolve_alias(cmd: str) -> str:
    """Resolve commands aliases to its target command. \
        (e.g. Resolves 'sub' or 'subscribe' to 'subscribe' command)

    Args:
        cmd (str): Command alias to resolve

    Returns:
        str: Target command or None for invalid commands
    """
    if cmd in ['sub', 'subscribe']:
        return 'subscribe'
    else:
        return None
