import logging
from json import JSONDecodeError
from typing import List

from dto.pixel import RGBPixel
from pydantic import TypeAdapter
from pydantic import ValidationError
from services.client.data import Message
from services.client.receive.proto import MessageReceiver
from starlette.websockets import WebSocket

logger = logging.getLogger(__name__)


class WsRGBMessageReceiver(MessageReceiver):
    def __init__(self, ws: WebSocket):
        self._ws = ws

    async def blrecieve(self) -> Message:
        """Прием json сообщения, из объектов формата RGBPixel, через WS"""

        try:
            data = await self._ws.receive_json()
        except JSONDecodeError as ex:
            logging.info(ex)
            raise ConnectionError('Unable parse data')
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
