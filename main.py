import pygame # type: ignore

from maze.generator import RecursiveBacktrackingGenerator
from maze.maze import Maze

from solvers.tremaux import TremauxSolver
from solvers.events import EventType, SolveResult

from visualization.pygame_view import PygameMazeView
from visualization.menu import MazeMenu


def create_maze(rows: int, cols: int) -> Maze:
    generator = RecursiveBacktrackingGenerator()

    return generator.generate(rows, cols)

def solve_maze(maze: Maze, start: tuple[int, int], end: tuple[int, int]) -> SolveResult:

    solver = TremauxSolver()

    return solver.solve(maze, start, end)

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

    dimensions = menu.run()

    if dimensions is None:
        pygame.quit()
        return

    rows, cols = dimensions

    print("Generando laberinto...")

    maze = create_maze(rows, cols)

    print("Laberinto generado.")

    start = (0, 0)
    end = (rows - 1, cols - 1)

    print("Resolviendo con Trémaux...")

    result = solve_maze(maze, start, end)

    print("Laberinto resuelto.")

    print_result(result)

    print("Abriendo visualización...")

    pygame.display.quit()

    view = PygameMazeView(maze, result)
    view.run()

if __name__ == "__main__":
    main()