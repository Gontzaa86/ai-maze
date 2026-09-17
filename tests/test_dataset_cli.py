import json

from dataset.run import main

from generators.registry import discover_generators
from solvers.registry import discover_solvers

discover_generators()
discover_solvers()

def test_dataset_cli_generates_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "sys.argv",
        [
            "dataset.run",
            "--generators",
            "recursive_backtracking",
            "--solvers",
            "bfs",
            "--rows",
            "4",
            "--cols",
            "4",
            "--count",
            "2",
            "--seed",
            "42",
            "--output",
            "datasets/test",
        ],
    )

    main()

    output_dir = tmp_path / "datasets" / "test"

    assert (output_dir / "dataset.csv").exists()
    assert (output_dir / "dataset.json").exists()
    assert (output_dir / "metadata.json").exists()

    metadata = json.loads(
        (output_dir / "metadata.json").read_text(
            encoding="utf-8"
        )
    )

    assert metadata["seed"] == 42
    assert metadata["seed_count"] == 2
    assert metadata["rows"] == 4
    assert metadata["cols"] == 4
    assert metadata["records"] == 2