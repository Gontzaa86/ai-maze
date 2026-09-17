import pytest # type: ignore

from dataset.builder import generate_dataset

from generators.registry import discover_generators
from solvers.registry import discover_solvers

discover_generators()
discover_solvers()

def test_generate_dataset_combines_generators_and_solvers():
    records = generate_dataset(
        generators=[
            "recursive_backtracking",
            "cyclic",
        ],
        solvers=["bfs"],
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed_count=3,
        seed=123,
    )

    assert len(records) == 6

    generators = {record.generator for record in records}
    solvers = {record.solver for record in records}

    assert generators == {
        "recursive_backtracking",
        "cyclic",
    }

    assert solvers == {"bfs"}

def test_generate_dataset_with_multiple_solvers():
    records = generate_dataset(
        generators=["recursive_backtracking"],
        solvers=["bfs", "tremaux"],
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed_count=4,
        seed=456,
    )

    assert len(records) == 8

    solver_names = {record.solver for record in records}

    assert solver_names == {"bfs", "tremaux"}

def test_generate_dataset_uses_same_seeds_for_combinations():
    records = generate_dataset(
        generators=[
            "recursive_backtracking",
            "cyclic",
        ],
        solvers=["bfs"],
        rows=4,
        cols=4,
        start=(0, 0),
        end=(3, 3),
        seed_count=5,
        seed=999,
    )

    recursive_seeds = {
        record.seed
        for record in records
        if record.generator == "recursive_backtracking"
    }

    cyclic_seeds = {
        record.seed
        for record in records
        if record.generator == "cyclic"
    }

    assert recursive_seeds == cyclic_seeds
    assert len(recursive_seeds) == 5

def test_generate_dataset_is_reproducible():
    kwargs = {
        "generators": [
            "recursive_backtracking",
            "cyclic",
        ],
        "solvers": ["bfs"],
        "rows": 5,
        "cols": 5,
        "start": (0, 0),
        "end": (4, 4),
        "seed_count": 5,
        "seed": 777,
    }

    first = generate_dataset(**kwargs)
    second = generate_dataset(**kwargs)

    assert [
        (
            record.generator,
            record.solver,
            record.seed,
            record.maze,
            record.solution,
        )
        for record in first
    ] == [
        (
            record.generator,
            record.solver,
            record.seed,
            record.maze,
            record.solution,
        )
        for record in second
    ]

def test_generate_dataset_requires_generator():
    with pytest.raises(ValueError):
        generate_dataset(
            generators=[],
            solvers=["bfs"],
            rows=5,
            cols=5,
            start=(0, 0),
            end=(4, 4),
            seed_count=1,
        )

def test_generate_dataset_requires_solver():
    with pytest.raises(ValueError):
        generate_dataset(
            generators=["recursive_backtracking"],
            solvers=[],
            rows=5,
            cols=5,
            start=(0, 0),
            end=(4, 4),
            seed_count=1,
        )

def test_generate_dataset_rejects_negative_seed_count():
    with pytest.raises(ValueError):
        generate_dataset(
            generators=["recursive_backtracking"],
            solvers=["bfs"],
            rows=5,
            cols=5,
            start=(0, 0),
            end=(4, 4),
            seed_count=-1,
        )