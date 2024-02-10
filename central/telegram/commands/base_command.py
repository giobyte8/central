from central.telegram.models import (
    TGMessage,
    TGResponseMsg,
)
from typing import Optional


class Command:
    name: str
    args: 'list[str]'
    req_msg: TGMessage

    def __init__(self, name: str, args: 'list[str]', req_msg: TGMessage):
        self.name = name
        self.args = args
        self.req_msg = req_msg

    async def execute(self) -> Optional[TGResponseMsg]:
        raise NotImplementedError()
