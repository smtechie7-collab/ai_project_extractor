from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit,
    QHBoxLayout, QComboBox, QProgressBar, QMessageBox, QCheckBox
)
from state.output_registry import OutputRegistry
from ui.widgets import PrimaryButton, SecondaryButton
from core.ai.prompt_templates import PROMPT_TEMPLATES
from core.security.sanitizer import SecuritySanitizer  # 🔥 Import Sanitizer

class Workspace(QWidget):
    def __init__(self, start_cb, open_project_cb):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # ---------- TOP BAR ----------
        top = QHBoxLayout()
        
        # 1. Output Selector
        lbl_out = QLabel("View:")
        lbl_out.setStyleSheet("color: #aaaaaa; font-weight: bold;")
        
        self.phase_selector = QComboBox()
        self.phase_selector.setMinimumWidth(150)
        self.phase_selector.setStyleSheet("""
            QComboBox { padding: 5px; background: #3e3e42; color: white; border: none; border-radius: 4px; }
            QComboBox::drop-down { border: none; }
        """)
        self.phase_selector.currentTextChanged.connect(self.load_output)

        # 2. AI Task Selector
        lbl_task = QLabel("  AI Task:")
        lbl_task.setStyleSheet("color: #4ec9b0; font-weight: bold;")

        self.template_selector = QComboBox()
        self.template_selector.setMinimumWidth(180)
        self.template_selector.setStyleSheet("""
            QComboBox { padding: 5px; background: #252526; color: #4ec9b0; border: 1px solid #3e3e42; border-radius: 4px; }
            QComboBox::drop-down { border: none; }
        """)
        
        # Load templates
        for key in PROMPT_TEMPLATES.keys():
            self.template_selector.addItem(key)

        # 3. Safe Mode Checkbox (NEW)
        self.safe_mode_cb = QCheckBox("🛡️ Safe Mode")
        self.safe_mode_cb.setChecked(True)  # Default ON for safety
        self.safe_mode_cb.setToolTip("Redact API keys, passwords, and emails before copying")
        self.safe_mode_cb.setStyleSheet("""
            QCheckBox { color: #e0e0e0; font-weight: bold; spacing: 5px; }
            QCheckBox::indicator { width: 16px; height: 16px; }
            QCheckBox::indicator:checked { background-color: #007acc; border-radius: 2px; }
            QCheckBox::indicator:unchecked { background-color: #3e3e42; border-radius: 2px; }
        """)

        # 4. Smart Copy Button
        self.copy_btn = SecondaryButton("📋 Copy with Prompt")
        self.copy_btn.clicked.connect(self.copy_output)

        top.addWidget(lbl_out)
        top.addWidget(self.phase_selector, 1)
        top.addWidget(lbl_task)
        top.addWidget(self.template_selector, 1)
        top.addWidget(self.safe_mode_cb) # Added to layout
        top.addWidget(self.copy_btn)

        # ---------- OUTPUT AREA ----------
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 13px;
                padding: 5px;
            }
        """)

        # ---------- PROGRESS ----------
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #2d2d30;
                height: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #007acc;
            }
        """)

        # ---------- BOTTOM ACTIONS ----------
        bottom = QHBoxLayout()
        
        self.open_btn = SecondaryButton("📂 Open Project")
        self.open_btn.clicked.connect(open_project_cb)

        self.start_btn = PrimaryButton("▶ Run Analysis")
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(start_cb)

        bottom.addWidget(self.open_btn)
        bottom.addStretch(1)
        bottom.addWidget(self.start_btn)

        # ---------- ADD TO LAYOUT ----------
        layout.addLayout(top)
        layout.addWidget(self.output, 1)
        layout.addWidget(self.progress)
        layout.addLayout(bottom)

    # ---------- PROJECT ----------
    def project_loaded(self):
        self.start_btn.setEnabled(True)
        self.progress.setValue(0)

    # ---------- OUTPUT ----------
    def add_output(self, phase, content):
        OutputRegistry.add(phase, content)
        if self.phase_selector.findText(phase) == -1:
            self.phase_selector.addItem(phase)
        self.phase_selector.setCurrentText(phase)

    def load_output(self, phase):
        self.output.setPlainText(OutputRegistry.get(phase))

    def copy_output(self):
        """
        Copies content wrapped in the selected AI Template with optional Sanitization
        """
        raw_content = self.output.toPlainText()
        if not raw_content:
            return

        # 1. Run Sanitizer if Safe Mode is ON
        if self.safe_mode_cb.isChecked():
            raw_content = SecuritySanitizer.sanitize(raw_content)
            print("Sanitization applied!") # Debug log

        template_key = self.template_selector.currentText()
        template_str = PROMPT_TEMPLATES.get(template_key, "{content}")

        # 2. Wrap content in Template
        final_text = template_str.format(content=raw_content)

        # 3. Copy to clipboard
        from PySide6.QtGui import QGuiApplication
        QGuiApplication.clipboard().setText(final_text)

        # Feedback
        sanitized_msg = " [SANITIZED]" if self.safe_mode_cb.isChecked() else ""
        if template_key == "📋 Raw (No Prompt)":
            msg = f"Raw output copied!{sanitized_msg}"
        else:
            msg = f"Copied with '{template_key}' instruction!{sanitized_msg}"
            
        print(msg) 
        
        # Visual feedback: select all briefly
        self.output.selectAll()
        # Note: We can't block UI with sleep here, user will see the flash
        cursor = self.output.textCursor()
        cursor.clearSelection()
        self.output.setTextCursor(cursor)

    def current_phase(self):
        return self.phase_selector.currentText()

    def update_progress(self, value: int, phase: str):
        self.progress.setValue(value)