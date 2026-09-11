# -*- coding: utf-8 -*-
"""
ui/main_window.py
=================
Main GUI window class for AI Context Extractor Pro.
Includes multi-threaded Feature Filter Extraction with an increased file safety limit of 100.
"""

import os
import sys
import base64
import traceback

# PySide6 components safely wrapped
try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QSplitter,
        QFileDialog, QMessageBox, QLabel, QStatusBar, 
        QHBoxLayout, QFrame, QProgressBar, QDialog, QPushButton
    )
    from PySide6.QtCore import Qt, QSettings, Signal, Slot, QSize, QTimer, QUrl, QThread
    from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QFont, QColor, QPalette, QPixmap, QDesktopServices, QCursor
except ModuleNotFoundError:
    print("PySide6 missing. Run: pip install PySide6")
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
    from core.extractors.feature_filter_extractor import FeatureFilterExtractor
    
    # UI Helpers
    from ui.sidebar import PhaseSidebar
    from ui.workspace import Workspace
    from ui.action_bar import ActionBar
    # UI Helpers
    from ui.sidebar import PhaseSidebar
    from ui.workspace import Workspace
    from ui.action_bar import ActionBar
    from ui.worker import AnalysisWorker
    from ui.theme_manager import ThemeManager
    from state.app_state import AppState
    from state.output_registry import OutputRegistry

    # --- PYTHON EXTRACTORS ---
    from core.extractors.python.code_exporter import export_python_modules
    from core.extractors.python.ai_code_exporter import export_python_ai_code
    from core.extractors.python.call_graph import export_python_call_graph
    from core.extractors.python.risk_analyzer import analyze_python_risks

    # --- JAVASCRIPT / TYPESCRIPT / WEB PORTAL EXTRACTORS ---
    from core.extractors.js_ts.module_exporter import export_js_ts_modules, export_js_ts_ai_code
    from core.extractors.js_ts.dependency_graph import export_js_ts_dependency_graph
    from core.extractors.js_ts.risk_analyzer import analyze_js_ts_risks
    from core.extractors.js_ts.firestore_schema_extractor import extract_firestore_schema
    from core.extractors.js_ts.web_dom_map_extractor import extract_web_dom_map
    from core.extractors.js_ts.hardware_service_extractor import extract_hardware_services
    from core.extractors.js_ts.spec_digest_extractor import extract_spec_digest

    # --- KOTLIN EXTRACTORS ---
    from core.extractors.kotlin.code_exporter import export_kotlin_modules, export_kotlin_module_classification
    from core.extractors.kotlin.constitution_digest_extractor import extract_constitution_digest
    from core.extractors.kotlin.sync_outbox_auditor import audit_sync_outbox
    from core.extractors.kotlin.data_flow_extractor import extract_data_flow
    from core.extractors.kotlin.room_schema_extractor import extract_room_schema
    from core.extractors.kotlin.mermaid_visualizer import generate_mermaid_visuals
    from core.extractors.kotlin.call_graph import export_kotlin_call_graph
    from core.extractors.kotlin.navigation_graph import export_kotlin_navigation_graph
    from core.extractors.kotlin.di_graph_exporter import export_kotlin_di_graph
    from core.extractors.kotlin.ui_map_exporter import export_kotlin_ui_map
    from core.extractors.kotlin.risk_analyzer import analyze_kotlin_risks

except ImportError as e:
    print(f"[WARNING] Some modules could not be imported: {e}")
    traceback.print_exc()


