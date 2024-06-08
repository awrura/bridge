from typing import Protocol

from .data import UserInfo


class UserInfoRetriever(Protocol):
    """Класс запроса информации о пользователе у IdentityProvider"""

    async def request(self, token: str) -> UserInfo:
        """
        Получить информацию о пользователе исходя из его токена
        :raises:
            ConnectionError: Если возникли ошибки при отправке запроса в сервис
        """

        raise NotImplementedError()
