import pygame # type: ignore

from maze.maze import Maze
from solvers.events import SolveResult, SolverEvent, EventType
from visualization.pygame_view import PygameMazeView

def test_pygame_view_uses_solution_edge_marks_when_solved():
    maze = Maze(2, 2)

    solution = [
        (0, 0),
        (0, 1),
        (1, 1),
    ]

    edge_marks = {
        frozenset(((0, 0), (0, 1))): 1,
        frozenset(((0, 1), (1, 1))): 1,
    }

    result = SolveResult(
        solution=solution,
        events=[
            SolverEvent(
                type=EventType.START,
                position=(0, 0),
            ),
            SolverEvent(
                type=EventType.SOLVED,
                position=(1, 1),
            ),
        ],
        edge_marks=edge_marks,
    )

    pygame.init()

    view = PygameMazeView(
        maze,
        result,
    )

    view._apply_event(result.events[0])
    view._apply_event(result.events[1])

    assert view.finished is True
    assert view.edge_marks == edge_marks