from typing import Protocol
from typing import Any

class Stream(Protocol):
    """
    Общий интерфейс для реализаций
    соединения и общения с клиентом
    """

    async def accept(self) -> None:
        """Приянять соединение от клиента"""
        
        raise NotImplementedError()

    async def send_text(self, data: str) -> None:
        """Отправить сообщение клиенту"""
        
        raise NotImplementedError()

    async def wait_json(self) -> Any:
        """
        Ожидание данных от клиента, для передачи на матрицу
        :raises:
            ValueError: В случае проблем с обработкой входных данных
        """
        
        raise NotImplementedError()
        
