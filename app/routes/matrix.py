import logging

from config.config import Settings
from deps.config import get_settings
from deps.delivery import get_msg_delivery
from deps.notify import get_notifier
from deps.receive import get_msg_receiver
from deps.stream import get_stream
from deps.usr_info import get_info_retriver
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from fastapi import WebSocketException
from fastapi_limiter.depends import WebSocketRateLimiter as Limiter
from services.auth import UserInfoRetriever
from services.delivery import MessageDelivery
from services.notify import Notifier
from services.receive import MessageReceiver
from services.stream import Stream
from starlette.status import WS_1008_POLICY_VIOLATION
from starlette.websockets import WebSocket

router = APIRouter()
logger = logging.getLogger()


@router.websocket('/rgb/{matrix_name}')
async def control(
    ws: WebSocket,
    matrix_name: str = Path(),
    token: str = Query(),
    notifier: Notifier = Depends(get_notifier),
    receiver: MessageReceiver = Depends(get_msg_receiver),
    stream: Stream = Depends(get_stream),
    usr_retriver: UserInfoRetriever = Depends(get_info_retriver),
    delivery: MessageDelivery = Depends(get_msg_delivery),
    conf: Settings = Depends(get_settings),
):
    try:
        # В случае проблем с сервисом идентификации (Клиенту об этом знать необязательно)
        info = await usr_retriver.request(token)
        # В случае ошибок с принятием подключения (Правами)
        await stream.accept()
    except ConnectionError:
        await ws.accept()  # Для корректного отображения сообщения об ошибке
        raise WebSocketException(WS_1008_POLICY_VIOLATION, 'Access denied')

    limit = Limiter(seconds=1, times=conf.WS_QUERY_COUNT_PER_SECOND)
    logger.info(f'{info.login} connected to matrix {matrix_name}')
    while True:
        data = await receiver.blrecieve()
        await limit(ws)
        if not data.is_valid:
            await notifier.send_error(data.errors)
            continue
        await delivery.send(matrix_name, message=data.data)
        await notifier.send_success()
