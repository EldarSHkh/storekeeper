from functools import wraps
from collections.abc import Callable
from key_builder import BaseKeyBuilder

from storekeeper.backend.base import BaseCacheBackend


def cache(backend: BaseCacheBackend, key_builder: BaseKeyBuilder) -> Callable:
    def wrapper(func: Callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            cache_key = key_builder.build(args, kwargs)
            time, cache_res = await backend.get_with_ttl(cache_key)
            if cache_res is None:
                result = await func(*args, **kwargs)
                await backend.set(cache_key, result)
            else:
                result = cache_res
            return result
        return inner
    return wrapper

