from benchmark.csv_exporter import BenchmarkCSVExporter
from benchmark.record import BenchmarkRecord
from benchmark.metrics import SolveMetrics
from benchmark.runner import BenchmarkRunner
from generators.recursive_backtracking import RecursiveBacktrackingGenerator
from solvers.bfs import BFSSolver

def test_csv_exporter(tmp_path):
    metrics = SolveMetrics(
        solution_length=10,
        moves=12,
        backtracks=2,
        success=True,
        visited_cells=8,
        execution_time=0.001,
    )

    record = BenchmarkRecord(
        generator="recursive_backtracking",
        solver="bfs",
        rows=5,
        cols=5,
        seed=12345,
        metrics=metrics,
    )

    filepath = tmp_path / "benchmark.csv"

    exporter = BenchmarkCSVExporter()

    exporter.export(
        records=[record],
        filepath=filepath,
    )

    assert filepath.exists()

    content = filepath.read_text(encoding="utf-8")

    assert "generator,solver,rows,cols,seed" in content
    assert "recursive_backtracking,bfs,5,5,12345" in content
    assert ",10,12,2,True,8,0.001" in content

def test_benchmark_result_can_be_exported_to_csv(tmp_path):

    generator = RecursiveBacktrackingGenerator(
        seed=12345
    )

    solver = BFSSolver()

    runner = BenchmarkRunner()

    benchmark = runner.run(
        generator=generator,
        solver=solver,
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
    )

    filepath = tmp_path / "benchmark.csv"

    exporter = BenchmarkCSVExporter()

    exporter.export(
        records=[benchmark.record],
        filepath=filepath,
    )

    content = filepath.read_text(
        encoding="utf-8"
    )

    assert "recursive_backtracking,bfs,5,5,12345" in content

def test_csv_exporter_multiple_records(tmp_path):

    generator_a = RecursiveBacktrackingGenerator(
        seed=12345
    )

    generator_b = RecursiveBacktrackingGenerator(
        seed=54321
    )

    solver = BFSSolver()

    runner = BenchmarkRunner()

    benchmark_a = runner.run(
        generator=generator_a,
        solver=solver,
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
    )

    benchmark_b = runner.run(
        generator=generator_b,
        solver=solver,
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
    )

    filepath = tmp_path / "benchmarks.csv"

    exporter = BenchmarkCSVExporter()

    exporter.export(
        records=[
            benchmark_a.record,
            benchmark_b.record,
        ],
        filepath=filepath,
    )

    lines = filepath.read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(lines) == 3
    assert "12345" in lines[1]
    assert "54321" in lines[2]