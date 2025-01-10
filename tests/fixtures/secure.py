import pytest

from app.dto.access import UserAccess
from app.services.secure.access import JwtParser


@pytest.fixture
def jwt_parser() -> JwtParser:
    return JwtParser(secret_key='some-best-secret', algorithms=['HS256'])


@pytest.fixture
def valid_jwt_claims() -> dict:
    return {
        'user_uuid': 'c3ec2264-36bc-4deb-9c86-92b240349643',
        'username': 'twoics',
        'available_matrices': [
            {
                'uuid': 'a9184058-5a4e-4dc7-b94a-3968c470e281',
                'name': 'awrura',
                'height': 16,
                'weight': 16,
            }
        ],
    }


@pytest.fixture
def valid_userinfo(valid_jwt_claims) -> UserAccess:
    return UserAccess.model_validate(valid_jwt_claims)
