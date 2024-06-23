import aioredis
import central.utils.config as cfg
import logging
from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from typing import List, Union
from uuid import UUID


logger = logging.getLogger(__name__)
REDIS_HOSTS_KEY = f'{ cfg.rd_prefix() }.hosts'


class _RedisClientBuilder:
    __proto: str = 'redis'
    __host: str = 'localhost'
    __port: str = '6379'
    __db_idx: str = None
    __username: str = None
    __password: str = None


    def host(self, host: str) -> '_RedisClientBuilder':
        self.__host = host
        return self

    def port(self, port: str) -> '_RedisClientBuilder':
        self.__port = port
        return self

    def ssl(self, ssl: bool) -> '_RedisClientBuilder':
        if ssl:
            self.__proto = 'rediss'

    def db(self, db_idx: str) -> '_RedisClientBuilder':
        self.__db_idx = db_idx
        return self

    def username(self, username: str) -> '_RedisClientBuilder':
        self.__username = username
        return self

    def password(self, password: str) -> '_RedisClientBuilder':
        self.__password = password
        return self

    def build(self) -> aioredis.Redis:
        url = f'{ self.__proto }://{ self.__host }:{ self.__port }'
        if self.__db_idx is not None:
            url += f'/{ self.__db_idx }'

        logger.debug('Connecting to redis: %s', url)
        if self.__username is not None:
            return aioredis.from_url(
                url,
                username=self.__username,
                password=self.__password
            )
        else:
            return aioredis.from_url(url)

    @staticmethod
    def init_from_env() -> '_RedisClientBuilder':
        builder = _RedisClientBuilder()
        builder.host(cfg.redis_host())
        builder.port(cfg.redis_port())
        builder.ssl(cfg.redis_ssl())

        if cfg.redis_username() is not None:
            builder.username(cfg.redis_username())
            builder.password(cfg.redis_password())

        return builder


_redis = _RedisClientBuilder.init_from_env().build()


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
    ip_key = f'{ REDIS_HOSTS_KEY }.{ host_id }.ipv4_public'
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


async def str_get(key: str) -> Union[str, None]:
    b_value = await _redis.get(key)
    if b_value is None:
        return None
    return b_value.decode('utf-8')


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


async def list_rpush(key: str, value: str) -> int:
    """Pushes a value to the tail (right) of a redis list

    Args:
        key (str): Redis key of the list
        value (str): Value to push to the list

    Returns:
        int: Number of elements in the list after the push operation
    """
    return await _redis.rpush(key, value)
