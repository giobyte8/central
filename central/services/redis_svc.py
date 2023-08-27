import aioredis
import central.utils.config as cfg
import logging
from typing import Callable

logger = logging.getLogger(__name__)


_redis = aioredis.from_url(
    f'redis://{ cfg.redis_host() }:{ cfg.redis_port() }'
)


async def consume(q_name: str, on_message: Callable):
    """Keeps polling redis for new received messages on given
    queue and invokes 'on_message' callback upon received message

    Args:
        q_name (str): Redis list to consume
        on_message (Callable): Callback to invoke upon received message
    """
    logger.info('Consuming messages from redis list: %s', q_name)
    while True:
        msg = await _redis.blpop(q_name, 30)
        if msg is not None:
            msg = msg[1]
            await on_message(msg.decode('utf-8'))
