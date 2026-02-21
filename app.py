import sys
from PyQt6.QtWidgets import QApplication
from SudokuApp import SudokuApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuApp()
    window.show()
    sys.exit(app.exec())
