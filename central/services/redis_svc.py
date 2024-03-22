import aioredis
import central.utils.config as cfg
import logging
from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from typing import List
from uuid import UUID


logger = logging.getLogger(__name__)

REDIS_HOSTS_KEY = f'{ cfg.rd_prefix() }.hosts'

_redis = aioredis.from_url(
    f'redis://{ cfg.redis_host() }:{ cfg.redis_port() }'
)


class MessageConsumer(ABC):

    @abstractmethod
    async def on_message(self, msg: str):
        """Callback to be invoked upon message arrival on \
            monitored queue

        Args:
            msg (str): Message received
        """
        pass


async def consume(q_name: str, consumer: MessageConsumer):
    """Keeps polling redis for new received messages on given \
        queue and invokes 'consumer.on_message' callback upon \
        received message

    Args:
        q_name (str): Redis list to consume
        consumer (MessageConsumer): Callback to invoke upon \
            received message.
    """
    logger.info('Consuming messages from redis list: %s', q_name)
    while True:
        msg = await _redis.blpop(q_name, 30)
        if msg is not None:
            msg = msg[1]
            await consumer.on_message(msg.decode('utf-8'))


async def stop():
    logger.debug('Closing redis connections')
    await _redis.close()


async def set_host_ip(host_id: UUID, ip: IPv4Address) -> None:
    ip_key = f'{ REDIS_HOSTS_KEY }.{ host_id }.ip'
    await _redis.set(ip_key, str(ip))


async def exists(key: str) -> bool:
    count = await _redis.exists(key)
    return count == 1


async def delete(key: str) -> None:
    await _redis.delete(key)


async def str_set(key: str, value: str, expiry: int = None) -> None:
    await _redis.set(key, value)
    if expiry is not None:
        await _redis.expire(key, expiry)


async def set_add(key: str, value: str, expiry: int = None) -> None:
    await _redis.sadd(key, value)
    if expiry is not None:
        await _redis.expire(key, expiry)


async def set_contains(key: str, value: str) -> bool:
    return await _redis.sismember(key, value)


async def set_members(key: str) -> List[str]:
    b_members = await _redis.smembers(key)

    # return list(map(str, b_members)) # Would str() use utf-8 by default?
    return [m.decode('utf-8') for m in b_members]
