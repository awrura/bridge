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

    DRAW_PIC_COMMAND = 1
    SET_BRIGHTNESS_COMMAND = 2

    def __init__(self, redis: AsyncRedis, conf: Settings):
        self._redis = redis
        self._conf = conf

    async def send_pic(self, matrix_name: str, message: List[Tuple[int, int, int]]):
        """
        Отправить сообщение на матрицу - по ее уникальному имени,
        в redis брокер для дальнейшей отправки
        """

        logger.info(f'Pushing pic to matrix: {matrix_name}')
        to_send = json.dumps(
            {
                'topic': f'matrix/{matrix_name}',
                'data': [color for pixel in message for color in pixel],
                'command': self.DRAW_PIC_COMMAND,
            }
        )
        await self._redis.rpush(self._conf.BROKER_QUEUE_NAME, to_send)  # pyright: ignore[reportGeneralTypeIssues]

    async def send_brightness(self, matrix_name: str, value: int):
        """
        Отправить на матрицу команду с установкой яркости
        """

        logger.info(f'Pushing brightness to matrix: {matrix_name}')

        if not 0 <= value <= 255:
            logger.error('Brightness level out of range')
            return

        to_send = json.dumps(
            {
                'topic': f'matrix/{matrix_name}',
                'data': [value],
                'command': self.SET_BRIGHTNESS_COMMAND,
            }
        )
        await self._redis.rpush(self._conf.BROKER_QUEUE_NAME, to_send)  # pyright: ignore[reportGeneralTypeIssues]
