from dataclasses import dataclass
from pathlib import Path

from generators.registry import create_generator
from solvers.registry import create_solver

from .suite import BenchmarkSuite
from .record import BenchmarkRecord
from .summary import BenchmarkSummary, summarize

@dataclass(frozen = True)
class BenchmarkRun:
    records: list[BenchmarkRecord]
    summary: BenchmarkSummary

def run_benchmark(
        generator_name: str,
        solver_name: str,
        rows: int,
        cols: int,
        start: tuple[int, int],
        end: tuple[int, int],
        seed_count: int,
        seed: int | None = None,
        filepath: str | Path = "benchmark_results.csv",
) -> BenchmarkRun:
    generator = create_generator(generator_name)
    solver = create_solver(solver_name)
    
    suite = BenchmarkSuite()

    records = suite.run_many(
        generators=[generator.__class__],
        solvers=[solver.__class__],
        rows=rows,
        cols=cols,
        start=start,
        end=end,
        seed_count=seed_count,
        seed=seed
    )

    suite.export(
        records = records,
        filepath = filepath
    )

    summary = summarize(records)

    return BenchmarkRun(
        records=records,
        summary=summary
    )