import numpy as np # type: ignore

from maze.maze import Maze

class GlobalMapRepresentation:
    """
    Representación global de un laberinto para aprendizaje automático.
    La representación utiliza siete canales con forma: (7, rows, cols)

    Canales:
        0 -> pared arriba
        1 -> pared derecha
        2 -> pared abajo
        3 -> pared izquierda
        4 -> posición START
        5 -> posición GOAL
        6 -> posición CURRENT

    Los canales de paredes utilizan:
        1.0 --> pared presente
        0.0 --> paso abierto

    Los canales START, GOAL y CURRENT utilizan:
        1.0 --> posición
        0.0 --> resto de celdas
    """

    CHANNELS = 7

    WALL_UP = 0
    WALL_RIGHT = 1
    WALL_DOWN = 2
    WALL_LEFT = 3
    START = 4
    GOAL = 5
    CURRENT = 6

    def encode(self, maze: Maze, start: tuple[int, int], end: tuple[int, int], current: tuple[int, int]) -> np.ndarray:
        """
        Convierte el estado actual del laberinto en una representación global preparada para ML.
        """
        self._validate_position(maze, start, "start")
        self._validate_position(maze, end, "end")
        self._validate_position(maze, current, "current")

        representation = np.zeros(
            (self.CHANNELS, maze.rows, maze.cols),
            dtype = np.float32
        )

        for row in range(maze.rows):
            for col in range(maze.cols):
                cell = maze.get_cell(row, col)

                representation[
                    self.WALL_UP,
                    row, col
                ] = float(cell.walls["up"])

                representation[
                    self.WALL_RIGHT,
                    row, col,
                ] = float(cell.walls["right"])

                representation[
                    self.WALL_DOWN,
                    row, col,
                ] = float(cell.walls["down"])

                representation[
                    self.WALL_LEFT,
                    row, col,
                ] = float(cell.walls["left"])

        start_row, start_col = start
        representation[
            self.START,
            start_row, start_col
        ] = 1.0

        end_row, end_col = end
        representation[
            self.GOAL,
            end_row, end_col
        ] = 1.0

        current_row, current_col = current
        representation[
            self.CURRENT,
            current_row, current_col
        ] = 1.0

        return representation

    def _validate_position(self, maze: Maze, position: tuple[int, int], name: str) -> None:
        row, col = position

        if not maze.is_inside(row, col):
            raise ValueError(f"La posición '{name}' está fiera del laberinto: {position}")