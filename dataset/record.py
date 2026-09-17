from dataclasses import dataclass

from maze.maze import Maze

def encode_cell(cell) -> int:
    """
    Codifica las paredes de una celda usando el orden (U/R/D/L).
    Es decir, (Up, Right, Down, Left) - 1: Hay pared; 0: No hay pared.
    La matriz "laberinto" almacenará la suma de los valores decimales de las combinaciones binarias correspondientes.

    Bits:
        U = 8
        R = 4
        D = 2
        L = 1
    Ejemplos:
        1001 = 9
        1100 = 12
        0101 = 5
    """

    value = 0

    # El operador |= es un OR inclusivo a nivel de bits.
    if cell.walls["up"]:
        value |= 8
    if cell.walls["right"]:
        value |= 4
    if cell.walls["down"]:
        value |= 2
    if cell.walls["left"]:
        value |= 1

    return value

def encode_maze(maze: Maze) -> list[list[int]]:
    """
    Convierte un Maze en una matriz determinista de enteros.
    Cada entero representa las paredes (U/R/L/D) de una celda.
    """

    return [
        [
            encode_cell(maze.get_cell(row, col))
            for col in range(maze.cols)
        ]
        for row in range(maze.rows)
    ]

@dataclass(frozen = True)
class DatasetRecord:
    generator: str
    solver: str

    rows: int
    cols: int

    seed: int | None

    start: tuple[int, int]
    end: tuple[int, int]

    maze: list[list[int]]

    solution: list[tuple[int, int]]

    solution_length: int
    moves: int
    backtracks: int
    visited_cells: int

    execution_time: float
    success: bool