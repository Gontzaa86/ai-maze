from dataclasses import dataclass

from .record import BenchmarkRecord

@dataclass(frozen = True)
class BenchmarkSummary:
    total_runs: int
    successful_runs: int
    average_solution_length: float
    average_moves: float
    total_execution_time: float

def summarize(records: list[BenchmarkRecord]) -> BenchmarkSummary:
    if not records:
        return BenchmarkSummary(
            total_runs=0,
            successful_runs=0,
            average_solution_length=0.0,
            average_moves=0.0,
            total_execution_time=0.0
        )

    successful_runs = sum(1 for record in records if record.metrics.success)

    average_solution_length = (sum(record.metrics.solution_length for record in records) / len(records))

    average_moves = (sum(record.metrics.moves for record in records) / len(records))

    total_execution_time = sum(record.metrics.execution_time for record in records)

    return BenchmarkSummary(
        total_runs=len(records),
        successful_runs=successful_runs,
        average_solution_length=average_solution_length,
        average_moves=average_moves,
        total_execution_time=total_execution_time
    )