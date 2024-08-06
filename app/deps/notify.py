from deps.stream import get_stream
from fastapi import Depends
from services.notify import Notifier
from services.notify.stream import StreamNotifier
from services.stream import Stream


def get_notifier(stream: Stream = Depends(get_stream)) -> Notifier:
    """Получить объект оповещения клиента о статусе его запроса"""

    return StreamNotifier(stream=stream)
