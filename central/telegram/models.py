from pydantic import BaseModel
from typing import List, Optional


class TGChat(BaseModel):
    id: int
    first_name: str
    type: str


class TGWebAppData(BaseModel):
    button_text: str
    data: str


class TGMessage(BaseModel):
    message_id: int
    chat: TGChat
    date: int
    text: Optional[str] = None
    web_app_data: Optional[TGWebAppData] = None


class TGWebAppInfo(BaseModel):
    url: str


class TGInlineKeyboardBtn(BaseModel):
    """Parent class for all Inline Keyboard Buttons. \
        NOTE: Always use one of its children classes instead
    """
    text: str


class TGInlineKeyboardWebAppBtn(TGInlineKeyboardBtn):
    web_app: TGWebAppInfo


class TGInlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[List[TGInlineKeyboardWebAppBtn]]


class TGResponseMsg(BaseModel):
    chat_id: int
    text: str

    # Should be a JSON serialized repr of 'TGInlineKeyboardMarkup'
    reply_markup: Optional[str] = None
