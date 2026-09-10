from abc import ABC, abstractmethod

from maze.maze import Maze
from solvers.events import SolveResult

class Solver(ABC):
    @abstractmethod
    def solve(self, maze: Maze, start: tuple[int, int], end: tuple[int, int]) -> SolveResult:
        """Resuelve un laberinto y devuelve el resultado."""
        raise NotImplementedError