from benchmark.metrics import calculate_metrics, measure_execution_time
from benchmark.seeds import generate_seeds

from dataset.record import DatasetRecord, encode_maze

from generators.registry import create_generator

from solvers.registry import create_solver

class DatasetGenerator:
    def generate(
            self,
            generator_name: str,
            solver_name: str,
            rows: int,
            cols: int,
            start: tuple[int, int],
            end: tuple[int, int],
            seed: int | None = None
    ) -> DatasetRecord:
        generator = create_generator(generator_name, seed=seed)
        solver = create_solver(solver_name)

        maze = generator.generate(rows, cols)

        result, execution_time = measure_execution_time(solver, maze, start, end)

        metrics = calculate_metrics(result, start, end, execution_time=execution_time)

        return DatasetRecord(
            generator=generator_name,
            solver=solver_name,
            rows=rows,
            cols=cols,
            seed=seed,
            start=start,
            end=end,
            maze=self._encode_maze(maze),
            solution=result.solution,
            solution_length=metrics.solution_length,
            moves=metrics.moves,
            backtracks=metrics.backtracks,
            visited_cells=metrics.visited_cells,
            execution_time=metrics.execution_time,
            success=metrics.success
        )

    def generate_many(
            self,
            generator_name: str,
            solver_name: str,
            rows: int,
            cols: int,
            start: tuple[int, int],
            end: tuple[int, int],
            seed_count: int,
            seed: int | None = None
    ) -> list[DatasetRecord]:
        seeds = generate_seeds(count=seed_count, seed=seed)

        return [
            self.generate(
                generator_name=generator_name,
                solver_name=solver_name,
                rows=rows,
                cols=cols,
                start=start,
                end=end,
                seed=current_seed
            )
            for current_seed in seeds
        ]

    def _encode_maze(self, maze):
        from dataset.record import encode_maze

        return encode_maze(maze)