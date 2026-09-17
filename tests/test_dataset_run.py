import json
from unittest.mock import patch

from dataset.run import run_dataset

from generators.registry import discover_generators
from solvers.registry import discover_solvers

discover_generators()
discover_solvers()

def test_run_dataset_generates_records(tmp_path):
    result = run_dataset(
        generators=["recursive_backtracking"],
        solvers=["bfs"],
        rows=4,
        cols=4,
        start=(0, 0),
        end=(3, 3),
        seed_count=3,
        seed=123,
    )

    assert len(result.records) == 3
    assert result.csv_path is None
    assert result.json_path is None

def test_run_dataset_exports_csv(tmp_path):
    csv_path = tmp_path / "dataset.csv"

    result = run_dataset(
        generators=["recursive_backtracking"],
        solvers=["bfs"],
        rows=4,
        cols=4,
        start=(0, 0),
        end=(3, 3),
        seed_count=3,
        seed=123,
        csv_filepath=csv_path,
    )

    assert result.csv_path == csv_path
    assert csv_path.exists()

    content = csv_path.read_text(encoding="utf-8")

    assert "generator" in content
    assert "maze" in content
    assert "solution" in content

def test_run_dataset_exports_json(tmp_path):
    json_path = tmp_path / "dataset.json"

    result = run_dataset(
        generators=["recursive_backtracking"],
        solvers=["bfs"],
        rows=4,
        cols=4,
        start=(0, 0),
        end=(3, 3),
        seed_count=3,
        seed=123,
        json_filepath=json_path,
    )

    assert result.json_path == json_path
    assert json_path.exists()

    data = json.loads(
        json_path.read_text(encoding="utf-8")
    )

    assert len(data) == 3
    assert data[0]["generator"] == "recursive_backtracking"
    assert data[0]["solver"] == "bfs"

def test_run_dataset_exports_both_formats(tmp_path):
    csv_path = tmp_path / "dataset.csv"
    json_path = tmp_path / "dataset.json"

    result = run_dataset(
        generators=[
            "recursive_backtracking",
            "cyclic",
        ],
        solvers=["bfs"],
        rows=4,
        cols=4,
        start=(0, 0),
        end=(3, 3),
        seed_count=2,
        seed=456,
        csv_filepath=csv_path,
        json_filepath=json_path,
    )

    assert len(result.records) == 4
    assert result.csv_path == csv_path
    assert result.json_path == json_path

    assert csv_path.exists()
    assert json_path.exists()

def test_run_dataset_validates_records():
    with patch(
        "dataset.run.validate_records"
    ) as mock_validate:
        run_dataset(
            generators=["recursive_backtracking"],
            solvers=["bfs"],
            rows=4,
            cols=4,
            start=(0, 0),
            end=(3, 3),
            seed_count=2,
            seed=123,
        )

    mock_validate.assert_called_once()


def test_run_dataset_does_not_export_invalid_records(tmp_path):
    csv_path = tmp_path / "dataset.csv"

    with patch(
        "dataset.run.validate_records",
        side_effect=ValueError("invalid dataset"),
    ):
        try:
            run_dataset(
                generators=["recursive_backtracking"],
                solvers=["bfs"],
                rows=4,
                cols=4,
                start=(0, 0),
                end=(3, 3),
                seed_count=2,
                seed=123,
                csv_filepath=csv_path,
            )
        except ValueError:
            pass

    assert not csv_path.exists()