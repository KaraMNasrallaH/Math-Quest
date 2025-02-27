# app_controller.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout
from menu import MainMenu
from question_form_1 import QuestionForm1
from fractionsQG import FractionQG

class AppController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Math Quest")
        
        # Use a QStackedWidget to switch between screens
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        
        # Initialize the Main Menu screen
        self.main_menu = MainMenu()
        self.main_menu.topicSelected.connect(self.on_topic_selected)
        self.stack.addWidget(self.main_menu)
        
        # Placeholders for question form and generator
        self.question_form = None
        self.question_generator = None

    def on_topic_selected(self, topic):
        """Handle topic selection from Main Menu."""
        if topic == "Fraction":
            # Create the question form for fractions. This could be one of several forms.
            self.question_form = QuestionForm1()
            # Create the fraction question generator
            self.question_generator = FractionQG()
            question_data = self.question_generator.generate()
            self.question_form.load_question(question_data)

            
            
            # If needed, connect signals between question form and generator here.
            # For example, if your question form has a signal for submission:
            # self.question_form.answerSubmitted.connect(self.handle_submission)
            
            # Add the new widget(s) to the stack and display them.
            self.stack.addWidget(self.question_form)
            self.stack.setCurrentWidget(self.question_form)
        else:
            # Handle other topics similarly
            pass

    # Example handler for when an answer is submitted from the question form
    def handle_submission(self, answer):
        # You could validate the answer here using the question generator,
        # update scores, or display feedback.
        # For example:
        correct_answer = self.question_generator.get_correct_answer()
        if answer == correct_answer:
            print("Correct!")
        else:
            print("Incorrect, try again!")
        # Optionally, move to the next question or screen.
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = AppController()
    controller.show()
    sys.exit(app.exec())
