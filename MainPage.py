import random
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox, QFrame, \
    QSizePolicy
from PyQt6.QtGui import QValidator, QIcon, QColor
from PyQt6.QtCore import Qt

from SudokuGrid import SudokuGrid
from SudokuSolver import SudokuSolver


class MainPage(QWidget):
    def __init__(self, controller, difficulty):
        super().__init__()
        self.controller = controller
        self.cells = {}
        self.undo_stack = []
        self.redo_stack = []
        self.colors = {
            "default": "#ffffff",
            "highlight": "#aed6f1",
            "readonly": "#d6eaf8",
            "number_highlight": "#5dade2",
            "focus_highlight": "#2e86c1",
            "error": "#e74c3c"
        }
        self.cell_borders = {}

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._create_header()
        self._create_grid()
        self._create_buttons()

        grid_row = QHBoxLayout()
        grid_row.addStretch()
        grid_row.addWidget(self.grid_frame)
        grid_row.addStretch()

        main_layout.addWidget(self.header_frame)
        main_layout.addStretch()
        main_layout.addLayout(grid_row)
        main_layout.addStretch()
        main_layout.addWidget(self.button_frame)

        self.generate_puzzle(difficulty)

    def _create_header(self):
        self.header_frame = QFrame()
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.addStretch()
        settings_button = QPushButton(QIcon("settings.png"), "")
        settings_button.setIconSize(settings_button.sizeHint())
        settings_button.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_button)

    def open_settings(self):
        QMessageBox.information(self, "Settings", "Settings functionality is not yet implemented.")

    def _create_grid(self):
        self.grid_frame = QFrame()
        self.grid_frame.setStyleSheet("background-color: #1a252f; padding: 8px;")
        self.grid_frame.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        grid_layout = QGridLayout(self.grid_frame)
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        for i in range(9):
            for j in range(9):
                cell = QLineEdit()
                cell.setFixedSize(52, 52)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                font = cell.font()
                font.setPointSize(18)
                cell.setFont(font)
                cell.setValidator(NumberValidator())
                cell.textChanged.connect(self.record_state)
                cell.installEventFilter(self)

                border = self._border_style_for_cell(i, j)
                self.cell_borders[(i, j)] = border
                cell.setStyleSheet(f"background-color: {self.colors['default']}; {border}")

                grid_layout.addWidget(cell, i, j)
                self.cells[(i, j)] = cell

        # 9 cells * 52px + 16px padding (8px each side)
        self.grid_frame.setFixedSize(9 * 52 + 16, 9 * 52 + 16)

    def _border_style_for_cell(self, row, col):
        thick = "3px solid #1a252f"
        thin = "1px solid #7f8c8d"
        top = thick if row % 3 == 0 else thin
        left = thick if col % 3 == 0 else thin
        bottom = thick if row == 8 else thin
        right = thick if col == 8 else thin
        return (f"border-top: {top}; border-left: {left}; "
                f"border-bottom: {bottom}; border-right: {right};")

    def eventFilter(self, source, event):
        if isinstance(source, QLineEdit):
            if event.type() == event.Type.FocusIn:
                for r in range(9):
                    for c in range(9):
                        if self.cells[(r, c)] == source:
                            self._on_cell_focus(r, c)
                            break
        return super().eventFilter(source, event)

    def _on_cell_focus(self, focused_row, focused_col):
        error_cells = self._validate_and_highlight_errors()
        self._clear_highlighting(exclude_errors=True)

        focused_cell = self.cells[(focused_row, focused_col)]
        number_to_match = focused_cell.text()

        for c in range(9):
            self._set_cell_bg(self.cells[(focused_row, c)], self.colors["highlight"])
        for r in range(9):
            self._set_cell_bg(self.cells[(r, focused_col)], self.colors["highlight"])

        if number_to_match.isdigit():
            for (r, c), cell_widget in self.cells.items():
                if (r, c) in error_cells:
                    continue
                if cell_widget.text() == number_to_match:
                    self._set_cell_bg(cell_widget, self.colors["number_highlight"])

        self._set_cell_bg(focused_cell, self.colors["focus_highlight"])

    def _set_cell_bg(self, cell_widget, color):
        # Find this cell's position to get its border style
        pos = next((k for k, v in self.cells.items() if v == cell_widget), None)
        border = self.cell_borders.get(pos, "") if pos else ""
        cell_widget.setStyleSheet(f"background-color: {color}; {border}")

    def _create_buttons(self):
        self.button_frame = QFrame()
        self.button_frame.setStyleSheet("background-color: transparent;")
        button_layout = QHBoxLayout(self.button_frame)
        button_layout.setSpacing(8)

        btn_style = """
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #3d5166; }
            QPushButton:pressed { background-color: #1a252f; }
        """

        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(self.controller.show_intro_page)
        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self.solve_puzzle)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_grid)
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.undo)
        redo_button = QPushButton("Redo")
        redo_button.clicked.connect(self.redo)

        for btn in [new_game_button, solve_button, clear_button, undo_button, redo_button]:
            btn.setStyleSheet(btn_style)
            button_layout.addWidget(btn)

    def get_holes_for_difficulty(self, difficulty):
        if difficulty == "Easy":
            return 35
        elif difficulty == "Medium":
            return 51
        elif difficulty == "Hard":
            return 56
        return 40

    def generate_puzzle(self, difficulty):
        board = SudokuGrid()
        solver = SudokuSolver(board)
        solver.solve()

        empty_cells_count = self.get_holes_for_difficulty(difficulty)

        all_cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(all_cells)

        for i in range(empty_cells_count):
            r, c = all_cells[i]
            board.grid[r][c] = 0

        for r in range(9):
            for c in range(9):
                if board.grid[r][c] != 0:
                    self.cells[(r, c)].setReadOnly(True)
                    font = self.cells[(r, c)].font()
                    font.setBold(True)
                    self.cells[(r, c)].setFont(font)
                    border = self.cell_borders.get((r, c), "")
                    self.cells[(r, c)].setStyleSheet(
                        f"background-color: {self.colors['readonly']}; color: #1a252f; {border}"
                    )
                else:
                    self.cells[(r, c)].setReadOnly(False)
                    font = self.cells[(r, c)].font()
                    font.setBold(False)
                    self.cells[(r, c)].setFont(font)
                    border = self.cell_borders.get((r, c), "")
                    self.cells[(r, c)].setStyleSheet(
                        f"background-color: {self.colors['default']}; color: #2e86c1; {border}"
                    )

        self.update_grid_ui(board.grid)
        self.record_state()

    def solve_puzzle(self):
        board = SudokuGrid()
        try:
            for (r, c), cell in self.cells.items():
                val = cell.text()
                board.grid[r][c] = int(val) if val else 0
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Invalid number in grid.")
            return

        solver = SudokuSolver(board)
        if solver.solve():
            self.update_grid_ui(board.grid)
            self.record_state()
        else:
            QMessageBox.critical(self, "Error", "This puzzle cannot be solved.")

    def update_grid_ui(self, grid):
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                if grid[i][j] != 0:
                    cell.setText(str(grid[i][j]))
                else:
                    cell.setText("")

    def record_state(self):
        state = {pos: cell.text() for pos, cell in self.cells.items()}
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
            cell.setText(value)

    def _clear_highlighting(self, exclude_errors=False):
        for pos, cell_widget in self.cells.items():
            if exclude_errors and cell_widget.styleSheet().find(self.colors["error"]) != -1:
                continue
            default_color = self.colors["readonly"] if cell_widget.isReadOnly() else self.colors["default"]
            self._set_cell_bg(cell_widget, default_color)

    def clear_grid(self):
        for pos, cell in self.cells.items():
            if not cell.isReadOnly():
                cell.clear()
        self._validate_and_highlight_errors()
        self.record_state()

    def _validate_and_highlight_errors(self):
        board = [[0] * 9 for _ in range(9)]
        for (r, c), cell in self.cells.items():
            val = cell.text()
            if val.isdigit():
                board[r][c] = int(val)

        error_cells = set()
        for r in range(9):
            for c in range(9):
                num = board[r][c]
                if num == 0:
                    continue

                is_valid = (
                        sum(1 for i in range(9) if board[r][i] == num) == 1 and
                        sum(1 for i in range(9) if board[i][c] == num) == 1 and
                        sum(1 for i in range(3) for j in range(3) if board[r - r % 3 + i][c - c % 3 + j] == num) == 1
                )

                if not is_valid:
                    error_cells.add((r, c))

        for (r, c), cell in self.cells.items():
            if (r, c) in error_cells:
                self._set_cell_bg(cell, self.colors["error"])

        return error_cells


class NumberValidator(QValidator):
    def validate(self, input_str, pos):
        if input_str == "" or (input_str.isdigit() and '1' <= input_str <= '9' and len(input_str) == 1):
            return (QValidator.State.Acceptable, input_str, pos)
        return (QValidator.State.Invalid, input_str, pos)