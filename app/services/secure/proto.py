from typing import Protocol

from dto.access import UserAccess


class AccessKeyParser(Protocol):
    def parse(self, access_key: str) -> UserAccess | None:
        """
        Парсинг ключа доступа в структуру доступных пользователю матриц
        """

        raise NotImplementedError()


class AccessValidator(Protocol):
    def ask_permission(self, access_key: str, target_matrix: str) -> bool:
        """
        Спросить разрешения о возможности подключения
        с данным ключом доступа к конкретной матрице
        """

        raise NotImplementedError()
