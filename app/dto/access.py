from pydantic import BaseModel


class AvailableUserMatrix(BaseModel):
    """Информация о доступной пользователю матрице"""

    uuid: str
    name: str
    height: int
    weight: int


class UserAccess(BaseModel):
    """Описание доступных пользователю матриц"""

    user_uuid: str
    username: str
    available_matrices: list[AvailableUserMatrix]
