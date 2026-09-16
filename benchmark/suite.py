from .record import BenchmarkRecord
from .runner import BenchmarkRunner
from .csv_exporter import BenchmarkCSVExporter
from .seeds import generate_seeds

class BenchmarkSuite:
    def __init__(self, runner: BenchmarkRunner | None = None):
        self.runner = runner or BenchmarkRunner()

    def run(
            self,
            generator,
            solver,
            rows: int,
            cols: int,
            start: tuple[int, int],
            end: tuple[int, int],
            seeds: list[int | None]
    ) -> list[BenchmarkRecord]:
        records = []

        for seed in seeds:
            generator_instance = generator(seed = seed)

            result = self.runner.run(
                generator = generator_instance,
                solver = solver(),
                rows = rows,
                cols = cols,
                start = start,
                end = end
            )

            records.append(result.record)

        return records

    def run_many(
        self,
        generators,
        solvers,
        rows: int,
        cols: int,
        start: tuple[int, int],
        end: tuple[int, int],
        seeds: list[int | None] | None = None,
        seed_count: int | None = None,
        seed: int | None = None
    ) -> list[BenchmarkRecord]:
        if seeds is not None and seed_count is not None:
            raise ValueError("No se pueden indicar seeds y seed_count a la vez")

        if seeds is None:
            if seed_count is None:
                raise ValueError("Debe indicarse seeds o seed_count.")

            seeds = generate_seeds(count = seed_count, seed = seed)
        
        records = []

        for generator in generators:
            for solver in solvers:
                records.extend(
                    self.run(
                        generator=generator,
                        solver=solver,
                        rows=rows,
                        cols=cols,
                        start=start,
                        end=end,
                        seeds=seeds
                    )
                )

        return records

    def export(self, records: list[BenchmarkRecord], filepath) -> None:
        exporter = BenchmarkCSVExporter()

        exporter.export(records = records, filepath = filepath)