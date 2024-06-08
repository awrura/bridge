from enum import StrEnum
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field


class Status(StrEnum):
    SUCCESS = 'OK'
    ERROR = 'ERR'


class StatusMessage(BaseModel):
    status: Status = Status.SUCCESS
    err_msg: List[Dict] = Field(default_factory=list)
