import pytest # type: ignore

from solvers.events import SolveResult
from solvers.registry import create_solver, get_solver_names, register_solver, get_solver, SolverRegistryError
from solvers.tremaux import TremauxSolver
from solvers.base import Solver

def test_tremaux_is_registered():
    assert "tremaux" in get_solver_names()

def test_create_tremaux_solver():
    solver = create_solver("tremaux")

    assert isinstance(solver, TremauxSolver)

def test_create_solver_is_case_insensitive():
    solver = create_solver("TREMAUX")

    assert isinstance(solver, TremauxSolver)

def test_unknown_solver():
    with pytest.raises(SolverRegistryError):
        create_solver("inexistente")

def test_register_custom_solver():
    @register_solver(
        name="dummy",
        display_name="Dummy Solver",
        description="Solver utilizado para probar la extensibilidad.",
        category="test",
    )
    class DummySolver(Solver):

        def solve(
            self,
            maze,
            start,
            end
        ) -> SolveResult:
            return SolveResult(
                solution=[start, end],
                events=[],
                edge_marks={}
            )

    info = get_solver("dummy")

    assert info.metadata.name == "dummy"
    assert info.metadata.display_name == "Dummy Solver"
    assert info.metadata.description == (
        "Solver utilizado para probar la extensibilidad."
    )
    assert info.metadata.category == "test"

    solver = create_solver("dummy")

    assert isinstance(solver, DummySolver)
    assert isinstance(solver, Solver)

def test_register_duplicate_solver():
    @register_solver(
        name="duplicate",
        display_name="Duplicate Solver",
        description="Primer registro.",
        category="test",
    )
    class FirstSolver(Solver):

        def solve(
            self,
            maze,
            start,
            end
        ) -> SolveResult:
            return SolveResult(
                solution=[start, end],
                events=[],
                edge_marks={}
            )

    with pytest.raises(SolverRegistryError):
        @register_solver(
            name="duplicate",
            display_name="Another Solver",
            description="Segundo registro.",
            category="test",
        )
        class SecondSolver(Solver):

            def solve(
                self,
                maze,
                start,
                end
            ) -> SolveResult:
                return SolveResult(
                    solution=[start, end],
                    events=[],
                    edge_marks={}
                )

def test_register_non_solver_class():
    with pytest.raises(SolverRegistryError):

        @register_solver(
            name="invalid",
            display_name="Invalid",
            description="No es un solver.",
            category="test",
        )
        class InvalidSolver:
            pass

def test_register_empty_name():
    with pytest.raises(SolverRegistryError):

        @register_solver(
            name="   ",
            display_name="Invalid",
            description="Nombre vacío.",
            category="test",
        )
        class EmptyNameSolver(Solver):

            def solve(
                self,
                maze,
                start,
                end
            ) -> SolveResult:
                return SolveResult(
                    solution=[start, end],
                    events=[],
                    edge_marks={}
                )