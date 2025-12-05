import tkinter as tk
from tkinter import messagebox
import random

# Assuming Sudoku.py contains SudokuGrid and SudokuSolver
from Sudoku import SudokuGrid, SudokuSolver

class SudokuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry("550x600")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.show_intro_page()

    def show_frame(self, context, *args, **kwargs):
        # Always create a new frame for MainPage to ensure correct difficulty
        if context == MainPage:
            frame = self.frames.get(context)
            if frame:
                frame.destroy()
            frame = context(self.container, self, *args, **kwargs)
            self.frames[context] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        elif context not in self.frames:
            frame = context(self.container, self, *args, **kwargs)
            self.frames[context] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.frames[context].tkraise()

    def show_intro_page(self):
        self.show_frame(IntroPage)

    def start_game(self, difficulty):
        self.show_frame(MainPage, difficulty)

class IntroPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = tk.Frame(self)
        main_frame.grid(row=0, column=0)

        label = tk.Label(main_frame, text="Select Difficulty", font=("Arial", 24))
        label.pack(pady=20, padx=10)

        tk.Button(main_frame, text="Easy", font=("Arial", 18), command=lambda: controller.start_game("Easy")).pack(pady=10)
        tk.Button(main_frame, text="Medium", font=("Arial", 18), command=lambda: controller.start_game("Medium")).pack(pady=10)
        tk.Button(main_frame, text="Hard", font=("Arial", 18), command=lambda: controller.start_game("Hard")).pack(pady=10)

class MainPage(tk.Frame):
    def __init__(self, parent, controller, difficulty):
        super().__init__(parent)
        self.controller = controller
        self.cells = {}
        self.undo_stack = []
        self.redo_stack = []

        validation_command = (self.register(self.validate_input), '%P')
        self._create_grid(validation_command)
        self._create_buttons()
        self.generate_puzzle(difficulty)

    def validate_input(self, p):
        if p == "" or (len(p) == 1 and p.isdigit() and p != '0'):
            self.after_idle(self.record_state)
            return True
        return False

    def _create_grid(self, validation_command):
        grid_frame = tk.Frame(self)
        grid_frame.pack(pady=10)
        for i in range(9):
            for j in range(9):
                cell = tk.Entry(grid_frame, width=3, font=('Arial', 18), justify='center', bd=1, relief='solid',
                              validate="key", validatecommand=validation_command)
                cell.grid(row=i, column=j, padx=(5,0) if j%3==0 else (1,0), pady=(5,0) if i%3==0 else (1,0), ipady=5)
                self.cells[(i, j)] = cell

    def _create_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="New Game", command=self.controller.show_intro_page).pack(side="left", padx=5)
        tk.Button(button_frame, text="Solve", command=self.solve_puzzle).pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear_grid).pack(side="left", padx=5)
        tk.Button(button_frame, text="Undo", command=self.undo).pack(side="left", padx=5)
        tk.Button(button_frame, text="Redo", command=self.redo).pack(side="left", padx=5)

    def get_holes_for_difficulty(self, difficulty):
        """Returns the number of cells to remove for the given difficulty."""
        if difficulty == "Easy":
            return 35
        elif difficulty == "Medium":
            return 51
        elif difficulty == "Hard":
            return 56
        return 40 # Default to Easy

    def generate_puzzle(self, difficulty):
        board = SudokuGrid()
        solver = SudokuSolver(board)
        solver.solve() # Creates a full, valid grid

        empty_cells_count = self.get_holes_for_difficulty(difficulty)
        
        all_cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(all_cells)

        for i in range(empty_cells_count):
            r, c = all_cells[i]
            board.grid[r][c] = 0
            
        self._update_grid_ui(board.grid)
        self.record_state()

    def solve_puzzle(self):
        board = SudokuGrid()
        try:
            for (r, c), cell in self.cells.items():
                val = cell.get()
                board.grid[r][c] = int(val) if val else 0
        except ValueError:
            messagebox.showerror("Input Error", "Invalid number in grid.")
            return

        solver = SudokuSolver(board)
        if solver.solve():
            self._update_grid_ui(board.grid)
            self.record_state()
        else:
            messagebox.showerror("Error", "This puzzle cannot be solved.")

    def _update_grid_ui(self, grid):
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                cell.delete(0, tk.END)
                if grid[i][j] != 0:
                    cell.insert(0, str(grid[i][j]))

    def record_state(self):
        state = {pos: cell.get() for pos, cell in self.cells.items()}
        if not self.undo_stack or self.undo_stack[-1] != state:
            self.undo_stack.append(state)
            self.redo_stack.clear()

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
        for pos, value in state.items():
            self.cells[pos].delete(0, tk.END)
            if value:
                self.cells[pos].insert(0, value)

    def clear_grid(self):
        for cell in self.cells.values():
            cell.delete(0, tk.END)
        self.record_state()

if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()
