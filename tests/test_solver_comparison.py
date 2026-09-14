from generators.cyclic import CyclicMazeGenerator
from solvers.bfs import BFSSolver
from solvers.tremaux import TremauxSolver

def test_bfs_and_tremaux_on_same_cyclic_maze():
    generator = CyclicMazeGenerator(
        extra_connections=10,
        seed=12345
    )

    maze = generator.generate(10, 10)

    start = (0, 0)
    end = (9, 9)

    bfs_result = BFSSolver().solve(
        maze,
        start,
        end
    )

    assert bfs_result.solution

    try:
        tremaux_result = TremauxSolver().solve(
            maze,
            start,
            end
        )
    except RuntimeError:
        tremaux_result = None

    assert tremaux_result is not None
    assert tremaux_result.solution

def count_open_edges(maze):
    edges = 0

    for row in range(maze.rows):
        for col in range(maze.cols):
            cell = maze.get_cell(row, col)

            if (
                col + 1 < maze.cols
                and not cell.walls["right"]
            ):
                edges += 1

            if (
                row + 1 < maze.rows
                and not cell.walls["down"]
            ):
                edges += 1

    return edges

def test_cyclic_maze_has_cycles():
    generator = CyclicMazeGenerator(
        extra_connections=10,
        seed=12345
    )

    maze = generator.generate(10, 10)

    edges = count_open_edges(maze)

    vertices = 10 * 10

    assert edges == vertices - 1 + 10