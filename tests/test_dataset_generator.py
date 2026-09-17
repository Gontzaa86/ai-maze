from dataset.generator import DatasetGenerator

from generators.registry import discover_generators
from solvers.registry import discover_solvers

discover_generators()
discover_solvers()

def test_generate_dataset_record():
    generator = DatasetGenerator()

    record = generator.generate(
        generator_name="recursive_backtracking",
        solver_name="bfs",
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed=123,
    )

    assert record.generator == "recursive_backtracking"
    assert record.solver == "bfs"

    assert record.rows == 5
    assert record.cols == 5
    assert record.seed == 123

    assert record.start == (0, 0)
    assert record.end == (4, 4)

    assert len(record.maze) == 5
    assert all(len(row) == 5 for row in record.maze)

    assert record.solution
    assert record.solution[0] == (0, 0)
    assert record.solution[-1] == (4, 4)

    assert record.solution_length == len(record.solution)
    assert record.success is True


def test_generate_dataset_is_reproducible():
    generator = DatasetGenerator()

    first = generator.generate(
        generator_name="recursive_backtracking",
        solver_name="bfs",
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed=999,
    )

    second = generator.generate(
        generator_name="recursive_backtracking",
        solver_name="bfs",
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed=999,
    )

    assert first.maze == second.maze
    assert first.solution == second.solution
    assert first.solution_length == second.solution_length
    assert first.moves == second.moves
    assert first.backtracks == second.backtracks
    assert first.visited_cells == second.visited_cells
    assert first.success == second.success


def test_generate_dataset_supports_cyclic_generator():
    generator = DatasetGenerator()

    record = generator.generate(
        generator_name="cyclic",
        solver_name="bfs",
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed=321,
    )

    assert record.generator == "cyclic"
    assert record.solver == "bfs"
    assert record.success is True
    assert len(record.maze) == 5

def test_generate_many_returns_requested_number_of_records():
    generator = DatasetGenerator()

    records = generator.generate_many(
        generator_name="recursive_backtracking",
        solver_name="bfs",
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed_count=10,
        seed=123,
    )

    assert len(records) == 10


def test_generate_many_uses_unique_seed_values():
    generator = DatasetGenerator()

    records = generator.generate_many(
        generator_name="recursive_backtracking",
        solver_name="bfs",
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed_count=20,
        seed=123,
    )

    seeds = [record.seed for record in records]

    assert len(seeds) == len(set(seeds))


def test_generate_many_is_reproducible():
    generator = DatasetGenerator()

    first = generator.generate_many(
        generator_name="recursive_backtracking",
        solver_name="bfs",
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed_count=10,
        seed=999,
    )

    second = generator.generate_many(
        generator_name="recursive_backtracking",
        solver_name="bfs",
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed_count=10,
        seed=999,
    )

    assert [record.seed for record in first] == [
        record.seed for record in second
    ]

    assert [record.maze for record in first] == [
        record.maze for record in second
    ]

    assert [record.solution for record in first] == [
        record.solution for record in second
    ]