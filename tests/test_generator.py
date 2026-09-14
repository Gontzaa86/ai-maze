from generators.recursive_backtracking import RecursiveBacktrackingGenerator

def test_generator_creates_correct_dimensions():
    generator = RecursiveBacktrackingGenerator()

    maze = generator.generate(10, 15)

    assert maze.rows == 10
    assert maze.cols == 15

def test_generator_connects_all_cells():
    generator = RecursiveBacktrackingGenerator()

    maze = generator.generate(10, 10)

    visited = set()
    stack = [(0, 0)]

    while stack:

        position = stack.pop()

        if position in visited:
            continue

        if not maze.is_inside(*position):
            continue

        visited.add(position)

        row, col = position
        cell = maze.get_cell(row, col)

        if not cell.walls["up"]:
            stack.append((row - 1, col))

        if not cell.walls["right"]:
            stack.append((row, col + 1))

        if not cell.walls["down"]:
            stack.append((row + 1, col))

        if not cell.walls["left"]:
            stack.append((row, col - 1))

    assert len(visited) == maze.rows * maze.cols

def test_every_cell_is_reachable():
    generator = RecursiveBacktrackingGenerator()

    maze = generator.generate(20, 20)

    visited = set()
    stack = [(0, 0)]

    while stack:

        position = stack.pop()

        if position in visited:
            continue

        visited.add(position)

        row, col = position
        cell = maze.get_cell(row, col)

        if not cell.walls["up"] and row > 0:
            stack.append((row - 1, col))

        if not cell.walls["right"] and col < maze.cols - 1:
            stack.append((row, col + 1))

        if not cell.walls["down"] and row < maze.rows - 1:
            stack.append((row + 1, col))

        if not cell.walls["left"] and col > 0:
            stack.append((row, col - 1))

    assert len(visited) == maze.rows * maze.cols

def test_wall_consistency():
    generator = RecursiveBacktrackingGenerator()

    maze = generator.generate(20, 20)

    for row in range(maze.rows):
        for col in range(maze.cols):

            cell = maze.get_cell(row, col)

            if col < maze.cols - 1:

                east = maze.get_cell(row, col + 1)

                assert (
                    cell.walls["right"]
                    == east.walls["left"]
                )

            if row < maze.rows - 1:

                south = maze.get_cell(row + 1, col)

                assert (
                    cell.walls["down"]
                    == south.walls["up"]
                )

def test_small_mazes():
    generator = RecursiveBacktrackingGenerator()

    for rows, cols in [
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (3, 3),
        (5, 1),
        (1, 5),
    ]:

        maze = generator.generate(rows, cols)

        assert maze.rows == rows
        assert maze.cols == cols

def test_same_seed_generates_same_maze():
    generator_a = RecursiveBacktrackingGenerator(seed=12345)
    generator_b = RecursiveBacktrackingGenerator(seed=12345)

    maze_a = generator_a.generate(10, 10)
    maze_b = generator_b.generate(10, 10)

    assert maze_a.grid == maze_b.grid

def test_different_seeds_generate_different_mazes():
    generator_a = RecursiveBacktrackingGenerator(seed=12345)
    generator_b = RecursiveBacktrackingGenerator(seed=54321)

    maze_a = generator_a.generate(10, 10)
    maze_b = generator_b.generate(10, 10)

    assert maze_a.grid != maze_b.grid