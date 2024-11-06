import contextlib
import logging

from asgi_correlation_id import CorrelationIdMiddleware
from deps.config import get_settings
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from middleware.log import LoggingMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from redis.asyncio import Redis as aredis
from routes.matrix import router as matrix_router
from utils.callback import websocket_limit_callback

logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(*_):
    logger.info('Start configuring server...')
    conf = get_settings()
    redis_connection = aredis.from_url(conf.REDIS_URL, encoding='utf8')
    await FastAPILimiter.init(redis_connection, ws_callback=websocket_limit_callback)
    logger.info('Server started and configured successfully')
    yield
    logger.info('Server shut down')


app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)

app.add_middleware(LoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matrix_router, tags=['matrix'], prefix='/matrix')
