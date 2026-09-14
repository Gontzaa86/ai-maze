import pygame # type: ignore

from solvers.registry import get_solvers
from generators.registry import get_generators

class MazeMenu:
    MIN_SIZE = 2
    MAX_SIZE = 50

    def __init__(self):
        self.width = 600
        self.height = 640

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("AI-Maze")

        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.Font(None, 52)
        self.label_font = pygame.font.Font(None, 32)
        self.input_font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 32)
        self.info_font = pygame.font.Font(None, 24)

        self.rows = "10"
        self.cols = "10"
        self.seed = "" # Para la generación aleatoria (o no) de laberintos

        self.active_field = "rows"

        # .Rect --> pygame object for storing rectangular coordinates (left, top, width, height)
        self.rows_rect = pygame.Rect(280, 150, 180, 45)
        self.cols_rect = pygame.Rect(280, 220, 180, 45)
        self.seed_rect = pygame.Rect(280, 290, 180, 45)

        self.error_message = ""

        self.solvers = get_solvers()
        self.selected_solver = 0

        if not self.solvers:
            raise RuntimeError("No hay solvers disponibles.")

        self.solver_rect = pygame.Rect(280, 360, 180, 45)

        self.generators = get_generators()
        self.selected_generator = 0

        if not self.generators:
            raise RuntimeError("No hay generadores disponibles.")

        self.generator_rect = pygame.Rect(280, 430, 180, 45)

        self.button_rect = pygame.Rect(190, 500, 220, 60)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key == pygame.K_RETURN:
                        return self._create_dimensions()
                    if event.key == pygame.K_BACKSPACE:
                        self._handle_backspace()
                    elif event.unicode.isdigit():
                        self._handle_digit(event.unicode)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rows_rect.collidepoint(event.pos):
                        self.active_field = "rows"
                        self.error_message = ""
                    elif self.cols_rect.collidepoint(event.pos):
                        self.active_field = "cols"
                        self.error_message = ""
                    elif self.seed_rect.collidepoint(event.pos):
                        self.active_field = "seed"
                        self.error_message = ""

                    elif self.button_rect.collidepoint(event.pos):
                        dimensions = self._create_dimensions()

                        if dimensions is not None:
                            return dimensions
                        
                    elif self.solver_rect.collidepoint(event.pos):
                        self._next_solver()
                    elif self.generator_rect.collidepoint(event.pos):
                        self._next_generator()

            self._draw()

            pygame.display.flip()

            self.clock.tick(60)

        return None

    def _handle_digit(self, digit: str):
        if self.active_field == "rows":
            if len(self.rows) < 2:
                self.rows += digit

        elif self.active_field == "cols":
            if len(self.cols) < 2:
                self.cols += digit

        elif self.active_field == "seed":
            self.seed += digit

        self.error_message = ""

    def _handle_backspace(self):
        if self.active_field == "rows":
            self.rows = self.rows[:-1]

        elif self.active_field == "cols":
            self.cols = self.cols[:-1]

        elif self.active_field == "seed":
            self.seed = self.seed[:-1]

        self.error_message = ""

    def _create_dimensions(self):
        if not self.rows or not self.cols:
            self.error_message = ("Introduce filas y columnas.")
            return None

        rows = int(self.rows)
        cols = int(self.cols)

        if not (self.MIN_SIZE <= rows <= self.MAX_SIZE):
            self.error_message = (
                f"Las filas deben estar entre "
                f"{self.MIN_SIZE} y {self.MAX_SIZE}"
            )
            return None

        if not (self.MIN_SIZE <= cols <= self.MAX_SIZE):
            self.error_message = (
                f"Las columnas deben estar entre "
                f"{self.MIN_SIZE} y {self.MAX_SIZE}"
            )
            return None

        seed = None
        
        if self.seed.strip():
            seed = int(self.seed)

        return rows, cols, self._get_selected_generator(), self._get_selected_solver(), seed

    def _draw(self):
        self.screen.fill((30, 30, 30))

        self._draw_title()
        self._draw_label("Filas:", 120, 160)
        self._draw_label("Columnas:", 80, 230)
        self._draw_label("Seed:", 120, 300)
        self._draw_input(self.rows_rect, self.rows, self.active_field == "rows")
        self._draw_input(self.cols_rect, self.cols, self.active_field == "cols")
        self._draw_input(self.seed_rect, self.seed, self.active_field == "seed")
        self._draw_button()
        self._draw_label("Generador:", 70, 370)
        self._draw_generator_selector()
        self._draw_label("Algoritmo:", 70, 440)
        self._draw_solver_selector()

        if self.error_message:
            self._draw_error()

        self._draw_info()

    def _draw_title(self):
        text = self.title_font.render("AI-Maze", True, (255, 255, 255))

        rect = text.get_rect(center = (self.width // 2, 70))

        self.screen.blit(text, rect)

    def _draw_label(self, text: str, x: int, y: int):
        rendered = self.label_font.render(text, True, (255, 255, 255))

        self.screen.blit(rendered, (x, y))

    def _draw_input(self, rect, value: str, active: bool):
        border_color = ((100, 180, 255) if active else (180, 180, 180))

        pygame.draw.rect(self.screen, (50, 50, 50), rect)
        pygame.draw.rect(self.screen, border_color, rect, 2)

        text = self.input_font.render(value, True, (255, 255, 255))

        text_rect = text.get_rect(center = rect.center)

        self.screen.blit(text, text_rect)

    def _draw_button(self):
        pygame.draw.rect(self.screen, (70, 70, 70), self.button_rect)
        pygame.draw.rect(self.screen, (180, 180, 180), self.button_rect, 2)

        text = self.button_font.render("GENERAR", True, (255, 255, 255))

        text_rect = text.get_rect(center = self.button_rect.center)

        self.screen.blit(text, text_rect)

    def _draw_error(self):
        text = self.info_font.render(self.error_message, True, (255, 120, 120))

        rect = text.get_rect(center=(self.width // 2, 550))

        self.screen.blit(text, rect)

    def _draw_info(self):
        text = self.info_font.render(
            "ENTER para generar. ESC para salir",
            True, (180, 180, 180)
        )

        rect = text.get_rect(center = (self.width // 2 , 590))

        self.screen.blit(text, rect)

    def _draw_solver_selector(self):
        pygame.draw.rect(self.screen, (50, 50, 50), self.solver_rect)

        pygame.draw.rect(self.screen, (180, 180, 180), self.solver_rect, 2)

        solver_name = self._get_selected_solver()

        display_name = self._get_selected_solver_display_name()

        text = self.input_font.render(display_name, True, (255, 255, 255))

        text_rect = text.get_rect(center = self.solver_rect.center)

        self.screen.blit(text, text_rect)

    def _draw_generator_selector(self):
        pygame.draw.rect(self.screen, (50, 50, 50), self.generator_rect)

        pygame.draw.rect(self.screen, (180, 180, 180), self.generator_rect, 2)

        display_name = self._get_selected_generator_display_name()

        text = self.input_font.render(display_name, True, (255, 255, 255))

        text_rect = text.get_rect(center = self.generator_rect.center)

        self.screen.blit(text, text_rect)

    def _next_solver(self):
        self.selected_solver = (
            self.selected_solver + 1
        ) % len(self.solvers)

        self.error_message = ""

    def _get_selected_solver(self) -> str:
        return self.solvers[self.selected_solver].metadata.name

    def _get_selected_solver_display_name(self) -> str:
        return self.solvers[self.selected_solver].metadata.display_name

    def _next_generator(self):
        self.selected_generator = (
            self.selected_generator + 1
        ) % len(self.generators)

        self.error_message = ""

    def _get_selected_generator(self) -> str:
        return self.generators[self.selected_generator].metadata.name

    def _get_selected_generator_display_name(self) -> str:
        return self.generators[self.selected_generator].metadata.display_name