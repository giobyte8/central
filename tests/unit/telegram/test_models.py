import pytest
from central.telegram.tg_models import TGMessage
from pydantic import ValidationError


def test_load_invalid_msg():
    data = {
        'message_id': 321,
        'date': 1707251447,
        'text': 'Lorem Ipsum'
    }

    with pytest.raises(ValidationError):
        TGMessage(**data)


def test_load_text_msg():
    data = {
        'message_id': 321,
        'chat': {
            'id': 886441966,
            'first_name': 'Gio',
            'type': 'private'
        },
        'date': 1707251447,
        'text': 'Lorem Ipsum'
    }

    msg = TGMessage(**data)
    assert msg.message_id == 321
    assert msg.text == 'Lorem Ipsum'


def test_load_web_app_data_msg():
    data = {
        "message_id": 321,
        "from": {
            "id": 886441966,
            "is_bot": False,
            "first_name": "Gio",
            "language_code": "en"
        },
        "chat": {
            "id": 886441966,
            "first_name": "Gio",
            "type": "private"
        },
        "date": 1707251447,
        "web_app_data": {
            "button_text": "🔐 Authenticate",
            "data": "test data"
        }
    }

    msg = TGMessage(**data)
    assert msg.message_id == 321
    assert msg.web_app_data.data == 'test data'


def test_load_no_content_msg():
    """Even though not very usefull, since 'text' and 'web_app_data' are  \
        both optional fields, technically, we could have a message        \
        none of those fields assigned.
    """
    data = {
        'message_id': 321,
        'chat': {
            'id': 886441966,
            'first_name': 'Gio',
            'type': 'private'
        },
        'date': 1707251447,
    }

    msg = TGMessage(**data)
    assert msg.message_id == 321
    assert not msg.text
