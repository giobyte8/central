from enum import Enum
from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator
from pydantic.networks import FileUrl, HttpUrl
from typing import Dict, List
from typing_extensions import Annotated


def is_semi_alphanumeric(value: str) -> str:
    """Validates given string contains only chars from \
        A-Z, a-z, '_' and '-'

    Args:
        value (str): String to validate

    Raises:
        ValueError: In case provided string is not semi alphanumeric
    """
    if not value:
        raise ValueError('Value cannot be empty')

    # Verify that string contains only chars from A-Z, a-z, '_' and '-'
    if not value.replace('_', '').replace('-', '').isalnum():
        raise ValueError(f'Value "{value}" contains invalid chars')

    return value


# Custom defined types
SemiAlphaNum = Annotated[str, AfterValidator(is_semi_alphanumeric)]


###############################################################################
# Actions models

class Action(BaseModel):
    name: SemiAlphaNum


class RedisListRPushAction(Action):
    list_key: str = Field(min_length=1)
    msg_template: str


class RenderTemplateAction(Action):
    template_path: FileUrl
    output_path: FileUrl


class DockerCtrStartAction(Action):
    container: str


class DockerCtrStopAction(Action):
    container: str


###############################################################################
# Observers definitions

class Observer(BaseModel):
    name: SemiAlphaNum
    interval: int = Field(ge=1)


class RedisStringObserver(Observer):

    # From redis doc: You can use any binary sequence as a key,
    # from a string like "foo" to the content of a JPEG file.
    # https://redis.io/docs/manual/keyspace/
    key: str = Field(min_length=1)

    on_change: List[SemiAlphaNum] = Field(min_length=1)


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


class HttpStatusObserverState(Enum):
    ok = 'ok'
    triggered = 'triggered'


class HttpStatusObserver(Observer):
    state: HttpStatusObserverState = HttpStatusObserverState.ok

    request: HttpStatusRequest
    expected_status: int = Field(ge=100, le=599)
    threshold: int
    actions_interval: List[int]
    on_unexpected_status: List[SemiAlphaNum] = Field(min_length=1)