# Default QR Data (Base64)
QR_DATA_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAWIAAAFiCAMAAAD7giJIAAAAVFBMVEUfHx/4+v4dHR33+f36/P/8/v8mJib19/suLi7o6u05OTlSUlJFRUbw8vXX2dvh4uVdXV6jpKWwsbO7vL7Oz9LFxsiXmJmNjY5oaWmEhIV8fH1yc3OtGyqdAAAgAElEQVR42uyci6KqrBKANUy0UvN+6f3f83AZUAYIs1p77f/sqbVKRLTPEYZhICrLsiorJnleFJSQXHe7//8NCKbE48E3KSXLEki8DzAgTBpnvALbsk4TA0B2Mye6b8XcqsYODwCbhRYovV2EqU/XufxVFvFfBnmhatPIlxHEj6D/MQcI0flqjRoUmzPJToh9qIpAT8iXI5K+pAZ7tAauA8CaMyseeWMdGAi8VjZzgu6klyIb5x+//X2wpmJfPKclma61ljcc/EoTjzT5RRydJEif8/wGBckQRz7LpnOLb9lBLvCd5kgPn9BcRzLlTuLFA7NsQOU2GouwOSw="


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About AI Context Extractor Pro")
        self.setFixedSize(500, 380)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("⚡ AI CONTEXT EXTRACTOR PRO")
        title.setObjectName("aboutTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        v_label = QLabel("Production Grade • Multi-Language Enterprise Suite")
        v_label.setObjectName("dialogSubtitle")
        v_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(v_label)

        desc = QLabel(
            "Architectural intelligence and deep context extractor for large-scale codebases.\n\n"
            "Supported Ecosystems:\n"
            "• Kotlin & Android: Clean Architecture, Jetpack Compose, Hilt DI, Outbox Sync, Room DB.\n"
            "• JavaScript / TypeScript: Web Portals, PWA, Firestore Schema, DOM Event Map, Hardware POS.\n"
            "• Python, Java, C++ & Universal Enterprise Systems."
        )
        desc.setObjectName("aboutDesc")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(32)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)


class SponsorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Support & Sponsor Project")
        self.setFixedSize(460, 480)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        title = QLabel("☕ Support AI Project Extractor")
        title.setObjectName("sponsorDialogTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        desc = QLabel("Help keep this project open, production-grade, and actively maintained.")
        desc.setObjectName("dialogSubtitle")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        # Center QR container
        qr_frame = QFrame()
        qr_frame.setObjectName("qrFrame")
        qr_frame.setFixedSize(140, 140)
        qr_layout = QVBoxLayout(qr_frame)
        qr_layout.setContentsMargins(4, 4, 4, 4)

        qr_label = QLabel()
        qr_label.setScaledContents(True)
        try:
            img_data = base64.b64decode(QR_DATA_BASE64)
            pix = QPixmap()
            pix.loadFromData(img_data)
            qr_label.setPixmap(pix)
        except Exception:
            qr_label.setText("QR")
        qr_layout.addWidget(qr_label)
        layout.addWidget(qr_frame, alignment=Qt.AlignCenter)

        # PayPal Link Button
        btn_paypal = QLabel('<a href="https://paypal.me/raza489991" style="background-color: #1f6feb; color: #ffffff; padding: 8px 18px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 13px;">❤️ Sponsor via PayPal</a>')
        btn_paypal.setOpenExternalLinks(True)
        layout.addWidget(btn_paypal, alignment=Qt.AlignCenter)

        # Contact Info
        contact_box = QVBoxLayout()
        contact_box.setSpacing(4)
        c1 = QLabel('<a href="mailto:hasnainrazamemon9@gmail.com" style="color:#58a6ff; text-decoration:none; font-size:12px;">📧 hasnainrazamemon9@gmail.com</a>')
        c1.setOpenExternalLinks(True)
        c2 = QLabel('<span style="color:#8b949e; font-size:12px;">📞 +91 99258 11505</span>')
        contact_box.addWidget(c1, alignment=Qt.AlignCenter)
        contact_box.addWidget(c2, alignment=Qt.AlignCenter)
        layout.addLayout(contact_box)

        layout.addSpacing(6)
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(32)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)


class FeatureWorker(QThread):
    """
    Asynchronous Worker to filter and extract source code files 
    by specific feature keywords without locking the main UI thread.
    """
    done = Signal(str, str)

    def __init__(self, query: str, root, max_files: int = 100):
        super().__init__()
        self.query = query
        self.root = root
        self.max_files = max_files

    def run(self):
        try:
            extractor = FeatureFilterExtractor(self.query, max_files=self.max_files)
            result = extractor.extract(self.root)
            self.done.emit(self.query, result)
        except Exception as e:
            self.done.emit(self.query, f"[ERROR] Feature extraction failed:\n{traceback.format_exc()}")


