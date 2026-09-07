import random

from .maze import Maze
from .cell import Cell

class RecursiveBacktrackingGenerator:
    def generate(self, rows: int, cols: int) -> Maze:
        maze = Maze(rows, cols)

        start = maze.get_cell(0, 0)

        stack = [start]
        start.visited = True

        while stack:
            current = stack[-1]

            neighbors = self._get_unvisited_neighbors(maze, current)

            if not neighbors:
                stack.pop()
                continue

            neighbor = random.choice(neighbors)

            maze.remove_wall(current, neighbor)

            neighbor.visited = True
            stack.append(neighbor)

        return maze

    def _get_unvisited_neighbors(self, maze: Maze, cell: Cell) -> list[Cell]:
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

            neighbor = maze.get_cell(row, col)

            if not neighbor.visited:
                neighbors.append(neighbor)

        return neighbors