from typing import List
from typing import Protocol
from typing import Tuple


class MessageDelivery(Protocol):
    async def send_pic(self, matrix_name: str, message: List[Tuple[int, int, int]]):
        """
        Отправить картинку на матрицу, с данным именем

        :param matrix_name: Уникальное имя матрицы, которой адресовано сообщение
        :param message: Представляет собой список элементов (пикселей)
        каждый элемент содержит в себе rgb значения
        """

        raise NotImplementedError()


    async def send_brightness(self, matrix_name: str, value: int):
        """
        Установка яроксти для матрицы

        :param matrix_name: Уникальное имя матрицы, которой адресовано сообщение
        :param value: Уровень яркости. От 0 до 255
        """

        raise NotImplementedError()
