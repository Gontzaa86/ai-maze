import random

from maze.maze import Maze

from .recursive_backtracking import RecursiveBacktrackingGenerator

from .registry import register_generator

# Busca crear laberintos "no perfectos" (tengas más de un camino a la solución)
@register_generator(
    name = "cyclic",
    display_name = "Cíclico",
    description = "Genera laberintos con conexiones adicionales y ciclos.",
    category = "classic"
)
class CyclicMazeGenerator:
    def __init__(self, extra_connections: int = 5, seed: int | None = None):
        if extra_connections < 0:
            raise ValueError("El número de conexiones adicionales no puede ser negativo.")

        self.extra_connections = extra_connections
        self.random = random.Random(seed)

    def generate(self, rows: int, cols: int) -> Maze:
        maze = RecursiveBacktrackingGenerator(rng = self.random).generate(rows, cols)

        candidates = self._get_closed_internal_walls(maze)

        if self.extra_connections > len(candidates):
            raise ValueError("No hay suficientes paredes internas para crear tantas conexiones.")

        selected = self.random.sample(candidates, self.extra_connections)

        for current, neighbor in selected:
            maze.remove_wall(current, neighbor)

        return maze

    def _get_closed_internal_walls(self, maze: Maze) -> list[tuple]:
        candidates = []

        for row in range(maze.rows):
            for col in range(maze.cols):
                current = maze.get_cell(row, col)

                # Solo comprobamos derecha y abajo para no añadir cada pared dos veces.
                if col + 1 < maze.cols:
                    neighbor = maze.get_cell(row, col + 1)

                    if current.walls["right"]:
                        candidates.append((current, neighbor))

                if row + 1 < maze.rows:
                    neighbor = maze.get_cell(row + 1, col)

                    if current.walls["down"]:
                        candidates.append((current, neighbor))

        return candidates