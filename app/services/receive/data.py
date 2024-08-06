from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Tuple


@dataclass(frozen=True)
class Message:
    data: List[Tuple[int, int, int]]
    errors: List[Dict] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return bool(self.data)
