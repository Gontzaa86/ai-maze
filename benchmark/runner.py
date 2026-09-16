from dataclasses import dataclass

from maze.maze import Maze

from solvers.base import Solver
from solvers.events import SolveResult

from .metrics import SolveMetrics, calculate_metrics, measure_execution_time
from .record import BenchmarkRecord

from generators.registry import get_generators
from solvers.registry import get_solvers

@dataclass(frozen = True)
class BenchmarkResult:
    result: SolveResult
    metrics: SolveMetrics
    record: BenchmarkRecord

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

        generator_name = next(
            info.metadata.name
            for info in get_generators()
            if info.generator_class is generator.__class__
        )
        solver_name = next(
            info.metadata.name
            for info in get_solvers()
            if info.solver_class is solver.__class__
        )

        record = BenchmarkRecord(
            generator = generator_name,
            solver = solver_name,
            rows = rows,
            cols = cols,
            seed = generator.seed,
            metrics = metrics
        )

        return BenchmarkResult(
            result = result,
            metrics = metrics,
            record = record
        )