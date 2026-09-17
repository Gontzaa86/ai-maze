import json

from dataset.exporter import DatasetCSVExporter, DatasetJSONExporter
from dataset.generator import DatasetGenerator

from generators.registry import discover_generators
from solvers.registry import discover_solvers

discover_generators()
discover_solvers()

def create_records():
    generator = DatasetGenerator()

    return generator.generate_many(
        generator_name="recursive_backtracking",
        solver_name="bfs",
        rows=4,
        cols=4,
        start=(0, 0),
        end=(3, 3),
        seed_count=3,
        seed=123,
    )

def test_csv_exporter_creates_file(tmp_path):
    records = create_records()

    filepath = tmp_path / "dataset.csv"

    exporter = DatasetCSVExporter()
    exporter.export(records, filepath)

    assert filepath.exists()

    content = filepath.read_text(encoding="utf-8")

    assert "generator" in content
    assert "solver" in content
    assert "maze" in content
    assert "solution" in content


def test_json_exporter_creates_file(tmp_path):
    records = create_records()

    filepath = tmp_path / "dataset.json"

    exporter = DatasetJSONExporter()
    exporter.export(records, filepath)

    assert filepath.exists()

    data = json.loads(filepath.read_text(encoding="utf-8"))

    assert len(data) == 3
    assert data[0]["generator"] == "recursive_backtracking"
    assert data[0]["solver"] == "bfs"

def test_json_exporter_preserves_maze(tmp_path):
    records = create_records()

    filepath = tmp_path / "dataset.json"

    DatasetJSONExporter().export(records, filepath)

    data = json.loads(filepath.read_text(encoding="utf-8"))

    assert data[0]["maze"] == records[0].maze
    assert data[0]["solution"] == [
        list(position)
        for position in records[0].solution
    ]