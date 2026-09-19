import heapq

from maze.maze import Maze
from .base import Solver
from .events import EventType, SolveResult, SolverEvent
from .registry import register_solver

@register_solver(
    name="astar",
    display_name="A*",
    description="Búsqueda informada que prioriza los caminos más prometedores.",
    category="classic"
)
class AStarSolver(Solver):
    """
    f(n) = g(n) + h(n)

    Donde:
        g(n) → Cuánto me ha costado llegar hasta esta celda.
        h(n) → Cuánto creo que me falta para llegar al objetivo.
        f(n) → Estimación del coste total.
    
    El coste de todos los movimientos es de uno.
    """
    def solve(self, maze: Maze, start: tuple[int, int], end: tuple[int, int]) -> SolveResult:
        open_set = []
        g_score = {start: 0}
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

        counter = 0

        heapq.heappush(open_set, (self._heuristic(start, end), 0, start))

        events = [self._start_event(start)]

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current == end:
                break

            for neighbor in self._get_neighbors(maze, current):
                tentative_g_score = g_score[current] + 1
                current_g_score = g_score.get(neighbor, float("inf"))

                if tentative_g_score >= current_g_score:
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score

                f_score = (tentative_g_score + self._heuristic(neighbor, end))

                counter += 1

                heapq.heappush(open_set, (f_score, counter, neighbor))

                events.append(self._move_event(current, neighbor))

        solution = self._build_solution(came_from, start, end)
        edge_marks = self._build_edge_marks(solution)
        events.append(self._solved_event(end))

        return SolveResult(solution=solution, events=events, edge_marks=edge_marks)

    def _get_neighbors(self, maze, position):
        row, col = position
        neighbors = []

        cell = maze.get_cell(row, col)

        directions = [
            ("up", -1, 0),
            ("right", 0, 1),
            ("down", 1, 0),
            ("left", 0, -1),
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

    def _heuristic(self, current, end): # Calcula la diferencia entre actual y objetivo para determinar "cercanía"
        return abs(current[0] - end[0]) + abs(current[1] - end[1])

    def _build_solution(self, came_from, start, end):
        if end not in came_from:
            return []

        path = []
        current = end

        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path

    def _build_edge_marks(self, solution):
        edge_marks = {}

        for current, neighbor in zip(solution, solution[1:]):
            edge = frozenset((current, neighbor))
            edge_marks[edge] = 1

        return edge_marks

    def _start_event(self, position):
        return SolverEvent(
            type=EventType.START,
            position=position,
        )

    def _move_event(self, current, neighbor):
        return SolverEvent(
            type=EventType.MOVE,
            position=neighbor,
            from_position=current,
            to_position=neighbor,
        )

    def _solved_event(self, position):
        return SolverEvent(
            type=EventType.SOLVED,
            position=position,
        )