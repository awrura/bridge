from jwt.exceptions import PyJWTError
from pydantic import ValidationError

from app.dto.access import UserAccess
from app.services.secure.access import AccessByJwtValidator
from app.services.secure.access import JwtParser


class TestJwtParser:
    def test_success_parse(self, mocker, jwt_parser: JwtParser, valid_jwt_claims: dict):
        decode_mocker = mocker.patch('jwt.decode')
        decode_mocker.return_value = valid_jwt_claims
        assert jwt_parser.parse('valid-access-key') is not None

    def test_jwt_error(self, mocker, jwt_parser: JwtParser):
        mocker.patch('jwt.decode', side_effect=PyJWTError('JWT decode error'))
        assert jwt_parser.parse('unparsable-jwt-key') is None

    def test_pydantic_error(self, mocker, jwt_parser: JwtParser):
        mocker.patch(
            'jwt.decode',
            side_effect=ValidationError.from_exception_data(
                title='Unable parse jwt claims', line_errors=[]
            ),
        )
        assert jwt_parser.parse('invalid-access-key') is None


class TestAccessValidatior:
    def test_access_denied(self, mocker):
        jwt_parser = mocker.Mock(parse=mocker.Mock(return_value=None))
        validator = AccessByJwtValidator(parser=jwt_parser)
        assert not validator.ask_permission(
            'invalid-access-key', 'a9184058-5a4e-4dc7-b94a-3968c470e281'
        )

    def test_access_allowed(self, mocker, valid_userinfo: UserAccess):
        jwt_parser = mocker.Mock(parse=mocker.Mock(return_value=valid_userinfo))
        validator = AccessByJwtValidator(parser=jwt_parser)
        assert validator.ask_permission(
            'valid-access-key', 'a9184058-5a4e-4dc7-b94a-3968c470e281'
        )
