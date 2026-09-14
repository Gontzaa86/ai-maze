from dataclasses import dataclass
import time

from solvers.events import EventType, SolveResult

@dataclass(frozen = True)
class SolveMetrics:
    solution_length: int
    moves: int
    backtracks: int
    success: bool
    visited_cells: int
    execution_time: float

def calculate_metrics(result: SolveResult, start: tuple[int, int], end: tuple[int, int], execution_time: float = 0.0) -> SolveMetrics:
    moves = sum(1 for event in result.events if event.type == EventType.MOVE)

    backtracks = sum(1 for event in result.events if event.type == EventType.BACKTRACK)

    success = bool(result.solution) and result.solution[-1] == end

    visited_cells = len(
        {
            event.position
            for event in result.events
            if event.type in {
                EventType.MOVE,
                EventType.BACKTRACK
            }
        }
    )

    return SolveMetrics(
        solution_length = len(result.solution),
        moves = moves,
        backtracks = backtracks,
        success = success,
        visited_cells = visited_cells,
        execution_time = execution_time
    )

def measure_execution_time(solver, maze, start: tuple[int, int], end: tuple[int, int]) -> tuple[SolveResult, float]:
    start_time = time.perf_counter()

    result = solver.solve(maze, start, end)

    execution_time = (time.perf_counter() - start_time)

    return result, execution_time