import logging
from typing import List

from config.config import Settings
from deps.config import get_settings
from deps.delivery import get_msg_delivery
from deps.notify import get_notifier
from deps.receive import get_msg_receiver
from deps.stream import get_stream
from dto.pixel import RGBPixel
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi import Response
from fastapi import status
from fastapi import WebSocketException
from fastapi_limiter.depends import WebSocketRateLimiter as Limiter
from services.delivery import MessageDelivery
from services.notify import Notifier
from services.receive import MessageReceiver
from services.stream import Stream
from starlette.status import WS_1008_POLICY_VIOLATION
from starlette.websockets import WebSocket

router = APIRouter()
logger = logging.getLogger()


@router.post('/rgb/{matrix_name}')
async def draw(
    matrix_name: str = Path(),
    delivery: MessageDelivery = Depends(get_msg_delivery),
    pixels: List[RGBPixel] = Body(...),
):
    """Отрисовать пиксельную картинку на матрице"""

    raw_pixels = [(p.red, p.green, p.blue) for p in pixels]
    await delivery.send(matrix_name, raw_pixels)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.websocket('/rgb/{matrix_name}')
async def control(
    ws: WebSocket,
    matrix_name: str = Path(),
    notifier: Notifier = Depends(get_notifier),
    receiver: MessageReceiver = Depends(get_msg_receiver),
    stream: Stream = Depends(get_stream),
    delivery: MessageDelivery = Depends(get_msg_delivery),
    conf: Settings = Depends(get_settings),
):
    try:
        # В случае ошибок с принятием подключения
        await stream.accept()
    except ConnectionError:
        await ws.accept()  # Для корректного отображения сообщения об ошибке
        raise WebSocketException(WS_1008_POLICY_VIOLATION, 'Access denied')

    limit = Limiter(seconds=1, times=conf.WS_QUERY_COUNT_PER_SECOND)
    logger.info(f'Someone connected to matrix {matrix_name}')
    while True:
        try:
            data = await receiver.blrecieve()
        except ConnectionError:
            logger.info(f'Someone disconnected from matrix {matrix_name}')
            return

        await limit(ws)
        if not data.is_valid:
            await notifier.send_error(data.errors)
            continue
        await delivery.send(matrix_name, message=data.data)
        await notifier.send_success()
