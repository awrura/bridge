from pydantic import BaseModel
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo


class RGBPixel(BaseModel):
    """Объект приема цвета пикселя матрицы по WS"""

    red: int
    green: int
    blue: int

    @field_validator('*')  # noqa
    @classmethod
    def out_of_range_validator(cls, v: int, info: ValidationInfo) -> int:
        if not 0 <= v <= 255:
            raise ValueError(f'{info.field_name} out of range')
        return v

    class Config:
        json_schema_extra = {
            'example': {
                'red': 211,
                'green': 82,
                'blue': 22,
            }
        }
