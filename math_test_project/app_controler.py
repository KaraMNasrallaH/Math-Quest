# app_controller.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import pyqtSignal
from menu import MainMenu
from question_form_1 import QuestionForm1
from fractionsQG import FractionQG
import ctypes

class AppController(QMainWindow):
    counting = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Math Quest")
        self.setStyleSheet("background-color: #0d0d0c")
        
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        
        self.main_menu = MainMenu()
        self.main_menu.topicSelected.connect(self.on_topic_selected)
        self.stack.addWidget(self.main_menu)

        self.question_form = None
        self.question_generator = None
        self.question_data = None
        self.num_of_questions = 15
        self.passed_questions = 0

        self.enable_dark_title_bar()

    def on_topic_selected(self, topic):
        """Handle topic selection from Main Menu."""
        if topic == "Fractions":
            self.question_generator = FractionQG()
        else:
            return
        self.generateQF()
    
    def generateQF(self):
        if self.question_form is not None:
            self.stack.removeWidget(self.question_form)
            self.question_form.deleteLater()
        
        self.question_form = QuestionForm1()
        
        self.counting.connect(self.question_form.update_count)
        
        self.question_data = self.question_generator.generate()
        self.question_form.load_question(self.question_data)
        
        self.stack.addWidget(self.question_form)
        self.stack.setCurrentWidget(self.question_form)
        
        if self.passed_questions == self.num_of_questions:
            self.close()
        self.question_form.new_question.connect(self.generateQF)
        self.passed_questions += 1
        self.counting.emit(str(self.passed_questions))

        
        

            
    def enable_dark_title_bar(self):
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
