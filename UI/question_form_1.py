from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, 
    QPushButton, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QFontMetrics

from Utils.calculator_widget import CalculatorWidget

import sys
import random

# Predefined positions for answer buttons on the grid.
POSITIONS = [(0, 0), (1, 0), (2, 0), (3, 0)]
# Prefixes for the answer choices.
prefixes = ["A. ", "B. ", "C. ", "D. "]

class QuestionForm1(QWidget):
    # Signal to request a new question.
    new_question = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        # Layout for top labels (time, average, question count).
        self.top_labels_layout = QHBoxLayout()

        # Initialize UI components.
        self.question_title = QLabel("Question Example.........")
        self.time_label = QLabel("Time: 00:00:00")
        self.average_label = QLabel("Average: 00:00:00")
        self.question_count_label = QLabel("Question: 0 out of 15")
        
        # Container widget for the embedded calculator.
        self.calculator_container = QWidget()

        self.grid_layout = QGridLayout()
        self.base_size = QSize(800, 600)
        # List to store answer buttons.
        self.answer_buttons = []
        self.answer_length = None

        self.initUI()

    def initUI(self):
        """Initializes and arranges UI components."""
        self.setWindowTitle("Math Quest")
        self.resize(self.base_size)
        self.setStyleSheet("background-color: #0d0d0c")

        # Configure and add top labels (time, average, question count).
        for label in [self.time_label, self.average_label, self.question_count_label]:
            label.setStyleSheet("color: white; border: 4px solid #2e2e2e; padding: 3px; border-radius: 20px;")
            label.setAlignment(Qt.AlignCenter)
            self.top_labels_layout.addWidget(label)
        self.main_layout.addLayout(self.top_labels_layout)

        # Set up the question title label.
        self.question_title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.question_title.setStyleSheet("color: white; letter-spacing: 1px; padding-top: 40px;")
        self.main_layout.addWidget(self.question_title)

        # Set up the calculator container.
        self.calculator_container.setStyleSheet(
            "border: 3px solid #111111; background-color: #0E0E0E; color: white; border-radius: 11px"
        )
        container_layout = QVBoxLayout(self.calculator_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        self.calculator = CalculatorWidget()
        container_layout.addWidget(self.calculator)
        self.grid_layout.addWidget(self.calculator_container, 0, 2, 4, 1, alignment=Qt.AlignRight)

        # Create navigation buttons: "Show" to reveal the answer and "Next" for next question.
        self.show_answer_btn = QPushButton("Show", self)
        self.show_answer_btn.setEnabled(False)
        self.show_answer_btn.clicked.connect(self.show_answer)
        
        self.next_btn = QPushButton("Next", self)
        self.next_btn.clicked.connect(self.next_button)

        # Add the navigation buttons to the grid layout.
        self.grid_layout.addWidget(self.next_btn, 3, 1, alignment=Qt.AlignLeft)
        self.grid_layout.addWidget(self.show_answer_btn, 3, 1, alignment=Qt.AlignCenter)

        # Create answer buttons and add them to the grid.
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
        """
        Loads a new question into the form.
        
        Args:
            question_data (dict): Dictionary containing keys 'question', 'solution', and 'distractors'.
        """
        self.correct_solution = question_data['solution']
        self.answer_length = self.find_longest(question_data)
        self.question_title.setText(question_data['question'])
        # Combine the correct answer with distractors and randomize their order.
        choices = [question_data['solution']] + question_data['distractors']
        random.shuffle(choices)
        for i, btn in enumerate(self.answer_buttons):
            btn.setText(prefixes[i] + choices[i])
            btn.setProperty("UserAnswer", choices[i])

    def user_input(self):
        """Handles the user clicking an answer button and updates UI based on correctness."""
        sender_button = self.sender()
        if sender_button:
            answer = sender_button.property("UserAnswer")
            # Set green border if correct, red if incorrect.
            new_color = "#3CE217" if answer == self.correct_solution else "#BF0505"
            sender_button.setStyleSheet(
                f"border: 3px solid {new_color}; color: white; padding: 6px; border-radius: 10px; "
                "background-color: black; font-weight: bold; text-align: left;"
            )
            # Disable all answer buttons after selection.
            for btn in self.answer_buttons:
                btn.setEnabled(False)
            # Enable show button to reveal the correct answer.
            self.show_answer_btn.setEnabled(True)

    def show_answer(self):
        """Highlights the correct answer by updating its style."""
        for btn in self.answer_buttons:
            if btn.property("UserAnswer") == self.correct_solution:
                btn.setStyleSheet(
                    f"border: 3px solid #3CE217; color: white; padding: 6px; border-radius: 10px; "
                    "background-color: black; font-weight: bold; text-align: left;"
                )
    
    def find_longest(self,question_data):
        length = 0
        for key,value in question_data.items():
            if len(value) > length and key != "question":
                length = len(str(value))
        return length

    def next_button(self):
        """Emits the signal to load the next question."""
        self.new_question.emit("")

    def update_count(self, count_str):
        """Method to update the question count label."""
        self.question_count_label.setText(f"Question: {count_str} out of 15")
        
    def resizeEvent(self, event):
        """Handles window resizing by adjusting component sizes and layout margins."""
        super().resizeEvent(event)
        width, height = self.size().width(), self.size().height()
        
        self.update_answer_buttons(width, height)
        self.update_navigation_buttons(width, height)
        self.update_labels(width, height)
        self.update_question_title(width, height)

        # Adjust the calculator container size.
        self.calculator_container.setFixedSize(int(width * 0.3), int(height * 0.54))

        # Update margins for top labels.
        self.top_labels_layout.setContentsMargins(
            int(self.base_size.width() * 0.03),
            int(self.base_size.width() * 0.04),
            int(self.base_size.width() * 0.03),
            0
        )
        # Update margins and spacing for the grid layout.
        self.grid_layout.setContentsMargins(
            int(width * 0.03), 0, int(width * 0.03), int(height * 0.05)
        )
        self.grid_layout.setSpacing(int(height * 0.03))

    def update_answer_buttons(self, width, height):
        """Updates the size and font of answer buttons based on the current window size."""
        for btn in self.answer_buttons:
            btn.setFixedSize(int(width * 0.25), int(height * 0.07))
            btn.setFont(QFont("Arial", min(int(height/30), int((((height/8) - self.answer_length))*0.15))))

    def update_navigation_buttons(self, width, height):
        """Updates the navigation buttons' (Next and Show) size and style."""
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
        """Updates the size and font of the top labels based on the current window size."""
        for label in [self.time_label, self.average_label, self.question_count_label]:
            label.setFixedSize(int(width * 0.3), int(height * 0.1))
            label.setFont(QFont("Arial", max(10, int(height * 0.022))))
    
    def update_question_title(self, width, height):
        # Adjust the question title font size.
        available_width = int(width * 0.9) 
        font = QFont("Arial", 24)
        fm = QFontMetrics(font)
        longest_line = ""
        for line in self.question_title.text().split("\n"):
            if fm.width(line) > fm.width(longest_line):
                longest_line = line
        # Reduce font size until text fits within available width, with a minimum size threshold.
        while fm.width(longest_line) > available_width and font.pointSize() > 10:
            print(fm.width(self.question_title.text()))
            font.setPointSize(font.pointSize() - 1)
            fm = QFontMetrics(font)

        self.question_title.setFont(font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuestionForm1()
    # Sample question data for testing purposes.
    sample_question = {
        "question": "What is 1/2 of 8?",
        "solution": "4",
        "distractors": ["2", "3", "5"]
    }
    window.load_question(sample_question)
    window.show()
    sys.exit(app.exec())


