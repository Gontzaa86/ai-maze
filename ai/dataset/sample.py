from dataclasses import dataclass
from enum import IntEnum

import numpy as np # type: ignore

class Action(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

@dataclass(frozen = True)
class TrainingSample:
    state: np.ndarray
    action: int