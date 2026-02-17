import tkinter as tk

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
