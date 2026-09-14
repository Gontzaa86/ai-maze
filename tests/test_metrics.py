from benchmark.metrics import SolveMetrics, calculate_metrics, measure_execution_time

from solvers.events import EventType, SolveResult, SolverEvent

def test_solve_metrics_creation():
    metrics = SolveMetrics(
        solution_length=10,
        moves=15,
        backtracks=5,
        success=True,
        visited_cells=20,
        execution_time=0.001,
    )

    assert metrics.solution_length == 10
    assert metrics.moves == 15
    assert metrics.backtracks == 5
    assert metrics.success is True
    assert metrics.visited_cells == 20
    assert metrics.execution_time == 0.001

def test_calculate_metrics():
    result = SolveResult(
        solution=[(0, 0), (0, 1), (1, 1)],
        events=[
            SolverEvent(
                type=EventType.START,
                position=(0, 0),
            ),
            SolverEvent(
                type=EventType.MOVE,
                position=(0, 1),
                from_position=(0, 0),
                to_position=(0, 1),
            ),
            SolverEvent(
                type=EventType.MOVE,
                position=(1, 1),
                from_position=(0, 1),
                to_position=(1, 1),
            ),
            SolverEvent(
                type=EventType.SOLVED,
                position=(1, 1),
            ),
        ],
        edge_marks={},
    )

    metrics = calculate_metrics(
        result,
        start=(0, 0),
        end=(1, 1),
        execution_time=0.001,
    )

    assert metrics.solution_length == 3
    assert metrics.moves == 2
    assert metrics.backtracks == 0
    assert metrics.success is True
    assert metrics.visited_cells == 2
    assert metrics.execution_time == 0.001

def test_calculate_metrics_with_backtracking():
    result = SolveResult(
        solution=[
            (0, 0),
            (0, 1),
            (1, 1),
        ],
        events=[
            SolverEvent(
                type=EventType.START,
                position=(0, 0),
            ),
            SolverEvent(
                type=EventType.MOVE,
                position=(0, 1),
                from_position=(0, 0),
                to_position=(0, 1),
            ),
            SolverEvent(
                type=EventType.BACKTRACK,
                position=(0, 0),
                from_position=(0, 1),
                to_position=(0, 0),
            ),
            SolverEvent(
                type=EventType.MOVE,
                position=(1, 0),
                from_position=(0, 0),
                to_position=(1, 0),
            ),
            SolverEvent(
                type=EventType.MOVE,
                position=(1, 1),
                from_position=(1, 0),
                to_position=(1, 1),
            ),
            SolverEvent(
                type=EventType.SOLVED,
                position=(1, 1),
            ),
        ],
        edge_marks={},
    )

    metrics = calculate_metrics(
        result,
        start=(0, 0),
        end=(1, 1),
        execution_time=0.001,
    )


    assert metrics.solution_length == 3
    assert metrics.moves == 3
    assert metrics.backtracks == 1
    assert metrics.success is True
    assert metrics.visited_cells == 4
    assert metrics.execution_time == 0.001

def test_measure_execution_time():
    class FakeSolver:
        def solve(self, maze, start, end):
            return SolveResult(
                solution=[start, end],
                events=[
                    SolverEvent(
                        type=EventType.START,
                        position=start,
                    ),
                    SolverEvent(
                        type=EventType.MOVE,
                        position=end,
                        from_position=start,
                        to_position=end,
                    ),
                    SolverEvent(
                        type=EventType.SOLVED,
                        position=end,
                    ),
                ],
                edge_marks={},
            )

    solver = FakeSolver()

    result, execution_time = measure_execution_time(
        solver,
        maze=None,
        start=(0, 0),
        end=(0, 1),
    )

    assert result.solution == [
        (0, 0),
        (0, 1),
    ]

    assert execution_time >= 0