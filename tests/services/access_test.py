from jwt.exceptions import PyJWTError
from pydantic import ValidationError

from app.services.secure.access import JwtParser


class TestJwtParser:
    def test_success_parse(self, mocker, jwt_parser: JwtParser):
        decode_mocker = mocker.patch('jwt.decode')
        decode_mocker.return_value = {
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
