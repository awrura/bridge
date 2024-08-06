from typing import Dict
from typing import List
from typing import Protocol


class Notifier(Protocol):
    """Отправка сообщений клиенту о статусе выполнения"""

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
