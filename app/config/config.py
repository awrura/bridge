from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str
    WS_QUERY_COUNT_PER_SECOND: int
    BROKER_QUEUE_NAME: str
    KEYCLOACK_BASE_URL: str
    KEYCLOACK_REALM: str

    class Config:
        env_file = '.env'
