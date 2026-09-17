from dataset.generator import DatasetGenerator
from dataset.summary import summarize_dataset

from generators.registry import discover_generators
from solvers.registry import discover_solvers

discover_generators()
discover_solvers()

def create_records():
    generator = DatasetGenerator()

    return generator.generate_many(
        generator_name="recursive_backtracking",
        solver_name="bfs",
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed_count=5,
        seed=123,
    )

def test_empty_dataset_summary():
    summary = summarize_dataset([])

    assert summary.total_records == 0
    assert summary.successful_records == 0
    assert summary.failed_records == 0

    assert summary.generators == ()
    assert summary.solvers == ()
    assert summary.sizes == ()
    assert summary.unique_seeds == 0

    assert summary.average_solution_length == 0.0
    assert summary.average_moves == 0.0
    assert summary.average_visited_cells == 0.0

def test_dataset_summary_counts_records():
    records = create_records()

    summary = summarize_dataset(records)

    assert summary.total_records == 5
    assert summary.successful_records == 5
    assert summary.failed_records == 0

def test_dataset_summary_detects_generators_and_solvers():
    records = create_records()

    summary = summarize_dataset(records)

    assert summary.generators == ("recursive_backtracking",)

    assert summary.solvers == ("bfs",)

def test_dataset_summary_detects_sizes():
    records = create_records()

    summary = summarize_dataset(records)

    assert summary.sizes == ((5, 5),)

def test_dataset_summary_counts_unique_seeds():
    records = create_records()

    summary = summarize_dataset(records)

    assert summary.unique_seeds == 5

def test_dataset_summary_calculates_averages():
    records = create_records()

    summary = summarize_dataset(records)

    expected_solution_length = (
        sum(
            record.solution_length
            for record in records
        )
        / len(records)
    )

    expected_moves = (
        sum(
            record.moves
            for record in records
        )
        / len(records)
    )

    expected_visited_cells = (
        sum(
            record.visited_cells
            for record in records
        )
        / len(records)
    )

    assert (
        summary.average_solution_length
        == expected_solution_length
    )

    assert summary.average_moves == expected_moves

    assert (
        summary.average_visited_cells
        == expected_visited_cells
    )