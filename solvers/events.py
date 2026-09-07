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

    # Información de la arista recorrida
    from_position: tuple[int, int] | None = None
    to_position: tuple[int, int] | None = None

    # Marca Trémaux de la arista después del moviminto: 1 o 2
    mark: int | None = None

@dataclass
class SolveResult:
    solution: list[tuple[int, int]]
    events: list[SolverEvent]

    # Estado final de las aristas. Cada arista tendrá marca 0, 1 o 2.
        # 0 = nunca recorrida
        # 1 = recorrida una vez
        # 2 = recorrida dos veces
    edge_marks: dict[frozenset, int]