from maze.maze import Maze
from solvers.astar import AStarSolver
from solvers.events import EventType


def test_astar_finds_path_in_simple_maze():
    maze = Maze(1, 3)

    maze.remove_wall(
        maze.get_cell(0, 0),
        maze.get_cell(0, 1),
    )

    maze.remove_wall(
        maze.get_cell(0, 1),
        maze.get_cell(0, 2),
    )

    solver = AStarSolver()

    result = solver.solve(
        maze,
        (0, 0),
        (0, 2),
    )

    assert result.solution == [
        (0, 0),
        (0, 1),
        (0, 2),
    ]

    assert result.solution[-1] == (0, 2)
    assert result.events[0].type == EventType.START
    assert result.events[-1].type == EventType.SOLVED


def test_astar_returns_empty_solution_when_unreachable():
    maze = Maze(1, 2)

    solver = AStarSolver()

    result = solver.solve(
        maze,
        (0, 0),
        (0, 1),
    )

    assert result.solution == []
    assert result.events[0].type == EventType.START
    assert result.events[-1].type == EventType.SOLVED


def test_astar_marks_solution_edges():
    maze = Maze(1, 3)

    maze.remove_wall(
        maze.get_cell(0, 0),
        maze.get_cell(0, 1),
    )

    maze.remove_wall(
        maze.get_cell(0, 1),
        maze.get_cell(0, 2),
    )

    solver = AStarSolver()

    result = solver.solve(
        maze,
        (0, 0),
        (0, 2),
    )

    assert result.edge_marks == {
        frozenset(((0, 0), (0, 1))): 1,
        frozenset(((0, 1), (0, 2))): 1,
    }


def test_astar_uses_manhattan_heuristic():
    solver = AStarSolver()

    assert solver._heuristic((0, 0), (3, 4)) == 7
    assert solver._heuristic((2, 5), (2, 5)) == 0