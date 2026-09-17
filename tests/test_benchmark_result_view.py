import pygame # type: ignore

from benchmark.run_benchmark import BenchmarkRun
from benchmark.summary import BenchmarkSummary
from visualization.benchmark_result_view import BenchmarkResultView

def create_view():
    pygame.init()

    benchmark_run = BenchmarkRun(
        records=[],
        summary=BenchmarkSummary(
            total_runs=100,
            successful_runs=98,
            average_solution_length=42.5,
            average_moves=57.3,
            total_execution_time=0.123456,
        ),
    )

    return BenchmarkResultView(
        benchmark_run=benchmark_run,
        filepath="benchmark_results.csv",
    )

def test_benchmark_result_view_initializes():
    view = create_view()

    assert view.width == 600
    assert view.height == 640
    assert view.filepath == "benchmark_results.csv"

def test_benchmark_result_view_run_returns_back_on_escape():
    view = create_view()

    event = pygame.event.Event(
        pygame.KEYDOWN,
        key=pygame.K_ESCAPE,
    )

    pygame.event.post(event)

    assert view.run() == "back"