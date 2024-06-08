from starlette.status import WS_1013_TRY_AGAIN_LATER
from websockets import WebSocketException


async def websocket_limit_callback(*_):
    """Обратный вызов, возникающий в случае превышения количества запросов по ws"""

    raise WebSocketException(WS_1013_TRY_AGAIN_LATER, 'Too Many Requests')
