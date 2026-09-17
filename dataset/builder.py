from itertools import product

from benchmark.seeds import generate_seeds
from dataset.generator import DatasetGenerator
from dataset.record import DatasetRecord

def generate_dataset(
    generators: list[str],
    solvers: list[str],
    rows: int,
    cols: int,
    start: tuple[int, int],
    end: tuple[int, int],
    seed_count: int,
    seed: int | None = None,
) -> list[DatasetRecord]:
    if not generators:
        raise ValueError("Debe haber al menos un generador.")
    if not solvers:
        raise ValueError("Debe haber al menos un solver.")
    if seed_count < 0:
        raise ValueError("El número de seeds no puede ser negativo.")

    seeds = generate_seeds(count=seed_count, seed=seed)

    dataset_generator = DatasetGenerator()
    records = []

    for generator_name, solver_name in product(generators, solvers):
        for current_seed in seeds:
            record = dataset_generator.generate(
                generator_name=generator_name,
                solver_name=solver_name,
                rows=rows,
                cols=cols,
                start=start,
                end=end,
                seed=current_seed
            )

            records.append(record)

    return records