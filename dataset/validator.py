from dataset.record import DatasetRecord

class DatasetValidationError(ValueError):
    """Error de validación de un registro del dataset."""

DIRECTION_DELTAS = {
    8: (-1, 0),     # Up
    4: (0, 1),      # Right
    2: (1, 0),      # Down
    1: (0, -1)      # Left
}

def validate_record(record: DatasetRecord) -> None:
    if record.rows <= 0 or record.cols <= 0:
        raise DatasetValidationError("Las dimensiones del laberinto deben ser mayores que 0.")

    if len(record.maze) != record.rows:
        raise DatasetValidationError("El número de filas del maze no coincide con las rows.")

    if any(len(row) != record.cols for row in record.maze):
        raise DatasetValidationError("El número de columnas del maze no coincide con cols.")

    for row in record.maze:
        for value in row:
            if not isinstance(value, int) or not 0 <= value <= 15:
                raise DatasetValidationError("Cada celda del maze debe ser un entero entre 0 y 15.")

    if not _is_inside(record.start, record.rows, record.cols):
        raise DatasetValidationError("La posición start está fuera del laberinto.")
    if not _is_inside(record.end, record.rows, record.cols):
            raise DatasetValidationError("La posición end está fuera del laberinto.")

    if record.solution:
        if record.solution[0] != record.start:
            raise DatasetValidationError("La solución no comienza en start.")
        if record.solution[-1] != record.end:
            raise DatasetValidationError("La solcuión no termina en end.")

        for position in record.solution:
            if not _is_inside(position, record.rows, record.cols):
                raise DatasetValidationError("La solución contiene una posición fuera del laberinto.")

        _validate_solution_path(record)

    if record.solution_length != len(record.solution):
        raise DatasetValidationError("'solution_length' no coincide con la solución.")

    if record.moves < 0:
        raise DatasetValidationError("'moves' no puede ser negativo.")
    if record.backtracks < 0:
        raise DatasetValidationError("'backtracks' no puede ser negativo.")
    if record.visited_cells < 0:
        raise DatasetValidationError("'visited_cells' no puede ser negativo.")
    if record.execution_time < 0:
        raise DatasetValidationError("'execution_time' no puede ser negativo.")

def validate_records(records: list[DatasetRecord]) -> None:
    for record in records:
        validate_record(record)

def _is_inside(position: tuple[int, int], rows: int, cols: int) -> bool:
    row, col = position

    return (
        0 <= row < rows
        and 0 <= col < cols
    )

def _validate_solution_path(record: DatasetRecord) -> None:
    for current, next_position in zip(record.solution, record.solution[1:]):
        row, col = current
        next_row, next_col = next_position

        row_delta = next_row - row
        col_delta = next_col - col

        direction = _get_direction(row_delta, col_delta)

        if direction is None:
            raise DatasetValidationError("La solución contiene un movimiento no adyacente.")

        current_cell = record.maze[row][col]
        next_cell = record.maze[next_row][next_col]

        opposite_direction = _get_opposite_direction(direction)

        # En el encoding: 1 = pared; 0 = paso abierto.
        if current_cell & direction:
            raise DatasetValidationError("La solución atraviesa una pared cerrada.")

        if next_cell & opposite_direction:
            raise DatasetValidationError("Las paredes entre dos celdas no son consistentes.")

def _get_direction(row_delta: int, col_delta: int) -> int | None:
    for direction, delta in DIRECTION_DELTAS.items():
        if delta == (row_delta, col_delta):
            return direction

    return None

def _get_opposite_direction(direction: int) -> int:
    return {
        8: 2,  # U <-> D
        4: 1,  # R <-> L
        2: 8,
        1: 4,
    }[direction]