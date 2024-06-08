import logging
from typing import Dict
from typing import List

from dto.info import Status
from dto.info import StatusMessage
from services.auth import UserInfo
from services.client.proto import MatrixClient
from services.client.data import Message
from services.client.receive import MessageReceiver
from starlette.websockets import WebSocket


logger = logging.getLogger(__name__)


class WsMatrixClient(MatrixClient):
    """Реализация клиента матрицы для подключения по WS"""

    def __init__(self, ws: WebSocket, receiver: MessageReceiver):
        self._ws = ws
        self._receiver = receiver

    async def accept(self, matrix_name: str, usr_info: UserInfo):
        """
        Принять соединение от клиента
        :raises:
            ConnectionError: В случае проблем с соединением
        """

        if matrix_name not in usr_info.matrices:
            logger.info(
                f'For user with username {usr_info.login} access denied to {matrix_name}'
            )
            raise ConnectionError('Access denied')

        await self._ws.accept()

    async def blreceive(self) -> Message:
        """
        Ожидать входных данных клиента, после
        получения преобразовать их в тип message
        :raises:
            ConnectionError: При возникновении проблем с получением сообщения
        """

        return await self._receiver.blrecieve()

    async def send_error(self, msg: List[Dict]):
        """
        Отправка сообщений об ошибках клиенту
        Поддерживается отправка нескольких сообщений - каждое сообщение отдельный словарь

        :param msg: Список сообщений об ошибках
        """

        await self._send_to_client(StatusMessage(status=Status.ERROR, err_msg=msg))

    async def send_success(self):
        """
        Отправка сообщению клиенту об успешном
        отправлении изображения на матрицу
        """

        await self._send_to_client(StatusMessage())

    async def _send_to_client(self, message: StatusMessage):
        """Реализация сериализации сообщения и отправки его клиенту"""
        
        await self._ws.send_text(message.json())
