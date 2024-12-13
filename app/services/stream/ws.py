from json import JSONDecodeError
from typing import Any

from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from services.stream.proto import Stream


class WsStream(Stream):
    def __init__(self, ws: WebSocket):
        self._ws = ws

    async def accept(self) -> None:
        """Приянять соединение от клиента"""

        await self._ws.accept()

    async def close(self) -> None:
        """Закрыть соединение от клиента"""

        await self._ws.close()

    async def send_text(self, data: str) -> None:
        """Отправить сообщение клиенту"""

        await self._ws.send_text(data)  # pragma: no cover

    async def wait_json(self) -> Any:
        """
        Ожидание данных от клиента
        :raises:
            ValueError: В случае проблем с обработкой входных данных
            ConnectionError: В случае проблем с соединенем при считывании данных
        """

        try:
            return await self._ws.receive_json()
        except JSONDecodeError:
            raise ValueError('Unable parse data')
        except WebSocketDisconnect:
            raise ConnectionError('Bad connection')
