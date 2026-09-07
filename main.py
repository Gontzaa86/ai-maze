from maze.generator import RecursiveBacktrackingGenerator
from solvers.tremaux import TremauxSolver

generator = RecursiveBacktrackingGenerator()

maze = generator.generate(rows = 20, cols = 20)

solver = TremauxSolver()

solution = solver.solve(
    maze,
    start = (0, 0),
    end = (19, 19)
)

print(maze)
print("Longitud: ", len(solution))
print("Solución: ", solution)