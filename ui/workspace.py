from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.ai.prompt_templates import PROMPT_TEMPLATES
from core.security.sanitizer.SecuritySanitizer import SecuritySanitizer
from state.output_registry import OutputRegistry
from ui.widgets import PrimaryButton, SecondaryButton


class Workspace(QWidget):
    def __init__(self, start_cb, open_project_cb, feature_extract_cb=None, stop_cb=None):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        # ── 1. FEATURE SEARCH BAR ──
        from ui.feature_search_bar import FeatureSearchBar
        self.feature_bar = FeatureSearchBar()
        if feature_extract_cb:
            self.feature_bar.extract_requested.connect(feature_extract_cb)
        layout.addWidget(self.feature_bar)

        # ── 2. TOP TOOLBAR ──
        top_frame = QFrame()
        top_frame.setObjectName("workspaceTopFrame")
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(12, 6, 12, 6)
        top_layout.setSpacing(10)

        lbl_view = QLabel("Phase:")
        self.phase_selector = QComboBox()
        self.phase_selector.setMinimumWidth(220)
        self.phase_selector.currentTextChanged.connect(self.load_output)

        lbl_task = QLabel("AI Task:")
        self.template_selector = QComboBox()
        self.template_selector.setMinimumWidth(180)
        for k in PROMPT_TEMPLATES.keys():
            self.template_selector.addItem(k)

        self.safe_mode_cb = QCheckBox("🛡️ Safe Sanitizer")
        self.safe_mode_cb.setChecked(True)
        self.safe_mode_cb.setToolTip("Mask API keys, secrets, and private tokens before copy")

        self.wrap_cb = QCheckBox("Wrap Text")
        self.wrap_cb.setChecked(False)
        self.wrap_cb.stateChanged.connect(self.toggle_wrap)

        self.copy_btn = SecondaryButton("📋 Copy with Prompt")
        self.copy_btn.clicked.connect(self.copy_output)

        top_layout.addWidget(lbl_view)
        top_layout.addWidget(self.phase_selector, 1)
        top_layout.addWidget(lbl_task)
        top_layout.addWidget(self.template_selector, 1)
        top_layout.addWidget(self.safe_mode_cb)
        top_layout.addWidget(self.wrap_cb)
        top_layout.addWidget(self.copy_btn)

        layout.addWidget(top_frame)

        # ── 3. CODE EDITOR / VIEWER ──
        self.output = QTextEdit()
        self.output.setObjectName("codeEditor")
        self.output.setReadOnly(True)
        self.output.setLineWrapMode(QTextEdit.NoWrap)

        font = QFont("Cascadia Code", 10)
        if not font.exactMatch():
            font = QFont("Consolas", 10)
        font.setStyleHint(QFont.Monospace)
        self.output.setFont(font)

        layout.addWidget(self.output, 1)

        # ── 4. PROGRESS BAR ──
        self.progress = QProgressBar()
        self.progress.setObjectName("analysisProgress")
        self.progress.setFixedHeight(4)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)

        # ── 5. BOTTOM ACTION CONTROLS ──
        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 4, 0, 0)

        self.meta_label = QLabel("No active project loaded")
        self.meta_label.setObjectName("metaLabel")

        self.start_btn = PrimaryButton("▶  Run Deep Analysis")
        self.start_btn.setObjectName("startBtn")
        self.start_btn.setMinimumWidth(180)
        self.start_btn.clicked.connect(start_cb)

        self.stop_btn = SecondaryButton("⏹  Stop")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setMinimumWidth(90)
        self.stop_btn.setEnabled(False)
        if stop_cb:
            self.stop_btn.clicked.connect(stop_cb)

        bottom.addWidget(self.meta_label)
        bottom.addStretch()
        bottom.addWidget(self.start_btn)
        bottom.addWidget(self.stop_btn)

        layout.addLayout(bottom)

    def project_loaded(self):
        self.start_btn.setEnabled(True)

    def reset_outputs(self):
        OutputRegistry.clear()
        self.phase_selector.blockSignals(True)
        self.phase_selector.clear()
        self.phase_selector.blockSignals(False)
        self.output.clear()
        self.meta_label.setText("No active outputs")
        self.progress.setValue(0)

    def update_progress(self, percent: int, phase_name: str):
        self.progress.setValue(percent)
        self.meta_label.setText(f"Processing ({percent}%): {phase_name}...")

    def add_output(self, phase, content):
        OutputRegistry.add(phase, content)
        if self.phase_selector.findText(phase) == -1:
            self.phase_selector.addItem(phase)
        self.phase_selector.setCurrentText(phase)

    def load_output(self, phase):
        txt = OutputRegistry.get(phase) or ""
        self.output.setPlainText(txt)
        lines = txt.count("\n") + 1 if txt else 0
        size_kb = len(txt.encode('utf-8')) / 1024
        self.meta_label.setText(f"Phase: {phase}  |  {lines:,} lines  |  {size_kb:.1f} KB")

    def toggle_wrap(self, state):
        if self.wrap_cb.isChecked():
            self.output.setLineWrapMode(QTextEdit.WidgetWidth)
        else:
            self.output.setLineWrapMode(QTextEdit.NoWrap)

    def copy_output(self):
        txt = self.output.toPlainText()
        if not txt:
            return

        if self.safe_mode_cb.isChecked():
            txt = SecuritySanitizer.sanitize(txt)

        tmpl = PROMPT_TEMPLATES.get(self.template_selector.currentText(), "{content}")
        final_text = tmpl.format(content=txt)

        QGuiApplication.clipboard().setText(final_text)

        original_text = self.copy_btn.text()
        self.copy_btn.setText("✔ Copied!")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: #ffffff;
                border: 1px solid #2ea043;
                border-radius: 6px;
                font-size: 12.5px;
                font-weight: 600;
                padding: 0 14px;
            }
        """)
        self.copy_btn.setEnabled(False)

        QTimer.singleShot(1600, lambda: self._reset_copy_btn(original_text))

    def _reset_copy_btn(self, text):
        self.copy_btn.setText(text)
        self.copy_btn.setStyleSheet("")
        self.copy_btn.setEnabled(True)
