from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    START = "start"             # Comienza el Solver
    MOVE = "move"               # Avanza a una nueva celda
    BACKTRACK = "backtrack"     # Retrocede
    SOLVED = "solved"           # Ha encontrado la salida

@dataclass(frozen=True)
class SolverEvent:
    type: EventType
    position: tuple[int, int]

@dataclass
class SolveResult:
    solution: list[tuple[int, int]]
    events: list[SolverEvent]