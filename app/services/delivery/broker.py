import json
import logging
from typing import List
from typing import Tuple

from config.config import Settings
from redis.asyncio import Redis as AsyncRedis
from services.delivery.proto import MessageDelivery

logger = logging.getLogger(__name__)


class RedisBrokerDelivery(MessageDelivery):
    """
    Отправка сообщений обработчикам (worker) используя
    брокер сообщений основанный на redis
    """

    def __init__(self, redis: AsyncRedis, conf: Settings):
        self._redis = redis
        self._conf = conf

    async def send(self, matrix_uuid: str, message: List[Tuple[int, int, int]]):
        """
        Отправить сообщение на матрицу - по ее уникальному имени,
        в redis брокер для дальнейшей отправки
        """

        logger.info(f'Pushing msg to matrix: {matrix_uuid}')
        to_send = json.dumps(
            {
                'topic': f'matrix/{matrix_uuid}',
                'data': [color for pixel in message for color in pixel],
            }
        )
        await self._redis.rpush(self._conf.BROKER_QUEUE_NAME, to_send)  # pyright: ignore[reportGeneralTypeIssues]
