from dataclasses import dataclass
from pathlib import Path
import argparse
import json

from .builder import generate_dataset
from .exporter import DatasetCSVExporter, DatasetJSONExporter
from .record import DatasetRecord
from .validator import validate_records

from generators.registry import discover_generators
from solvers.registry import discover_solvers

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

def _parse_position(value: str) -> tuple[int, int]:
    try:
        row, col = value.split(",")
        return int(row), int(col)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("La posición debe tener formato fila,columna.") from exc


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Genera un dataset reproducible de AI-Maze.")

    parser.add_argument(
        "--generators",
        default="recursive_backtracking",
        help="Generadores separados por comas.",
    )

    parser.add_argument(
        "--solvers",
        default="bfs",
        help="Solvers separados por comas.",
    )

    parser.add_argument(
        "--rows",
        type=int,
        default=20,
        help="Número de filas.",
    )

    parser.add_argument(
        "--cols",
        type=int,
        default=20,
        help="Número de columnas.",
    )

    parser.add_argument(
        "--start",
        type=_parse_position,
        default=(0, 0),
        help="Posición inicial: fila,columna.",
    )

    parser.add_argument(
        "--end",
        type=_parse_position,
        default=None,
        help="Posición final: fila,columna.",
    )

    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Número de seeds por combinación.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed maestro.",
    )

    parser.add_argument(
        "--output",
        default="dataset/data",
        help="Directorio de salida.",
    )

    return parser

def main() -> None: # Función de ejecución del creador de dataset.
    parser = _build_parser()
    args = parser.parse_args()

    discover_generators()
    discover_solvers()

    if args.rows <= 0 or args.cols <= 0:
        parser.error("Filas y columnas deben ser mayores que cero.")
    if args.count < 0:
        parser.error("Count no puede ser negativo.")

    end = args.end

    if end is None:
        end = (args.rows - 1, args.cols - 1)

    generators = [
        name.strip()
        for name in args.generators.split(",")
        if name.strip()
    ]

    solvers = [
        name.strip()
        for name in args.solvers.split(",")
        if name.strip()
    ]

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "dataset.csv"
    json_path = output_dir / "dataset.json"
    metadata_path = output_dir / "metadata.json"

    print("Generando dataset...")
    print(f"  Generators: {generators}")
    print(f"  Solvers:    {solvers}")
    print(f"  Size:       {args.rows}x{args.cols}")
    print(f"  Start:      {args.start}")
    print(f"  End:        {end}")
    print(f"  Seeds:      {args.count}")
    print(f"  Seed:       {args.seed}")

    result = run_dataset(
        generators=generators,
        solvers=solvers,
        rows=args.rows,
        cols=args.cols,
        start=args.start,
        end=end,
        seed_count=args.count,
        seed=args.seed,
        csv_filepath=csv_path,
        json_filepath=json_path
    )

    metadata = {
        "version": "5.6",
        "seed": args.seed,
        "generators": generators,
        "solvers": solvers,
        "rows": args.rows,
        "cols": args.cols,
        "start": list(args.start),
        "end": list(end),
        "seed_count": args.count,
        "records": len(result.records)
    }

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)

    print()
    print("Dataset generado correctamente.")
    print(f"  Records:  {len(result.records)}")
    print(f"  CSV:      {csv_path}")
    print(f"  JSON:     {json_path}")
    print(f"  Metadata: {metadata_path}")

if __name__ == "__main__":
    main()