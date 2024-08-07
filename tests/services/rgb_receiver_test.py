import pytest

from app.services.receive.rgb import RGBMessageReceiver


class TestRGBMessageReceiver:
    @pytest.mark.parametrize(
        'data',
        [
            {},
            {'key': 42},
            {'data': 42},
            {'data': []},
            {'data': ['hello', 24, 'world']},
            {'data': [{'hello': 1, 'world': 2}]},
            {'data': [{'red': 122, 'green': 888, 'blue': 25}]},
        ],
    )
    @pytest.mark.asyncio
    async def test_unsupported_data(self, mocker, data):
        stream = mocker.Mock(wait_json=mocker.AsyncMock(return_value=data))

        receiver = RGBMessageReceiver(stream)
        response = await receiver.blrecieve()

        assert response.is_valid is False

    @pytest.mark.asyncio
    async def test_decode_error(self, mocker):
        stream = mocker.Mock(wait_json=mocker.AsyncMock(side_effect=ValueError()))

        receiver = RGBMessageReceiver(stream)
        response = await receiver.blrecieve()

        assert not response.is_valid

    @pytest.mark.parametrize(
        'data',
        [
            {'data': [{'red': 122, 'green': 212, 'blue': 25}]},
            {
                'data': [
                    {'red': 122, 'green': 212, 'blue': 25},
                    {'red': 1, 'green': 1, 'blue': 1},
                ]
            },
        ],
    )
    @pytest.mark.asyncio
    async def test_retrieve_success(self, mocker, data):
        stream = mocker.Mock(wait_json=mocker.AsyncMock(return_value=data))

        receiver = RGBMessageReceiver(stream)
        response = await receiver.blrecieve()

        assert response.is_valid is True
