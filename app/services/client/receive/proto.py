from typing import Protocol

from services.client.data import Message


class MessageReceiver(Protocol):
    """Класс приема сообщений от клиента"""

    async def blrecieve(self) -> Message:
        """
        Ожидание сообщений от клиента и их считывание

        :raises:
            ConnectionError: При возникновении проблем с получением сообщения
        """

        raise NotImplementedError()
