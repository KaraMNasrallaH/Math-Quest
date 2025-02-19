from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, 
    QPushButton, QSizePolicy, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
import sys
import ctypes

POSITIONS = [(0, 0), (1, 0), (2, 0), (3, 0)]
answers = ["A. ", "B. ", "C. ", "D. "]

class QuestionForm1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.top_labels_layout = QHBoxLayout()

        # Initialize widgets
        self.question_title = QLabel("Question Example.........")
        self.time_label = QLabel("Time: 00:00:00")
        self.average_label = QLabel("Average: 00:00:00")
        self.question_count_label = QLabel("Question: 0 out of 30")
        self.calculator_label = QLabel()

        self.grid_layout = QGridLayout()
        self.base_size = QSize(800, 600)  # Reference size for scaling
        self.initUI()
        self.enable_dark_title_bar()

    def initUI(self):

        self.grid_layout.setSpacing(int(self.base_size.height() * 0.03))  # 3% of window height
        
        # Set margins for padding between the buttons and the screen (left and down)
        self.grid_layout.setContentsMargins(
            int(self.base_size.width() * 0.03),   # left
            0,                                    # top
            int(self.base_size.width() * 0.03),   # right
            int(self.base_size.height() * 0.05)   # bottom
        )

        self.setWindowTitle("Math Quest")
        self.resize(self.base_size)
        self.setStyleSheet("background-color: #0d0d0c")

        # Configure top labels
        for label in [self.time_label, self.average_label, self.question_count_label]:
            label.setFont(QFont("Arial", int(self.base_size.height() * 0.02)))  # 2% of window height
            label.setStyleSheet(f"color: white; border: 4px solid #2e2e2e; padding: 3px; border-radius: 20px;")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(
                int(self.base_size.width() * 0.3),   # 30% of window width
                int(self.base_size.height() * 0.1)   # 10% of window height
            )
        
            self.top_labels_layout.addWidget(label)

        self.top_labels_layout.setContentsMargins(
        int(self.base_size.width() * 0.03),   # left
        int(self.base_size.width() * 0.04),   # top
        int(self.base_size.width() * 0.03),   # right
        0
        )
        
        self.main_layout.addLayout(self.top_labels_layout)

        # Configure question title
        self.question_title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.question_title.setFont(QFont("Arial", int(self.base_size.height() * 0.035)))
        self.question_title.setStyleSheet("""
            color: white;
            letter-spacing: 1px;
            padding-top: 40px;
            line-height: 1.2;""")
        self.main_layout.addWidget(self.question_title)

        # Configure calculator
        self.calculator_label.setStyleSheet(
            "border: 2px solid #2e2e2e; background-color: #121212; color: white; border-radius: 11px")
        self.grid_layout.addWidget(self.calculator_label, 0, 2, 4, 1, alignment=Qt.AlignRight)

        # Create answer buttons
        for pos, answer in zip(POSITIONS, answers):
            btn = QPushButton(answer, self.central_widget)
            btn.setFont(QFont("Arial", int(self.base_size.height() * 0.03)))
            btn.setStyleSheet("""
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
                    background-color: #444444;
                    border: 5px solid #121111;
                }
            """)
            btn.setMinimumSize(150, 40)  # Minimum size for readability
            self.grid_layout.addWidget(btn, *pos, alignment=Qt.AlignLeft)

        self.main_layout.addLayout(self.grid_layout)

    def resizeEvent(self, event):
        """Handle dynamic scaling when window is resized"""
        super().resizeEvent(event)
        window_size = self.size()
        
        # update button sizes
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.setFixedSize(
                    int(window_size.width() * 0.2),   # 20% of window width
                    int(window_size.height() * 0.07)   # 7% of window height
                )
                widget.setFont(QFont("Arial", max(12, int(window_size.height() * 0.025))))

        # update calculator size
        self.calculator_label.setFixedSize(
            int(window_size.width() * 0.3),   # 30% of window width
            int(window_size.height() * 0.54)   # 54% of window height
        )
        
        # update top labels
        for label in [self.time_label, self.average_label, self.question_count_label]:
            label.setFixedSize(
                int(window_size.width() * 0.3),   # 30% of window width
                int(window_size.height() * 0.1)   # 10% of window height
            )
            label.setFont(QFont("Arial", max(10, int(window_size.height() * 0.022))))
            

        # update top labels padding
        self.top_labels_layout.setContentsMargins(
        int(self.base_size.width() * 0.03),   # left
        int(self.base_size.width() * 0.04),   # top
        int(self.base_size.width() * 0.03),   # right
        0                                     # buttom
        )

        # update question title font
        self.question_title.setFont(QFont("Arial", max(16, int(window_size.height() * 0.035))))

        # update grid layout padding
        self.grid_layout.setContentsMargins(
            int(window_size.width() * 0.03),  # left
            0,                                # top
            int(window_size.width() * 0.03),  # right
            int(window_size.height() * 0.05)  # bottom
        )
        self.grid_layout.setSpacing(int(window_size.height() * 0.03))

    def enable_dark_title_bar(self):
        hwnd = int(self.winId())
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 
            ctypes.byref(ctypes.c_int(1)), 4
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuestionForm1()
    window.show()
    sys.exit(app.exec())
