from config.config import Settings
from deps.aredis import get_redis
from deps.config import get_settings
from fastapi import Depends
from redis.asyncio import Redis as AsyncRedis
from services.delivery import MessageDelivery
from services.delivery.broker import RedisBrokerDelivery


def get_msg_delivery(
    aredis: AsyncRedis = Depends(get_redis), conf: Settings = Depends(get_settings)
) -> MessageDelivery:
    """Получить объект доставщика сообщений"""

    return RedisBrokerDelivery(redis=aredis, conf=conf)
