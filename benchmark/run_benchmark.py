from dataclasses import dataclass
from pathlib import Path

from .suite import BenchmarkSuite
from .record import BenchmarkRecord
from .summary import BenchmarkSummary, summarize

@dataclass(frozen = True)
class BenchmarkRun:
    records: list[BenchmarkRecord]
    summary: BenchmarkSummary

def run_benchmark(
        generator,
        solver,
        rows: int,
        cols: int,
        start: tuple[int, int],
        end: tuple[int, int],
        seed_count: int,
        seed: int | None = None,
        filepath: str | Path = "benchmark_results.csv",
) -> BenchmarkRun:
    suite = BenchmarkSuite()

    records = suite.run_many(
        generators=[generator],
        solvers=[solver],
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