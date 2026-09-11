from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QFrame, QCompleter, QComboBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor


FEATURE_SUGGESTIONS = [
    "billing", "purchase", "sales", "repair", "inventory",
    "accounting", "customer", "supplier", "dashboard", "service",
    "report", "settings", "auth", "migration", "restaurant",
    "manufacture", "expense", "warranty", "staff", "payment",
    "backup", "navigation", "di", "database", "notification", "kyc",
    "emi", "batch", "quotation", "ledger", "stockmovement",
    "pos", "wholesale", "garments", "healthcare", "media", "sync"
]


class FeatureSearchBar(QWidget):
    extract_requested = Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 2, 0, 8)
        outer.setSpacing(0)

        frame = QFrame()
        frame.setObjectName("searchFrame")

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 6, 8, 6)
        layout.setSpacing(10)

        # Search icon
        icon_lbl = QLabel("🔍")
        icon_lbl.setStyleSheet("font-size: 14px; border: none; background: transparent;")

        # Search input
        self.input_field = QLineEdit()
        self.input_field.setObjectName("searchInput")
        self.input_field.setPlaceholderText("Quick filter & extract feature (e.g. billing, kyc, auth, sync, sales)...")
        self.input_field.returnPressed.connect(self._on_search)

        # Autocomplete
        completer = QCompleter(FEATURE_SUGGESTIONS)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.input_field.setCompleter(completer)

        # Limit Combo
        self.limit_combo = QComboBox()
        self.limit_combo.setObjectName("limitCombo")
        self.limit_combo.setFixedHeight(32)
        self.limit_combo.addItem("Max 20 Files", 20)
        self.limit_combo.addItem("Max 40 Files", 40)
        self.limit_combo.addItem("Max 80 Files", 80)
        self.limit_combo.addItem("Max 150 Files", 150)
        self.limit_combo.setCurrentIndex(1)
        self.limit_combo.setToolTip("File limit threshold for prompt context efficiency")

        # Extract Button
        self.search_btn = QPushButton("🎯 Extract")
        self.search_btn.setObjectName("searchBtn")
        self.search_btn.setFixedHeight(32)
        self.search_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_btn.clicked.connect(self._on_search)

        # Assemble
        layout.addWidget(icon_lbl)
        layout.addWidget(self.input_field, 1)
        layout.addWidget(self.limit_combo)
        layout.addWidget(self.search_btn)

        outer.addWidget(frame)

    def _on_search(self):
        query = self.input_field.text().strip()
        if not query:
            return
        limit = self.get_file_limit()
        self.extract_requested.emit(query, limit)

    def get_file_limit(self) -> int:
        return self.limit_combo.currentData() or 40

    def set_loading(self, is_loading: bool):
        if is_loading:
            self.search_btn.setEnabled(False)
            self.search_btn.setText("⏳ Extracting...")
            self.input_field.setEnabled(False)
        else:
            self.search_btn.setEnabled(True)
            self.search_btn.setText("🎯 Extract")
            self.input_field.setEnabled(True)
            self.input_field.setFocus()