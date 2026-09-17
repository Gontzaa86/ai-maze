from dataset.record import encode_cell, encode_maze
from maze.maze import Maze

def test_encode_cell_all_walls():
    maze = Maze(1, 1)

    cell = maze.get_cell(0, 0)

    assert encode_cell(cell) == 15


def test_encode_cell_no_walls():
    maze = Maze(1, 1)

    cell = maze.get_cell(0, 0)

    cell.walls["up"] = False
    cell.walls["right"] = False
    cell.walls["down"] = False
    cell.walls["left"] = False

    assert encode_cell(cell) == 0


def test_encode_cell_uses_u_r_d_l_bits():
    maze = Maze(1, 1)

    cell = maze.get_cell(0, 0)

    cell.walls["up"] = True
    cell.walls["right"] = False
    cell.walls["down"] = True
    cell.walls["left"] = True

    assert encode_cell(cell) == 11


def test_encode_cell_single_walls():
    maze = Maze(1, 1)

    cell = maze.get_cell(0, 0)

    cell.walls["up"] = True
    cell.walls["right"] = False
    cell.walls["down"] = False
    cell.walls["left"] = False

    assert encode_cell(cell) == 8

    cell.walls["up"] = False
    cell.walls["right"] = True

    assert encode_cell(cell) == 4

    cell.walls["right"] = False
    cell.walls["down"] = True

    assert encode_cell(cell) == 2

    cell.walls["down"] = False
    cell.walls["left"] = True

    assert encode_cell(cell) == 1


def test_encode_maze_dimensions():
    maze = Maze(3, 4)

    encoded = encode_maze(maze)

    assert len(encoded) == 3
    assert all(len(row) == 4 for row in encoded)


def test_encode_maze_initial_walls():
    maze = Maze(2, 2)

    encoded = encode_maze(maze)

    assert encoded == [[15, 15], [15, 15]]