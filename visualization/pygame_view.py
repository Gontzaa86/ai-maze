import pygame

from maze.maze import Maze

class PygameMazeView:
    def __init__(self, maze: Maze, cell_size: int = 40):
        self.maze = maze
        self.cell_size = cell_size

        self.width = maze.cols * cell_size
        self.height = maze.rows * cell_size

        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("AI-Maze")

        self.clock = pygame.time.Clock()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    def draw(self):
        self.screen.fill((30, 30, 30))

        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                cell = self.maze.get_cell(row, col)

                x = col * self.cell_size
                y = row * self.cell_size

                self._draw_cell(cell, x, y)

    def _draw_cell(self, cell, x: int, y: int):
        wall_width = 2

        if cell.walls["up"]:
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (x, y),
                (x + self.cell_size, y),
                wall_width
            )

        if cell.walls["right"]:
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (x + self.cell_size, y),
                (x + self.cell_size, y + self.cell_size),
                wall_width
            )

        if cell.walls["down"]:
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (x, y + self.cell_size),
                (x + self.cell_size, y + self.cell_size),
                wall_width
            )

        if cell.walls["left"]:
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (x, y),
                (x, y + self.cell_size),
                wall_width
            )