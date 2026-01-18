from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, 
    QComboBox, QProgressBar, QCheckBox
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QGuiApplication, QFont
from state.output_registry import OutputRegistry
from ui.widgets import PrimaryButton, SecondaryButton
from core.ai.prompt_templates import PROMPT_TEMPLATES
# 🔥 FIXED IMPORT: Was 'from core.security.sanitizer', now pointing to the file explicitly
from core.security.sanitizer.SecuritySanitizer import SecuritySanitizer

class Workspace(QWidget):
    def __init__(self, start_cb, open_project_cb):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # --- TOP BAR ---
        top = QHBoxLayout()
        
        self.phase_selector = QComboBox()
        self.phase_selector.setMinimumWidth(200)
        self.phase_selector.currentTextChanged.connect(self.load_output)
        
        self.template_selector = QComboBox()
        self.template_selector.setMinimumWidth(180)
        for k in PROMPT_TEMPLATES.keys():
            self.template_selector.addItem(k)
        
        self.safe_mode_cb = QCheckBox("🛡️ Safe Mode")
        self.safe_mode_cb.setChecked(True)
        self.safe_mode_cb.setToolTip("Hide API Keys & Passwords")

        # UX Feature: Word Wrap Toggle
        self.wrap_cb = QCheckBox("Wrap Text")
        self.wrap_cb.setChecked(False)
        self.wrap_cb.stateChanged.connect(self.toggle_wrap)
        
        self.copy_btn = SecondaryButton("📋 Copy w/ Prompt")
        self.copy_btn.clicked.connect(self.copy_output)
        
        top.addWidget(QLabel("Output:"))
        top.addWidget(self.phase_selector, 1)
        top.addWidget(QLabel("Task:"))
        top.addWidget(self.template_selector, 1)
        top.addWidget(self.safe_mode_cb)
        top.addWidget(self.wrap_cb)
        top.addWidget(self.copy_btn)
        
        # --- EDITOR ---
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setLineWrapMode(QTextEdit.NoWrap)
        
        # Set Modern Font
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.Monospace)
        self.output.setFont(font)
        
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #dcdcaa;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 8px;
                selection-background-color: #264f78;
            }
        """)
        
        self.progress = QProgressBar()
        self.progress.setStyleSheet("QProgressBar { height: 4px; border: none; background: #2d2d30; } QProgressBar::chunk { background: #007acc; }")
        
        # --- BOTTOM ACTIONS ---
        bottom = QHBoxLayout()
        self.open_btn = SecondaryButton("📂 Open Project")
        self.open_btn.clicked.connect(open_project_cb)
        
        self.start_btn = PrimaryButton("▶ Run Analysis")
        self.start_btn.clicked.connect(start_cb)
        self.start_btn.setMinimumWidth(150)
        
        bottom.addWidget(self.open_btn)
        bottom.addStretch()
        bottom.addWidget(self.start_btn)
        
        layout.addLayout(top)
        layout.addWidget(self.output, 1)
        layout.addWidget(self.progress)
        layout.addLayout(bottom)
        
    def project_loaded(self):
        self.start_btn.setEnabled(True)

    def add_output(self, phase, content):
        OutputRegistry.add(phase, content)
        if self.phase_selector.findText(phase) == -1:
            self.phase_selector.addItem(phase)
        self.phase_selector.setCurrentText(phase)

    def load_output(self, phase):
        self.output.setPlainText(OutputRegistry.get(phase))

    def toggle_wrap(self, state):
        if self.wrap_cb.isChecked():
            self.output.setLineWrapMode(QTextEdit.WidgetWidth)
        else:
            self.output.setLineWrapMode(QTextEdit.NoWrap)

    def copy_output(self):
        txt = self.output.toPlainText()
        if not txt: return

        if self.safe_mode_cb.isChecked():
            txt = SecuritySanitizer.sanitize(txt)
            
        tmpl = PROMPT_TEMPLATES.get(self.template_selector.currentText(), "{content}")
        final_text = tmpl.format(content=txt)
        
        QGuiApplication.clipboard().setText(final_text)
        
        original_text = self.copy_btn.text()
        self.copy_btn.setText("✅ Copied!")
        self.copy_btn.setStyleSheet("background-color: #2da44e; color: white; border: none; border-radius: 4px;")
        self.copy_btn.setEnabled(False)
        
        QTimer.singleShot(1500, lambda: self._reset_copy_btn(original_text))

    def _reset_copy_btn(self, text):
        self.copy_btn.setText(text)
        self.copy_btn.setEnabled(True)
        self.copy_btn.setStyleSheet("background-color: #3e3e42; color: #e0e0e0; border: 1px solid #505050; border-radius: 4px;")

    def update_progress(self, v, p):
        self.progress.setValue(v)

    def current_phase(self):
        return self.phase_selector.currentText()