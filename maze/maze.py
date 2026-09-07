from .cell import Cell

class Maze:
    def __init__(self, rows: int, cols: int):
        if rows <= 0 or cols <= 0:
            raise ValueError("Las dimensiones deben ser mayores que 0.")

        self.rows = rows
        self.cols = cols

        self.grid = [
            [Cell(row, col) for col in range(cols)]
            for row in range(rows)
        ]

    def get_cell(self, row: int, col: int) -> Cell:
        return self.grid[row][col]

    def is_inside(self, row: int, col: int) -> bool:
        return (
            0 <= row < self.rows
            and 0 <= col < self.cols
        )

    # Para el generador
    def remove_wall(self, current: Cell, neighbor: Cell):
        row_diff = neighbor.row - current.row
        col_diff = neighbor.col - current.col

        if row_diff == -1:
            current.walls["up"] = False
            neighbor.walls["down"] = False

        elif row_diff == 1:
            current.walls["down"] = False
            neighbor.walls["up"] = False

        elif col_diff == -1:
            current.walls["left"] = False
            neighbor.walls["right"] = False

        elif col_diff == 1:
            current.walls["right"] = False
            neighbor.walls["left"] = False

        else:
            raise ValueError("Las celdas no son adyacentes.")

    # ======= TEMPORAL =======
    def __str__(self):
        result = ""

        # Borde Superior
        result += "┌"
        result += "───┬" * (self.cols - 1)
        result += "───┐\n"

        for row in range(self.rows):
            # Contenido y paredes verticales
            result += "│"

            for col in range(self.cols):
                cell = self.get_cell(row, col)

                if row == 0 and col == 0:
                    result += " S "
                else:
                    result += "   "

                if cell.walls["left"]:
                    result += "│"
                else:
                    result += " "

            result += "\n"

            # Paredes Horizontales
            if row < self.rows - 1:

                result += "├"

                for col in range(self.cols):

                    cell = self.get_cell(row, col)

                    if cell.walls["down"]:
                        result += "───"
                    else:
                        result += "   "

                    if col < self.cols - 1:
                        result += "┼"

                result += "┤\n"

        # Borde inferior
        result += "└"
        result += "───┴" * (self.cols - 1)
        result += "───┘"

        return result