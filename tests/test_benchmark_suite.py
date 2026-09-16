from benchmark.suite import BenchmarkSuite

from generators.recursive_backtracking import RecursiveBacktrackingGenerator
from generators.cyclic import CyclicMazeGenerator

from solvers.bfs import BFSSolver

def test_benchmark_suite_runs_multiple_seeds():
    suite = BenchmarkSuite()

    records = suite.run(
        generator=RecursiveBacktrackingGenerator,
        solver=BFSSolver,
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seeds=[1, 2, 3],
    )

    assert len(records) == 3

    assert records[0].seed == 1
    assert records[1].seed == 2
    assert records[2].seed == 3

    for record in records:
        assert record.generator == "recursive_backtracking"
        assert record.solver == "bfs"
        assert record.metrics.success is True

def test_benchmark_suite_runs_multiple_generators_and_solvers():
    suite = BenchmarkSuite()

    records = suite.run_many(
        generators=[
            RecursiveBacktrackingGenerator,
            CyclicMazeGenerator,
        ],
        solvers=[
            BFSSolver,
        ],
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seeds=[1, 2],
    )

    assert len(records) == 4

    assert records[0].generator == "recursive_backtracking"
    assert records[1].generator == "recursive_backtracking"
    assert records[2].generator == "cyclic"
    assert records[3].generator == "cyclic"

    for record in records:
        assert record.solver == "bfs"
        assert record.metrics.success is True

def test_benchmark_suite_can_export_records(tmp_path):

    suite = BenchmarkSuite()

    records = suite.run_many(
        generators=[
            RecursiveBacktrackingGenerator,
            CyclicMazeGenerator,
        ],
        solvers=[
            BFSSolver,
        ],
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seeds=[1, 2],
    )

    filepath = tmp_path / "benchmarks.csv"

    suite.export(
        records=records,
        filepath=filepath,
    )

    assert filepath.exists()

    lines = filepath.read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(lines) == 5
    assert "recursive_backtracking,bfs" in lines[1]
    assert "cyclic,bfs" in lines[3]

def test_benchmark_suite_generates_seeds():

    suite = BenchmarkSuite()

    records = suite.run_many(
        generators=[CyclicMazeGenerator],
        solvers=[BFSSolver],
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed_count=3,
        seed=12345,
    )

    assert len(records) == 3

    assert [
        record.seed
        for record in records
    ] == [
        record.seed
        for record in suite.run_many(
            generators=[CyclicMazeGenerator],
            solvers=[BFSSolver],
            rows=5,
            cols=5,
            start=(0, 0),
            end=(4, 4),
            seed_count=3,
            seed=12345,
        )
    ]


def test_benchmark_suite_rejects_seeds_and_seed_count():

    suite = BenchmarkSuite()

    try:
        suite.run_many(
            generators=[CyclicMazeGenerator],
            solvers=[BFSSolver],
            rows=5,
            cols=5,
            start=(0, 0),
            end=(4, 4),
            seeds=[1, 2, 3],
            seed_count=3,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Debe lanzar ValueError."
        )