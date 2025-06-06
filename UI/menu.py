from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QLabel, QGridLayout, 
    QPushButton, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFontDatabase, QFont, QColor

import sys

# List of available topics/specializations for the quiz.
SPECIALIZATIONS = [
    "Fractions", "Mixed Numbers", "Percentages",
    "Geometry", "Ratios && Proportions", "Statistics",
    "Measurement", "Integer Arithmetic", "Exponents",
    "Algebra Basics"
]

# Predefined grid positions for the topic buttons.
POSITIONS = [
    (0, 0), (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2),
    (2, 0), (2, 1), (2, 2),
    (3, 1)
]

class MainMenu(QWidget):
    # Signal emitted when a topic is selected; carries the topic name.
    topicSelected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.title_label = QLabel("Welcome to Mathematics Test\nPick a Topic to Begin.", self)
        self.grid_layout = QGridLayout()
        self.base_size = QSize(800, 650)
        
        self.initUI()

    def initUI(self):
        """Initializes the UI components and applies styles."""
        self.setWindowTitle("Math Quest")
        self.resize(self.base_size)
        self.setMinimumSize(self.base_size)
        self.setStyleSheet("background-color: #0d0d0c;")
        
        # Load custom font if available.
        font_id = QFontDatabase.addApplicationFont("assets/Inter-Medium.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        self.font_family = families[0] if families else "Arial"
        
        # Configure the title label.
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title_label.setStyleSheet("color: white; letter-spacing: 1px; line-height: 1.2;")
        self.main_layout.addWidget(self.title_label)
        
        # Create a button for each specialization at its corresponding grid position.
        for text, pos in zip(SPECIALIZATIONS, POSITIONS):
            btn = QPushButton(text, self)
            btn.setFont(QFont("Arial", 20))
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #888888;
                    color: white;
                    padding: 13px;
                    border-radius: 10px;
                    background-color: black;
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
            # Apply initial glow effect with lower intensity.
            self.apply_glow_effect(btn, 10)
            # Install event filter to handle hover effects.
            btn.installEventFilter(self) 
            # Connect the clicked signal to the button_clicked method, passing the button text.
            btn.clicked.connect(lambda checked, t=text: self.button_clicked(t))
            self.grid_layout.addWidget(btn, *pos)
        
        self.main_layout.addLayout(self.grid_layout)

    def eventFilter(self, obj, event):
        """Handles hover effects for buttons.
        
        Increases glow intensity on mouse enter and resets on mouse leave.
        """
        if isinstance(obj, QPushButton):
            if event.type() == 10:  # MouseEnter event type
                self.apply_glow_effect(obj, 35)
            elif event.type() == 11:  # MouseLeave event type
                self.apply_glow_effect(obj, 10)
        return super().eventFilter(obj, event)

    def apply_glow_effect(self, button, intensity):
        """Applies a white glow effect to the given button.
        
        Args:
            button: The QPushButton to style.
            intensity: The blur radius for the glow effect.
        """
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(intensity)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setColor(QColor(255, 255, 255))
        button.setGraphicsEffect(effect)

    def button_clicked(self, text):
        """Emits the topicSelected signal with the chosen topic text."""
        self.topicSelected.emit(text)

    def resizeEvent(self, event):
        """Handles resizing of the window by updating layout spacing, margins, and button sizes."""
        super().resizeEvent(event)
        window_size = self.size()
        
        self.grid_layout.setSpacing(int(window_size.height() * 0.06))
        self.grid_layout.setContentsMargins(0, 0, 0, int(window_size.height() * 0.13))
        
        # Update the title label font size based on window height.
        self.title_label.setFont(QFont(self.font_family, max(10, int(window_size.height() * 0.03)), QFont.Medium))

        # Loop through each button in the grid and update its size and font.
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.setFixedSize(
                    int(window_size.width() * 0.3),  
                    int(window_size.height() * 0.085)
                )
                widget.setFont(QFont("Arial", max(12, int(window_size.height() * 0.025))))

if __name__ == "__main__":
    # Entry point for the application.
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())








