import csv
from pathlib import Path

from .record import BenchmarkRecord

class BenchmarkCSVExporter:
    def export(self, records: list[BenchmarkRecord], filepath: str | Path) -> None:
        filepath = Path(filepath)

        with filepath.open(
            "w",
            newline = "",
            encoding = "utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "generator",
                "solver",
                "rows",
                "cols",
                "seed",
                "solution_length",
                "moves",
                "backtracks",
                "success",
                "visited_cells",
                "execution_time"
            ])

            for record in records:
                metrics = record.metrics

                writer.writerow([
                    record.generator,
                    record.solver,
                    record.rows,
                    record.cols,
                    record.seed,
                    metrics.solution_length,
                    metrics.moves,
                    metrics.backtracks,
                    metrics.success,
                    metrics.visited_cells,
                    metrics.execution_time
                ])