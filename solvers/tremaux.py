from maze.maze import Maze
from maze.cell import Cell

from .events import EventType, SolverEvent, SolveResult

from solvers.base import Solver

from solvers.registry import register_solver

"""
Regla 1
- Si estamos en una intersección y existe un camino con 0 marcas, preferimos ese camino.

Regla 2
- Si no existe ninguno, podemos utilizar un camino con 1 marca para retroceder.

Regla 3
- Nunca queremos elegir un camino con 2 marcas salvo que sea necesario para salir del laberinto.
"""

@register_solver(
    name = "tremaux",
    display_name = "Trémaux",
    description = "Algoritmo de exploración basado en marcas de aristas.",
    category = "classic"
)
class TremauxSolver(Solver):
    def solve(self, maze: Maze, start: tuple[int, int], end: tuple[int, int]) -> SolveResult:
        if not maze.is_inside(*start):
            raise ValueError("La posición inicial no está dentro del laberinto.")
        if not maze.is_inside(*end):
            raise ValueError("La posición final no está dentro del laberinto.")

        # Todas las aristas comienzan con marca 0.
        # Solo almacenamos explícitamente las que hemos recorrido.
        edge_marks: dict[frozenset, int] = {}

        # La pila representa el camino actual.
        path = [start]

        events = [
            SolverEvent(
                type = EventType.START,
                position = start
            )
        ]

        current = start

        while current != end:
            cell = maze.get_cell(*current)

            neighbors = self._get_open_neighbors(maze, cell)

            # ----------------------------------------
            # 1º Preferencia de Trémaux:
            #   - Buscar una arista con marca 0.
            # ----------------------------------------

            unmarked = [
                neighbor
                for neighbor in neighbors
                if self._get_edge_mark(edge_marks, current, neighbor) == 0
            ]

            if unmarked:
                # Seleccionamos primera arista no marcada.
                neighbor = unmarked[0]

                new_mark = self._traverse_edge(edge_marks, current, neighbor)

                events.append(
                    SolverEvent(
                        EventType.MOVE,
                        position = neighbor,
                        from_position = current,
                        to_position = neighbor,
                        mark = new_mark
                    )
                )

                current = neighbor
                path.append(current)

                continue

            # ----------------------------------------
            # 2º Preferencia de Trémaux:
            #   - Si no quedan aristas 0.
            #   - Buscamos aristas marcadas con 1.
            # ----------------------------------------

            once_marked = [
                neighbor
                for neighbor in neighbors
                if self._get_edge_mark(edge_marks, current, neighbor) == 1
            ]

            if once_marked:
                neighbor = once_marked[0]

                new_mark = self._traverse_edge(edge_marks, current, neighbor)

                events.append(
                    SolverEvent(
                        EventType.BACKTRACK,
                        position = neighbor,
                        from_position = current,
                        to_position = neighbor,
                        mark = new_mark
                    )
                )

                current = neighbor

                # Si volvemos a una posición anterior, actualizamos la representación del camino actual.
                if len(path) > 1 and neighbor == path[-2]:
                    path.pop()
                else:
                    path.append(neighbor)

                continue

            # ----------------------------------------
            # 3º Preferencia de Trémaux:
            #   - No quedan caminos disponibles.
            # ----------------------------------------

            raise RuntimeError("No existe una solución.")

        events.append(
            SolverEvent(
                EventType.SOLVED,
                position = end
            )
        )

        return SolveResult(
            solution = path,
            events = events,
            edge_marks = edge_marks
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

    def _edge_key(self, a: tuple[int, int], b: tuple[int, int]) -> frozenset:
        return frozenset((a, b))

    def _get_edge_mark(self, edge_marks: dict[frozenset, int], a: tuple[int, int], b: tuple[int, int]) -> int:
        edge = self._edge_key(a, b)

        return edge_marks.get(edge, 0)

    def _traverse_edge(self, edge_marks: dict[frozenset, int], a: tuple[int, int], b: tuple[int, int]) -> int:
        edge = self._edge_key(a, b)

        current_mark = edge_marks.get(edge, 0)

        if current_mark >= 2:
            raise RuntimeError("Se ha intentado recorred una arista marcada dos veces.")

        new_mark = current_mark + 1

        edge_marks[edge] = new_mark

        return new_mark