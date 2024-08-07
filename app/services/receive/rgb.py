import logging
from typing import List

from dto.pixel import RGBPixel
from pydantic import TypeAdapter
from pydantic import ValidationError
from services.receive.data import Message
from services.receive.proto import MessageReceiver
from services.stream import Stream

logger = logging.getLogger(__name__)


class RGBMessageReceiver(MessageReceiver):
    def __init__(self, stream: Stream):
        self._stream = stream

    async def blrecieve(self) -> Message:
        """
        Прием json сообщения, из объектов формата RGBPixel, через WS
        """

        try:
            data = await self._stream.wait_json()
        except ValueError as ex:
            logging.warn(ex)
            return Message(data=[], errors=[{'data': 'Received data not supported'}])
        return self.parse(data)

    def parse(self, data) -> Message:
        """Парсинг полученого сообщения, и приведение к типу Message"""

        adapter = TypeAdapter(List[RGBPixel])
        try:
            out = [
                list(rgb.model_dump().values())
                for rgb in adapter.validate_python(data['data'])
            ]
        except KeyError:
            return Message(data=[], errors=[{'data': 'Field required'}])
        except ValidationError as ex:
            return Message(
                data=[],
                errors=ex.errors(include_url=False, include_context=False),  # pyright: ignore[reportArgumentType]
            )
        return Message(data=out)  # pyright: ignore[reportArgumentType]
