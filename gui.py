from f1_backend import F1DataManager
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget, QVBoxLayout, QComboBox, QLabel
from PySide6.QtCore import Qt

class RaceSimulatorGUI(QMainWindow):

    def __init__ (self):
        super().__init__()

        # Main window properties
        self.setWindowTitle("F1 Race Simulator Dashboard")
        self.resize(1200,700)

        # Sets the splitter as the main widget
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(splitter)

        left_container = QWidget()
        left_layout = QVBoxLayout()
        left_container.setLayout(left_layout)

        right_container = QWidget()
        right_layout = QVBoxLayout()
        right_container.setLayout(right_layout)

        splitter.addWidget(left_container)
        splitter.addWidget(right_container)

        # left_label = QLabel("Left Side")
        # left_layout.addWidget(left_label)
        # left_layout.addStretch()

        # right_label = QLabel("Right Side")
        # right_layout.addWidget(right_label)
        # right_layout.addStretch()

        splitter.setSizes([900, 300]) # Sets the left side to 900 pixels and the right side to 300 pixels
        splitter.setStretchFactor(0 , 3) # Left side gets 3 shares of the space when the window is maximized
        splitter.setStretchFactor(1, 1) # Right side gets 1 share of the space when the window is maximized
        
        # Sets the splitter's colour to white for visibility
        splitter.setHandleWidth(2)
        splitter.setStyleSheet("QSplitter::handle { background-color: white; }")
        
        # Grabs the divider handle between the right and left sides
        handle = splitter.handle(1)

        # Completely disables dragging and clicking on the handle
        handle.setEnabled(False)

if __name__ == "__main__":
    app = QApplication([])      # Initializes the toolkit engine
    window = RaceSimulatorGUI() # Creates your window object
    window.show()               # Makes the window visible on screen
    app.exec()                  # Starts the infinite event loop