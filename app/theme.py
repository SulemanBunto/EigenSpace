def apply_dark_theme(app):
    app.setStyleSheet("""
        QWidget {
            background-color: #0f172a;
            color: #e2e8f0;
            font-size: 14px;
        }

        QPushButton {
            background-color: #1e293b;
            border: 1px solid #334155;
            padding: 6px;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: #2563eb;
        }

        QLineEdit {
            background-color: #1e293b;
            border: 1px solid #334155;
            padding: 4px;
            border-radius: 4px;
        }

        QComboBox {
            background-color: #1e293b;
            border: 1px solid #334155;
            padding: 4px;
        }
    """)