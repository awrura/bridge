import pytest
from app.services.stream.ws import WsStream
from json import JSONDecodeError

class TestWsStream:
    @pytest.mark.asyncio
    async def test_decode_error(self, mocker):
        ws = mocker.AsyncMock(receive_json=mocker.AsyncMock(side_effect=JSONDecodeError(
            msg='Test',
            doc='',
            pos=0
        )))

        receiver = WsStream(ws)
        with pytest.raises(ValueError):
            await receiver.wait_json()

    @pytest.mark.asyncio
    async def test_decode_success(self, mocker):
        ws = mocker.AsyncMock(receive_json=mocker.AsyncMock(return_value={'hello': 'world'}))

        receiver = WsStream(ws)
        data = await receiver.wait_json()
        assert data['hello'] == 'world'
