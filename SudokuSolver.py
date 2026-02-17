import random

class SudokuSolver:
    """A solver that uses a backtracking algorithm to fill a SudokuGrid."""
    def __init__(self, grid_obj):
        self.grid = grid_obj

    def solve(self):
        """Solves the Sudoku grid using backtracking."""
        find = self.grid.find_empty()
        if not find:
            return True  # Grid is full
        else:
            row, col = find

        numbers = list(range(1, 10))
        random.shuffle(numbers)  # Add randomness to the generation

        for num in numbers:
            # Here, the Solver communicates with the Grid, asking if a move is valid
            if self.grid.is_valid(num, (row, col)):
                # The Solver tells the Grid to place the number
                self.grid.grid[row][col] = num

                if self.solve():
                    return True

                # The Solver tells the Grid to undo the move (backtrack)
                self.grid.grid[row][col] = 0

        return False
