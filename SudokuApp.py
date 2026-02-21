import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from IntroPage import IntroPage
from MainPage import MainPage

class SudokuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku")
        self.setGeometry(100, 100, 550, 650)
        self.setStyleSheet("background-color: #f0f4f8;")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.intro_page = IntroPage(self)
        self.stacked_widget.addWidget(self.intro_page)

        self.show_intro_page()

    def show_intro_page(self):
        self.stacked_widget.setCurrentWidget(self.intro_page)

    def start_game(self, difficulty):
        self.main_page = MainPage(self, difficulty)
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.setCurrentWidget(self.main_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuApp()
    window.show()
    sys.exit(app.exec())