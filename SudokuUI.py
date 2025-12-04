import tkinter as tk
from tkinter import messagebox
import random

# Import the classes that contain the Sudoku logic
from Sudoku import SudokuGrid, SudokuSolver

def main():
    class SudokuUI(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Sudoku")
            self.geometry("450x550")
            self.cells = {}
            
            # Register the validation command
            vcmd = (self.register(self.validate_input), '%P')
            self._create_grid(vcmd)
            self._create_buttons()

        def validate_input(self, P):
            """Validates the input to allow only single digits from 1-9."""
            # P is the value of the entry if the edit is allowed
            if P == "":
                return True  # Allow deletion
            if len(P) == 1 and P.isdigit() and P != '0':
                return True  # Allow a single digit (1-9)
            return False # Reject all other inputs

        def _create_grid(self, vcmd):
            frame = tk.Frame(self)
            frame.pack(pady=10)
            for i in range(9):
                for j in range(9):
                    cell = tk.Entry(frame, width=3, font=('Arial', 18), justify='center', bd=1, relief='solid',
                                  validate="key", validatecommand=vcmd)
                    padx = (5, 0) if j % 3 == 0 else (1, 0)
                    pady = (5, 0) if i % 3 == 0 else (1, 0)
                    cell.grid(row=i, column=j, padx=padx, pady=pady, ipady=5)
                    self.cells[(i, j)] = cell

        def _create_buttons(self):
            button_frame = tk.Frame(self)
            button_frame.pack(pady=20)
            
            generate_button = tk.Button(button_frame, text="Generate", command=self.generate_puzzle)
            generate_button.pack(side="left", padx=10)

            solve_button = tk.Button(button_frame, text="Solve", command=self.solve_puzzle)
            solve_button.pack(side="left", padx=10)

            clear_button = tk.Button(button_frame, text="Clear", command=self.clear_grid)
            clear_button.pack(side="left", padx=10)

        def generate_puzzle(self):
            # Use the imported classes to handle the logic
            board = SudokuGrid()
            solver = SudokuSolver(board)
            solver.solve()
            self._update_grid_ui(board.grid)

        def _update_grid_ui(self, grid):
            for i in range(9):
                for j in range(9):
                    cell = self.cells[(i, j)]
                    cell.delete(0, tk.END)
                    # Don't display zeros for a cleaner look
                    if grid[i][j] != 0:
                        cell.insert(0, str(grid[i][j]))

        def solve_puzzle(self):
            # 1. Create a new grid object to represent the current UI state
            current_board = SudokuGrid()
            
            # 2. Read the numbers from the UI into the grid object
            try:
                for (r, c), cell_widget in self.cells.items():
                    val = cell_widget.get()
                    if val == "":
                        current_board.grid[r][c] = 0
                    else:
                        num = int(val)
                        if 1 <= num <= 9:
                            current_board.grid[r][c] = num
                        else:
                            raise ValueError("Invalid Number")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter only numbers between 1 and 9.")
                return

            # 3. Use the solver on the grid object
            solver = SudokuSolver(current_board)
            if solver.solve():
                # 4. Update the UI with the solved grid
                self._update_grid_ui(current_board.grid)
            else:
                messagebox.showerror("Error", "This puzzle cannot be solved.")

        def clear_grid(self):
            for cell in self.cells.values():
                cell.delete(0, tk.END)

    app = SudokuUI()
    app.mainloop()

if __name__ == "__main__":
    main()
