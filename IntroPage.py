from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class IntroPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Select Difficulty")
        font = label.font()
        font.setPointSize(28)
        font.setBold(True)
        label.setFont(font)
        label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_style = """
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #3d5166; }
            QPushButton:pressed { background-color: #1a252f; }
        """

        easy_button = QPushButton("Easy")
        easy_button.setFixedSize(160, 55)
        easy_button.setStyleSheet(btn_style)
        easy_button.clicked.connect(lambda: self.controller.start_game("Easy"))
        layout.addWidget(easy_button, alignment=Qt.AlignmentFlag.AlignCenter)

        medium_button = QPushButton("Medium")
        medium_button.setFixedSize(160, 55)
        medium_button.setStyleSheet(btn_style)
        medium_button.clicked.connect(lambda: self.controller.start_game("Medium"))
        layout.addWidget(medium_button, alignment=Qt.AlignmentFlag.AlignCenter)

        hard_button = QPushButton("Hard")
        hard_button.setFixedSize(160, 55)
        hard_button.setStyleSheet(btn_style)
        hard_button.clicked.connect(lambda: self.controller.start_game("Hard"))
        layout.addWidget(hard_button, alignment=Qt.AlignmentFlag.AlignCenter)