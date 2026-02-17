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
