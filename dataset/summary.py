from dataclasses import dataclass

from dataset.record import DatasetRecord

@dataclass(frozen = True)
class DatasetSummary:
    total_records: int
    successful_records: int
    failed_records: int

    generators: tuple[str, ...]
    solvers: tuple[str, ...]

    sizes: tuple[tuple[int, int], ...]
    unique_seeds: int

    average_solution_length: float
    average_moves: float
    average_visited_cells: float

def summarize_dataset(records: list[DatasetRecord]) -> DatasetSummary:
    if not records: return DatasetSummary(
            total_records=0,
            successful_records=0,
            failed_records=0,
            generators=(),
            solvers=(),
            sizes=(),
            unique_seeds=0,
            average_solution_length=0.0,
            average_moves=0.0,
            average_visited_cells=0.0
    )

    successful_records = sum(1 for record in records if record.success)
    generators = tuple(sorted({record.generator for record in records}))
    solvers = tuple(sorted({record.solver for record in records}))
    sizes = tuple(sorted({(record.rows, record. cols) for record in records}))
    unique_seeds = len({record.seed for record in records})
    total = len(records)

    return DatasetSummary(
        total_records=total,
        successful_records=successful_records,
        failed_records=total - successful_records,
        generators=generators,
        solvers=solvers,
        sizes=sizes,
        unique_seeds=unique_seeds,
        average_solution_length=(sum(record.solution_length for record in records) / total),
        average_moves=(sum(record.moves for record in records) / total),
        average_visited_cells=(sum(record.visited_cells for record in records) / total)
    )