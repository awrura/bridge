from config.config import Settings
from deps.config import get_settings
from fastapi import Depends
from services.secure.access import AccessByJwtValidator
from services.secure.access import JwtParser
from services.secure.proto import AccessKeyParser
from services.secure.proto import AccessValidator


def get_access_key_parser(conf: Settings = Depends(get_settings)) -> AccessKeyParser:
    """Получить объект парсинга ключа доступа"""

    return JwtParser(secret_key=conf.SECRET_KEY, algorithms=['HS256'])


def get_access_validator(
    parser: AccessKeyParser = Depends(get_access_key_parser),
) -> AccessValidator:
    """Получить объект проверки прав доступа"""

    return AccessByJwtValidator(parser=parser)
