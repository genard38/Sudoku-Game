import random


class SudokuGrid:
    """Represents the Sudoku grid and its rules."""
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def find_empty(self):
        """Finds an empty cell in the grid (represented by 0)."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j  # row, col
        return None

    def is_valid(self, num, pos):
        """Checks if a number is valid in a given position."""
        row, col = pos

        # Check row
        for j in range(9):
            if self.grid[row][j] == num:
                return False

        # Check column
        for i in range(9):
            if self.grid[i][col] == num:
                return False

        # Check 3x3 box
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.grid[i][j] == num:
                    return False

        return True

    def print(self):
        """Prints the grid to the console."""
        for i in range(9):
            for j in range(9):
                print(self.grid[i][j], end=" ")
            print()


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


if __name__ == "__main__":
    board = SudokuGrid()
    solver = SudokuSolver(board) # The Solver is given the board to work on
    solver.solve()
    board.print()