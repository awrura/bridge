import logging
from typing import Dict
from typing import List

from dto.info import Status
from dto.info import StatusMessage
from services.notify.proto import Notifier
from services.stream import Stream

logger = logging.getLogger(__name__)


class StreamNotifier(Notifier):
    """Реализация уведомления пользователя о выполнении операции через Stream"""

    def __init__(self, stream: Stream):
        self._stream = stream

    async def send_error(self, msg: List[Dict]):
        """
        Отправка сообщений об ошибках клиенту
        Поддерживается отправка нескольких сообщений - каждое сообщение отдельный словарь

        :param msg: Список сообщений об ошибках
        """

        await self._send_to_client(
            StatusMessage(status=Status.ERROR, err_msg=msg)
        )  # pragma: no cover

    async def send_success(self):
        """
        Отправка сообщению клиенту об успешном
        отправлении изображения на матрицу
        """

        await self._send_to_client(StatusMessage())  # pragma: no cover

    async def _send_to_client(self, message: StatusMessage):
        """Реализация сериализации сообщения и отправки его клиенту"""

        await self._stream.send_text(message.json())  # pragma: no cover
