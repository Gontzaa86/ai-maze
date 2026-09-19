from ai.dataset.builder import TrainingSampleBuilder
from ai.dataset.sample import Action
from dataset.record import DatasetRecord

def create_record(
    *,
    maze=None,
    solution=None,
    success=True,
):
    if maze is None:
        maze = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

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
        seed=42,
        start=solution[0],
        end=solution[-1],
        maze=maze,
        solution=solution,
        solution_length=len(solution),
        moves=len(solution) - 1,
        backtracks=0,
        visited_cells=len(solution),
        execution_time=0.001,
        success=success,
    )

def test_builder_creates_one_sample_per_solution_transition():
    record = create_record()
    builder = TrainingSampleBuilder()

    samples = builder.build(record)

    assert len(samples) == len(record.solution) - 1

def test_builder_generates_expected_actions():
    record = create_record()
    builder = TrainingSampleBuilder()

    samples = builder.build(record)

    assert [sample.action for sample in samples] == [
        Action.RIGHT,
        Action.RIGHT,
        Action.DOWN,
        Action.DOWN,
    ]

def test_sample_state_has_expected_shape():
    record = create_record()
    builder = TrainingSampleBuilder()

    samples = builder.build(record)

    assert all(
        sample.state.shape == (7, 3, 3)
        for sample in samples
    )

def test_current_position_changes_between_samples():
    record = create_record()
    builder = TrainingSampleBuilder()

    samples = builder.build(record)

    for sample, current in zip(
        samples,
        record.solution[:-1],
    ):
        current_channel = sample.state[6]

        assert current_channel[current] == 1.0
        assert current_channel.sum() == 1.0

def test_start_and_goal_remain_constant():
    record = create_record()
    builder = TrainingSampleBuilder()

    samples = builder.build(record)

    for sample in samples:
        assert sample.state[4, 0, 0] == 1.0
        assert sample.state[5, 2, 2] == 1.0

def test_failed_record_generates_no_samples():
    record = create_record(success=False)
    builder = TrainingSampleBuilder()

    samples = builder.build(record)

    assert samples == []

def test_single_cell_solution_generates_no_samples():
    record = create_record(
        solution=[(1, 1)],
    )

    builder = TrainingSampleBuilder()

    samples = builder.build(record)

    assert samples == []

def test_invalid_transition_raises_value_error():
    record = create_record(
        solution=[
            (0, 0),
            (2, 2),
        ],
    )

    builder = TrainingSampleBuilder()

    try:
        builder.build(record)
    except ValueError:
        return

    raise AssertionError(
        "Se esperaba ValueError para una transición inválida."
    )