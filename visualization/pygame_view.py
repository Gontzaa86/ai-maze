import pygame # type: ignore

from maze.maze import Maze
from solvers.events import EventType, SolveResult

class PygameMazeView:
    def __init__(self, maze: Maze, result:SolveResult, cell_size: int = 40, event_delay: int = 120):
        self.maze = maze
        self.result = result

        self.cell_size = cell_size
        self.event_delay = event_delay

        self.width = maze.cols * cell_size
        self.height = maze.rows * cell_size

        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("AI-Maze")

        self.clock = pygame.time.Clock()

        # Estado de la animación
        self.current_position = None

        # Marcas que vamos descubriendo a lo largo de la animación
        self.edge_marks = {}

        self.event_index = 0
        self.last_event_time = pygame.time.get_ticks()

        self.finished = False

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self._process_next_event()

            self.draw()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    def _process_next_event(self):
        if self.finished:
            return

        now = pygame.time.get_ticks()

        if now - self.last_event_time < self.event_delay:
            return

        if self.event_index >= len(self.result.events):
            self.finished = True
            return

        event = self.result.events[self.event_index]

        self._apply_event(event)

        self.event_index += 1
        self.last_event_time = now

    def _apply_event(self, event):
        self.current_position = event.position

        if event.from_position is not None:
            edge = frozenset(
                (event.from_position, event.to_position)
            )

            self.edge_marks[edge] = event.mark

        if event.type == EventType.SOLVED:
            self.finished = True

    def draw(self):
        self.screen.fill((30, 30, 30))

        self._draw_edges()
        self._draw_walls()
        self._draw_start()
        self._draw_end()
        self._draw_agent()

    def _draw_walls(self):
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                cell = self.maze.get_cell(row, col)

                x = col * self.cell_size
                y = row * self.cell_size

                self._draw_cell_walls(cell, x, y)

    def _draw_cell_walls(self, cell, x: int, y: int):
        wall_width = 2
        wall_color = (255, 255, 255)

        if cell.walls["up"]:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x, y),
                (x + self.cell_size, y),
                wall_width
            )

        if cell.walls["right"]:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x + self.cell_size, y),
                (x + self.cell_size, y + self.cell_size),
                wall_width
            )

        if cell.walls["down"]:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x, y + self.cell_size),
                (x + self.cell_size, y + self.cell_size),
                wall_width
            )

        if cell.walls["left"]:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x, y),
                (x, y + self.cell_size),
                wall_width
            )

    def _draw_edges(self):
        for edge, mark in self.edge_marks.items():
            position = list(edge)

            if len(position) != 2:
                continue

            first = position[0]
            second = position[1]

            start = self._cell_center(first)
            end = self._cell_center(second)

            if mark == 1:
                width = 4
                line_color = (80, 160, 255)
            else:
                width = 6
                line_color = (255, 80, 80)

            pygame.draw.line(
                self.screen,
                line_color,
                start,
                end,
                width
            )

    def _draw_agent(self):
        if self.current_position is None:
            return

        center = self._cell_center(self.current_position)

        radius = max(5, self.cell_size // 4)

        pygame.draw.circle(
            self.screen,
            (255, 220, 80),
            center,
            radius
        )

    def _draw_start(self):
        center = self._cell_center((0, 0))

        pygame.draw.circle(
            self.screen,
            (80, 220, 120),
            center,
            max(4, self.cell_size // 8)
        )

    def _draw_end(self):
        end = (
            self.maze.rows - 1,
            self.maze.cols -1
        )

        center = self._cell_center(end)

        pygame.draw.circle(
            self.screen,
            (220, 80, 80),
            center,
            max(4, self.cell_size // 8)
        )

    def _cell_center(self, position: tuple[int, int]) -> tuple[int, int]:
        row, col = position

        return(
            col * self.cell_size + self.cell_size // 2,
            row * self.cell_size + self.cell_size // 2,
        )