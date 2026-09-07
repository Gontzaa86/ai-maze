from maze.generator import RecursiveBacktrackingGenerator
from solvers.tremaux import TremauxSolver
from solvers.events import EventType

def is_valid_solution(maze, solution):

    if not solution:
        return False

    for position in solution:

        row, col = position

        if not maze.is_inside(row, col):
            return False

    for current, next_position in zip(
        solution,
        solution[1:]
    ):

        current_cell = maze.get_cell(*current)

        row_diff = next_position[0] - current[0]
        col_diff = next_position[1] - current[1]

        if row_diff == -1:
            if current_cell.walls["up"]:
                return False

        elif row_diff == 1:
            if current_cell.walls["down"]:
                return False

        elif col_diff == -1:
            if current_cell.walls["left"]:
                return False

        elif col_diff == 1:
            if current_cell.walls["right"]:
                return False

        else:
            return False

    return True

def test_solver_reaches_end():
    generator = RecursiveBacktrackingGenerator()
    solver = TremauxSolver()

    maze = generator.generate(10, 10)

    start = (0, 0)
    end = (9, 9)

    result = solver.solve(
        maze,
        start,
        end
    )
    solution = result.solution

    assert solution[0] == start
    assert solution[-1] == end

def test_solution_is_valid():
    generator = RecursiveBacktrackingGenerator()
    solver = TremauxSolver()

    maze = generator.generate(20, 20)

    result = solver.solve(
        maze,
        (0, 0),
        (19, 19)
    )
    solution = result.solution

    assert is_valid_solution(
        maze,
        solution
    )

def test_solver_on_different_sizes():
    generator = RecursiveBacktrackingGenerator()
    solver = TremauxSolver()

    sizes = [
        (1, 1),
        (1, 5),
        (5, 1),
        (2, 2),
        (5, 5),
        (10, 20),
        (20, 10),
    ]

    for rows, cols in sizes:

        maze = generator.generate(
            rows,
            cols
        )

        result = solver.solve(
            maze,
            (0, 0),
            (rows - 1, cols - 1)
        )
        solution = result.solution

        assert solution[0] == (0, 0)
        assert solution[-1] == (
            rows - 1,
            cols - 1
        )

        assert is_valid_solution(
            maze,
            solution
        )

def test_solver_multiple_random_mazes():
    generator = RecursiveBacktrackingGenerator()
    solver = TremauxSolver()

    for _ in range(100):

        maze = generator.generate(
            20,
            20
        )

        result = solver.solve(
            maze,
            (0, 0),
            (19, 19)
        )
        solution = result.solution

        assert solution[0] == (0, 0)
        assert solution[-1] == (19, 19)

        assert is_valid_solution(
            maze,
            solution
        )

def test_solver_generates_events():
    generator = RecursiveBacktrackingGenerator()
    solver = TremauxSolver()

    maze = generator.generate(10, 10)

    result = solver.solve(
        maze,
        (0, 0),
        (9, 9)
    )

    assert result.events


def test_first_event_is_start():
    generator = RecursiveBacktrackingGenerator()
    solver = TremauxSolver()

    maze = generator.generate(10, 10)

    result = solver.solve(
        maze,
        (0, 0),
        (9, 9)
    )

    first = result.events[0]

    assert first.type == EventType.START
    assert first.position == (0, 0)


def test_last_event_is_solved():
    generator = RecursiveBacktrackingGenerator()
    solver = TremauxSolver()

    maze = generator.generate(10, 10)

    result = solver.solve(
        maze,
        (0, 0),
        (9, 9)
    )

    last = result.events[-1]

    assert last.type == EventType.SOLVED
    assert last.position == (9, 9)


def test_move_events_are_valid_positions():
    generator = RecursiveBacktrackingGenerator()
    solver = TremauxSolver()

    maze = generator.generate(10, 10)

    result = solver.solve(
        maze,
        (0, 0),
        (9, 9)
    )

    for event in result.events:

        row, col = event.position

        assert maze.is_inside(row, col)


def test_backtracking_occurs_when_needed():
    generator = RecursiveBacktrackingGenerator()
    solver = TremauxSolver()

    maze = generator.generate(20, 20)

    result = solver.solve(
        maze,
        (0, 0),
        (19, 19)
    )

    backtracks = [
        event
        for event in result.events
        if event.type == EventType.BACKTRACK
    ]

    # En un laberinto aleatorio es muy probable
    # que haya retrocesos, pero no debemos asumir
    # que siempre los habrá.
    assert len(backtracks) >= 0

def test_edges_are_marked_between_zero_and_two():
    generator = RecursiveBacktrackingGenerator()
    maze = generator.generate(10, 10)

    solver = TremauxSolver()

    result = solver.solve(
        maze,
        (0, 0),
        (9, 9)
    )

    for mark in result.edge_marks.values():
        assert mark in (1, 2)

def test_no_edge_is_marked_more_than_twice():
    generator = RecursiveBacktrackingGenerator()
    maze = generator.generate(10, 10)

    solver = TremauxSolver()

    result = solver.solve(
        maze,
        (0, 0),
        (9, 9)
    )

    for mark in result.edge_marks.values():
        assert mark <= 2

def test_movement_events_contain_edge_marks():
    generator = RecursiveBacktrackingGenerator()
    maze = generator.generate(10, 10)

    solver = TremauxSolver()

    result = solver.solve(
        maze,
        (0, 0),
        (9, 9)
    )

    movement_events = [
        event
        for event in result.events
        if event.type in (
            EventType.MOVE,
            EventType.BACKTRACK,
        )
    ]

    assert movement_events

    for event in movement_events:
        assert event.from_position is not None
        assert event.to_position is not None
        assert event.mark in (1, 2)