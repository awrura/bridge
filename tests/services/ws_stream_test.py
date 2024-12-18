from json import JSONDecodeError

import pytest
from fastapi import WebSocketDisconnect

from app.services.stream.ws import WsStream


class TestWsStream:
    @pytest.mark.asyncio
    async def test_decode_error(self, mocker):
        ws = mocker.AsyncMock(
            receive_json=mocker.AsyncMock(
                side_effect=JSONDecodeError(msg='Test', doc='', pos=0)
            )
        )

        stream = WsStream(ws)
        with pytest.raises(ValueError):
            await stream.wait_json()

    @pytest.mark.asyncio
    async def test_connection_error(self, mocker):
        ws = mocker.AsyncMock(
            receive_json=mocker.AsyncMock(side_effect=WebSocketDisconnect())
        )

        stream = WsStream(ws)
        with pytest.raises(ConnectionError):
            await stream.wait_json()

    @pytest.mark.asyncio
    async def test_decode_success(self, mocker):
        ws = mocker.AsyncMock(
            receive_json=mocker.AsyncMock(return_value={'hello': 'world'})
        )

        stream = WsStream(ws)
        data = await stream.wait_json()
        assert data['hello'] == 'world'

    @pytest.mark.asyncio
    async def test_accept_ws(self, mocker):
        ws = mocker.AsyncMock()

        stream = WsStream(ws)
        await stream.accept()
        ws.accept.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_ws(self, mocker):
        ws = mocker.AsyncMock()

        stream = WsStream(ws)
        await stream.close()
        ws.close.assert_called_once()
