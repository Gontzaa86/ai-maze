from benchmark.record import BenchmarkRecord
from benchmark.metrics import SolveMetrics
from benchmark.summary import summarize

def create_record(
    solution_length,
    moves,
    success,
    execution_time,
):
    return BenchmarkRecord(
        generator="cyclic",
        solver="bfs",
        rows=5,
        cols=5,
        seed=123,
        metrics=SolveMetrics(
            solution_length=solution_length,
            moves=moves,
            backtracks=0,
            success=success,
            visited_cells=10,
            execution_time=execution_time,
        ),
    )

def test_summarize_records():
    records = [
        create_record(10, 9, True, 0.1),
        create_record(20, 19, True, 0.2),
        create_record(30, 29, False, 0.3),
    ]

    summary = summarize(records)

    assert summary.total_runs == 3
    assert summary.successful_runs == 2
    assert summary.average_solution_length == 20
    assert summary.average_moves == 19
    assert summary.total_execution_time == 0.6

def test_summarize_empty_records():
    summary = summarize([])

    assert summary.total_runs == 0
    assert summary.successful_runs == 0
    assert summary.average_solution_length == 0.0
    assert summary.average_moves == 0.0
    assert summary.total_execution_time == 0.0