from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, 
    QPushButton, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont
import sys
from calculator_widget import CalculatorWidget
import random


POSITIONS = [(0, 0), (1, 0), (2, 0), (3, 0)]
prefixes = ["A. ", "B. ", "C. ", "D. "]

class QuestionForm1(QWidget):
    new_question = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.top_labels_layout = QHBoxLayout()

        self.question_title = QLabel("Question Example.........")
        self.time_label = QLabel("Time: 00:00:00")
        self.average_label = QLabel("Average: 00:00:00")
        self.question_count_label = QLabel(f"Question: 0 out of 15")
        self.calculator_container = QWidget()

        self.grid_layout = QGridLayout()
        self.base_size = QSize(800, 600)
        self.answer_buttons = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Math Quest")
        self.resize(self.base_size)
        self.setStyleSheet("background-color: #0d0d0c")

        for label in [self.time_label, self.average_label, self.question_count_label]:
            label.setStyleSheet("color: white; border: 4px solid #2e2e2e; padding: 3px; border-radius: 20px;")
            label.setAlignment(Qt.AlignCenter)
            self.top_labels_layout.addWidget(label)
        self.main_layout.addLayout(self.top_labels_layout)

        self.question_title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.question_title.setStyleSheet("color: white; letter-spacing: 1px; padding-top: 40px;")
        self.main_layout.addWidget(self.question_title)

        self.calculator_container.setStyleSheet(
            "border: 3px solid #111111; background-color: #0E0E0E; color: white; border-radius: 11px"
        )
        container_layout = QVBoxLayout(self.calculator_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        self.calculator = CalculatorWidget()
        container_layout.addWidget(self.calculator)
        self.grid_layout.addWidget(self.calculator_container, 0, 2, 4, 1, alignment=Qt.AlignRight)

        self.show_answer_btn = QPushButton("Show", self)
        self.show_answer_btn.setEnabled(False)
        self.show_answer_btn.clicked.connect(self.show_answer)
        

        self.next_btn = QPushButton("Next", self)
        self.next_btn.clicked.connect(self.next_button)

        self.grid_layout.addWidget(self.next_btn, 3, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.show_answer_btn, 3, 1, alignment=Qt.AlignCenter)

        for pos in POSITIONS:
            btn = QPushButton("", self)
            btn.setStyleSheet(
                """
                QPushButton {
                    border: 2px solid #888888;
                    color: white;
                    padding: 6px;
                    border-radius: 10px;
                    background-color: black;
                    font-weight: bold;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #2e2e2e;
                    border: 2px solid white;
                }
                QPushButton:pressed {
                    background-color: #2e2e2e;
                    border: 5px solid black;
                }
                """
            )
            btn.setMinimumSize(200, 40)
            self.grid_layout.addWidget(btn, *pos, alignment=Qt.AlignLeft)
            btn.clicked.connect(self.user_input)
            self.answer_buttons.append(btn)

        self.main_layout.addLayout(self.grid_layout)

    def load_question(self, question_data):
        self.correct_solution = question_data['solution']
        self.question_title.setText(question_data['question'])
        choices = [question_data['solution']] + question_data['distractors']
        random.shuffle(choices)
        for i, btn in enumerate(self.answer_buttons):
            btn.setText(prefixes[i] + choices[i])
            btn.setProperty("UserAnswer", choices[i])

    def user_input(self):
        sender_button = self.sender()
        if sender_button:
            answer = sender_button.property("UserAnswer")
            new_color = "#3CE217" if answer == self.correct_solution else "#BF0505"
            sender_button.setStyleSheet(
                f"border: 3px solid {new_color}; color: white; padding: 6px; border-radius: 10px; "
                "background-color: black; font-weight: bold; text-align: left;"
            )
            for btn in self.answer_buttons:
                btn.setEnabled(False)
            self.show_answer_btn.setEnabled(True)

    def show_answer(self):
        for btn in self.answer_buttons:
            if btn.property("UserAnswer") == self.correct_solution:
                btn.setStyleSheet(
                f"border: 3px solid #3CE217; color: white; padding: 6px; border-radius: 10px; "
                "background-color: black; font-weight: bold; text-align: left;"
                )
    
    def next_button(self):
        self.new_question.emit("")

    def update_count(self, count_str):
        """Slot to update the question count label."""
        self.question_count_label.setText(f"Question: {count_str} out of 15")
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        width, height = self.size().width(), self.size().height()
        
        self.update_answer_buttons(width, height)
        self.update_navigation_buttons(width, height)
        self.update_labels(width, height)

        self.calculator_container.setFixedSize(int(width * 0.3), int(height * 0.54))
        self.question_title.setFont(QFont("Arial", max(16, int(height * 0.035))))
        self.top_labels_layout.setContentsMargins(
            int(self.base_size.width() * 0.03),
            int(self.base_size.width() * 0.04),
            int(self.base_size.width() * 0.03),
            0
        )
        self.grid_layout.setContentsMargins(
            int(width * 0.03), 0, int(width * 0.03), int(height * 0.05)
        )
        self.grid_layout.setSpacing(int(height * 0.03))

    def update_answer_buttons(self, width, height):
        for btn in self.answer_buttons:
            btn.setFixedSize(int(width * 0.25), int(height * 0.07))
            btn.setFont(QFont("Arial", max(12, int(height * 0.025))))

    def update_navigation_buttons(self, width, height):
        d = int(min(width, height) * 0.09)
        style_template = f"""
            QPushButton {{
                border: 2px solid #888888;
                color: white;
                border-radius: {d//2}px;
                background-color: black;
                font-weight: bold;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: #2e2e2e;
                border: 2px solid white;
            }}
            QPushButton:pressed {{
                background-color: #2e2e2e;
                border: 5px solid black;
            }}
        """
        for btn in [self.next_btn, self.show_answer_btn]:
            btn.setFixedSize(d, d)
            btn.setStyleSheet(style_template)
            btn.setFont(QFont("Arial", int(self.base_size.height() * 0.02)))

    def update_labels(self, width, height):
        for label in [self.time_label, self.average_label, self.question_count_label]:
            label.setFixedSize(int(width * 0.3), int(height * 0.1))
            label.setFont(QFont("Arial", max(10, int(height * 0.022))))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuestionForm1()
    sample_question = {
        "question": "What is 1/2 of 8?",
        "solution": "4",
        "distractors": ["2", "3", "5"]
    }
    window.load_question(sample_question)
    window.show()
    sys.exit(app.exec())

