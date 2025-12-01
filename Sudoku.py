import random


def create_empty_grid():
    return [[0 for _ in range(9)] for _ in range(9)]


def find_empty(grid):
    """Finds an empty cell in the grid (represented by 0)."""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j  # row, col
    return None


def is_valid(grid, num, pos):
    """Checks if a number is valid in a given position."""
    row, col = pos

    # Check row
    # Checks the number is already in the same row
    for j in range(9):
        if grid[row][j] == num and col != j:
            return False

    # Check column
    # Checks the number is already in the same column
    for i in range(9):
        if grid[i][col] == num and row != i:
            return False

    # Check 3x3 box
    # Checks the number is already in the same 3x3 box
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grid[i][j] == num and (i, j) != pos:
                return False

    return True



def solve_sudoku(grid):
    """Solves the Sudoku grid using backtracking."""
    find = find_empty(grid)
    if not find:
        return True  # Grid is full
    else:
        row, col = find

    numbers = list(range(1, 10))
    random.shuffle(numbers)  # Add randomness to the generation

    for num in numbers:
        if is_valid(grid, num, (row, col)):
            grid[row][col] = num

            if solve_sudoku(grid):
                return True

            grid[row][col] = 0  # Backtrack

    return False



def print_grid(grid):
    for i in range(9):
        for j in range(9):
            # Hidden Lines - This line was causing an error due to 'j' not being defined.
            print(grid[i][j], end=" ")
        print()

if __name__ == "__main__":
    sudoku_grid = create_empty_grid()
    solve_sudoku(sudoku_grid)
    print_grid(sudoku_grid)