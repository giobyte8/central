import pytest
from central.telegram import tg_bot
from central.telegram.models import TGMessage
from unittest.mock import patch


@pytest.fixture
def msg_data():
    return {
        'message_id': 321,
        'chat': {
            'id': 886441966,
            'first_name': 'John',
            'type': 'private'
        },
        'date': 1707251447,
    }


@pytest.mark.asyncio
@patch('central.telegram.tg_bot.tg_cmd_svc.on_command')
async def test_non_command_msg(m_on_command, msg_data):
    msg = TGMessage(**msg_data)
    await tg_bot.on_message(msg)
    assert not m_on_command.called


@pytest.mark.asyncio
@patch('central.telegram.tg_bot.tg_cmd_svc.on_command')
async def test_non_command_text_msg(m_on_command, msg_data):
    msg_data['text'] = 'I\'m not a command'
    msg = TGMessage(**msg_data)
    await tg_bot.on_message(msg)
    assert not m_on_command.called


@pytest.mark.asyncio
@patch('central.telegram.tg_bot.tg_cmd_svc.on_command')
async def test_non_command_web_app_data_msg(m_on_command, msg_data):
    msg_data['web_app_data'] = {
        'button_text': '🔐 Authenticate',
        'data': 'I\'am not a command'
    }

    msg = TGMessage(**msg_data)
    await tg_bot.on_message(msg)
    assert not m_on_command.called


@pytest.mark.asyncio
@patch('central.telegram.tg_bot.tg_cmd_svc.on_command')
async def test_text_command_msg(m_on_command, msg_data):
    msg_data['text'] = '/start'

    msg = TGMessage(**msg_data)
    await tg_bot.on_message(msg)
    m_on_command.assert_called_once_with(msg)


@pytest.mark.asyncio
@patch('central.telegram.tg_bot.tg_cmd_svc.on_command')
async def test_web_app_data_command_msg(m_on_command, msg_data):
    msg_data['web_app_data'] = {
        'button_text': '🔐 Authenticate',
        'data': '/start'
    }

    msg = TGMessage(**msg_data)
    await tg_bot.on_message(msg)
    m_on_command.assert_called_once_with(msg)
