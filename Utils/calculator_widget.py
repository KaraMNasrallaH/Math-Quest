from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class CalculatorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_size = QSize(350, 500)  # Default size if not embedded in a parent
        self.initUI()

    def initUI(self):
        # Set up the main grid layout and widget style
        self.layout = QGridLayout(self)
        self.setStyleSheet("background-color: #070708; color: white;")
        self.resize(self.base_size)

        # Create and configure the display field
        self.display = QLineEdit()
        self.display.setStyleSheet("border: 3px solid #111111; border-radius: 7px;")
        self.display.setFixedSize(self.base_size.width(), int(self.base_size.height() * 0.08))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Arial", int(self.base_size.height() * 0.04)))
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display, 0, 0, 1, 4)

        # Define button labels and their grid positions
        buttons = {
            '7': (1, 0), '8': (1, 1), '9': (1, 2), '<': (1, 3),
            '4': (2, 0), '5': (2, 1), '6': (2, 2), '/': (2, 3),
            '1': (3, 0), '2': (3, 1), '3': (3, 2), '*': (3, 3),
            '0': (4, 0), '.': (4, 1), '=': (4, 2), '-': (4, 3),
            'C': (5, 2), '+': (5, 3)
        }

        # Create and style each button, with a special style for "="
        for btnText, pos in buttons.items():
            btn = QPushButton(btnText)
            btn.setFont(QFont("Arial", int(self.base_size.height() * 0.03)))
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #0E0E0E;
                    color: white;
                    padding: 6px;
                    border-radius: 10px;
                    background-color: #070708;
                    font-weight: bold;
                    text-align: middle;
                }
                QPushButton:hover {
                    background-color: #0A0A0A;
                }
                QPushButton:pressed {
                    background-color: #0A0A0A;
                    border: #0C0B0B;
                }
            """)
            if btnText == "=":
                btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #0E0E0E;
                    color: white;
                    padding: 6px;
                    border-radius: 10px;
                    background-color: #9e5103;
                    font-weight: bold;
                    text-align: middle;
                }
                QPushButton:hover {
                    background-color: #d16900;
                }
                QPushButton:pressed {
                    background-color: #d16900;
                    border: #7f3f00;
                }
                """)
            btn.setFixedSize(int(self.base_size.width() * 0.23), int(self.base_size.height() * 0.13))
            self.layout.addWidget(btn, pos[0], pos[1])
            btn.clicked.connect(lambda checked, t=btnText: self.on_button_click(t))
        
        self.justcalculated = False

    def on_button_click(self, button_text):
        if button_text == "=":
            try:
                result = self.calculate(self.display.text())
                result = round(result, 10)
                if result.is_integer():
                    self.display.setText(str(int(result)))
                else:
                    self.display.setText(str(result))
            except ZeroDivisionError:
                self.display.setText("Cannot divide by zero")
            except Exception:
                self.display.setText("Error")
            self.justcalculated = True
            return
        elif button_text == "C":
            self.display.clear()
            return
        elif button_text == "<":
            self.display.setText(self.display.text()[:-1])
            return

        # Clear display if last operation produced an error or final result
        if self.justcalculated:
            if self.display.text() in ["Error", "Cannot divide by zero"] or button_text.isdigit() or button_text == ".":
                self.display.clear()
            self.justcalculated = False

        self.display.setText(self.display.text() + button_text)


    def calculate(self, expression):
        """Tokenize and compute the arithmetic expression."""
        def tokenize(expression):
            tokens = []
            current = ""
            for char in expression:
                if char.isdigit() or char == '.':
                    current += char
                elif char in "+-*/":
                    if current:
                        tokens.append(current)
                        current = ""
                    # Handle negative numbers
                    if char == "-" and (not tokens or tokens[-1] in "+-*/("):
                        current = char
                    else:
                        tokens.append(char)
                else:
                    raise ValueError("Invalid character")
            if current:
                tokens.append(current)
            return tokens

        tokens = tokenize(expression)

        # First pass: handle multiplication and division
        new_tokens = []
        i = 0
        while i < len(tokens):
            if tokens[i] in ['*', '/']:
                operator = tokens[i]
                left = float(new_tokens.pop())
                right = float(tokens[i + 1])
                if operator == '*':
                    new_tokens.append(str(left * right))
                elif right == 0:
                    raise ZeroDivisionError
                else:
                    new_tokens.append(str(left / right))
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1

        # Second pass: handle addition and subtraction
        result = float(new_tokens[0])
        i = 1
        while i < len(new_tokens):
            operator = new_tokens[i]
            next_val = float(new_tokens[i + 1])
            if operator == '+':
                result += next_val
            elif operator == '-':
                result -= next_val
            i += 2

        return result

    def update_sizes(self, new_width, new_height):
        """Update display and button sizes based on new dimensions."""
        self.display.setFont(QFont("Arial", int(new_height * 0.04)))
        self.display.setFixedSize(int(new_width * 0.95), int(new_height * 0.09))
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.setFixedSize(int(new_width * 0.23), int(new_height * 0.13))
                widget.setFont(QFont("Arial", int(new_height * 0.03)))

    def resizeEvent(self, event):
        """Handle widget resizing."""
        super().resizeEvent(event)
        window_size = self.parentWidget().size() if self.parentWidget() else self.size()
        self.update_sizes(window_size.width(), window_size.height())

    def showEvent(self, event):
        """Adjust sizes when the widget is shown (if embedded in a parent)."""
        super().showEvent(event)
        if self.parentWidget():
            parent_size = self.parentWidget().size()
            self.base_size = parent_size
            self.resize(self.base_size)
            self.update_sizes(parent_size.width(), parent_size.height())

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    calculator = CalculatorWidget()
    calculator.show()
    sys.exit(app.exec_())


