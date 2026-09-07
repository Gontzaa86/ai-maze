from dataclasses import dataclass, field

@dataclass
class Cell:
    row: int
    col: int

    # Toda celda comienza con sus cuatro paredes cerradas
    # Antes del algoritmo generador
    walls: dict[str, bool] = field(
        default_factory=lambda: {
            "up": True,
            "down": True,
            "right": True,
            "left": True
        }
    )