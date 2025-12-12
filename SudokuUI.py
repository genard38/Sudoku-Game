import tkinter as tk
from tkinter import messagebox, PhotoImage
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
        self.colors = {
            "default": "white",
            "highlight": "#e0e0e0",  # A light gray
            "readonly": "#f5f5f5",   # A slightly different gray for given numbers
            "number_highlight": "#cce5ff", # A light blue for matching numbers
            "focus_highlight": "#a6d7ff" # A brighter blue for the focused cell
        }

        # Load the settings icon image before any methods that might use it.
        # Store it as an instance attribute to prevent garbage collection.
        try:
            # Ensure 'settings.png' is in the same folder as your script.
            self.settings_img = PhotoImage(file="settings.png").subsample(1, 1)
        except tk.TclError:
            self.settings_img = None # Fallback if image is not found

        self._create_header()
        validation_command = (self.register(self.validate_input), '%P')
        self._create_grid(validation_command)
        self._create_buttons()
        self.generate_puzzle(difficulty)

        # Bind a click on the frame to clear cell highlighting
        self.bind("<Button-1>", lambda event: self._clear_highlighting())

    def _create_header(self):
        header = tk.Frame(self)
        header.pack(fill="x", padx=10, pady=5)
        tk.Label(header, text="").pack(side="left", expand=True)

        # Use the loaded image if it exists, otherwise fall back to the Unicode character.
        if self.settings_img:
            settings_button = tk.Button(header, image=self.settings_img, command=self.open_settings, borderwidth=0)
        else:
            settings_button = tk.Button(header, text="\u2699", font=("Arial", 16), command=self.open_settings, borderwidth=0)
        settings_button.pack(side="right")

    @staticmethod
    def open_settings():
        messagebox.showinfo("Settings", "Settings functionality is not yet implemented.")

    def validate_input(self, p):
        if p == "" or (len(p) == 1 and p.isdigit() and p != '0'):
            return True
        return False

    def _create_grid(self, validation_command):
        grid_frame = tk.Frame(self)
        grid_frame.pack(pady=10)
        for i in range(9):
            for j in range(9):
                cell = tk.Entry(grid_frame, width=3, font=('Arial', 18), justify='center',
                              bg=self.colors["default"], bd=1, relief='solid',
                              validate="key", validatecommand=validation_command)

                # Bind events to the cell
                cell.bind("<FocusIn>", lambda event, r=i, c=j: self._on_cell_focus(r, c))
                # Chain two commands to the KeyRelease event
                cell.bind("<KeyRelease>", lambda event, r=i, c=j: (self._on_cell_focus(r, c), self.record_state()))

                cell.grid(row=i, column=j, padx=(5,0) if j%3==0 else (1,0), pady=(5,0) if i%3==0 else (1,0), ipady=5)
                self.cells[(i, j)] = cell

    def _get_cell_value(self, cell_widget):
        """Safely gets the value from a cell, even if it's readonly."""
        is_readonly = cell_widget.cget('state') == 'readonly'
        if is_readonly: cell_widget.config(state='normal')
        value = cell_widget.get()
        if is_readonly: cell_widget.config(state='readonly')
        return value

    def _set_cell_bg(self, cell_widget, color):
        """Sets the background of a cell, handling readonly state correctly."""
        if cell_widget.cget('state') == 'readonly':
            cell_widget.config(readonlybackground=color)
        else:
            cell_widget.config(bg=color)

    def _on_cell_focus(self, focused_row, focused_col):
        """Highlights the row, column, and matching numbers for the focused cell."""
        self._clear_highlighting()

        focused_cell = self.cells[(focused_row, focused_col)]
        number_to_match = self._get_cell_value(focused_cell)

        # Always highlight the row and column first
        for c in range(9):
            self._set_cell_bg(self.cells[(focused_row, c)], self.colors["highlight"])
        for r in range(9):
            self._set_cell_bg(self.cells[(r, focused_col)], self.colors["highlight"])

        # Only apply highlights if the cell is not empty
        if number_to_match and number_to_match.isdigit():
            # Then, apply the number highlight, which will override the row/col highlight where necessary
            for (r, c), cell_widget in self.cells.items():
                if self._get_cell_value(cell_widget) == number_to_match:
                    self._set_cell_bg(cell_widget, self.colors["number_highlight"])

        # Finally, the focused cell gets the most prominent highlight, overriding any other color
        self._set_cell_bg(self.cells[(focused_row, focused_col)], self.colors["focus_highlight"])

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

        # Make the given numbers read-only
        for r in range(9):
            for c in range(9):
                if board.grid[r][c] != 0:
                    self.cells[(r, c)].config(state='readonly', readonlybackground=self.colors["readonly"])
                else:
                    self.cells[(r, c)].config(state='normal')

        self.update_grid_ui(board.grid)
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
            self.update_grid_ui(board.grid)
            self.record_state()
        else:
            messagebox.showerror("Error", "This puzzle cannot be solved.")

    def update_grid_ui(self, grid):
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                # Temporarily make cell normal to update it
                is_readonly = cell.cget('state') == 'readonly'
                if is_readonly: cell.config(state='normal')
                cell.delete(0, tk.END)
                if grid[i][j] != 0:
                    cell.insert(0, str(grid[i][j]))
                if is_readonly: cell.config(state='readonly')

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
            cell = self.cells[pos]
            is_readonly = cell.cget('state') == 'readonly'
            if is_readonly: cell.config(state='normal')
            cell.delete(0, tk.END)
            if value:
                cell.insert(0, value)
            if is_readonly: cell.config(state='readonly')

    def _clear_highlighting(self):
        """Resets the background color of all cells to their default (normal or readonly) state."""
        for pos, cell_widget in self.cells.items():
            default_color = self.colors["readonly"] if cell_widget.cget('state') == 'readonly' else self.colors["default"]
            self._set_cell_bg(cell_widget, default_color)

    def clear_grid(self):
        for pos, cell in self.cells.items():
            # Only clear user-editable cells, not the read-only puzzle numbers
            if cell.cget('state') != 'readonly':
                cell.delete(0, tk.END)
        self.record_state()

if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()
