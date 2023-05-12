from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# https://stackoverflow.com/questions/66448588/is-there-a-way-to-make-a-priority-queue-sort-by-the-priority-value-in-a-tuple-on?noredirect=1&lq=1
@dataclass(order=True)
class PrioritizedPuzzle:
    priority: int
    item: Any = field(compare=False)


# https://docs.python.org/3/library/enum.html
class Direction(Enum):
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)
