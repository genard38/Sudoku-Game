from SudokuGrid import SudokuGrid
from SudokuSolver import SudokuSolver

if __name__ == "__main__":
    board = SudokuGrid()
    solver = SudokuSolver(board) # The Solver is given the board to work on
    solver.solve()
    board.print()
