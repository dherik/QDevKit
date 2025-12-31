#!/usr/bin/env python3
"""
QDevTools - A Qt-based Developer Tools Application
Main entry point
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("QDevTools")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("QDevTools")

    # Enable high DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
