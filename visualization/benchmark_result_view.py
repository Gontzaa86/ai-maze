import pygame # type: ignore

from benchmark.run_benchmark import BenchmarkRun

class BenchmarkResultView:
    def __init__(self, benchmark_run: BenchmarkRun, filepath: str):
        self.benchmark_run = benchmark_run
        self.filepath = filepath

        self.width = 600
        self.height = 640

        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("AI-Maze - Benchmark Result")

        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.Font(None, 48)
        self.label_font = pygame.font.Font(None, 30)
        self.value_font = pygame.font.Font(None, 30)
        self.info_font = pygame.font.Font(None, 22)
        self.button_font = pygame.font.Font(None, 28)
        self.button_rect = pygame.Rect(170, 520, 260, 60)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key in (
                        pygame.K_ESCAPE,
                        pygame.K_RETURN,
                    ):
                        return "back"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        return "back"

            self._draw()

            pygame.display.flip()

            self.clock.tick(60)

        return "back"

    def _draw(self):
        self.screen.fill((30, 30, 30))

        self._draw_title()
        self._draw_metrics()
        self._draw_csv()
        self._draw_button()
        self._draw_info()

    def _draw_title(self):
        text = self.title_font.render("BENCHMARK COMPLETADO", True, (255, 255, 255))

        rect = text.get_rect(center=(self.width // 2, 70))

        self.screen.blit(text, rect)

    def _draw_metrics(self):
        summary = self.benchmark_run.summary

        metrics = [
            ("Ejecuciones:", str(summary.total_runs)),
            ("Exitosos:", str(summary.successful_runs)),
            ("Longitud media:", f"{summary.average_solution_length:.2f}"),
            ("Movimientos medios:", f"{summary.average_moves:.2f}"),
            ("Tiempo total:", f"{summary.total_execution_time:.6f} s"),
        ]

        y = 150

        for label, value in metrics:
            label_text = self.label_font.render(label, True, (220, 220, 220))

            value_text = self.value_font.render(value, True, (255, 255, 255))

            self.screen.blit(label_text, (70, y))

            value_rect = value_text.get_rect(midright=(self.width - 70, y + 15))

            self.screen.blit(value_text, value_rect)

            y += 55

    def _draw_csv(self):
        text = self.info_font.render(f"CSV: {self.filepath}", True, (180, 180, 180))

        rect = text.get_rect(center=(self.width // 2, 445))

        self.screen.blit(text, rect)

    def _draw_button(self):
        pygame.draw.rect(self.screen, (70, 70, 70), self.button_rect)

        pygame.draw.rect(self.screen, (180, 180, 180), self.button_rect, 2)

        text = self.button_font.render("VOLVER", True, (255, 255, 255))

        rect = text.get_rect(center=self.button_rect.center)

        self.screen.blit(text, rect)

    def _draw_info(self):
        text = self.info_font.render("ENTER o ESC para volver", True, (180, 180, 180))

        rect = text.get_rect(center=(self.width // 2, 610))

        self.screen.blit(text, rect)