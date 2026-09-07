from maze.maze import Maze
from maze.cell import Cell

from .events import EventType, SolverEvent, SolveResult

"""
Regla 1
- Si estamos en una intersección y existe un camino con 0 marcas, preferimos ese camino.

Regla 2
- Si no existe ninguno, podemos utilizar un camino con 1 marca para retroceder.

Regla 3
- Nunca queremos elegir un camino con 2 marcas salvo que sea necesario para salir del laberinto.
"""

class TremauxSolver:
    def solve(self, maze: Maze, start: tuple[int, int], end: tuple[int, int]) -> SolveResult:
        events = []

        current = start
        path = [current] # Inicio del camino recorrido, posición inicial
        visited_edges = set()

        events.append(
            SolverEvent(
                EventType.START,
                current
            )
        )

        while current != end:
            cell = maze.get_cell(*current)

            neighbors = self._get_open_neighbors(maze, cell)

            unvisited = [
                neighbor
                for neighbor in neighbors
                if self._edge_key(current, neighbor) not in visited_edges
            ]

            if unvisited:
                neighbor = unvisited[0]

                edge = self._edge_key(current, neighbor)

                visited_edges.add(edge)

                current = neighbor
                path.append(current)

                events.append(
                    SolverEvent(
                        EventType.MOVE,
                        current
                    )
                )

            else:
                if len(path) == 1:
                    raise RuntimeError("No existe una solución.")

                path.pop()
                current = path[-1]

                events.append(
                    SolverEvent(
                        EventType.BACKTRACK,
                        current
                    )
                )

        events.append(
            SolverEvent(
                EventType.SOLVED,
                current
            )
        )

        return SolveResult(
            solution = path,
            events = events
        )

    def _get_open_neighbors(self, maze: Maze, cell: Cell) -> list[tuple[int, int]]:
        neighbors = []

        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "right": (0, 1),
            "left": (0, -1)
        }

        for direction, (dr, dc) in directions.items():
            if cell.walls[direction]:
                continue

            row = cell.row + dr
            col = cell.col + dc

            if maze.is_inside(row, col):
                neighbors.append((row, col))

        return neighbors

    def _edge_key(self, a: tuple[int, int], b: tuple[int, int]):
        return frozenset((a, b))