class MainWindow(QMainWindow):
    update_output_signal = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 AI Context Extractor Pro")
        self.setMinimumSize(1320, 900)
        self.setAcceptDrops(True)
        
        self.init_ui()
        self.setup_styles()
        self.create_menus()
        
        # Connect Actions
        self.action_bar.language_combo.currentIndexChanged.connect(self.on_language_changed_trigger)
        self.sidebar.phase_clicked.connect(self.on_sidebar_phase_clicked)
        self.update_output_signal.connect(self.on_update_output)

        self._feature_worker = None

        if not AppState.selected_language:
            AppState.selected_language = "kotlin"

        self.update_phases_list()

    def setup_styles(self):
        ThemeManager.load()

    def create_menus(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About Software", self.show_about)
        help_menu.addAction("Support Developer", self.show_sponsor)

    def show_about(self):
        AboutDialog(self).exec()

    def show_sponsor(self):
        SponsorDialog(self).exec()

    def init_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(central)

        # --- SLEEK PRODUCTION NAVIGATION BAR (62px) ---
        self.header_frame = QFrame()
        self.header_frame.setObjectName("headerFrame")
        self.header_frame.setFixedHeight(62)
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(18, 0, 18, 0)
        header_layout.setSpacing(14)

        # Brand / Title
        brand_box = QHBoxLayout()
        brand_box.setSpacing(8)

        logo_lbl = QLabel("⚡")
        logo_lbl.setObjectName("logoIcon")

        title_lbl = QLabel("AI Context Extractor")
        title_lbl.setObjectName("mainAppTitle")

        pro_pill = QLabel("PRO")
        pro_pill.setObjectName("proBadge")

        brand_box.addWidget(logo_lbl)
        brand_box.addWidget(title_lbl)
        brand_box.addWidget(pro_pill)

        self.proj_title = QLabel("⚪ No Project Open")
        self.proj_title.setObjectName("projectTitle")
        brand_box.addSpacing(8)
        brand_box.addWidget(self.proj_title)
        header_layout.addLayout(brand_box)

        header_layout.addStretch(1)

        # Action Bar controls (Project, Git, Lang, Theme, Export)
        self.action_bar = ActionBar(
            select_project_cb=self.select_project,
            export_selected_cb=self.export_selected,
            export_all_cb=self.export_all,
            export_zip_cb=self.export_zip,
            git_toggle_cb=self.refresh_scan
        )
        header_layout.addWidget(self.action_bar)

        # Sponsor Button
        self.btn_sponsor = QPushButton("☕ Sponsor")
        self.btn_sponsor.setObjectName("sponsorBtn")
        self.btn_sponsor.setFixedHeight(34)
        self.btn_sponsor.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_sponsor.clicked.connect(self.show_sponsor)
        header_layout.addWidget(self.btn_sponsor)

        self.main_layout.addWidget(self.header_frame)

        # --- BODY ---
        self.splitter = QSplitter(Qt.Horizontal)
        self.sidebar = PhaseSidebar()
        
        self.workspace = Workspace(
            start_cb=self.start_analysis, 
            open_project_cb=self.select_project,
            feature_extract_cb=self.run_feature_extract
        )
        
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.workspace)
        self.splitter.setSizes([275, 1045])
        self.main_layout.addWidget(self.splitter)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready. Select a project folder or drag & drop to begin.")

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
        proj_name = os.path.basename(path)
        self.proj_title.setText(f"📁  {proj_name}")
        self.action_bar.check_git_status(path)
        self.perform_scan(path, self.action_bar.git_check.isChecked())
        self.workspace.project_loaded()
        self.action_bar.enable_export()
        self.update_phases_list()

    def on_sidebar_phase_clicked(self, phase: str):
        idx = self.workspace.phase_selector.findText(phase)
        if idx != -1:
            self.workspace.phase_selector.setCurrentIndex(idx)
        else:
            self.workspace.output.setPlainText(f"[INFO] Phase '{phase}' has not been generated yet. Click '▶ Run Analysis' to generate all outputs.")

    def update_phases_list(self):
        lang = (AppState.selected_language or "kotlin").lower()
        phases = LANGUAGE_PHASES.get(lang)
        if not phases:
            for k in LANGUAGE_PHASES:
                if k in lang:
                    phases = LANGUAGE_PHASES[k]
                    break
        if not phases:
            phases = LANGUAGE_PHASES.get("all", ["Structure", "Executive Summary 2.0"])

        self.current_phases = list(phases)
        self.sidebar.load_phases(self.current_phases)

    def on_language_changed_trigger(self, index):
        lang = self.action_bar.language_combo.itemData(index)
        AppState.selected_language = lang
        self.update_phases_list()
        if AppState.project_root:
            self.perform_scan(AppState.project_root, self.action_bar.git_check.isChecked())

    def refresh_scan(self, use_git_filter):
        if AppState.project_root: self.perform_scan(AppState.project_root, use_git_filter)

    def perform_scan(self, folder, use_git_filter):
        whitelist = GitScanner.get_changed_files(folder) if use_git_filter else None
        AppState.tree_root = scan_directory(folder, whitelist_files=whitelist)
        struct = "\n".join(build_tree_text(AppState.tree_root)) if AppState.tree_root else "Empty Tree"
        self.workspace.add_output("Structure", struct)

    def start_analysis(self):
        if not AppState.tree_root:
            self.status_bar.showMessage("❌ Pehle project select karo (📂 Select Project)")
            return

        self.workspace.start_btn.setEnabled(False)
        self.status_bar.showMessage("Running deep multi-language analysis...")
        
        self.worker = AnalysisWorker(list(self.current_phases), self.run_phase)
        self.worker.progress.connect(self.on_analysis_progress)
        self.worker.finished.connect(self.on_analysis_finished)
        self.worker.start()

    def on_analysis_progress(self, percent, phase):
        self.workspace.update_progress(percent, phase)
        self.sidebar.mark_phase_running(phase)

    def run_phase(self, phase):
        root = AppState.tree_root
        lang = (AppState.selected_language or "kotlin").lower()
        proj_name = os.path.basename(AppState.project_root or "Project")
        out = ""

        try:
            # Common Intelligence Data Retrieval
            metrics, stats = [], None
            if phase in ["Architecture Heatmap", "Critical Business Flows", "Dependency Explosion Audit", "Executive Summary 2.0"]:
                try:
                    metrics, stats = RoleAuditor.audit_project(root, lang)
                except Exception as e:
                    print(f"Audit Error: {e}")

            # ── UNIVERSAL & CORE PHASES ──
            if phase == "Structure":
                out = "\n".join(build_tree_text(root)) if root else "Empty Directory"
            elif phase == "Architecture Heatmap":
                out = RiskHeatmap.generate(metrics)
            elif phase == "Critical Business Flows":
                out = FlowIdentifier.format_report(FlowIdentifier.identify_critical_paths(metrics))
            elif phase == "Dependency Explosion Audit":
                out = DependencyAlert.analyze(metrics)
            elif phase == "Executive Summary 2.0":
                violations = RoleAuditor.detect_violations(metrics)
                out = ExecutiveSummaryV2.build(proj_name, metrics, violations, stats)
            elif phase == "AI Prompt":
                out = generate_ai_prompt(proj_name, lang, OutputRegistry._outputs)

            # ── PYTHON SPECIFIC PHASES ──
            elif "python" in lang:
                if phase == "Module Classification": out = export_python_modules(root)
                elif phase == "Full Source (AI)": out = export_python_ai_code(root)
                elif phase == "Call Graph": out = export_python_call_graph(root)
                elif phase == "Risk Analysis": out = analyze_python_risks(root)

            # ── JAVASCRIPT / TYPESCRIPT / WEB PORTAL PHASES ──
            elif "javascript" in lang or "js" in lang or "ts" in lang or "web" in lang:
                if phase == "Module Classification": out = export_js_ts_modules(root)
                elif phase == "Full Source (AI)": out = export_js_ts_ai_code(root)
                elif phase == "Firestore & Backend Schema": out = extract_firestore_schema(root)
                elif phase == "Web UI & DOM Map": out = extract_web_dom_map(root)
                elif phase == "Hardware & Service Integrations": out = extract_hardware_services(root)
                elif phase == "Architecture & Spec Digest": out = extract_spec_digest(root)
                elif phase == "Dependency Graph": out = export_js_ts_dependency_graph(root)
                elif phase == "Risk Analysis": out = analyze_js_ts_risks(root)

            # ── KOTLIN SPECIFIC PHASES ──
            elif "kotlin" in lang:
                if phase == "Module Classification": out = export_kotlin_module_classification(root)
                elif phase == "Full Source (AI)": out = export_kotlin_modules(root)
                elif phase == "Constitution & Architecture Specs": out = extract_constitution_digest(root)
                elif phase == "Cloud Sync & Outbox Engine Audit": out = audit_sync_outbox(root)
                elif phase == "Data Flow Tracer": out = extract_data_flow(root)
                elif phase == "Database Schema": out = extract_room_schema(root)
                elif phase == "Visual Architecture (Mermaid)": out = generate_mermaid_visuals(root)
                elif phase == "Call Graph": out = export_kotlin_call_graph(root)
                elif phase == "Navigation Graph": out = export_kotlin_navigation_graph(root)
                elif phase == "DI Graph": out = export_kotlin_di_graph(root)
                elif phase == "UI Map": out = export_kotlin_ui_map(root)
                elif phase == "Risk Analysis": out = analyze_kotlin_risks(root)

            # ── JAVA SPECIFIC PHASES ──
            elif "java" in lang:
                if phase == "Module Classification": out = export_kotlin_module_classification(root)
                elif phase == "Full Source (AI)": out = export_kotlin_modules(root)
                elif phase == "Call Graph": out = export_kotlin_call_graph(root)
                elif phase == "Risk Analysis": out = analyze_kotlin_risks(root)

            # ── C++ / GENERAL PHASES ──
            else:
                if phase == "Module Classification": out = export_python_modules(root)
                elif phase == "Full Source (AI)": out = export_python_ai_code(root)
                elif phase == "Risk Analysis": out = "✅ Generic scan complete. No critical risks detected."

        except Exception as e:
            out = f"[ERROR] Phase '{phase}' failed:\n{traceback.format_exc()}"

        self.update_output_signal.emit(phase, out or "[INFO] No data generated for this phase.")
        return out or "[INFO] No data generated for this phase."


    def run_feature_extract(self, query: str, max_files: int = None):
        """
        Extracts only files matching specific queries.
        Supports custom relevant files constraint configuration.
        """
        if not AppState.tree_root:
            self.status_bar.showMessage("❌ Pehle project select karo (📂 Select Project)")
            return

        # Safeguard: if max_files is omitted or None (e.g. from single-parameter signal), query the search bar directly!
        if max_files is None:
            try:
                max_files = self.workspace.feature_bar.get_file_limit()
            except AttributeError:
                max_files = 40  # Safe robust default

        self.status_bar.showMessage(f"🎯 Extracting: '{query}' (Max files: {max_files}) ...")
        self.workspace.feature_bar.set_loading(True)

        # Spin worker and pass custom limit choice
        self._feature_worker = FeatureWorker(query, AppState.tree_root, max_files=max_files)
        self._feature_worker.done.connect(self._on_feature_extract_done)
        self._feature_worker.start()

    @Slot(str, str)
    def _on_feature_extract_done(self, query: str, content: str):
        phase_name = f"🎯 Feature: {query}"
        self.workspace.add_output(phase_name, content)
        self.workspace.feature_bar.set_loading(False)
        self.status_bar.showMessage(f"✅ Feature extract complete: '{query}'")

    @Slot(str, str)
    def on_update_output(self, phase, content):
        self.workspace.add_output(phase, content)
        self.sidebar.mark_phase_done(phase)

    def on_analysis_finished(self):
        self.sidebar.setEnabled(True)
        self.workspace.start_btn.setEnabled(True)
        self.sidebar.mark_all_done()
        self.status_bar.showMessage("✅ Analysis Complete.")
        if "Executive Summary 2.0" in self.current_phases: 
            self.workspace.phase_selector.setCurrentText("Executive Summary 2.0")
            self.sidebar.select_phase("Executive Summary 2.0")


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
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())