from typing import List  # pragma: no cover
from typing import Protocol  # pragma: no cover
from typing import Tuple  # pragma: no cover


class MessageDelivery(Protocol):
    async def send(self, matrix_name: str, message: List[Tuple[int, int, int]]):
        """
        Отправить сообщение на матрицу, с данным именем

        :param matrix_name: Уникальное имя матрицы, которой адресовано сообщение
        :param message: Представляет собой список элементов (пикселей)
        каждый элемент содержит в себе rgb значения
        """

        raise NotImplementedError()
