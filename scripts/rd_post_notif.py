import redis.asyncio as aioredis
import asyncio
import json
import os
import sys
from dotenv import load_dotenv


load_dotenv()

# Parse title and content from command line arguments
if len(sys.argv) < 3:
    raise Exception('Notif title and content are required')
notif_title = str(sys.argv[1])
notif_content = str(sys.argv[2])

# Retrieve redis connection params from env
rd_notif_q = os.getenv('QUEUE_NOTIFICATIONS')

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

        print(f'Connecting to redis: {url}')
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
        builder.host(os.getenv('REDIS_HOST'))
        builder.port(os.getenv('REDIS_PORT'))
        builder.ssl(os.getenv('REDIS_SSL', 'false') == 'true')

        if os.getenv('REDIS_USERNAME', None) is not None:
            builder.username(os.getenv('REDIS_USERNAME'))
            builder.password(os.getenv('REDIS_PASSWORD'))

        return builder


async def post_notif():
    _redis = _RedisClientBuilder.init_from_env().build()

    # Assembly json notif
    notif = { 'title': notif_title, 'content': notif_content }
    j_notif = json.dumps(notif)

    print(f'Posting notif: {j_notif}')
    await _redis.rpush(rd_notif_q, j_notif)
    await _redis.aclose()

asyncio.run(post_notif())
