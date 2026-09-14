import random

from maze.maze import Maze
from maze.cell import Cell

from .registry import register_generator

# Genera laberintos perfectos (1 solo camino hasta la meta)
@register_generator(
    name = "recursive_backtracking",
    display_name = "Perfecto",
    description = "Genera laberintos perfectos mediante recursive backtracking.",
    category = "classic"
)
class RecursiveBacktrackingGenerator:
    def __init__(self, seed: int | None = None, rng: random.Random | None = None):
        self.random = rng or random.Random(seed) # Generar laberintos mediante semillas. De modo que se genere el mismo siempre

    def generate(self, rows: int, cols: int) -> Maze:
        maze = Maze(rows, cols)

        visited = set()

        start = maze.get_cell(0, 0)

        stack = [start]
        visited.add((start.row, start.col))

        while stack:
            current = stack[-1]

            neighbors = self._get_unvisited_neighbors(maze, current, visited)

            if not neighbors:
                stack.pop()
                continue

            neighbor = self.random.choice(neighbors)

            maze.remove_wall(current, neighbor)

            visited.add((neighbor.row, neighbor.col))
            stack.append(neighbor)

        return maze

    def _get_unvisited_neighbors(self, maze: Maze, cell: Cell, visited: set[tuple[int, int]]) -> list[Cell]:
        neighbors = []

        directions = [
            (-1, 0),    # UP
            (1, 0),     # DOWN
            (0, -1),    # RIGHT
            (0, 1),     # LEFT
        ]

        for row_offset, col_offset in directions:
            row = cell.row + row_offset
            col = cell.col + col_offset

            if not maze.is_inside(row, col):
                continue

            if (row, col) in visited:
                continue

            neighbors.append(maze.get_cell(row, col))

        return neighbors