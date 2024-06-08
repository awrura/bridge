from config.config import Settings
from deps.config import get_settings
from fastapi import Depends
from services.auth import UserInfoRetriever
from services.auth.keycloack import KeycloackInfoRetriver


def get_info_retriver(conf: Settings = Depends(get_settings)) -> UserInfoRetriever:
    """Получить объект класса запрашивающий информацию о пользователе у Identity Provider"""

    return KeycloackInfoRetriver(
        base_url=conf.KEYCLOACK_BASE_URL, realm=conf.KEYCLOACK_REALM
    )
