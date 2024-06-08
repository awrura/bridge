from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class UserInfo:
    fullname: str
    login: str
    matrices: List[str]
    roles: List[str]
