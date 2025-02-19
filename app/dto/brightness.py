from pydantic import BaseModel
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo


class Brightness(BaseModel):
    """Яркость матрицы. В пределах от 0 до 255"""

    level: int

    @field_validator('level')  # noqa
    @classmethod
    def level_out_of_range_val(cls, v: int, info: ValidationInfo) -> int:
        if not 0 <= v <= 255:
            raise ValueError(f'{info.field_name} out of range')
        return v

    class Config:
        json_schema_extra = {
            'example': {
                'level': 20,
            }
        }
