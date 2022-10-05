from redis.asyncio.client import Redis
from .base import BaseCacheBackend


class RedisBackend(BaseCacheBackend):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_with_ttl(self, key: str) -> tuple[int, str]:
        async with self.redis.pipeline(transaction=True) as pipe:
            return await (pipe.ttl(key).get(key).execute())

    async def get(self, key) -> str:
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: int = None):
        return await self.redis.set(key, value, ex=expire)


