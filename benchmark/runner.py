from dataclasses import dataclass

from maze.maze import Maze

from solvers.base import Solver
from solvers.events import SolveResult

from .metrics import SolveMetrics, calculate_metrics, measure_execution_time

@dataclass(frozen = True)
class BenchmarkResult:
    result: SolveResult
    metrics: SolveMetrics

class BenchmarkRunner:
    def run(
            self,
            generator,
            solver: Solver,
            rows: int,
            cols: int,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> BenchmarkResult:
        maze = generator.generate(rows, cols)

        result, execution_time = measure_execution_time(solver, maze, start, end)

        metrics = calculate_metrics(result, start, end, execution_time = execution_time)

        return BenchmarkResult(
            result = result,
            metrics = metrics
        )