from typing import Dict
from typing import List
from typing import Protocol

from services.auth import UserInfo
from services.client.data import Message


class MatrixClient(Protocol):
    async def accept(self, matrix_name: str, usr_info: UserInfo):
        """
        Принять соединение от клиента
        :raises:
            ConnectionError: В случае проблем с соединением
        """

        raise NotImplementedError()

    async def blreceive(self) -> Message:
        """
        Ожидать входных данных клиента, после
        получения преобразовать их в тип message
        """

        raise NotImplementedError()

    async def send_error(self, msg: List[Dict]):
        """
        Отправка сообщений об ошибках клиенту
        Поддерживается отправка нескольких сообщений - каждое сообщение отдельный словарь

        :param msg: Список сообщений об ошибках
        """

        raise NotImplementedError()

    async def send_success(self):
        """
        Отправка сообщению клиенту об успешном
        отправлении изображения на матрицу
        """

        raise NotImplementedError()
