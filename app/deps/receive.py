from deps.stream import get_stream
from fastapi import Depends
from services.receive import MessageReceiver
from services.receive.rgb import RGBMessageReceiver
from services.stream import Stream


def get_msg_receiver(stream: Stream = Depends(get_stream)) -> MessageReceiver:
    """Получить объект приема входящих сообщений от клиента"""

    return RGBMessageReceiver(stream=stream)
