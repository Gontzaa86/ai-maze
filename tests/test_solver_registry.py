import pytest # type: ignore

from solvers.registry import create_solver, get_solver_names
from solvers.tremaux import TremauxSolver

def test_tremaux_is_registered():
    assert "tremaux" in get_solver_names()

def test_create_tremaux_solver():
    solver = create_solver("tremaux")

    assert isinstance(solver, TremauxSolver)

def test_create_solver_is_case_insensitive():
    solver = create_solver("TREMAUX")

    assert isinstance(solver, TremauxSolver)

def test_unknown_solver():
    with pytest.raises(ValueError):
        create_solver("inexistente")