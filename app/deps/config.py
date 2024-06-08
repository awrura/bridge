from functools import lru_cache

from config.config import Settings


@lru_cache
def get_settings() -> Settings:
    """Получить настройки приложения"""

    return Settings()  # pyright: ignore[reportCallIssue]
