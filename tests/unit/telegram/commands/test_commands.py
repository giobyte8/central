import pytest
from central.telegram.commands import commands as tg_cmd
from central.telegram.errors import InvalidCommandError
from central.telegram.models import TGMessage


def msg_with_attr(attr: dict) -> TGMessage:
    j_msg = {
        "message_id": 321,
        "chat": {
            "id": 886441966,
            "first_name": "Gio",
            "type": "private"
        },
        "date": 1707251447,
    }

    j_msg.update(attr)
    return TGMessage(**j_msg)


@pytest.mark.asyncio
@pytest.mark.parametrize('req_msg', [
    msg_with_attr({}),                  # No text command
    msg_with_attr({'text': '/start'}),  # Invalid command name
    msg_with_attr({'text': 'sub '}),    # Missing '/' prefix
    msg_with_attr({'web_app_data': {    # Web app data: No text command
        'button_text': 'a button',
        'data': ''
    }}),
    msg_with_attr({'web_app_data': {    # Web app: Invalid command name
        'button_text': 'a button',
        'data': '/wrong_command'
    }}),
    msg_with_attr({'web_app_data': {    # Web app: Missing '/' prefix
        'button_text': 'a button',
        'data': 'subscription'
    }}),
])
async def test_invalid_command(req_msg: TGMessage):
    with pytest.raises(InvalidCommandError):
        await tg_cmd.parse(req_msg)


@pytest.mark.asyncio
@pytest.mark.parametrize('req_msg', [
    msg_with_attr({'text': '/sub'}),
    msg_with_attr({'text': '/subscription with args'}),
    msg_with_attr({'web_app_data': {
        'button_text': 'a button',
        'data': '/sub with args'
    }}),
    msg_with_attr({'web_app_data': {
        'button_text': 'a button',
        'data': '/subscription'
    }}),
])
async def test_parse_subscription(req_msg: TGMessage):
    cmd = await tg_cmd.parse(req_msg)
    assert cmd.name == 'subscription'
    assert cmd.req_msg == req_msg
