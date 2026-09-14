from benchmark.runner import BenchmarkRunner

from generators.recursive_backtracking import RecursiveBacktrackingGenerator

from solvers.bfs import BFSSolver

def test_benchmark_runner():
    generator = RecursiveBacktrackingGenerator(seed=12345)

    solver = BFSSolver()

    runner = BenchmarkRunner()

    result = runner.run(
        generator=generator,
        solver=solver,
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
    )

    metrics = result.metrics

    assert metrics.success is True
    assert metrics.solution_length > 0
    assert metrics.moves > 0
    assert metrics.visited_cells > 0
    assert metrics.execution_time >= 0

def test_generators_with_same_seed_generate_same_maze():

    generator_a = RecursiveBacktrackingGenerator(
        seed=12345
    )

    generator_b = RecursiveBacktrackingGenerator(
        seed=12345
    )

    maze_a = generator_a.generate(5, 5)
    maze_b = generator_b.generate(5, 5)

    for row in range(5):
        for col in range(5):

            cell_a = maze_a.get_cell(row, col)
            cell_b = maze_b.get_cell(row, col)

            assert cell_a.walls == cell_b.walls

def test_bfs_is_reproducible_on_same_maze():

    generator_a = RecursiveBacktrackingGenerator(
        seed=12345
    )

    generator_b = RecursiveBacktrackingGenerator(
        seed=12345
    )

    maze_a = generator_a.generate(5, 5)
    maze_b = generator_b.generate(5, 5)

    solver = BFSSolver()

    result_a = solver.solve(
        maze_a,
        (0, 0),
        (4, 4),
    )

    result_b = solver.solve(
        maze_b,
        (0, 0),
        (4, 4),
    )

    assert result_a.solution == result_b.solution
    assert result_a.events == result_b.events
    assert len(result_a.events) == len(result_b.events)

def test_benchmark_runner_is_reproducible():

    generator_a = RecursiveBacktrackingGenerator(
        seed=12345
    )

    generator_b = RecursiveBacktrackingGenerator(
        seed=12345
    )

    solver_a = BFSSolver()
    solver_b = BFSSolver()

    runner = BenchmarkRunner()

    result_a = runner.run(
        generator=generator_a,
        solver=solver_a,
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
    )

    result_b = runner.run(
        generator=generator_b,
        solver=solver_b,
        rows=5,
        cols=5,
        start=(0, 0),
        end=(4, 4),
    )

    assert result_a.result.solution == result_b.result.solution
    assert result_a.result.events == result_b.result.events

    assert (
        result_a.metrics.solution_length
        == result_b.metrics.solution_length
    )

    assert (
        result_a.metrics.moves
        == result_b.metrics.moves
    )

    assert (
        result_a.metrics.backtracks
        == result_b.metrics.backtracks
    )

    assert (
        result_a.metrics.visited_cells
        == result_b.metrics.visited_cells
    )

def test_benchmark_runner_generates_same_maze():

    generator_a = RecursiveBacktrackingGenerator(
        seed=12345
    )

    generator_b = RecursiveBacktrackingGenerator(
        seed=12345
    )

    maze_a = generator_a.generate(5, 5)
    maze_b = generator_b.generate(5, 5)

    for row in range(5):
        for col in range(5):

            cell_a = maze_a.get_cell(row, col)
            cell_b = maze_b.get_cell(row, col)

            assert cell_a.walls == cell_b.walls