"""
feature_search_bar.py
======================
Workspace ke andar ek dedicated search bar widget.
User isme feature/module ka naam likhta hai, file limit choose karta hai aur "Extract" dabata hai.

Is file ko ui/ folder mein rakhein.
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QFrame, QCompleter, QComboBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


# Common feature suggestions (autocomplete ke liye)
FEATURE_SUGGESTIONS = [
    "billing", "purchase", "sales", "repair", "inventory",
    "accounting", "customer", "supplier", "dashboard", "service",
    "report", "settings", "auth", "migration", "restaurant",
    "manufacture", "expense", "warranty", "staff", "payment",
    "backup", "navigation", "di", "database", "notification", "kyc",
    "emi", "batch", "quotation", "ledger", "stockmovement",
    "pos", "wholesale", "garments", "healthcare", "media"
]


class FeatureSearchBar(QWidget):
    """
    Ek standalone search bar widget.
    Signal emit karta hai jab user feature extract karna chahta hai along with file limits.
    """

    # Signal emits: (feature_query: str, max_files: int)
    extract_requested = Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        # Outer frame for visual separation
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 6, 0, 6)
        outer.setSpacing(0)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border: 1px solid #4fc3f7;
                border-radius: 8px;
                padding: 4px;
            }
        """)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 6, 8, 6)
        layout.setSpacing(8)

        # Label
        lbl = QLabel("🎯 Feature Extract:")
        lbl.setStyleSheet("color: #4fc3f7; font-weight: bold; font-size: 13px; border: none;")
        lbl.setFixedWidth(130)

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Feature/module ka naam likho... (e.g. billing, repair, purchase)"
        )
        self.search_input.setFixedHeight(32)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #0d0d1a;
                color: #ffffff;
                border: 1px solid #333355;
                border-radius: 5px;
                padding: 4px 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #4fc3f7;
            }
        """)

        # Autocomplete
        completer = QCompleter(FEATURE_SUGGESTIONS, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.search_input.setCompleter(completer)

        # Enter key se bhi extract ho jaye
        self.search_input.returnPressed.connect(self._on_extract)

        # File limit combobox
        self.limit_combo = QComboBox()
        self.limit_combo.setFixedHeight(32)
        self.limit_combo.setMinimumWidth(105)
        self.limit_combo.setStyleSheet("""
            QComboBox {
                background-color: #0d0d1a;
                color: #ffffff;
                border: 1px solid #333355;
                border-radius: 5px;
                padding: 4px 10px;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 1px solid #4fc3f7;
            }
            QComboBox QAbstractItemView {
                background-color: #1a1a2e;
                color: #ffffff;
                selection-background-color: #4fc3f7;
                selection-color: #000000;
            }
        """)
        # Populate selector ranges (10 to 200 files consent dropdown)
        for num in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]:
            self.limit_combo.addItem(f"{num} Files", num)
        self.limit_combo.setCurrentIndex(3)  # Default index pointing to 40 Files

        # Clear Button
        self.clear_btn = QPushButton("✕")
        self.clear_btn.setFixedSize(28, 28)
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setToolTip("Clear")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #3e3e42;
                color: #aaa;
                border: none;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #555; color: white; }
        """)
        self.clear_btn.clicked.connect(self.search_input.clear)

        # Extract Button
        self.extract_btn = QPushButton("⚡ Extract")
        self.extract_btn.setFixedSize(90, 32)
        self.extract_btn.setCursor(Qt.PointingHandCursor)
        self.extract_btn.setStyleSheet("""
            QPushButton {
                background-color: #4fc3f7;
                color: #000000;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #81d4fa;
            }
            QPushButton:pressed {
                background-color: #0288d1;
                color: white;
            }
        """)
        self.extract_btn.clicked.connect(self._on_extract)

        layout.addWidget(lbl)
        layout.addWidget(self.search_input, 1)
        layout.addWidget(self.limit_combo)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.extract_btn)

        outer.addWidget(frame)

    def _on_extract(self):
        query = self.search_input.text().strip()
        limit = self.limit_combo.currentData()
        if query:
            self.extract_requested.emit(query, limit)

    def get_query(self) -> str:
        return self.search_input.text().strip()

    def get_file_limit(self) -> int:
        """Fallback helper returning selected combobox item data"""
        return self.limit_combo.currentData() or 40

    def set_loading(self, loading: bool):
        """Extract button ko loading state mein dalo"""
        if loading:
            self.extract_btn.setText("⏳ ...")
            self.extract_btn.setEnabled(False)
        else:
            self.extract_btn.setText("⚡ Extract")
            self.extract_btn.setEnabled(True)