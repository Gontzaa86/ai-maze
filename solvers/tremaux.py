from maze.maze import Maze
from maze.cell import Cell

class TremauxSolver:
    def solve(self, maze: Maze, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
        current = start
        path = [current] # Inicio del camino recorrido, posición inicial
        visited_edges = set()

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

            else:
                if len(path) == 1:
                    raise RuntimeError("No existe una solución.")

                path.pop()
                current = path[-1]

        return path

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