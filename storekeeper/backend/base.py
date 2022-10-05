from typing import Protocol
from abc import abstractmethod


class BaseCacheBackend(Protocol):

    @abstractmethod
    async def get_with_ttl(self, key: str) -> tuple[int, str]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key) -> str:
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: str, expire: int = None):
        raise NotImplementedError

