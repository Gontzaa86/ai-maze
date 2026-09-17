from maze.maze import Maze
from solvers.bfs import BFSSolver
from generators.cyclic import CyclicMazeGenerator

def solver_maze():
    from maze.maze import Maze

    maze = Maze(3, 3)

    maze.remove_wall(maze.get_cell(0, 0), maze.get_cell(0, 1))

    maze.remove_wall(maze.get_cell(0, 1), maze.get_cell(0, 2))

    maze.remove_wall(maze.get_cell(0, 2), maze.get_cell(1, 2))

    maze.remove_wall(maze.get_cell(1, 2), maze.get_cell(2, 2))

    return maze

def test_bfs_finds_solution():
    solver = BFSSolver()

    maze = solver_maze()

    result = solver.solve(maze, (0, 0), (2, 2))

    assert result.solution
    assert result.solution[0] == (0, 0)
    assert result.solution[-1] == (2, 2)


def test_bfs_finds_shortest_path():
    maze = Maze(3, 3)

    # Camino corto:
    # (0,0) → (0,1) → (0,2)
    #                    ↓
    #                  (1,2)
    #                    ↓
    #                  (2,2)

    maze.remove_wall(maze.get_cell(0, 0), maze.get_cell(0, 1))

    maze.remove_wall(maze.get_cell(0, 1), maze.get_cell(0, 2))

    maze.remove_wall(maze.get_cell(0, 2), maze.get_cell(1, 2))

    maze.remove_wall(maze.get_cell(1, 2), maze.get_cell(2, 2))

    # Camino alternativo más largo:
    # (0,0) → (1,0) → (2,0)
    #                    ↓
    #                  (2,1)
    #                    ↓
    #                  (2,2)

    maze.remove_wall(maze.get_cell(0, 0), maze.get_cell(1, 0))

    maze.remove_wall(maze.get_cell(1, 0), maze.get_cell(2, 0))

    maze.remove_wall(maze.get_cell(2, 0), maze.get_cell(2, 1))

    maze.remove_wall(maze.get_cell(2, 1), maze.get_cell(2, 2))

    solver = BFSSolver()

    result = solver.solve(maze, (0, 0), (2, 2))

    assert len(result.solution) == 5

def test_bfs_solves_cyclic_maze():
    generator = CyclicMazeGenerator(extra_connections=10, seed=12345)

    maze = generator.generate(10, 10)

    solver = BFSSolver()

    result = solver.solve(maze, (0, 0), (9, 9))

    assert result.solution
    assert result.solution[0] == (0, 0)
    assert result.solution[-1] == (9, 9)

def test_bfs_solution_edges_are_marked_as_one():
    maze = Maze(3, 3)

    maze.remove_wall(maze.get_cell(0, 0), maze.get_cell(0, 1))
    maze.remove_wall(maze.get_cell(0, 1), maze.get_cell(0, 2))
    maze.remove_wall(maze.get_cell(0, 2), maze.get_cell(1, 2))
    maze.remove_wall(maze.get_cell(1, 2), maze.get_cell(2, 2))

    solver = BFSSolver()

    result = solver.solve(maze, (0, 0), (2, 2))

    assert result.solution == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
    ]

    assert all(
        mark == 1
        for mark in result.edge_marks.values()
    )

    assert len(result.edge_marks) == 4