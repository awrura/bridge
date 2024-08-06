from typing import Protocol

from services.receive.data import Message


class MessageReceiver(Protocol):
    """Класс приема сообщений от клиента"""

    async def blrecieve(self) -> Message:
        """
        Ожидание сообщений от клиента и их считывание

        :raises:
            ValueError: При возникновении проблем с обработкой сообщения
        """

        raise NotImplementedError()
