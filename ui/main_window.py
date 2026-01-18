import os
import sys
import base64
import traceback

# PySide6 components
try:
    from PySide6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QSplitter,
        QFileDialog, QMessageBox, QLabel, QStatusBar, 
        QHBoxLayout, QFrame, QProgressBar, QDialog, QPushButton
    )
    from PySide6.QtCore import Qt, QSettings, Signal, Slot, QSize, QTimer, QUrl
    from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QFont, QColor, QPalette, QPixmap, QDesktopServices
except ModuleNotFoundError:
    print("PySide6 mising. Run: pip install PySide6")
    sys.exit(1)

# --- CORE LOGIC MODULES ---
try:
    from core.intelligence.role_auditor import RoleAuditor
    from core.intelligence.heatmap_generator import RiskHeatmap
    from core.intelligence.flow_identifier import FlowIdentifier
    from core.intelligence.dependency_alert import DependencyAlert
    from core.summary.executive_summary_v2 import ExecutiveSummaryV2
    from core.scanner import scan_directory
    from core.structure_builder import build_tree_text
    from core.language_profiles import LANGUAGE_PHASES
    from core.ai.prompt_generator import generate_ai_prompt
    from core.git_scanner import GitScanner
    
    # UI Helpers
    from ui.sidebar import PhaseSidebar
    from ui.workspace import Workspace
    from ui.action_bar import ActionBar
    from ui.worker import AnalysisWorker
    from state.app_state import AppState
    from state.output_registry import OutputRegistry

    # --- PYTHON EXTRACTORS ---
    from core.extractors.python.code_exporter import export_python_modules
    from core.extractors.python.ai_code_exporter import export_python_ai_code
    from core.extractors.python.call_graph import export_python_call_graph
    from core.extractors.python.risk_analyzer import analyze_python_risks

    # --- KOTLIN EXTRACTORS (CORRECTED IMPORTS) ---
    # These names now match the definitions in the core files exactly
    from core.extractors.kotlin.code_exporter import export_kotlin_modules
    from core.extractors.kotlin.room_schema_extractor import extract_room_schema
    from core.extractors.kotlin.mermaid_visualizer import generate_mermaid_visuals
    
    # Safe imports for individual Kotlin modules with CORRECT function names
    try:
        from core.extractors.kotlin.call_graph import export_kotlin_call_graph
    except ImportError: pass
    try:
        from core.extractors.kotlin.navigation_graph import export_kotlin_navigation_graph
    except ImportError: pass
    try:
        from core.extractors.kotlin.di_graph_exporter import export_kotlin_di_graph
    except ImportError: pass
    try:
        from core.extractors.kotlin.ui_map_exporter import export_kotlin_ui_map
    except ImportError: pass
    try:
        from core.extractors.kotlin.risk_analyzer import analyze_kotlin_risks
    except ImportError: pass

except ImportError as e:
    print(f"[WARNING] Some modules could not be imported: {e}")
    traceback.print_exc()

