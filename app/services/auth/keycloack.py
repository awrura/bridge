import logging
from functools import wraps
from typing import Callable
from typing import Dict

from httpx import AsyncClient
from httpx import HTTPStatusError
from services.auth.data import UserInfo
from services.auth.proto import UserInfoRetriever

logger = logging.getLogger(__name__)


def http_to_connection_err(func: Callable):
    """Перехват HTTPError и выкидывание ConnectionError для стандартизации исключений интерфейса"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPStatusError as ex:
            logger.info(ex)
            raise ConnectionError(str(ex))

    return wrapper


class KeycloackInfoRetriver(UserInfoRetriever):
    """Класс получения информации о пользователях из сервиса keycloack"""

    def __init__(self, base_url: str, realm: str):
        """
        :param base_url: Путь до сервиса keycloack (http://localhost:8080)
        :param realm: Раздел keycloack к которому идет запросо
        """

        self._base_url = base_url
        self._realm = realm

    @http_to_connection_err
    async def request(self, token: str) -> UserInfo:  # pyright: ignore[reportIncompatibleMethodOverride]
        """
        Получить информацию о пользователе исходя из его токена
        :raises:
            ConnectionError: Если возникли ошибки при отправке запроса в сервис
        """

        async with AsyncClient() as client:
            response = await client.get(
                f'{self._base_url}/realms/{self._realm}/protocol/openid-connect/userinfo',
                headers={'Authorization': f'Bearer {token}'},
            )
        response.raise_for_status()

        return self._parse_json(response.json())

    def _parse_json(self, data: Dict) -> UserInfo:
        """
        Из объекта ответа вытащить все
        нобходимые поля и создать объект UserInfo
        """

        return UserInfo(
            login=data['preferred_username'],
            fullname=data['name'],
            matrices=data.setdefault('matrices', []),
            roles=data.setdefault('roles', []),
        )
