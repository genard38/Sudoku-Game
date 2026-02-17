import tkinter as tk
from IntroPage import IntroPage
from MainPage import MainPage

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

if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()
