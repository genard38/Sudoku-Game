import tkinter as tk
from tkinter import messagebox

class SudokuUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Solver")
        self.geometry("450x550")
        self.cells = {}
        self._create_grid()
        self._create_buttons()

    def _create_grid(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        for i in range(9):
            for j in range(9):
                cell = tk.Entry(frame, width=3, font=('Arial', 18), justify='center', bd=1, relief='solid')
                
                # Add padding to create visual subgrids
                padx = (5, 0) if j % 3 == 0 else (1, 0)
                pady = (5, 0) if i % 3 == 0 else (1, 0)
                
                cell.grid(row=i, column=j, padx=padx, pady=pady, ipady=5)
                self.cells[(i, j)] = cell

    def _create_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        solve_button = tk.Button(button_frame, text="Solve", command=self.solve_puzzle)
        solve_button.pack(side="left", padx=10)

        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_grid)
        clear_button.pack(side="left", padx=10)

    def solve_puzzle(self):
        messagebox.showinfo("Not Implemented", "The 'Solve' functionality is not yet implemented.")

    def clear_grid(self):
        for cell in self.cells.values():
            cell.delete(0, tk.END)

if __name__ == "__main__":
    app = SudokuUI()
    app.mainloop()
