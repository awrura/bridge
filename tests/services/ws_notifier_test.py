import pytest

from app.dto.info import Status
from app.dto.info import StatusMessage
from app.services.notify.stream import StreamNotifier


class TestWsNotifier:
    @pytest.mark.parametrize(
        'err_msg',
        [
            [{'email': 'invalid'}, {'user': 'not authorized'}],
        ],
    )
    @pytest.mark.asyncio
    async def test_notify_about_error(self, err_msg, mocker):
        stream = mocker.AsyncMock()
        notifier = StreamNotifier(stream)

        await notifier.send_error(err_msg)

        stream.send_text.assert_called_once_with(
            StatusMessage(status=Status.ERROR, err_msg=err_msg).json()
        )

    @pytest.mark.asyncio
    async def test_notify_about_success(self, mocker):
        stream = mocker.AsyncMock()
        notifier = StreamNotifier(stream)

        await notifier.send_success()

        stream.send_text.assert_called_once_with(StatusMessage().json())
