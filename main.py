from maze.generator import RecursiveBacktrackingGenerator
from solvers.tremaux import TremauxSolver


def main():
    print("=== AI-Maze ===")
    print()

    rows = int(input("Número de filas: "))
    cols = int(input("Número de columnas: "))

    maze = RecursiveBacktrackingGenerator().generate(
        rows,
        cols
    )

    solver = TremauxSolver()

    result = solver.solve(
        maze,
        (0, 0),
        (rows - 1, cols - 1)
    )

    print()
    print("=== Resultado ===")
    print()

    print(f"Laberinto: {rows} x {cols}")
    print(f"Inicio:     (0, 0)")
    print(f"Final:      ({rows - 1}, {cols - 1})")
    print(f"Longitud:   {len(result.solution)} posiciones")
    print(f"Eventos:    {len(result.events)}")
    print()

    print("Solución:")
    print(result.solution)
    print()

    print("Marcas de aristas:")

    for edge, mark in result.edge_marks.items():
        print(f"{set(edge)} -> {mark}")


if __name__ == "__main__":
    main()