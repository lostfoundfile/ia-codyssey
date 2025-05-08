import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QSizePolicy
)


class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current = '0'
        self.operator = None
        self.operand = None
        self.result_shown = False

    def input_digit(self, digit):
        if self.result_shown:
            self.current = digit
            self.result_shown = False
        elif self.current == '0':
            self.current = digit
        else:
            self.current += digit

    def input_dot(self):
        if '.' not in self.current:
            self.current += '.'

    def set_operator(self, operator):
        if self.operator and not self.result_shown:
            self.equal()
        self.operand = float(self.current)
        self.operator = operator
        self.current = '0'

    def equal(self):
        if self.operator is None or self.operand is None:
            return
        try:
            right = float(self.current)
            if self.operator == '+':
                result = self.operand + right
            elif self.operator == '-':
                result = self.operand - right
            elif self.operator == '*':
                result = self.operand * right
            elif self.operator == '/':
                if right == 0:
                    self.current = 'Error'
                    return
                result = self.operand / right

            self.current = self.format_result(result)
            self.result_shown = True
            self.operator = None
            self.operand = None
        except OverflowError:
            self.current = 'Overflow'

    def format_result(self, result):
        if abs(result) > 999999999:
            return 'Overflow'
        return str(round(result, 6)).rstrip('0').rstrip('.') if '.' in str(result) else str(result)

    def toggle_sign(self):
        if self.current.startswith('-'):
            self.current = self.current[1:]
        else:
            self.current = '-' + self.current

    def percent(self):
        try:
            self.current = self.format_result(float(self.current) / 100)
        except:
            self.current = 'Error'

    def get_display(self):
        return self.current


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('계산기')
        self.calculator = Calculator()
        self.create_ui()

    def create_ui(self):
        self.layout = QVBoxLayout()
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setStyleSheet('font-size: 30px;')
        self.display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.display)

        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        grid = QGridLayout()
        for row, row_vals in enumerate(buttons):
            for col, val in enumerate(row_vals):
                button = QPushButton(val)
                button.setFixedSize(80, 60)
                button.setStyleSheet('font-size: 20px;')
                if val == '0':
                    grid.addWidget(button, row + 1, col, 1, 2)
                elif val == '=' and len(row_vals) == 3:
                    grid.addWidget(button, row + 1, col + 1)
                else:
                    grid.addWidget(button, row + 1, col)
                button.clicked.connect(self.on_button_clicked)
        self.layout.addLayout(grid)
        self.setLayout(self.layout)

    def on_button_clicked(self):
        sender = self.sender()
        key = sender.text()

        if key.isdigit():
            self.calculator.input_digit(key)
        elif key == '.':
            self.calculator.input_dot()
        elif key in '+-*/':
            self.calculator.set_operator(key)
        elif key == '=':
            self.calculator.equal()
        elif key == 'C':
            self.calculator.reset()
        elif key == '+/-':
            self.calculator.toggle_sign()
        elif key == '%':
            self.calculator.percent()

        self.update_display()

    def update_display(self):
        value = self.calculator.get_display()
        font_size = self.get_font_size(len(value))
        self.display.setStyleSheet(f'font-size: {font_size}px;')
        self.display.setText(value)

    def get_font_size(self, length):
        if length <= 8:
            return 30
        elif length <= 12:
            return 24
        else:
            return 18


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec_())