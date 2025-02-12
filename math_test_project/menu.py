import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, 
    QPushButton, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont
import ctypes

"""
Global Comments:
This script implements the main menu window for a Mathematics Test project.
It displays a title and a grid of buttons for different specializations.
The layout uses spacer items and stretch factors to dynamically adjust spacing.
A dark-themed title bar is enabled on Windows.
"""

SPECIALIZATIONS = [
    "Fractions", "Mixed Numbers", "Percentages",
    "Geometry", "Ratios && Proportions", "Statistics",
    "Measurement", "Integer Arithmetic", "Exponents",
    "Algebra Basics"
]

POSITIONS = [
    (0, 0), (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2),
    (2, 0), (2, 1), (2, 2),
    (3, 1)
]

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create a central widget and a main vertical layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Title label at the top of the window
        self.title_label = QLabel("Welcome to Mathematics Test\nPick a Topic to Begin.", self)
        
        # Grid layout for specialization buttons
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(50)
        
        self.initUI()
        self.enable_dark_title_bar()

    def initUI(self):
        self.setWindowTitle("Math Quest")
        self.resize(800, 600)
        self.central_widget.setStyleSheet("background-color: #0d0d0c;")
        
        # Load a custom font for the title
        font_id = QFontDatabase.addApplicationFont("Inter-Medium.ttf")
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        # Configure the title label and add it to the main layout
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title_label.setFont(QFont(family, 22, QFont.Medium))
        self.title_label.setStyleSheet("""
            color: white;
            letter-spacing: 1px; 
            line-height: 1.2;
        """)
        self.main_layout.addWidget(self.title_label)
        
        # Add a spacer to allow dynamic adjustment between the title and buttons
        self.main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Create and add buttons to the grid layout
        for text, pos in zip(SPECIALIZATIONS, POSITIONS):
            btn = QPushButton(text, self.central_widget)
            btn.setFont(QFont("Arial", 20))
            btn.setStyleSheet("""
                QPushButton {
                border: 2px solid #888888;
                color: white;
                padding: 13px;
                border-radius: 10px;
                background-color: #1c1c1c;
                font-size: 20px;
                font-weight: bold;
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
            btn.clicked.connect(lambda checked, t=text: self.button_clicked(t))
            self.grid_layout.addWidget(btn, *pos)
        
        # Add the grid layout to the main layout and then add a stretch at the bottom
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addStretch()

    def button_clicked(self, text):
        print(f"{text} button clicked!")

    def enable_dark_title_bar(self):
        # Enable Windows immersive dark mode for the title bar
        hwnd = int(self.winId())
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 
            ctypes.byref(ctypes.c_int(1)), 4
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())






