from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QTabWidget, QLabel
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from app.controllers.fourier import FourierTab
from app.controllers.hermitian import HermitianTab

class EigenSpaceApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EigenSpace")
        self.resize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        # Background
        self.setObjectName("MainWindow")
        self.setStyleSheet("""
        #MainWindow {
            background-image: url("background_placeholder.jpg");
            background-position: center;
        }
        """)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("logo_placeholder.png")
        logo.setPixmap(pixmap.scaledToHeight(80))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(logo)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(FourierTab(), "Fourier Lab")
        tabs.addTab(HermitianTab(), "Hermitian Playground")

        main_layout.addWidget(tabs)