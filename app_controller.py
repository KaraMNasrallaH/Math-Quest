from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

from UI.menu import MainMenu
from UI.question_form_1 import QuestionForm1
from Generators.fractionsQG import FractionQG
from Generators.mixednumbersQG import MixedNumbersQG
from Generators.percentsQG import PercentsQG
from Generators.ratiosQG import RatiosANDProportionQG
from Generators.geometryQG import GeometryQG
from Generators.integer_arithemticQG import Integer_ArithmeticQG
from Generators.exponentsQG import ExponentsQG
from Generators.statisticsQG import StatisticsQG
from Generators.measurementQG import MeasurementQG
from Generators.algbra_basicQG import AlgbraBasicQG

import ctypes
import sys

class AppController(QMainWindow):
    questionCount = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Math Quest")
        self.setStyleSheet("background-color: #0d0d0c")
        self.setWindowIcon(QIcon("assets//icon.png")) 
        
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        
        self.main_menu = MainMenu()
        self.main_menu.topicSelected.connect(self.on_topic_selected)
        self.stack.addWidget(self.main_menu)

        self.current_question_form = None
        self.question_generator = None
        self.question_data = None
        self.total_questions = 15
        self.question_passed = 0

        self.enable_dark_title_bar()

    def on_topic_selected(self, topic):
        """Handle topic selection from Main Menu."""
        if topic == "Fractions":
            self.question_generator = FractionQG()
        elif topic == "Mixed Numbers":
            self.question_generator = MixedNumbersQG()
        elif topic == "Percentages":
            self.question_generator = PercentsQG()
        elif topic == "Ratios && Proportions":
            self.question_generator = RatiosANDProportionQG()
        elif topic == "Geometry":
            self.question_generator = GeometryQG()
        elif topic == "Integer Arithmetic":
            self.question_generator = Integer_ArithmeticQG()
        elif topic == "Exponents":
            self.question_generator = ExponentsQG()
        elif topic == "Statistics":
            self.question_generator = StatisticsQG()
        elif topic == "Measurement":
            self.question_generator = MeasurementQG()
        elif topic == "Algebra Basics":
            self.question_generator = AlgbraBasicQG()
        else:
            return
        self.generate_question_form()
    
    def generate_question_form(self):
        """
        Create a new question form, load a question, update the count,
        and switch the view to the question form.
        """
        if self.current_question_form is not None:
            self.stack.removeWidget(self.current_question_form)
            self.current_question_form.deleteLater()
        
        self.current_question_form = QuestionForm1()
        self.questionCount.connect(self.current_question_form.update_count)
        
        self.question_data = self.question_generator.generate()
        self.current_question_form.load_question(self.question_data)
        
        self.stack.addWidget(self.current_question_form)
        self.stack.setCurrentWidget(self.current_question_form)
        
        if self.question_passed == self.total_questions:
            self.close()
        self.current_question_form.new_question.connect(self.generate_question_form)
        self.question_passed += 1
        self.questionCount.emit(str(self.question_passed))

    def enable_dark_title_bar(self):
        """Enable dark title bar on Windows."""
        if sys.platform == "win32":
            hwnd = int(self.winId())
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 
                ctypes.byref(ctypes.c_int(1)), 4
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = AppController()
    controller.show()
    sys.exit(app.exec())
