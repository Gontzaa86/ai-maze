import pytest # type: ignore

from generators.cyclic import CyclicMazeGenerator

def count_open_edges(maze):
    edges = 0

    for row in range(maze.rows):
        for col in range(maze.cols):
            cell = maze.get_cell(row, col)

            if not cell.walls["right"] and col + 1 < maze.cols:
                edges += 1

            if not cell.walls["down"] and row + 1 < maze.rows:
                edges += 1

    return edges

def get_reachable_cells(maze):
    start = (0, 0)

    visited = {start}
    stack = [start]

    while stack:
        row, col = stack.pop()

        cell = maze.get_cell(row, col)

        neighbors = []

        if not cell.walls["up"]:
            neighbors.append((row - 1, col))

        if not cell.walls["right"]:
            neighbors.append((row, col + 1))

        if not cell.walls["down"]:
            neighbors.append((row + 1, col))

        if not cell.walls["left"]:
            neighbors.append((row, col - 1))

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return visited

def test_cyclic_generator_dimensions():
    generator = CyclicMazeGenerator(extra_connections=5)

    maze = generator.generate(10, 15)

    assert maze.rows == 10
    assert maze.cols == 15

def test_zero_extra_connections_creates_perfect_maze():
    rows = 10
    cols = 10

    generator = CyclicMazeGenerator(extra_connections=0)

    maze = generator.generate(rows, cols)

    edges = count_open_edges(maze)

    assert edges == rows * cols - 1

def test_extra_connections_are_added():
    rows = 10
    cols = 10
    extra_connections = 10

    generator = CyclicMazeGenerator(extra_connections=extra_connections)

    maze = generator.generate(rows, cols)

    edges = count_open_edges(maze)

    assert edges == (rows * cols - 1 + extra_connections)

def test_cyclic_maze_is_connected():
    rows = 20
    cols = 20

    generator = CyclicMazeGenerator(extra_connections=30)

    maze = generator.generate(rows, cols)

    reachable = get_reachable_cells(maze)

    assert len(reachable) == rows * cols

def test_negative_extra_connections():
    with pytest.raises(ValueError):
        CyclicMazeGenerator(extra_connections=-1)

def test_too_many_extra_connections():
    generator = CyclicMazeGenerator(extra_connections=1000)

    with pytest.raises(ValueError):
        generator.generate(2, 2)