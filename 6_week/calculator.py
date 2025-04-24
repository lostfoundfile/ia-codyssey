import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setFixedSize(300, 400)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet('font-size: 30px; padding: 10px;')
        self.layout.addWidget(self.display)

        self.buttons = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        self.button_layout = QGridLayout()
        for row, row_buttons in enumerate(self.buttons):
            for col, btn_text in enumerate(row_buttons):
                if btn_text == '0':
                    button = QPushButton(btn_text)
                    button.setFixedSize(140, 60)
                    self.button_layout.addWidget(button, row + 1, col, 1, 2)
                elif btn_text == '=' and len(row_buttons) == 3:
                    button = QPushButton(btn_text)
                    button.setFixedSize(60, 60)
                    self.button_layout.addWidget(button, row + 1, col + 2)
                else:
                    button = QPushButton(btn_text)
                    button.setFixedSize(60, 60)
                    self.button_layout.addWidget(button, row + 1, col)
                button.clicked.connect(self.handle_input)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def handle_input(self):
        sender = self.sender()
        value = sender.text()

        # 숫자 입력 처리
        if value.isdigit() or value == '.':
            current = self.display.text()
            if current == '0':
                self.display.setText(value)
            else:
                self.display.setText(current + value)

        # 실제 연산 기능은 보너스 과제로 미구현
        # 연산자 처리 및 결과 출력은 추후 구현

        # if value in ['+', '-', '*', '/', '=']:
        #     pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
