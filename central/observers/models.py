from enum import Enum
from pydantic import BaseModel
from pydantic.networks import FileUrl, HttpUrl
from typing import Dict, List


class CTAction(BaseModel):
    name: str


class RedisListRPushAction(CTAction):
    list_key: str
    msg_template: str


class RenderTemplateAction(CTAction):
    template_path: FileUrl
    output_path: FileUrl


class DockerCtrStartAction(CTAction):
    container: str


class DockerCtrStopAction(CTAction):
    container: str


class CTObserver(BaseModel):
    name: str
    interval: int


class RedisStringObserver(CTObserver):
    key: str
    on_change: List[CTAction]


class _HttpVerb(Enum):
    get = 'GET'
    post = 'POST'
    put = 'PUT'
    delete = 'DELETE'
    patch = 'PATCH'
    head = 'HEAD'
    options = 'OPTIONS'


class HttpStatusRequest(BaseModel):
    endpoint: HttpUrl
    verb: _HttpVerb
    headers: Dict[str, str]
    params: Dict[str, str]


class HttpStatusObserver(CTObserver):
    request: HttpStatusRequest
    expected_status: int
    threshold: int
    actions_interval: List[int]
    on_unexpected_status: List[CTAction]
