import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QLabel, QComboBox
)


class HermitianTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.size_selector = QComboBox()
        self.size_selector.addItems(["2x2", "3x3"])
        self.size_selector.setCurrentText("3x3")
        self.size_selector.currentTextChanged.connect(self.change_size)

        layout.addWidget(self.size_selector)

        self.grid = QGridLayout()
        layout.addLayout(self.grid)

        self.result_label = QLabel("Eigenvalues:")
        layout.addWidget(self.result_label)

        btn = QPushButton("Compute")
        btn.clicked.connect(self.compute)
        layout.addWidget(btn)

        self.create_matrix(3)

    def create_matrix(self, size):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        self.size = size
        self.inputs = []

        for r in range(size):
            row = []
            for c in range(size):
                box = QLineEdit("0")
                if r == c:
                    box.setStyleSheet("background-color:#1e3a8a;")
                self.grid.addWidget(box, r, c)
                row.append(box)
            self.inputs.append(row)

    def change_size(self, text):
        self.create_matrix(2 if text == "2x2" else 3)

    def compute(self):
        M = np.zeros((self.size, self.size), dtype=complex)

        for i in range(self.size):
            for j in range(self.size):
                try:
                    M[i, j] = complex(self.inputs[i][j].text())
                except:
                    M[i, j] = 0

        M = (M + M.conj().T)/2  # enforce Hermitian
        vals, vecs = np.linalg.eigh(M)

        self.result_label.setText(f"Eigenvalues:\n{vals}")