import sys
import subprocess
import os

# ============================================================
# AUTO INSTALLER
# ============================================================

def ensure_pyside6():
    try:
        import PySide6  # noqa
        return
    except ModuleNotFoundError:
        print("\n[BOOTSTRAP] PySide6 not found.")
        print("[BOOTSTRAP] Installing PySide6 automatically...\n")

        try:
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "pip"
            ])

            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                "PySide6"
            ])
        except Exception as e:
            print("\n[FATAL] Automatic install failed.")
            print("Reason:", e)
            print("\nRun this manually:")
            print("  python -m pip install PySide6")
            sys.exit(1)

        print("\n[BOOTSTRAP] PySide6 installed successfully.")
        print("[BOOTSTRAP] Restarting application...\n")

        os.execv(sys.executable, [sys.executable] + sys.argv)

# ============================================================
# ENTRY
# ============================================================

def main():
    ensure_pyside6()

    from PySide6.QtWidgets import QApplication
    from ui.main_window import MainWindow
    from ui.theme_manager import ThemeManager

    app = QApplication(sys.argv)

    try:
        ThemeManager.load()
    except Exception as e:
        print("[WARN] Theme load failed:", e)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
