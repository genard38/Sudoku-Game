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
            self.geometry("550x550") # Adjusted for new buttons
            self.cells = {}
            self.undo_stack = []
            self.redo_stack = []
            
            vcmd = (self.register(self.validate_input), '%P', '%W')
            self._create_grid(vcmd)
            self._create_buttons()
            self.record_state() # Initial state

        def validate_input(self, P, W):
            if P == "" or (len(P) == 1 and P.isdigit() and P != '0'):
                # When input is valid, record the state for undo
                self.after_idle(self.record_state)
                return True
            return False

        def _create_grid(self, vcmd):
            frame = tk.Frame(self)
            frame.pack(pady=10)
            for i in range(9):
                for j in range(9):
                    cell = tk.Entry(frame, width=3, font=('Arial', 18), justify='center', bd=1, relief='solid',
                                  validate="key", validatecommand=vcmd)
                    cell.grid(row=i, column=j, padx=(5,0) if j%3==0 else (1,0), pady=(5,0) if i%3==0 else (1,0), ipady=5)
                    self.cells[(i, j)] = cell

        def _create_buttons(self):
            button_frame = tk.Frame(self)
            button_frame.pack(pady=20)
            
            tk.Button(button_frame, text="Generate", command=self.generate_puzzle).pack(side="left", padx=5)
            tk.Button(button_frame, text="Solve", command=self.solve_puzzle).pack(side="left", padx=5)
            tk.Button(button_frame, text="Clear", command=self.clear_grid).pack(side="left", padx=5)
            tk.Button(button_frame, text="Undo", command=self.undo).pack(side="left", padx=5)
            tk.Button(button_frame, text="Redo", command=self.redo).pack(side="left", padx=5)

        def record_state(self):
            """Saves the current grid state to the undo stack."""
            state = {pos: cell.get() for pos, cell in self.cells.items()}
            if not self.undo_stack or self.undo_stack[-1] != state:
                self.undo_stack.append(state)
                self.redo_stack.clear() # Clear redo stack on new action

        def undo(self):
            if len(self.undo_stack) > 1:
                self.redo_stack.append(self.undo_stack.pop())
                self._apply_state(self.undo_stack[-1])

        def redo(self):
            if self.redo_stack:
                state = self.redo_stack.pop()
                self.undo_stack.append(state)
                self._apply_state(state)

        def _apply_state(self, state):
            """Applies a grid state to the UI."""
            for pos, value in state.items():
                self.cells[pos].delete(0, tk.END)
                if value:
                    self.cells[pos].insert(0, value)

        def generate_puzzle(self):
            board = SudokuGrid()
            solver = SudokuSolver(board)
            solver.solve()
            self._update_grid_ui(board.grid)
            self.record_state()

        def _update_grid_ui(self, grid):
            for i in range(9):
                for j in range(9):
                    cell = self.cells[(i, j)]
                    cell.delete(0, tk.END)
                    if grid[i][j] != 0:
                        cell.insert(0, str(grid[i][j]))

        def solve_puzzle(self):
            current_board = SudokuGrid()
            try:
                for (r, c), cell in self.cells.items():
                    val = cell.get()
                    current_board.grid[r][c] = int(val) if val else 0
            except ValueError:
                messagebox.showerror("Input Error", "Invalid number in grid.")
                return

            solver = SudokuSolver(current_board)
            if solver.solve():
                self._update_grid_ui(current_board.grid)
                self.record_state()
            else:
                messagebox.showerror("Error", "This puzzle cannot be solved.")

        def clear_grid(self):
            for cell in self.cells.values():
                cell.delete(0, tk.END)
            self.record_state()

    app = SudokuUI()
    app.mainloop()

if __name__ == "__main__":
    main()
