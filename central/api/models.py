# generated by datamodel-codegen:
#   filename:  openapi.yaml
#   timestamp: 2024-11-28T05:20:41+00:00

from __future__ import annotations

from enum import Enum
from ipaddress import IPv4Address
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class HostStatus(BaseModel):
    ipv4Public: IPv4Address = Field(
        ..., description='External IPv4 address for the host.'
    )


class Notification(BaseModel):
    title: str = Field(..., description="Notification's title")
    content: str = Field(
        ..., description="Notification's body. Emojis are allowed here."
    )


class NotifDeliverySvc(Enum):
    TELEGRAM = 'telegram'
    WEBSOCKET = 'websocket'


class NotifSubscription(BaseModel):
    id: Optional[UUID] = Field(None, description='The UUID4 of the subscription.')
    notifDeliverySvc: NotifDeliverySvc = Field(
        ..., description='Name of service that will receive notifications.'
    )
    password: str = Field(
        ...,
        description='In order to receive notifications, subscription password must\nbe provided.\n',
    )
    servicePayload: Optional[str] = Field(
        None,
        description="This is a flexible field that can be used to transfer additonal\ninfo that might be required by notif delivery service:\n\n1. `telegram`: Init data string provided by telegram to embedded\n   'mini app'.\n\n   Value must be provided as passed by telegram to mini app\n   (without any modification) for validation on backend.\n\n   See: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app\n\n2. `websocket`: No additional info is required\n",
    )
