from dataclasses import dataclass
from pathlib import Path

from dataset.builder import generate_dataset
from dataset.exporter import DatasetCSVExporter, DatasetJSONExporter
from dataset.record import DatasetRecord
from dataset.validator import validate_records

@dataclass(frozen = True)
class DatasetRun:
    records: list[DatasetRecord]
    csv_path: Path | None
    json_path: Path | None

def run_dataset(
        generators: list[str],
        solvers: list[str],
        rows: int,
        cols: int,
        start: tuple[int, int],
        end: tuple[int, int],
        seed_count: int,
        seed: int | None = None,
        csv_filepath: str | Path | None = None,
        json_filepath: str | Path | None = None
) -> DatasetRun:
    records = generate_dataset (
        generators=generators,
        solvers=solvers,
        rows=rows,
        cols=cols,
        start=start,
        end=end,
        seed_count=seed_count,
        seed=seed
    )

    validate_records(records)

    csv_path = None
    json_path = None

    if csv_filepath is not None:
        csv_path = Path(csv_filepath)
        DatasetCSVExporter().export(records, csv_path)
    if json_filepath is not None:
        json_path = Path(json_filepath)
        DatasetJSONExporter().export(records, json_path)

    return DatasetRun(records=records, csv_path=csv_path, json_path=json_path)