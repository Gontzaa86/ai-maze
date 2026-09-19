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
        Codifica directamente un objeto Maze.
        """
        self._validate_position(maze.rows, maze.cols, start, "start")
        self._validate_position(maze.rows, maze.cols, end, "end")
        self._validate_position(maze.rows, maze.cols, current, "current")

        cells = [
            [
                self._encode_cell(maze.get_cell(row, col))
                for col in range(maze.cols)
            ]
            for row in range(maze.rows)
        ]

        return self.encode_cells(
            cells=cells,
            start=start,
            end=end,
            current=current
        )

    def encode_cells(
            self, 
            cells: list[list[int]], 
            start: tuple[int, int], 
            end: tuple[int, int], 
            current: tuple[int, int]
        ) -> np.ndarray:
        """
        Codifica directamente una matriz compacta de celdas.
        Cada celda debe estar codificada con el formato U/R/D/L:
            U = 8
            R = 4
            D = 2
            L = 1
        """

        rows = len(cells)

        if rows == 0:
            raise ValueError("La matriz del laberinto no puede estar vacía.")

        cols = len(cells[0])

        if cols == 0:
            raise ValueError("La matriz del laberinto no puede estar vacía.")

        if any(len(row) != cols for row in cells):
            raise ValueError("Todas las filas del laberinto deben tener el mismo tamaño.")

        for row in cells:
            for value in row:
                if not isinstance(value, int) or not 0 <= value <= 15:
                    raise ValueError("Cada celda debe ser un entero entre 0 y 15.")

        self._validate_position(rows, cols, start, "start")
        self._validate_position(rows, cols, end, "end")
        self._validate_position(rows, cols, current, "current")

        representation = np.zeros((self.CHANNELS, rows, cols), dtype=np.float32)

        for row in range(rows):
            for col in range(cols):
                value = cells[row][col]

                representation[self.WALL_UP, row, col] = float(bool(value & 8))
                representation[self.WALL_RIGHT, row, col] = float(bool(value & 4))
                representation[self.WALL_DOWN, row, col] = float(bool(value & 2))
                representation[self.WALL_LEFT, row, col] = float(bool(value & 1))

        start_row, start_col = start
        representation[self.START, start_row, start_col] = 1.0

        end_row, end_col = end
        representation[self.GOAL, end_row, end_col] = 1.0

        current_row, current_col = current
        representation[self.CURRENT, current_row, current_col] = 1.0

        return representation

    def _encode_cell(self, cell) -> int:
        value = 0

        if cell.walls["up"]:
            value |= 8

        if cell.walls["right"]:
            value |= 4

        if cell.walls["down"]:
            value |= 2

        if cell.walls["left"]:
            value |= 1

        return value

    def _validate_position(self, rows: int, cols: int, position: tuple[int, int], name: str) -> None:
        row, col = position

        if not (0 <= row < rows and 0 <= col < cols):
            raise ValueError(f"La posición '{name}' está fiera del laberinto: {position}")