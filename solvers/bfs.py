from collections import deque

from maze.maze import Maze

from .base import Solver
from .events import EventType, SolveResult, SolverEvent
from .registry import register_solver

@register_solver(
    name = "bfs",
    display_name = "BFS",
    description = "Búsqueda en achura para encontrar el camino más corto.",
    category = "classic"
)
class BFSSolver(Solver):
    def solve(self, maze: Maze, start: tuple[int, int], end: tuple[int, int]) -> SolveResult:
        queue = deque([start])

        visited = {start}

        previous: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

        events = [self._start_event(start)]

        while queue:
            current = queue.popleft()

            if current == end:
                break

            for neighbor in self._get_neighbors(maze, current):
                if neighbor in visited:
                    continue

                visited.add(neighbor)

                previous[neighbor] = current

                queue.append(neighbor)

                events.append(self._move_event(current, neighbor))

        solution = self._build_solution(previous, start, end)

        edge_marks = self._build_edge_marks(solution)

        events.append(self._solved_event(end))

        return SolveResult(
            solution = solution,
            events = events,
            edge_marks = edge_marks
        )

    def _get_neighbors(self, maze: Maze, position: tuple[int, int]) -> list[tuple[int, int]]:
        row, col = position

        neighbors = []

        cell = maze.get_cell(row, col)

        directions = [
            ("up", -1, 0),
            ("right", 0, 1),
            ("down", 1, 0),
            ("left", 0, -1)
        ]

        for wall, row_offset, col_offset in directions:
            if cell.walls[wall]:
                continue

            neighbor_row = row + row_offset
            neighbor_col = col + col_offset

            if not maze.is_inside(neighbor_row, neighbor_col):
                continue

            neighbors.append((neighbor_row, neighbor_col))

        return neighbors

    def _build_solution(
            self,
            previous: dict[tuple[int, int], tuple[int, int] | None],
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        if end not in previous:
            return []

        path = []

        current = end

        while current is not None:
            path.append(current)

            current = previous[current]

        path.reverse()

        return path

    def _build_edge_marks(self, solution: list[tuple[int, int]]) -> dict[frozenset, int]:
        edge_marks = {}

        for current, neighbor in zip(solution, solution[1:]):
            edge = frozenset((current, neighbor))
            edge_marks[edge] = 1

        return edge_marks

    def _start_event(self, position: tuple[int, int]):
        return SolverEvent(type = EventType.START, position = position)

    def _move_event(self, current: tuple[int, int], neighbor: tuple[int, int]):
        return SolverEvent(type = EventType.MOVE, position = neighbor, from_position = current, to_position = neighbor)

    def _solved_event(self, position: tuple[int, int]):
        return SolverEvent(type = EventType.SOLVED, position = position)