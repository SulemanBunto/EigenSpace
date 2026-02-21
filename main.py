import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from app.ui import EigenSpaceApp
from app.theme import apply_dark_theme

if __name__ == "__main__":
    app = QApplication(sys.argv)

    apply_dark_theme(app)

    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    icon_path = os.path.join(base_path, "icon.png")
    app.setWindowIcon(QIcon(icon_path))

    window = EigenSpaceApp()
    window.show()

    sys.exit(app.exec())