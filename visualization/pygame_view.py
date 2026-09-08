import pygame # type: ignore

from maze.maze import Maze
from solvers.events import EventType, SolveResult

class PygameMazeView:
    MIN_DELAY = 50
    MAX_DELAY = 1000
    DELAY_STEP = 50

    PANEL_WIDTH = 240 # Panel lateral de estadísticas.
    MIN_WINDOW_HEIGHT = 600

    def __init__(self, maze: Maze, result:SolveResult, cell_size: int = 40, event_delay: int = 200):
        self.maze = maze
        self.result = result

        self.cell_size = cell_size
        self.event_delay = event_delay

        self.maze_width = maze.cols * cell_size
        self.maze_height = maze.rows * cell_size

        self.width = (self.maze_width + self.PANEL_WIDTH)
        self.height = max(self.maze_height, self.MIN_WINDOW_HEIGHT)

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("AI-Maze")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 26)
        self.small_font = pygame.font.Font(None, 21)
        self.title_font = pygame.font.Font(None, 32)

        # Estado de la animación
        self.current_position = None

        # Marcas que vamos descubriendo a lo largo de la animación
        self.edge_marks = {}

        self.event_index = 0
        self.last_event_time = pygame.time.get_ticks()

        self.finished = False
        self.paused = False

        self.moves = 0
        self.backtracks = 0

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused

                        self.last_event_time = pygame.time.get_ticks()

                    elif (
                        event.key == pygame.K_MINUS
                        or event.unicode == "-"
                    ):
                        self._decrease_speed()
                    elif (
                        event.key == pygame.K_PLUS
                        or event.unicode == "+"
                    ):
                        self._increase_speed()

            self._process_next_event()

            self.draw()

            pygame.display.flip()

            self.clock.tick(60)

        return "quit"

    def _process_next_event(self):
        if self.finished:
            return

        if self.paused:
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

    def _decrease_speed(self):
        self.event_delay = min(
            self.MAX_DELAY,
            self.event_delay + self.DELAY_STEP
        )

    def _increase_speed(self):
        self.event_delay = max(
            self.MIN_DELAY,
            self.event_delay - self.DELAY_STEP
        )

    def draw(self):
        self.screen.fill((30, 30, 30))

        self._draw_maze()
        self._draw_panel()

    def _draw_maze(self):
        self._draw_edges()
        self._draw_walls()
        self._draw_start()
        self._draw_end()
        self._draw_agent()

    def _draw_panel(self):
        panel_x = self.maze_width

        pygame.draw.rect(
            self.screen,
            (45, 45, 45),
            (panel_x, 0, self.PANEL_WIDTH, self.height)
        )

        pygame.draw.line(
            self.screen,
            (100, 100, 100),
            (panel_x, 0),
            (panel_x, self.height),
            2
        )

        self._draw_panel_title(panel_x)
        self._draw_statistics(panel_x)
        self._draw_controls(panel_x)

    def _draw_panel_title(self, panel_x: int):
        text = self.title_font.render(
            "ESTADÍSTICAS",
            True, (255, 255, 255)
        )

        rect = text.get_rect(
            center = (panel_x + self.PANEL_WIDTH // 2, 35)
        )

        self.screen.blit(text, rect)

    def _draw_statistics(self, panel_x: int):
        x = panel_x + 20
        y = 80

        status = self._get_status()

        self._draw_stat("Estado:", status, x, y)

        y += 38

        self._draw_stat("Velocidad:",
                        f"{self.event_delay} ms",
                        x, y)

        y += 38

        self._draw_stat("Evento:",
                       (
                           f"{self.event_index} /"
                           f"{len(self.result.events)}"
                       ), x, y)

        y += 38

        self._draw_stat("Pasos:", str(self.moves), x, y)

        y += 38

        self._draw_stat("Retrocesos:", str(self.backtracks), x, y)

        y += 38

        mark_1 = sum(1 for mark in self.edge_marks.values() if mark == 1)
        self._draw_stat("Marca 1:", str(mark_1), x, y)

        y += 38

        mark_2 = sum(1 for mark in self.edge_marks.values() if mark == 2)
        self._draw_stat("Marca 2:", str(mark_2), x, y)

        y += 38

        position = self.current_position
        if position is None:
            position_text = "-"
        else:
            position_text = str(position)

        self._draw_stat("Posición:", position_text, x, y)

    def _draw_stat(self, label: str, value: str, x: int, y: int):
        label_text = self.small_font.render(label, True, (190, 190, 190))

        value_text = self.small_font.render(value, True, (255, 255, 255))

        self.screen.blit(label_text, (x, y))

        value_rect = value_text.get_rect(right=self.width - 15, top=y)

        self.screen.blit(value_text, value_rect)

    def _draw_controls(self, panel_x: int):
        y = self.height - 125

        pygame.draw.line(
            self.screen,
            (100, 100, 100),
            (panel_x + 15, y - 15),
            (self.width - 15, y - 15),
            1
        )

        controls = [
            "SPACE  Pausar / Continuar",
            "-      Reducir Velocidad",
            "+      Aumentar Velocidad",
            "ESC    Volver al Menú"
        ]

        for control in controls:
            text = self.small_font.render(control, True, (190, 190, 190))

            self.screen.blit(text, (panel_x + 15, y))

            y += 25

    def _get_status(self) -> str:
        if self.finished: return "SOLVED"
        if self.paused: return "PAUSED"

        return "RUNNING"

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