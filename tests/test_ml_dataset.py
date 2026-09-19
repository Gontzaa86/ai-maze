from ai.dataset.dataset import MLDataset
from ai.dataset.sample import Action
from dataset.record import DatasetRecord

def create_record(seed, solution=None):
    if solution is None:
        solution = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 2),
        ]

    return DatasetRecord(
        generator="recursive_backtracking",
        solver="bfs",
        rows=3,
        cols=3,
        seed=seed,
        start=solution[0],
        end=solution[-1],
        maze=[
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        solution=solution,
        solution_length=len(solution),
        moves=len(solution) - 1,
        backtracks=0,
        visited_cells=len(solution),
        execution_time=0.001,
        success=True,
    )

def create_records(count):
    return [
        create_record(seed)
        for seed in range(count)
    ]

def test_from_records_creates_expected_record_splits():
    records = create_records(100)

    dataset = MLDataset.from_records(
        records,
        seed=42,
    )

    assert len(dataset.train_records) == 70
    assert len(dataset.validation_records) == 15
    assert len(dataset.test_records) == 15

def test_from_records_creates_samples():
    records = create_records(10)

    dataset = MLDataset.from_records(
        records,
        seed=42,
    )

    total_samples = (
        len(dataset.train_samples)
        + len(dataset.validation_samples)
        + len(dataset.test_samples)
    )

    expected_samples = sum(
        len(record.solution) - 1
        for record in records
    )

    assert total_samples == expected_samples

def test_samples_are_not_generated_for_goal_position():
    records = create_records(1)

    dataset = MLDataset.from_records(
        records,
        train_ratio=1.0,
        validation_ratio=0.0,
        test_ratio=0.0,
    )

    samples = dataset.train_samples

    assert len(samples) == 4

    for sample in samples:
        assert sample.state[6].sum() == 1.0

def test_train_statistics_count_actions():
    records = create_records(10)

    dataset = MLDataset.from_records(
        records,
        train_ratio=1.0,
        validation_ratio=0.0,
        test_ratio=0.0,
    )

    statistics = dataset.train_statistics()

    assert statistics.records == 10
    assert statistics.samples == 40

    assert statistics.actions[Action.RIGHT] == 20
    assert statistics.actions[Action.DOWN] == 20
    assert statistics.actions[Action.UP] == 0
    assert statistics.actions[Action.LEFT] == 0

def test_statistics_sum_to_number_of_samples():
    records = create_records(20)

    dataset = MLDataset.from_records(
        records,
        seed=42,
    )

    for statistics in (
        dataset.train_statistics(),
        dataset.validation_statistics(),
        dataset.test_statistics(),
    ):
        assert sum(statistics.actions.values()) == statistics.samples

def test_failed_records_generate_no_samples():
    record = create_record(42)

    failed_record = DatasetRecord(
        generator=record.generator,
        solver=record.solver,
        rows=record.rows,
        cols=record.cols,
        seed=record.seed,
        start=record.start,
        end=record.end,
        maze=record.maze,
        solution=record.solution,
        solution_length=record.solution_length,
        moves=record.moves,
        backtracks=record.backtracks,
        visited_cells=record.visited_cells,
        execution_time=record.execution_time,
        success=False,
    )

    dataset = MLDataset.from_records(
        [failed_record],
        train_ratio=1.0,
        validation_ratio=0.0,
        test_ratio=0.0,
    )

    assert len(dataset.train_records) == 1
    assert len(dataset.train_samples) == 0