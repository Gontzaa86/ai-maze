from dataset.record import DatasetRecord

from ai.dataset.sample import Action, TrainingSample
from ai.representations.global_map import GlobalMapRepresentation

class TrainingSampleBuilder:
    """
    Convierte registros del dataset existente en muestras del ML.
    Cada transición de la solución genera una muestra:
        Estado actual -> Acción siguiente.
    """

    def __init__(self):
        self.representation = GlobalMapRepresentation()

    def build(self, record: DatasetRecord) -> list[TrainingSample]:
        if not record.success:
            return []

        samples = []

        for current, next_position in zip(record.solution, record.solution[1:]):
            state = self.representation.encode_cells(
                cells=record.maze,
                start=record.start,
                end=record.end,
                current=current
            )

            action = self._get_action(current, next_position)

            samples.append(TrainingSample(state=state, action=action))

        return samples

    def _get_action(self, current: tuple[int, int], nex_position: tuple[int, int]) -> int:
        current_row, current_col = current
        next_row, next_col = nex_position

        row_delta = next_row - current_row
        col_delta = next_col - current_col

        if row_delta == -1 and col_delta == 0:
            return Action.UP
        if row_delta == 0 and col_delta == 1:
            return Action.RIGHT
        if row_delta == 1 and col_delta == 0:
            return Action.DOWN
        if row_delta == 0 and col_delta == -1:
            return Action.LEFT

        raise ValueError(f"Movimiento inválido: {current} --> {nex_position}")