import sys

# Safe Import
try:
    from PySide6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QSplitter,
        QFileDialog, QMessageBox, QLabel, QStatusBar, QHBoxLayout
    )
    from PySide6.QtCore import Qt, QSettings, Signal, Slot
except ModuleNotFoundError as e:
    raise RuntimeError("PySide6 missing. Run: pip install PySide6") from e

# Core imports
from core.scanner import scan_directory
from core.structure_builder import build_tree_text
from core.language_profiles import LANGUAGE_PHASES
from core.ai.prompt_generator import generate_ai_prompt
from core.git_scanner import GitScanner

# Python extractors
from core.extractors.python.code_exporter import export_python_modules
from core.extractors.python.ai_code_exporter import export_python_ai_code
from core.extractors.python.call_graph import export_python_call_graph
from core.extractors.python.risk_analyzer import analyze_python_risks

# Kotlin extractors
from core.extractors.kotlin.code_exporter import export_kotlin_modules
from core.extractors.kotlin.navigation_graph import export_kotlin_navigation_graph
from core.extractors.kotlin.call_graph import export_kotlin_call_graph
from core.extractors.kotlin.di_graph_exporter import export_kotlin_di_graph
from core.extractors.kotlin.ui_map_exporter import export_kotlin_ui_map
from core.extractors.kotlin.risk_analyzer import analyze_kotlin_risks
from core.extractors.kotlin.room_schema_extractor import extract_room_schema
from core.extractors.kotlin.mermaid_visualizer import generate_mermaid_visuals
from core.extractors.kotlin.data_flow_extractor import extract_data_flow

# JS/TS extractors
from core.extractors.js_ts.module_exporter import export_js_ts_modules
from core.extractors.js_ts.dependency_graph import export_js_ts_dependency_graph
from core.extractors.js_ts.risk_analyzer import analyze_js_ts_risks

# Summary + State
from core.summary.executive_summary import build_executive_summary
from state.app_state import AppState
from state.output_registry import OutputRegistry

# UI
from ui.sidebar import PhaseSidebar
from ui.workspace import Workspace
from ui.action_bar import ActionBar
from ui.worker import AnalysisWorker


