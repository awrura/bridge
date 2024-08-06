from services.stream import Stream
from services.stream.ws import WsStream
from starlette.websockets import WebSocket


def get_stream(websocket: WebSocket) -> Stream:
    """Получить объекта потока входящих данных"""

    return WsStream(ws=websocket)
