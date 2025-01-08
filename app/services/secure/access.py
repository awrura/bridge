import logging

import jwt
import pydantic
from dto.access import UserAccess
from services.secure.proto import AccessKeyParser
from services.secure.proto import AccessValidator

logger = logging.getLogger(__name__)


class JwtParser(AccessKeyParser):
    def __init__(self, secret_key: str, algorithms: list[str]):
        self._secret = secret_key
        self._alorithms = algorithms

    def parse(self, access_key: str) -> UserAccess | None:
        try:
            decoded = jwt.decode(
                access_key, key=self._secret, algorithms=self._alorithms
            )
            return UserAccess.model_validate(decoded)
        except jwt.PyJWTError:
            logger.error(f'Unable to decode access key {access_key}')
        except pydantic.ValidationError:
            logger.error('Unable to parse access key to UserAccess')
        return None


class AccessByJwtValidator(AccessValidator):
    def __init__(self, parser: AccessKeyParser):
        self._parser = parser

    def ask_permission(self, access_key: str, target_matrix: str) -> bool:
        access = self._parser.parse(access_key)
        if not access:
            return False

        available_matrix_uuids = map(lambda m: m.uuid, access.available_matrices)
        return target_matrix in available_matrix_uuids