class MainWindow(QMainWindow):

    update_output_signal = Signal(str, str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Context Extractor v2.7 (Pro UI)")
        self.resize(1600, 950)
        self.setStyleSheet(
            "QMainWindow { background-color: #1e1e1e; color: #e0e0e0; }"
        )

        self.settings = QSettings("AIProjectExtractor", "App")

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ================= HEADER =================
        header_widget = QWidget()
        header_widget.setStyleSheet(
            "background-color: #252526; border-bottom: 1px solid #3e3e42;"
        )
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # Info row
        info_row = QWidget()
        info_layout = QHBoxLayout(info_row)
        info_layout.setContentsMargins(12, 8, 12, 4)

        self.header_label = QLabel("No project loaded")
        self.header_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #e0e0e0;"
        )

        # 🔥 UPDATED CONTACT DETAILS (FULL)
        self.links_label = QLabel(
            '<a href="https://paypal.me/raza489991" '
            'style="color:#FFD700; text-decoration:none; font-weight:bold;">'
            '☕ Buy me a Coffee</a>'
            '&nbsp;&nbsp;&nbsp;<span style="color:#555;">|</span>&nbsp;&nbsp;&nbsp;'
            '<span style="color:#4ec9b0;">📧 hasnainrazamemon9@gmail.com</span>'
            '&nbsp;&nbsp;&nbsp;<span style="color:#555;">|</span>&nbsp;&nbsp;&nbsp;'
            '<span style="color:#c586c0;">💸 UPI: 9925811505</span>'
        )
        self.links_label.setOpenExternalLinks(True)
        self.links_label.setCursor(Qt.PointingHandCursor)
        self.links_label.setStyleSheet("font-size: 13px;")

        info_layout.addWidget(self.header_label)
        info_layout.addStretch()
        info_layout.addWidget(self.links_label)

        # Action bar
        self.action_bar = ActionBar(
            select_project_cb=self.select_project,
            export_selected_cb=self.export_selected,
            export_all_cb=self.export_all,
            export_zip_cb=self.export_zip,
            git_toggle_cb=self.refresh_scan
        )

        header_layout.addWidget(info_row)
        header_layout.addWidget(self.action_bar)
        layout.addWidget(header_widget)

        # ================= MAIN SPLITTER =================
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(2)
        self.splitter.setStyleSheet(
            "QSplitter::handle { background-color: #3e3e42; }"
        )

        self.sidebar = PhaseSidebar()
        self.workspace = Workspace(
            start_cb=self.start_analysis,
            open_project_cb=self.select_project
        )

        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.workspace)
        self.splitter.setSizes([220, 1380])
        self.splitter.setCollapsible(0, False)

        layout.addWidget(self.splitter)

        # ================= STATUS BAR =================
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(
            "background:#007acc; color:white; font-weight:bold;"
        )
        self.status_bar.showMessage("Ready.")

        self.setCentralWidget(root)

        self.current_phases = []
        self.worker = None

        self.update_output_signal.connect(self.on_update_output)

    # ================= PROJECT =================
    def select_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project")
        if not folder:
            return

        AppState.project_root = folder
        self.action_bar.check_git_status(folder)
        self.perform_scan(folder, False)

        self.header_label.setText(f"📂 Project: {folder}")
        self.workspace.project_loaded()

        self.current_phases = LANGUAGE_PHASES.get(
            AppState.selected_language, ["Structure"]
        )
        self.sidebar.load_phases(self.current_phases)
        self.action_bar.enable_export()

    def refresh_scan(self, use_git_filter):
        if AppState.project_root:
            self.perform_scan(AppState.project_root, use_git_filter)

    def perform_scan(self, folder, use_git_filter):
        whitelist = None
        if use_git_filter:
            whitelist = GitScanner.get_changed_files(folder)
            self.status_bar.showMessage(
                f"Git Mode: {len(whitelist) if whitelist else 0} changed files."
            )
        else:
            self.status_bar.showMessage("Full Scan Mode")

        AppState.tree_root = scan_directory(folder, whitelist_files=whitelist)
        struct = "\n".join(build_tree_text(AppState.tree_root))
        self.workspace.add_output("Structure", struct)

    # ================= ANALYSIS =================
    def start_analysis(self):
        self.sidebar.setEnabled(False)
        self.workspace.start_btn.setEnabled(False)
        self.status_bar.showMessage("Analyzing... Please wait.")

        self.worker = AnalysisWorker(self.current_phases, self.run_phase)
        self.worker.progress.connect(self.workspace.update_progress)
        self.worker.finished.connect(self.on_analysis_finished)
        self.worker.start()

    def run_phase(self, phase):
        root = AppState.tree_root
        lang = AppState.selected_language
        out = ""

        try:
            if lang == "python":
                if phase == "Structure":
                    out = "\n".join(build_tree_text(root))
                elif phase == "Module Classification":
                    out = export_python_modules(root)
                elif phase == "Full Source (AI)":
                    out = export_python_ai_code(root)
                elif phase == "Call Graph":
                    out = export_python_call_graph(root)
                elif phase == "Risk Analysis":
                    out = analyze_python_risks(root)
                elif phase == "AI Prompt":
                    out = generate_ai_prompt(
                        "Proj", "python", OutputRegistry._outputs
                    )

            elif lang == "kotlin":
                if phase == "Structure":
                    out = "\n".join(build_tree_text(root))
                elif phase == "Module Classification":
                    out = export_kotlin_modules(root)
                elif phase == "Database Schema":
                    out = extract_room_schema(root)
                elif phase == "Visual Architecture (Mermaid)":
                    out = generate_mermaid_visuals(root)
                elif phase == "Data Flow Tracer":
                    out = extract_data_flow(root)
                elif phase == "Navigation Graph":
                    out = export_kotlin_navigation_graph(root)
                elif phase == "Call Graph":
                    out = export_kotlin_call_graph(root)
                elif phase == "DI Graph":
                    out = export_kotlin_di_graph(root)
                elif phase == "UI Map":
                    out = export_kotlin_ui_map(root)
                elif phase == "Risk Analysis":
                    out = analyze_kotlin_risks(root)

            elif lang == "javascript":
                if phase == "Structure":
                    out = "\n".join(build_tree_text(root))
                elif phase == "Module Classification":
                    out = export_js_ts_modules(root)
                elif phase == "Dependency Graph":
                    out = export_js_ts_dependency_graph(root)
                elif phase == "Risk Analysis":
                    out = analyze_js_ts_risks(root)

            if not out:
                out = f"[INFO] Phase '{phase}' returned empty or not implemented."

        except Exception as e:
            out = f"[ERROR] {e}"

        self.update_output_signal.emit(phase, out)

    @Slot(str, str)
    def on_update_output(self, phase, content):
        self.workspace.add_output(phase, content)

    def on_analysis_finished(self):
        self.sidebar.setEnabled(True)
        self.workspace.start_btn.setEnabled(True)

        summary = build_executive_summary(
            "Project", AppState.selected_language
        )
        self.workspace.add_output("Executive Summary", summary)
        self.workspace.phase_selector.setCurrentText("Executive Summary")

        self.status_bar.showMessage("Analysis Complete.")
        QMessageBox.information(self, "Success", "Analysis finished!")

    # ================= EXPORT =================
    def export_selected(self):
        path = QFileDialog.getExistingDirectory(self, "Export Selected")
        if path:
            OutputRegistry.export_selected(
                path, self.workspace.current_phase()
            )

    def export_all(self):
        path = QFileDialog.getExistingDirectory(self, "Export All")
        if path:
            OutputRegistry.export_all(path)

    def export_zip(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export ZIP", "context.zip", "ZIP (*.zip)"
        )
        if path:
            OutputRegistry.export_zip(path)
