import numpy as np # type: ignore
import pytest # type: ignore

from ai.representations.global_map import GlobalMapRepresentation
from maze.maze import Maze

def create_open_maze(rows=3, cols=4):
    maze = Maze(rows, cols)

    for row in range(rows):
        for col in range(cols):
            cell = maze.get_cell(row, col)

            if row > 0:
                cell.walls["up"] = False

            if col < cols - 1:
                cell.walls["right"] = False

            if row < rows - 1:
                cell.walls["down"] = False

            if col > 0:
                cell.walls["left"] = False

    return maze

def test_representation_has_expected_shape():
    maze = create_open_maze(3, 4)
    representation = GlobalMapRepresentation()

    result = representation.encode(
        maze=maze,
        start=(0, 0),
        end=(2, 3),
        current=(1, 2),
    )

    assert result.shape == (7, 3, 4)

def test_representation_uses_float32():
    maze = create_open_maze()
    representation = GlobalMapRepresentation()

    result = representation.encode(
        maze=maze,
        start=(0, 0),
        end=(2, 3),
        current=(1, 2),
    )

    assert result.dtype == np.float32

def test_start_channel_contains_only_start_position():
    maze = create_open_maze()
    representation = GlobalMapRepresentation()

    result = representation.encode(
        maze=maze,
        start=(0, 1),
        end=(2, 3),
        current=(1, 2),
    )

    start_channel = result[GlobalMapRepresentation.START]

    assert start_channel[0, 1] == 1.0
    assert np.sum(start_channel) == 1.0

def test_goal_channel_contains_only_goal_position():
    maze = create_open_maze()
    representation = GlobalMapRepresentation()

    result = representation.encode(
        maze=maze,
        start=(0, 0),
        end=(2, 2),
        current=(1, 2),
    )

    goal_channel = result[GlobalMapRepresentation.GOAL]

    assert goal_channel[2, 2] == 1.0
    assert np.sum(goal_channel) == 1.0

def test_current_channel_contains_only_current_position():
    maze = create_open_maze()
    representation = GlobalMapRepresentation()

    result = representation.encode(
        maze=maze,
        start=(0, 0),
        end=(2, 3),
        current=(1, 2),
    )

    current_channel = result[GlobalMapRepresentation.CURRENT]

    assert current_channel[1, 2] == 1.0
    assert np.sum(current_channel) == 1.0

def test_current_can_overlap_start():
    maze = create_open_maze()
    representation = GlobalMapRepresentation()

    result = representation.encode(
        maze=maze,
        start=(0, 0),
        end=(2, 3),
        current=(0, 0),
    )

    assert result[
        GlobalMapRepresentation.START,
        0,
        0,
    ] == 1.0

    assert result[
        GlobalMapRepresentation.CURRENT,
        0,
        0,
    ] == 1.0

def test_current_can_overlap_goal():
    maze = create_open_maze()
    representation = GlobalMapRepresentation()

    result = representation.encode(
        maze=maze,
        start=(0, 0),
        end=(2, 3),
        current=(2, 3),
    )

    assert result[
        GlobalMapRepresentation.GOAL,
        2,
        3,
    ] == 1.0

    assert result[
        GlobalMapRepresentation.CURRENT,
        2,
        3,
    ] == 1.0

@pytest.mark.parametrize(
    "position,name",
    [
        ((-1, 0), "start"),
        ((0, 4), "end"),
        ((3, 0), "current"),
    ],
)
def test_invalid_position_raises_value_error(position, name):
    maze = create_open_maze(3, 4)
    representation = GlobalMapRepresentation()

    kwargs = {
        "maze": maze,
        "start": (0, 0),
        "end": (2, 3),
        "current": (1, 1),
    }

    kwargs[name] = position

    with pytest.raises(ValueError):
        representation.encode(**kwargs)

def test_wall_channels_use_zero_and_one():
    maze = create_open_maze()
    representation = GlobalMapRepresentation()

    result = representation.encode(
        maze=maze,
        start=(0, 0),
        end=(2, 3),
        current=(1, 2),
    )

    wall_channels = result[
        :4,
    ]

    assert np.all((wall_channels == 0.0) | (wall_channels == 1.0))