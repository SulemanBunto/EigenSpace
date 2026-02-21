import numpy as np
import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QSlider
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class FourierTab(QWidget):
    def __init__(self):
        super().__init__()

        self.x_min = -np.pi
        self.x_max = np.pi
        self.N_terms = 10
        self.x = np.linspace(self.x_min, self.x_max, 1500)
        self.y_original = np.sin(self.x)

        self.draw_mode = False
        self.drawing = False
        self.last_index = None
        self.pan_mode = False
        self.last_pan = None

        self.init_ui()
        self.compute_coefficients()
        self.update_plot()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.fig = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas)

        self.ax_wave = self.fig.add_subplot(211)
        self.ax_energy = self.fig.add_subplot(212)

        top_buttons_layout = QHBoxLayout()
        self.zoom_in_btn = QPushButton()
        self.zoom_in_btn.setIcon(QIcon(resource_path("assets/zoom_in.png")))
        self.zoom_in_btn.clicked.connect(lambda: self.zoom(0.5))

        self.zoom_out_btn = QPushButton()
        self.zoom_out_btn.setIcon(QIcon(resource_path("assets/zoom_out.png")))
        self.zoom_out_btn.clicked.connect(lambda: self.zoom(2))

        self.pan_btn = QPushButton()
        self.pan_btn.setIcon(QIcon(resource_path("assets/pan.png")))
        self.pan_btn.setCheckable(True)
        self.pan_btn.clicked.connect(self.toggle_pan_mode)

        self.reset_btn = QPushButton()
        self.reset_btn.setIcon(QIcon(resource_path("assets/reset.png")))
        self.reset_btn.clicked.connect(self.reset_plot)

        top_buttons_layout.addWidget(self.zoom_in_btn)
        top_buttons_layout.addWidget(self.zoom_out_btn)
        top_buttons_layout.addWidget(self.pan_btn)
        top_buttons_layout.addWidget(self.reset_btn)
        main_layout.addLayout(top_buttons_layout)

        bottom_layout = QVBoxLayout()
        func_layout = QHBoxLayout()
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Example: x**2 + 2*x + 1")
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_manual_function)
        func_layout.addWidget(QLabel("Enter Function:"))
        func_layout.addWidget(self.function_input)
        func_layout.addWidget(apply_btn)
        bottom_layout.addLayout(func_layout)

        draw_layout = QHBoxLayout()
        self.draw_button = QPushButton("Enable Draw Mode")
        self.draw_button.setCheckable(True)
        self.draw_button.clicked.connect(self.toggle_draw_mode)
        draw_layout.addWidget(self.draw_button)
        bottom_layout.addLayout(draw_layout)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Fourier Terms:"))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(200)
        self.slider.setValue(self.N_terms)
        self.slider.valueChanged.connect(self.slider_changed)
        self.slider_label = QLabel(str(self.N_terms))
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.slider_label)
        bottom_layout.addLayout(slider_layout)

        domain_layout = QHBoxLayout()
        domain_layout.addWidget(QLabel("x min:"))
        self.xmin_box = QLineEdit(str(self.x_min))
        domain_layout.addWidget(self.xmin_box)
        domain_layout.addWidget(QLabel("x max:"))
        self.xmax_box = QLineEdit(str(self.x_max))
        domain_layout.addWidget(self.xmax_box)
        limits_btn = QPushButton("Set Limits")
        limits_btn.clicked.connect(self.set_limits)
        domain_layout.addWidget(limits_btn)
        bottom_layout.addLayout(domain_layout)

        main_layout.addLayout(bottom_layout)

        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("motion_notify_event", self.on_move)
        self.canvas.mpl_connect("button_release_event", self.on_release)

        self.setStyleSheet("""
            QWidget { background-color: #1E2A38; color: #FFFFFF; font-family: Arial; font-size: 13px; }
            QLineEdit { background-color: #2A3A50; color: #FFFFFF; border: 1px solid #3A4A5E; border-radius: 3px; padding: 2px; }
            QPushButton { background-color: #2A3A50; color: #FFFFFF; border: 1px solid #3A4A5E; border-radius: 5px; padding: 5px 10px; }
            QPushButton:hover { background-color: #3A4A6A; }
        """)

    # ===============================
    # Draw & Pan
    # ===============================
    def toggle_draw_mode(self):
        self.draw_mode = self.draw_button.isChecked()
        if self.draw_mode:
            self.pan_mode = False
            self.pan_btn.setChecked(False)
            self.last_pan = None
        self.draw_button.setText("Draw Mode ON" if self.draw_mode else "Enable Draw Mode")

    def toggle_pan_mode(self):
        self.pan_mode = self.pan_btn.isChecked()
        if self.pan_mode:
            self.draw_mode = False
            self.draw_button.setChecked(False)
            self.draw_button.setText("Enable Draw Mode")
        self.last_pan = None

    def slider_changed(self, value):
        self.N_terms = value
        self.slider_label.setText(str(value))
        self.compute_coefficients()
        self.update_plot()

    def apply_manual_function(self):
        text = self.function_input.text()
        try:
            x = self.x
            allowed = {"np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp,
                       "pi": np.pi, "sign": np.sign, "abs": np.abs, "x": x}
            y = eval(text, {"__builtins__": {}}, allowed)
            if isinstance(y, np.ndarray):
                self.y_original = y
                self.compute_coefficients()
                self.update_plot()
        except Exception as e:
            print("Invalid function:", e)

    def on_press(self, event):
        if event.inaxes != self.ax_wave:
            return
        if self.draw_mode:
            self.drawing = True
            self.last_index = None
        elif self.pan_mode:
            self.last_pan = (event.xdata, event.ydata)

    def on_move(self, event):
        if event.inaxes != self.ax_wave:
            return
        if self.draw_mode and self.drawing:
            self._draw(event)
        elif self.pan_mode and self.last_pan is not None:
            dx = event.xdata - self.last_pan[0]
            dy = event.ydata - self.last_pan[1]
            for ax in [self.ax_wave, self.ax_energy]:
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                ax.set_xlim(xlim[0]-dx, xlim[1]-dx)
                ax.set_ylim(ylim[0]-dy, ylim[1]-dy)
            self.last_pan = (event.xdata, event.ydata)
            self.canvas.draw_idle()

    def on_release(self, event):
        if self.draw_mode and self.drawing:
            self.drawing = False
            self.compute_coefficients()
            self.update_plot()
        elif self.pan_mode:
            self.last_pan = None

    def _draw(self, event):
        if event.xdata is None or event.ydata is None:
            return
        idx = (np.abs(self.x - event.xdata)).argmin()
        if self.last_index is not None:
            i1, i2 = self.last_index, idx
            indices = np.linspace(i1, i2, abs(i2-i1)+1, dtype=int)
            y_vals = np.linspace(self.y_original[i1], event.ydata, len(indices))
            self.y_original[indices] = y_vals
        else:
            self.y_original[idx] = event.ydata
        self.last_index = idx
        if self.ax_wave.lines:
            self.ax_wave.lines[0].set_ydata(self.y_original)
        self.canvas.draw_idle()

    def compute_coefficients(self):
        N = self.N_terms
        x = self.x
        y = self.y_original
        L = (self.x_max - self.x_min)/2
        self.a = np.zeros(N+1)
        self.b = np.zeros(N+1)
        self.a[0] = (1/L) * np.trapz(y, x)
        for n in range(1, N+1):
            self.a[n] = (1/L) * np.trapz(y*np.cos(n*np.pi*x/L), x)
            self.b[n] = (1/L) * np.trapz(y*np.sin(n*np.pi*x/L), x)

    def compute_fourier(self):
        x = self.x
        L = (self.x_max - self.x_min)/2
        y = np.full_like(x, self.a[0]/2)
        for n in range(1, self.N_terms+1):
            y += self.a[n]*np.cos(n*np.pi*x/L) + self.b[n]*np.sin(n*np.pi*x/L)
        return y

    def update_plot(self):
        self.ax_wave.clear()
        self.ax_energy.clear()

        y_fourier = self.compute_fourier()
        self.ax_wave.plot(self.x, self.y_original, color="#FFA500")
        self.ax_wave.plot(self.x, y_fourier, linestyle="--", color="#00FFFF")
        self.ax_wave.set_title("Function vs Fourier Approximation")

        energy = self.a**2 + self.b**2
        self.ax_energy.bar(np.arange(len(energy)), energy, color="#4CAF50")
        self.ax_energy.set_title("Energy Spectrum")

        self.fig.tight_layout()
        self.canvas.draw()

    def zoom(self, factor):
        for ax in [self.ax_wave, self.ax_energy]:
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            xmid = (xlim[0]+xlim[1])/2
            ymid = (ylim[0]+ylim[1])/2
            xrange = (xlim[1]-xlim[0])*factor/2
            yrange = (ylim[1]-ylim[0])*factor/2
            ax.set_xlim(xmid - xrange, xmid + xrange)
            ax.set_ylim(ymid - yrange, ymid + yrange)
        self.canvas.draw()

    def set_limits(self):
        try:
            xmin = float(self.xmin_box.text())
            xmax = float(self.xmax_box.text())
            self.x = np.linspace(xmin, xmax, 1500)
            self.compute_coefficients()
            self.update_plot()
        except:
            print("Invalid limits")

    def reset_plot(self):
        self.x = np.linspace(self.x_min, self.x_max, 1500)
        self.y_original = np.sin(self.x)
        self.N_terms = 10
        self.slider.setValue(self.N_terms)
        self.compute_coefficients()
        self.update_plot()