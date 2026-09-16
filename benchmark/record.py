from dataclasses import dataclass

from .metrics import SolveMetrics

@dataclass(frozen = True)
class BenchmarkRecord:
    generator: str
    solver: str
    rows: int
    cols: int
    seed: int | None
    metrics: SolveMetrics