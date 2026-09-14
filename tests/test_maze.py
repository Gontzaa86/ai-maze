import pytest # type: ignore

from maze.maze import Maze

def test_maze_creation():
    maze = Maze(5, 7)

    assert maze.rows == 5
    assert maze.cols == 7

def test_maze_has_correct_number_of_cells():
    maze = Maze(5, 7)

    assert len(maze.grid) == 5
    assert len(maze.grid[0]) == 7

def test_get_cell():
    maze = Maze(5, 7)

    cell = maze.get_cell(2, 4)

    assert cell.row == 2
    assert cell.col == 4


def test_is_inside():
    maze = Maze(5, 7)

    assert maze.is_inside(0, 0)
    assert maze.is_inside(4, 6)

    assert not maze.is_inside(-1, 0)
    assert not maze.is_inside(5, 0)
    assert not maze.is_inside(0, 7)


def test_invalid_dimensions():
    with pytest.raises(ValueError):
        Maze(0, 5)

    with pytest.raises(ValueError):
        Maze(5, 0)

    with pytest.raises(ValueError):
        Maze(-1, 5)


def test_remove_wall_between_horizontal_cells():
    maze = Maze(1, 2)

    left = maze.get_cell(0, 0)
    right = maze.get_cell(0, 1)

    maze.remove_wall(left, right)

    assert left.walls["right"] is False
    assert right.walls["left"] is False


def test_remove_wall_between_vertical_cells():
    maze = Maze(2, 1)

    top = maze.get_cell(0, 0)
    bottom = maze.get_cell(1, 0)

    maze.remove_wall(top, bottom)

    assert top.walls["down"] is False
    assert bottom.walls["up"] is False


def test_remove_wall_requires_adjacent_cells():
    maze = Maze(3, 3)

    first = maze.get_cell(0, 0)
    second = maze.get_cell(2, 2)

    with pytest.raises(ValueError):
        maze.remove_wall(first, second)