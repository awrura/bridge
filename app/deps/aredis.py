from functools import lru_cache

from deps.config import get_settings
from redis.asyncio import Redis as AsyncRedis


@lru_cache
def get_redis() -> AsyncRedis:
    """Получить экземпляр асинхронного redis"""

    return AsyncRedis.from_url(get_settings().REDIS_URL, decode_responses=True)