# Default QR (Fallback if no file found)
QR_DATA_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAWIAAAFiCAMAAAD7giJIAAAAVFBMVEUfHx/4+v4dHR33+f36/P/8/v8mJib19/suLi7o6u05OTlSUlJFRUbw8vXX2dvh4uVdXV6jpKWwsbO7vL7Oz9LFxsiXmJmNjY5oaWmEhIV8fH1yc3OtGyqdAAAgAElEQVR42uyci6KqrBKANUy0UvN+6f3f83AZUAYIs1p77f/sqbVKRLTPEYZhICrLsiorJnleFJTGXAh78Q/x/58ExQMKUqNKEs4lYcqyE0JjhpoScWQI857bQDf//4NCKbE48E3KSXLEki8DzAgTBpnvALbsk4TA0B2Mye6b8XcqsYODwCbhRYovV2EqU/XufxVFvFfBnmhatPIlxHEj6D/MQcI0flqjRoUmzPJToh9qIpAT8iXI5K+pAZ7tAauA8CaMyseeWMdGAi8VjZzgu6klyIb5x+//X2wpmJfPKclma61ljcc/EoTjzT5RRydJEif8/wGBckQRz7LpnOLb9lBLvCd5kgPn9BcRzLlTuLFA7NsQOU2GouwOSw="

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About AI Context Extractor Pro")
        self.setFixedSize(550, 480)
        self.setStyleSheet("background-color: #121212; color: #e0e0e0; border-radius: 15px;")
        
        layout = QVBoxLayout(self)
        title = QLabel("🚀 AI CONTEXT EXTRACTOR PRO")
        title.setStyleSheet("font-size: 24px; font-weight: 900; color: #4fc3f7; margin-top: 10px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        v_label = QLabel("Version 4.2.1 (Fixed Kotlin Analysis)")
        v_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(v_label, alignment=Qt.AlignCenter)

        desc = QLabel(
            "Ye software Python, Kotlin aur JS projects ko deeply scan karta hai.\n\n"
            "Features:\n"
            "• All Kotlin Phases Restored (DI, Nav, UI Map, etc.)\n"
            "• Custom QR & Support Integration\n"
            "• Crash-Proof Analysis Engine"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 14px; line-height: 22px; margin: 15px; color: #bbb;")
        layout.addWidget(desc)
        
        close_btn = QLabel('<a href="#" style="color:#4fc3f7; text-decoration:none;">[ CLOSE ]</a>')
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.mousePressEvent = lambda e: self.close()
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

class MainWindow(QMainWindow):
    update_output_signal = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 AI Context Extractor Pro")
        self.setMinimumSize(1300, 900)
        self.setAcceptDrops(True)
        
        self.init_ui()
        self.setup_styles()
        self.create_menus()
        
        # 1. Connect Actions
        self.action_bar.language_combo.currentIndexChanged.connect(self.on_language_changed_trigger)
        
        # 2. Connect Worker Signal
        self.update_output_signal.connect(self.on_update_output)

        # 3. Default Setup
        if not AppState.selected_language:
            AppState.selected_language = "kotlin"

        self.update_phases_list()

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #0c0c0c; }
            QStatusBar { background: #007acc; color: white; font-weight: bold; }
            QSplitter::handle { background-color: #2d2d2d; height: 1px; }
            QLabel { color: #dcdcdc; }
        """)

    def create_menus(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #1a1a1a; color: #dcdcdc; border-bottom: 1px solid #333;")
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About Software", self.show_about)

    def show_about(self):
        AboutDialog(self).exec()

    def init_ui(self):
        central = QWidget()
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(central)

        # --- HEADER ---
        self.header_frame = QFrame()
        self.header_frame.setFixedHeight(170)
        self.header_frame.setStyleSheet("background-color: #161616; border-bottom: 1px solid #2d2d2d;")
        
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(25, 10, 25, 10)

        # Left: Title & Actions
        left_box = QVBoxLayout()
        self.proj_title = QLabel("AI CONTEXT EXTRACTOR PRO")
        self.proj_title.setStyleSheet("font-size: 24px; font-weight: 900; color: #4fc3f7;")
        
        self.action_bar = ActionBar(
            select_project_cb=self.select_project,
            export_selected_cb=self.export_selected,
            export_all_cb=self.export_all,
            export_zip_cb=self.export_zip,
            git_toggle_cb=self.refresh_scan
        )
        left_box.addWidget(self.proj_title)
        left_box.addWidget(self.action_bar)
        header_layout.addLayout(left_box, 1)

        # --- RIGHT: SUPPORT CARD (QR & CONTACT) ---
        self.support_card = QFrame()
        self.support_card.setFixedWidth(400)
        self.support_card.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 12px;
                border: 1px solid #333;
            }
        """)
        
        support_layout = QHBoxLayout(self.support_card)
        support_layout.setContentsMargins(15, 12, 15, 12)
        
        # Info Column (Coffee, Contact)
        info_col = QVBoxLayout()
        info_col.setSpacing(6)
        
        lbl_support = QLabel("<b>☕ Support Project</b>")
        lbl_support.setStyleSheet("color: #FFD700; font-size: 15px; border:none;")
        
        # Clickable Link 1 - PAYPAL
        self.btn_coffee = QLabel('<a href="https://paypal.me/raza489991" style="color:#4fc3f7; text-decoration:none;">❤️ Buy Me a Coffee</a>')
        self.btn_coffee.setOpenExternalLinks(True)
        self.btn_coffee.setCursor(Qt.PointingHandCursor)
        self.btn_coffee.setStyleSheet("border:none; font-weight:bold;")

        # Clickable Link 2 - EMAIL
        self.btn_contact = QLabel('<a href="mailto:HASNAINRAZAMEMON9@GMAIL.COM" style="color:#999; text-decoration:none; font-size:11px;">📧 HASNAINRAZAMEMON9@GMAIL.COM</a>')
        self.btn_contact.setOpenExternalLinks(True)
        self.btn_contact.setCursor(Qt.PointingHandCursor)
        self.btn_contact.setStyleSheet("border:none;")

        # Label 3 - MOBILE
        self.btn_mobile = QLabel('<span style="color:#999; font-size:12px;">📞 +91 99258 11505</span>')
        self.btn_mobile.setStyleSheet("border:none;")

        info_col.addWidget(lbl_support)
        info_col.addWidget(self.btn_coffee)
        info_col.addWidget(self.btn_contact)
        info_col.addWidget(self.btn_mobile)
        info_col.addStretch()
        
        # QR Code Image
        self.qr_label = QLabel()
        self.qr_label.setFixedSize(110, 110)
        self.qr_label.setStyleSheet("border: 2px solid #555; background-color: #fff; border-radius: 8px;")
        self.qr_label.setScaledContents(True)
        self.qr_label.setAlignment(Qt.AlignCenter)
        
        self.load_embedded_qr() # Initial Load

        support_layout.addLayout(info_col)
        support_layout.addWidget(self.qr_label)
        
        header_layout.addWidget(self.support_card)
        self.main_layout.addWidget(self.header_frame)

        # --- BODY ---
        self.splitter = QSplitter(Qt.Horizontal)
        self.sidebar = PhaseSidebar()
        self.workspace = Workspace(start_cb=self.start_analysis, open_project_cb=self.select_project)
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.workspace)
        self.splitter.setSizes([260, 1040])
        self.main_layout.addWidget(self.splitter)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def load_embedded_qr(self):
        try:
            img_data = base64.b64decode(QR_DATA_BASE64)
            pix = QPixmap()
            pix.loadFromData(img_data)
            self.qr_label.setPixmap(pix)
        except:
            self.qr_label.setText("QR")

    def load_project_qr(self, folder_path):
        """
        Loads qr.gpg, qr.png, or qr.jpg from the project folder.
        """
        found = False
        possible_files = ["qr.jpg", "qr.png", "qr.jpeg", "qr.gpg"]
        
        for filename in possible_files:
            path = os.path.join(folder_path, filename)
            if os.path.exists(path):
                pix = QPixmap(path)
                if not pix.isNull():
                    self.qr_label.setPixmap(pix)
                    self.status_bar.showMessage(f"Loaded custom QR: {filename}")
                    found = True
                    break
        
        if not found:
            self.load_embedded_qr()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls(): event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        path = event.mimeData().urls()[0].toLocalFile()
        if os.path.isdir(path): self.load_project(path)

    def select_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder: self.load_project(folder)

    def load_project(self, path):
        AppState.project_root = path
        self.proj_title.setText(f"PROJECT: {os.path.basename(path).upper()}")
        self.action_bar.check_git_status(path)
        self.load_project_qr(path)
        self.perform_scan(path, self.action_bar.git_check.isChecked())
        self.workspace.project_loaded()
        self.action_bar.enable_export()
        self.update_phases_list()

    def update_phases_list(self):
        # Base Phases
        phases = [
            "Structure",
            "Architecture Heatmap",
            "Critical Business Flows",
            "Dependency Explosion Audit",
            "Executive Summary 2.0"
        ]
        
        lang = AppState.selected_language or "kotlin"
        lang = lang.lower()

        if "python" in lang:
            phases.extend([
                "Module Classification",
                "Full Source (AI)",
                "Call Graph",
                "Risk Analysis",
                "AI Prompt"
            ])
        elif "kotlin" in lang or "java" in lang:
            # 🔥 RESTORED ALL KOTLIN PHASES HERE
            phases.extend([
                "Module Classification",
                "Full Source (AI)",
                "Database Schema",
                "Visual Architecture (Mermaid)",
                "Call Graph",
                "Navigation Graph",
                "DI Graph",
                "UI Map",
                "Risk Analysis"
            ])
        
        self.current_phases = phases
        self.sidebar.load_phases(phases)

    def on_language_changed_trigger(self, index):
        lang = self.action_bar.language_combo.itemData(index)
        AppState.selected_language = lang
        settings = QSettings("AIProjectExtractor", "App")
        settings.setValue("language", lang)
        
        self.update_phases_list()

        if AppState.project_root:
            self.status_bar.showMessage(f"Re-scanning project for {lang}...")
            self.perform_scan(AppState.project_root, self.action_bar.git_check.isChecked())
            self.status_bar.showMessage(f"Switched to {lang}")

    def refresh_scan(self, use_git_filter):
        if AppState.project_root: self.perform_scan(AppState.project_root, use_git_filter)

    def perform_scan(self, folder, use_git_filter):
        try:
            whitelist = GitScanner.get_changed_files(folder) if use_git_filter else None
            AppState.tree_root = scan_directory(folder, whitelist_files=whitelist)
            
            struct = ""
            if AppState.tree_root:
                struct = "\n".join(build_tree_text(AppState.tree_root))
            else:
                struct = "[WARNING] Project tree is empty."
            
            self.workspace.add_output("Structure", struct)
        except Exception as e:
            err = traceback.format_exc()
            self.workspace.add_output("Scan Error", f"Scan Failed:\n{err}")

    def start_analysis(self):
        self.sidebar.setEnabled(False)
        self.workspace.start_btn.setEnabled(False)
        self.status_bar.showMessage("Running deep analysis...")
        
        phases_to_run = list(self.current_phases)
        
        self.worker = AnalysisWorker(phases_to_run, self.run_phase)
        self.worker.progress.connect(self.workspace.update_progress)
        self.worker.finished.connect(self.on_analysis_finished)
        self.worker.start()

    def run_phase(self, phase):
        root = AppState.tree_root
        lang = AppState.selected_language or "kotlin"
        out = ""

        try:
            # 1. Standard Logic (Language Agnostic)
            metrics = []
            if phase in ["Architecture Heatmap", "Critical Business Flows", "Dependency Explosion Audit", "Executive Summary 2.0"]:
                try:
                    metrics = RoleAuditor.audit_project(root, lang)
                except Exception as e:
                    metrics = [] # Fail gracefully

            if phase == "Structure":
                out = "\n".join(build_tree_text(root))
            elif phase == "Architecture Heatmap":
                out = RiskHeatmap.generate(metrics)
            elif phase == "Critical Business Flows":
                out = FlowIdentifier.format_report(FlowIdentifier.identify_critical_paths(metrics))
            elif phase == "Dependency Explosion Audit":
                out = DependencyAlert.analyze(metrics)
            elif phase == "Executive Summary 2.0":
                violations = RoleAuditor.detect_violations(metrics)
                out = ExecutiveSummaryV2.build(os.path.basename(AppState.project_root or "Project"), metrics, violations)

            # 2. Python Logic
            elif "python" in lang.lower():
                try:
                    if phase == "Module Classification": out = export_python_modules(root)
                    elif phase == "Full Source (AI)": out = export_python_ai_code(root)
                    elif phase == "Call Graph": out = export_python_call_graph(root)
                    elif phase == "Risk Analysis": out = analyze_python_risks(root)
                    elif phase == "AI Prompt": out = generate_ai_prompt("Proj", "python", OutputRegistry._outputs)
                except Exception as e:
                    out = f"Python Analysis Error: {e}"

            # 3. Kotlin Logic - CORRECTED CALLS
            elif "kotlin" in lang.lower() or "java" in lang.lower():
                try:
                    if phase == "Module Classification": 
                        out = export_kotlin_modules(root)
                    elif phase == "Full Source (AI)":
                        # Logic Fix: Use standard module export as fallback for now
                        out = export_kotlin_modules(root)
                    elif phase == "Database Schema": 
                        out = extract_room_schema(root)
                    elif phase == "Visual Architecture (Mermaid)": 
                        out = generate_mermaid_visuals(root)
                    
                    # 🔥 CORRECTED FUNCTION CALLS BELOW
                    elif phase == "Call Graph":
                        try:
                            from core.extractors.kotlin.call_graph import export_kotlin_call_graph
                            out = export_kotlin_call_graph(root)
                        except ImportError: out = "[ERROR] Call Graph module missing or naming error."
                    
                    elif phase == "Navigation Graph":
                        try:
                            from core.extractors.kotlin.navigation_graph import export_kotlin_navigation_graph
                            out = export_kotlin_navigation_graph(root)
                        except ImportError: out = "[ERROR] Nav Graph module missing or naming error."
                    
                    elif phase == "DI Graph":
                        try:
                            from core.extractors.kotlin.di_graph_exporter import export_kotlin_di_graph
                            out = export_kotlin_di_graph(root)
                        except ImportError: out = "[ERROR] DI Graph module missing or naming error."
                    
                    elif phase == "UI Map":
                        try:
                            from core.extractors.kotlin.ui_map_exporter import export_kotlin_ui_map
                            out = export_kotlin_ui_map(root)
                        except ImportError: out = "[ERROR] UI Map module missing or naming error."
                    
                    elif phase == "Risk Analysis":
                        try:
                            from core.extractors.kotlin.risk_analyzer import analyze_kotlin_risks
                            out = analyze_kotlin_risks(root)
                        except ImportError: out = "[ERROR] Risk Analyzer module missing or naming error."

                except Exception as e:
                    out = f"Kotlin Analysis Error: {e}\n{traceback.format_exc()}"

            if not out:
                out = f"[INFO] No data generated for '{phase}'."

        except Exception as e:
            out = f"[FATAL ERROR] Phase '{phase}' crashed:\n{traceback.format_exc()}"

        # Signal result to UI
        self.update_output_signal.emit(phase, out)

    @Slot(str, str)
    def on_update_output(self, phase, content):
        self.workspace.add_output(phase, content)

    def on_analysis_finished(self):
        self.sidebar.setEnabled(True)
        self.workspace.start_btn.setEnabled(True)
        self.status_bar.showMessage("Analysis Complete.")
        if "Executive Summary 2.0" in self.current_phases: 
            self.workspace.phase_selector.setCurrentText("Executive Summary 2.0")

    def export_selected(self):
        path = QFileDialog.getExistingDirectory(self, "Export")
        if path: OutputRegistry.export_selected(path, self.workspace.current_phase())

    def export_all(self):
        path = QFileDialog.getExistingDirectory(self, "Export All")
        if path: OutputRegistry.export_all(path)

    def export_zip(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export ZIP", "context.zip", "ZIP (*.zip)")
        if path: OutputRegistry.export_zip(path)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())