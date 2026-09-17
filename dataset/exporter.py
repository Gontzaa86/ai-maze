import csv, json
from pathlib import Path

from dataset.record import DatasetRecord

class DatasetCSVExporter:
    HEADERS = [
        "generator",
        "solver",
        "rows",
        "cols",
        "seed",
        "start",
        "end",
        "maze",
        "solution",
        "solution_length",
        "moves",
        "backtracks",
        "visited_cells",
        "execution_time",
        "success"
    ]

    def export(self, records: list[DatasetRecord], filepath: str | Path) -> None:
        filepath = Path(filepath)

        with filepath.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.HEADERS)
            writer.writeheader()

            for record in records:
                writer.writerow(
                    {
                        "generator": record.generator,
                        "solver": record.solver,
                        "rows": record.rows,
                        "cols": record.cols,
                        "seed": record.seed,
                        "start": json.dumps(record.start),
                        "end": json.dumps(record.end),
                        "maze": json.dumps(record.maze),
                        "solution": json.dumps(record.solution),
                        "solution_length": record.solution_length,
                        "moves": record.moves,
                        "backtracks": record.backtracks,
                        "visited_cells": record.visited_cells,
                        "execution_time": record.execution_time,
                        "success": record.success
                    }
                )

class DatasetJSONExporter:
    def export(self, records: list[DatasetRecord], filepath: str | Path) -> None:
        filepath = Path(filepath)

        data = [
            {
                "generator": record.generator,
                "solver": record.solver,
                "rows": record.rows,
                "cols": record.cols,
                "seed": record.seed,
                "start": list(record.start),
                "end": list(record.end),
                "maze": record.maze,
                "solution": [list(position) for position in record.solution],
                "solution_length": record.solution_length,
                "moves": record.moves,
                "backtracks": record.backtracks,
                "visited_cells": record.visited_cells,
                "execution_time": record.execution_time,
                "success": record.success
            }
            for record in records
        ]

        with filepath.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)