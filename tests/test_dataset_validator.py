from dataclasses import replace

import pytest # type: ignore

from dataset.generator import DatasetGenerator
from dataset.validator import DatasetValidationError, validate_record, validate_records

from generators.registry import discover_generators
from solvers.registry import discover_solvers

discover_generators()
discover_solvers()

def create_record():
    return DatasetGenerator().generate(
        generator_name="recursive_backtracking",
        solver_name="bfs",
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
        seed=123,
    )

def test_valid_record_passes_validation():
    record = create_record()

    validate_record(record)

def test_valid_records_pass_validation():
    records = [
        create_record(),
        create_record(),
    ]

    validate_records(records)

def test_invalid_maze_dimensions_are_rejected():
    record = create_record()

    invalid = replace(
        record,
        maze=record.maze[:-1],
    )

    with pytest.raises(DatasetValidationError):
        validate_record(invalid)

def test_invalid_maze_cell_value_is_rejected():
    record = create_record()

    maze = [row[:] for row in record.maze]
    maze[0][0] = 16

    invalid = replace(
        record,
        maze=maze,
    )

    with pytest.raises(DatasetValidationError):
        validate_record(invalid)

def test_invalid_start_is_rejected():
    record = create_record()

    invalid = replace(
        record,
        start=(99, 99),
    )

    with pytest.raises(DatasetValidationError):
        validate_record(invalid)

def test_invalid_solution_start_is_rejected():
    record = create_record()

    solution = record.solution[:]
    solution[0] = (1, 1)

    invalid = replace(
        record,
        solution=solution,
    )

    with pytest.raises(DatasetValidationError):
        validate_record(invalid)

def test_invalid_solution_length_is_rejected():
    record = create_record()

    invalid = replace(
        record,
        solution_length=record.solution_length + 1,
    )

    with pytest.raises(DatasetValidationError):
        validate_record(invalid)

def test_negative_metrics_are_rejected():
    record = create_record()

    invalid = replace(
        record,
        moves=-1,
    )

    with pytest.raises(DatasetValidationError):
        validate_record(invalid)

def test_solution_path_must_follow_open_walls():
    record = create_record()

    maze = [row[:] for row in record.maze]

    current = record.solution[0]
    next_position = record.solution[1]

    row, col = current
    next_row, next_col = next_position

    if next_row < row:
        direction = 8
        opposite = 2
    elif next_row > row:
        direction = 2
        opposite = 8
    elif next_col > col:
        direction = 4
        opposite = 1
    else:
        direction = 1
        opposite = 4

    maze[row][col] |= direction
    maze[next_row][next_col] |= opposite

    invalid = replace(
        record,
        maze=maze,
    )

    with pytest.raises(DatasetValidationError):
        validate_record(invalid)


def test_solution_cannot_jump_between_cells():
    record = create_record()

    invalid_solution = [
        record.start,
        record.end,
    ]

    invalid = replace(
        record,
        solution=invalid_solution,
        solution_length=len(invalid_solution),
    )

    with pytest.raises(DatasetValidationError):
        validate_record(invalid)