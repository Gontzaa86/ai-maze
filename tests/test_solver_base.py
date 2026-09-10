import pytest # type: ignore

from maze.maze import Maze
from solvers.base import Solver
from solvers.tremaux import TremauxSolver

def test_solver_is_abstract():
    with pytest.raises(TypeError):
        Solver()

def test_tremaux_is_solver():
    solver = TremauxSolver()

    assert isinstance(solver, Solver)