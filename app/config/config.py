from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str
    WS_QUERY_COUNT_PER_SECOND: int
    BROKER_QUEUE_NAME: str
    SECRET_KEY: str

    class Config:
        env_file = '.env'
