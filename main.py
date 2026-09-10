import pygame # type: ignore

from maze.generator import RecursiveBacktrackingGenerator
from maze.maze import Maze

from solvers.base import Solver
from solvers.tremaux import TremauxSolver
from solvers.events import EventType, SolveResult

from visualization.pygame_view import PygameMazeView
from visualization.menu import MazeMenu

def create_maze(rows: int, cols: int) -> Maze:
    generator = RecursiveBacktrackingGenerator()

    return generator.generate(rows, cols)

def solve_maze(solver: Solver, maze: Maze, start: tuple[int, int], end: tuple[int, int]) -> SolveResult:
    return solver.solve(maze, start, end)

def create_solver(name: str = "tremaux") -> Solver:
    solvers = {
        "tremaux": TremauxSolver,
    }

    try:
        solver_class = solvers[name.lower()]
    except KeyError:
        raise ValueError(
            f"Solver desconocido: {name}"
        )

    return solver_class()

def print_result(result: SolveResult):
    moves = sum(
        1
        for event in result.events
        if event.type == EventType.MOVE
    )

    backtracks = sum(
        1
        for event in result.events
        if event.type == EventType.BACKTRACK
    )

    print()
    print("=== Resultado ===")
    print()

    print(f"Longitud solución:  {len(result.solution)}")
    print(f"Movimientos:        {moves}")
    print(f"Retrocesos:         {backtracks}")
    print(f"Eventos:            {len(result.events)}")
    print(f"Aristas marcadas:   {len(result.edge_marks)}")

    print()

    print("Solución:")
    print(result.solution)

def main():
    pygame.init()

    menu = MazeMenu()

    solver = TremauxSolver() # A futuro, un selector.

    running = True

    while running:
        dimensions = menu.run()

        if dimensions is None:
            break

        rows, cols, solver_name = dimensions

        print(f"Algoritmo seleccionado: {solver_name}")

        print("Generando laberinto...")

        maze = create_maze(rows, cols)

        print("Laberinto generado.")

        start = (0, 0)
        end = (rows - 1, cols - 1)

        solver = create_solver(solver_name)

        print(f"Resolviendo con {solver_name}...")

        result = solve_maze(solver, maze, start, end)

        print("Laberinto resuelto.")

        print_result(result)

        print("Abriendo visualización...")

        view = PygameMazeView(maze, result)

        action = view.run()

        if action == "quit":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()