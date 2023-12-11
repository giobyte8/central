from enum import Enum
from pydantic import BaseModel, Field, TypeAdapter
from pydantic.networks import FileUrl, HttpUrl
from pydantic.types import conlist
from typing import Dict, List, Literal, Union
from typing_extensions import Annotated


class CTAction(BaseModel):
    name: str


class RedisListRPushAction(CTAction):
    action_type: Literal['redis_list_rpush']
    list_key: str
    msg_template: str


class RenderTemplateAction(CTAction):
    action_type: Literal['render_template']
    template_path: FileUrl
    output_path: FileUrl


class DockerCtrStartAction(CTAction):
    action_type: Literal['docker_ctr_start']
    container: str


class DockerCtrStopAction(CTAction):
    action_type: Literal['docker_ctr_stop']
    container: str


ActionsUnion = Annotated[
    Union[
        RedisListRPushAction,
        RenderTemplateAction,
        DockerCtrStartAction,
        DockerCtrStopAction
    ],
    Field(discriminator='action_type')
]

# Use adapter to parse list of actions using discriminator field
# ref: https://stackoverflow.com/a/70917353/3211029
actionsAdapter = TypeAdapter(List[ActionsUnion])


class CTObserver(BaseModel):
    name: str
    interval: int


class RedisStringObserver(CTObserver):
    observer_type: Literal['redis_string']

    # From redis doc: You can use any binary sequence as a key,
    # from a string like "foo" to the content of a JPEG file.
    # https://redis.io/docs/manual/keyspace/
    #
    # Then, any string can be used as a key
    key: str

    # Value must be a list of several actions. Actions can be
    # of several types depending on value from 'action_type' field.
    #
    # https://docs.pydantic.dev/2.3/usage/types/unions/#discriminated-unions-aka-tagged-unions
    on_change: conlist(
        Union[
            RedisListRPushAction,
            RenderTemplateAction
        ],
        min_length=1
    ) = Field(..., discriminator='action_type')


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
    headers: Dict[str, str] = None
    params: Dict[str, str] = None


class HttpStatusObserver(CTObserver):
    observer_type: Literal['http_status']
    request: HttpStatusRequest
    expected_status: int
    threshold: int
    actions_interval: List[int]
    on_unexpected_status: conlist(CTAction, min_length=1)


ObserversUnion = Annotated[
    Union[
        RedisStringObserver,
        HttpStatusObserver,
    ],
    Field(discriminator='observer_type')
]

# Use adapter to parse list of objects using discriminator field
# ref: https://stackoverflow.com/a/70917353/3211029
observersAdapter = TypeAdapter(List[ObserversUnion])
