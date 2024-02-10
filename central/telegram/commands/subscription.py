from central.telegram.commands.base_command import Command
from central.telegram.errors import InvalidCommandArgumentError
from central.telegram.models import (
    TGInlineKeyboardMarkup,
    TGInlineKeyboardWebAppBtn,
    TGMessage,
    TGResponseMsg,
    TGWebAppInfo,
)
from central.utils import config as cfg
from typing import Optional
from uuid import UUID


_TG_APP_AUTH_URL = f'{ cfg.tg_web_apps_url() }/auth.html'


class Subscription(Command):
    subcommand: Optional[Command]

    def __init__(self, args: 'list[str]', req_msg: TGMessage):
        super().__init__('subscription', args, req_msg)

        if args and args[0] == 'confirm':
            if len(args) != 2:
                raise InvalidCommandArgumentError(
                    'Invalid number of arguments for confirm command')
            self.subcommand = SubscriptionConfirm(args[1], req_msg)

    async def execute(self) -> Optional[TGResponseMsg]:
        if self.subcommand:
            return await self.subcommand.execute()

        # Ask for authentication to subscribe
        response_text = (
            f'Hello { self.req_msg.chat.first_name }! \n'
            'Please authenticate to receive notifications')

        auth_btn = TGInlineKeyboardWebAppBtn(
            text='🔐 Authenticate',
            web_app=TGWebAppInfo(url=_TG_APP_AUTH_URL))

        inline_keyboard = TGInlineKeyboardMarkup(inline_keyboard=[[auth_btn]])
        return TGResponseMsg(
            chat_id=self.req_msg.chat.id,
            text=response_text,
            reply_markup=inline_keyboard.model_dump_json())


class SubscriptionConfirm(Command):
    subscription_id: UUID

    def __init__(self, subs_id_arg: str, req_msg: TGMessage):
        super().__init__('confirm', [subs_id_arg], req_msg)

        # Parse subs_id_arg as uuid
        try:
            self.subscription_id = UUID(subs_id_arg)
        except ValueError:
            raise InvalidCommandArgumentError(
                f'Invalid subscription id: {subs_id_arg}'
            )

    async def execute(self) -> Optional[TGResponseMsg]:
        raise NotImplementedError()
