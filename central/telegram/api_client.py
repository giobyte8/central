import asyncio
import central.utils.config as cfg
import logging
from aiohttp import ClientSession
from aiohttp import client_exceptions as aiohttp_ex
from central.telegram.models import TGMessage, TGResponseMsg
from pydantic import ValidationError
from typing import Awaitable, Callable


logger = logging.getLogger(__name__)

_BASE_URL  = f'https://api.telegram.org/bot{ cfg.tg_bot_token() }'
_aiohttp_session: ClientSession = None

def _http() -> ClientSession:
    """Retrieve the shared http session for all telegram api calls. \

        Note: The session contains a cookie storage and connection
        pool, thus cookies and connections are shared between HTTP
        requests sent by the same session.

    Returns:
        ClientSession: Singleton aiohttp client session
    """
    global _aiohttp_session

    if not _aiohttp_session or _aiohttp_session.closed:
        logger.debug('Creating new aiohttp client session')
        _aiohttp_session = ClientSession()
    return _aiohttp_session


async def cleanup():
    global _aiohttp_session

    if _aiohttp_session and not _aiohttp_session.closed:
        await _aiohttp_session.close()


async def getMe():
    async with _http().get(f'{ _BASE_URL }/getMe') as res:
        return await res.json()


async def get_updates(offset: int):
    p = { 'offset': offset }

    try:
        async with _http().get(f'{ _BASE_URL }/getUpdates', params=p) as res:
            if res.status == 200:
                j_res = await res.json()

                if j_res['ok']:
                    return j_res['result']
                else:
                    logger.error('Telegram error: %s', j_res['description'])
            else:
                logger.error(
                    'HTTP error: %s, Text: %s',
                    res.status,
                    await res.text())
                await asyncio.sleep(3)
    except aiohttp_ex.ClientOSError as e:
        logger.warn('aiohttp error: %s', e)
        await asyncio.sleep(3)
    except Exception as e:
        logger.error('Error while retrieving telegram updates: %s', e)
        await asyncio.sleep(3)

    # In case error ocurred, return empty array of updates
    return []


async def poll_updates(on_message: Callable[[TGMessage], Awaitable]):
    """Starts constant updates polling from API and invokes 'on_update' \
        callback upon update received
    """
    highest_received_update = 0

    logger.info('Polling updates from telegram API')
    while True:
        updates = await get_updates(highest_received_update + 1)

        for update in updates:
            update_id = update['update_id']
            logger.info(' TG Update received: %s', update_id)
            logger.debug('TG Update body: %s', update)

            # Update highest received update id
            highest_received_update = max(highest_received_update, update_id)

            if 'message' in update:
                try:
                    message = TGMessage(**update['message'])
                    await on_message(message)
                except ValidationError as e:
                    logger.error('Deserialization error: %s', e.json())
            else:
                logger.warn('Unsupported telegram update: %s', update)


async def send_message(msg: TGResponseMsg):
    url = f'{ _BASE_URL }/sendMessage'
    d = msg.model_dump(exclude_unset=True, exclude_none=True)

    async with _http().post(url, json=d) as res:
        if res.status == 200:
            return True
        else:
            logger.error(
                'HTTP error: %s, Text: %s',
                res.status,
                await res.text())
            return False
