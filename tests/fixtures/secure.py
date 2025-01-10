import pytest

from app.services.secure.access import JwtParser


@pytest.fixture
def jwt_parser() -> JwtParser:
    return JwtParser(secret_key='some-best-secret', algorithms=['HS256'])
