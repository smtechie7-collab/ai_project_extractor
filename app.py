import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.theme_manager import ThemeManager


def main():
    app = QApplication(sys.argv)

    # 🔥 load saved theme BEFORE window
    ThemeManager.load()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
