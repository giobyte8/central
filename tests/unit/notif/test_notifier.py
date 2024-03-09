import asyncio
import json
import pytest
from unittest.mock import MagicMock

from central.notif import notifier
from central.notif.models import Notif


@pytest.fixture(scope='module')
def j_notif() -> str:
    notif = {
        'uuid': '8ef67d5c-f650-4f73-9099-f225be223d2a',
        'type': 'text',
        'title': 'Test Notif',
        'content': 'lorem...',
    }

    return json.dumps(notif)


@pytest.mark.asyncio
async def test_subscribe_listener(j_notif: str):
    future = asyncio.Future()
    future.set_result(None)
    listener = MagicMock(return_value=future)

    await notifier.subscribe(listener)
    await notifier.on_notif_msg(j_notif)
    listener.assert_called_once

    # Assert arguments received by listener
    notif: Notif = listener.call_args[0][0]
    assert notif.title == 'Test Notif'
    assert notif.type == 'text'


@pytest.mark.asyncio
async def test_listen_multiple_notifs(j_notif: str):
    future = asyncio.Future()
    future.set_result(None)
    listener = MagicMock(return_value=future)

    await notifier.subscribe(listener)
    await notifier.on_notif_msg(j_notif)
    await notifier.on_notif_msg(j_notif)

    assert listener.call_count == 2

    # Assert arguments received by listener
    notif: Notif = listener.call_args[0][0]
    assert notif.title == 'Test Notif'
    assert notif.type == 'text'


@pytest.mark.asyncio
async def test_listener_unsubscribe(j_notif: str):
    future = asyncio.Future()
    future.set_result(None)
    listener = MagicMock(return_value=future)

    # Subscribe and send 3 notifications
    await notifier.subscribe(listener)
    await notifier.on_notif_msg(j_notif)
    await notifier.on_notif_msg(j_notif)
    await notifier.on_notif_msg(j_notif)

    # Unsubscribe and send another notification
    await notifier.unsubscribe(listener)
    await notifier.on_notif_msg(j_notif)

    # Assert listener was invoked 3 times only
    assert listener.call_count == 3
