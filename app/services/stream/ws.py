from json import JSONDecodeError
from typing import Any

from fastapi import WebSocket
from services.stream.proto import Stream


class WsStream(Stream):
    def __init__(self, ws: WebSocket):
        self._ws = ws

    async def accept(self) -> None:
        """Приянять соединение от клиента"""

        await self._ws.accept()

    async def send_text(self, data: str) -> None:
        """Отправить сообщение клиенту"""

        await self._ws.send_text(data)

    async def wait_json(self) -> Any:
        """
        Ожидание данных от клиента, для передачи на матрицу
        :raises:
            ValueError: В случае проблем с обработкой входных данных
        """

        try:
            return await self._ws.receive_json()
        except JSONDecodeError:
            raise ValueError('Unable parse data')
