from services.client import MatrixClient
from services.client.receive.rgb import RGBMessageReceiver
from services.client.stream import StreamMatrixClient
from services.stream.ws import WsStream
from starlette.websockets import WebSocket


def get_matrix_client(websocket: WebSocket) -> MatrixClient:
    """Получить объект клиента матрицы для установки и работы с соединением"""

    stream = WsStream(ws=websocket)
    return StreamMatrixClient(
        stream,
        receiver=RGBMessageReceiver(stream),
    )
