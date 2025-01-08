from typing import Protocol

from dto.access import UserAccess


class JwtUserAccessParser(Protocol):
    def parse(self, jwt_access_key: str) -> UserAccess | None:
        """
        Парсинг JWT в структуру доступных пользователю матриц
        """

        raise NotImplementedError()


class ConnectValidator(Protocol):
    def ask_permission(self, target_matrix: str) -> bool:
        """
        Спросить разрешения о возможности подключения
        """

        raise NotImplementedError()
