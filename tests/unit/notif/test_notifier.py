import json
import pytest
from pytest_mock import MockerFixture

from central.notif import notifier
from central.notif.notifier import NotifListener
from central.notif.models import Notif


_NOTIF_TITLE = 'Test Notif'


@pytest.fixture(scope='module')
def j_notif() -> str:
    notif = {
        'uuid': '8ef67d5c-f650-4f73-9099-f225be223d2a',
        'type': 'text',
        'title': _NOTIF_TITLE,
        'content': 'lorem...',
    }

    return json.dumps(notif)


@pytest.fixture
def n_listener() -> NotifListener:
    class TestNotifListener(NotifListener):
        def __init__(self):
            super().__init__()

        async def on_notification(self, notif: Notif):
            assert notif.title == _NOTIF_TITLE

    return TestNotifListener()


@pytest.mark.asyncio
async def test_subscribe_listener(
    j_notif: str,
    n_listener: NotifListener,
    mocker: MockerFixture
):
    on_notif_spy = mocker.spy(n_listener, 'on_notification')

    # Subscribe and send notification
    await notifier.subscribe(n_listener)
    consumer = notifier.NotifMsgConsumer()
    await consumer.on_message(j_notif)

    # Assert listener was invoked
    on_notif_spy.assert_called_once()


@pytest.mark.asyncio
async def test_subscribe_and_multiple_notifications(
    j_notif: str,
    n_listener: NotifListener,
    mocker: MockerFixture
):
    on_notif_spy = mocker.spy(n_listener, 'on_notification')

    await notifier.subscribe(n_listener)

    # Send 2 notifications
    consumer = notifier.NotifMsgConsumer()
    await consumer.on_message(j_notif)
    await consumer.on_message(j_notif)

    # Assert listener was invoked twice
    assert on_notif_spy.call_count == 2


@pytest.mark.asyncio
async def test_unsubscribe(
    j_notif: str,
    n_listener: NotifListener,
    mocker: MockerFixture
):
    on_notif_spy = mocker.spy(n_listener, 'on_notification')

    # Subscribe to receive first two notifications
    await notifier.subscribe(n_listener)

    # Send 2 notifications
    consumer = notifier.NotifMsgConsumer()
    await consumer.on_message(j_notif)
    await consumer.on_message(j_notif)

    # Unsubscribe and send another notification
    await notifier.unsubscribe(n_listener)
    await consumer.on_message(j_notif)

    # Assert listener was invoked 2 times only
    assert on_notif_spy.call_count == 2
