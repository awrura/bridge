from typing import List
from typing import Protocol
from typing import Tuple


class MessageDelivery(Protocol):
    async def send(self, matrix_uuid: str, message: List[Tuple[int, int, int]]):
        """
        Отправить сообщение на матрицу, с данным именем

        :param matrix_name: Уникальное имя матрицы, которой адресовано сообщение
        :param message: Представляет собой список элементов (пикселей)
        каждый элемент содержит в себе rgb значения
        """

        raise NotImplementedError()
