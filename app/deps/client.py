from services.client import MatrixClient
from services.client.receive.rgb_ws import WsRGBMessageReceiver
from services.client.ws import WsMatrixClient
from starlette.websockets import WebSocket


def get_matrix_client(websocket: WebSocket) -> MatrixClient:
    """Получить объект клиента матрицы для установки и работы с соединением"""

    return WsMatrixClient(
        ws=websocket,
        receiver=WsRGBMessageReceiver(ws=websocket),
    )
