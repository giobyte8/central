import uuid
from enum import Enum
from pydantic import BaseModel
from uuid import UUID


class NotifType(str, Enum):
    TEXT = 'text'
    MD = 'markdown'


class Notif(BaseModel):
    id: UUID = uuid.uuid4()
    type: NotifType = NotifType.TEXT
    title: str
    content: str
