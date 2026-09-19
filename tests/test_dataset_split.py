import pytest # type: ignore

from ai.dataset.split import DatasetSplitter
from dataset.record import DatasetRecord

def create_record(seed):
    return DatasetRecord(
        generator="recursive_backtracking",
        solver="bfs",
        rows=3,
        cols=3,
        seed=seed,
        start=(0, 0),
        end=(2, 2),
        maze=[
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        solution=[
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 2),
        ],
        solution_length=5,
        moves=4,
        backtracks=0,
        visited_cells=5,
        execution_time=0.001,
        success=True,
    )

def create_records(count):
    return [create_record(seed) for seed in range(count)]

def test_split_uses_expected_ratios():
    records = create_records(100)

    result = DatasetSplitter().split(records)

    assert len(result.train) == 70
    assert len(result.validation) == 15
    assert len(result.test) == 15

def test_split_contains_all_records():
    records = create_records(100)

    result = DatasetSplitter().split(records)

    combined = (
        list(result.train)
        + list(result.validation)
        + list(result.test)
    )

    original_seeds = {record.seed for record in records}
    split_seeds = {record.seed for record in combined}

    assert len(combined) == len(records)
    assert split_seeds == original_seeds

def test_split_is_reproducible():
    records = create_records(100)
    splitter = DatasetSplitter()

    first = splitter.split(records, seed=123)
    second = splitter.split(records, seed=123)

    assert first == second

def test_different_seeds_produce_different_splits():
    records = create_records(100)
    splitter = DatasetSplitter()

    first = splitter.split(records, seed=123)
    second = splitter.split(records, seed=456)

    assert first != second

def test_original_records_are_not_modified():
    records = create_records(100)
    original = list(records)

    DatasetSplitter().split(records, seed=123)

    assert records == original

def test_empty_dataset_is_supported():
    result = DatasetSplitter().split([])

    assert result.train == ()
    assert result.validation == ()
    assert result.test == ()

@pytest.mark.parametrize(
    "ratios",
    [
        (0.5, 0.5, 0.5),
        (0.8, 0.1, 0.2),
        (-0.1, 0.6, 0.5),
        (1.1, -0.1, 0.0),
    ],
)
def test_invalid_ratios_raise_value_error(ratios):
    with pytest.raises(ValueError):
        DatasetSplitter().split(
            create_records(10),
            train_ratio=ratios[0],
            validation_ratio=ratios[1],
            test_ratio=ratios[2],
        )