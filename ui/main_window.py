from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QSplitter,
    QFileDialog, QMessageBox, QLabel
)
from PySide6.QtCore import Qt, QSettings

# ================= CORE =================
from core.scanner import scan_directory
from core.structure_builder import build_tree_text
from core.language_profiles import LANGUAGE_PHASES

# ================= PYTHON =================
from core.extractors.python.code_exporter import export_python_modules
from core.extractors.python.ai_code_exporter import export_python_ai_code

# ================= KOTLIN =================
from core.extractors.kotlin.code_exporter import export_kotlin_modules
from core.extractors.kotlin.navigation_graph import export_kotlin_navigation_graph
from core.extractors.kotlin.call_graph import export_kotlin_call_graph
from core.extractors.kotlin.di_graph_exporter import export_kotlin_di_graph
from core.extractors.kotlin.ui_map_exporter import export_kotlin_ui_map
from core.extractors.kotlin.risk_analyzer import analyze_kotlin_risks

# ================= JS / TS =================
from core.extractors.js_ts.module_exporter import export_js_ts_modules
from core.extractors.js_ts.dependency_graph import export_js_ts_dependency_graph
from core.extractors.js_ts.risk_analyzer import analyze_js_ts_risks

# ================= SUMMARY / GRAPHVIZ =================
from core.summary.executive_summary import build_executive_summary
from core.graphviz.kotlin_di_graph import build_kotlin_di_dot
from core.graphviz.kotlin_ui_graph import build_kotlin_ui_dot

# ================= STATE =================
from state.app_state import AppState
from state.output_registry import OutputRegistry
from state.performance_cache import PerformanceCache

# ================= UI =================
from ui.sidebar import PhaseSidebar
from ui.workspace import Workspace
from ui.action_bar import ActionBar
from ui.worker import AnalysisWorker
from ui.onboarding_dialog import OnboardingDialog


class MainWindow(QMainWindow):
    """
    FINAL MVP MAIN WINDOW
    Stable, audited, crash-free
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Project Extractor — MVP")
        self.resize(1400, 900)

        self.settings = QSettings("AIProjectExtractor", "App")

        # ---------- ROOT ----------
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        # ---------- HEADER ----------
        self.header = QLabel("No project selected")
        self.header.setStyleSheet("font-size:14px;font-weight:600;")
        layout.addWidget(self.header)

        # ---------- ACTION BAR ----------
        self.action_bar = ActionBar(
            select_project_cb=self.select_project,
            export_selected_cb=self.export_selected,
            export_all_cb=self.export_all,
            export_zip_cb=self.export_zip
        )
        layout.addWidget(self.action_bar)

        # ---------- SPLIT ----------
        splitter = QSplitter(Qt.Horizontal)

        self.sidebar = PhaseSidebar()
        self.workspace = Workspace(
            start_cb=self.start_analysis,
            open_project_cb=self.select_project
        )

        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.workspace)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter, 1)
        self.setCentralWidget(root)

        # ---------- STATE ----------
        self.current_phases = []
        self.worker = None
        self.cache = None

        # ---------- ONBOARDING ----------
        if not self.settings.value("onboarding_done", False):
            dlg = OnboardingDialog()
            dlg.exec()

        last_project = self.settings.value("last_project", "")
        if last_project:
            self.header.setText(f"Last Project: {last_project}")

    # ==================================================
    # PROJECT SELECTION
    # ==================================================
    def select_project(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Project Root"
        )
        if not folder:
            return

        self.settings.setValue("last_project", folder)

        OutputRegistry.clear()
        AppState.project_root = folder
        AppState.tree_root = scan_directory(folder)
        self.cache = PerformanceCache(folder)

        self.header.setText(folder)
        self.workspace.project_loaded()

        self.current_phases = LANGUAGE_PHASES.get(
            AppState.selected_language, ["Structure"]
        )

        self.sidebar.load_phases(self.current_phases)
        self.sidebar.unlock()

        structure = "\n".join(build_tree_text(AppState.tree_root))
        self.workspace.add_output("Structure", structure)

        self.action_bar.enable_export()

    # ==================================================
    # ANALYSIS
    # ==================================================
    def start_analysis(self):
        if not self.current_phases:
            QMessageBox.warning(self, "No Project", "Select a project first.")
            return

        self.worker = AnalysisWorker(
            self.current_phases,
            self.run_phase
        )
        self.worker.progress.connect(self.workspace.update_progress)
        self.worker.finished.connect(self.on_analysis_finished)
        self.worker.start()

    # ==================================================
    # 🔥 FULL PHASE HANDLER (NO MISSING BRANCHES)
    # ==================================================
    def run_phase(self, phase: str):
        lang = AppState.selected_language
        root = AppState.tree_root

        # ---------- PYTHON ----------
        if lang == "python":
            if phase == "Structure":
                output = "\n".join(build_tree_text(root))

            elif phase == "Module Classification":
                output = export_python_modules(root)

            elif phase == "Full Source (AI)":
                output = export_python_ai_code(root)

            else:
                output = f"{phase} not supported for Python."

        # ---------- KOTLIN ----------
        elif lang == "kotlin":
            if phase == "Structure":
                output = "\n".join(build_tree_text(root))

            elif phase == "Module Classification":
                output = export_kotlin_modules(root)

            elif phase == "Navigation Graph":
                output = export_kotlin_navigation_graph(root)

            elif phase == "Call Graph":
                output = export_kotlin_call_graph(root)

            elif phase == "DI Graph":
                output = export_kotlin_di_graph(root)

            elif phase == "UI Map":
                output = export_kotlin_ui_map(root)

            elif phase == "Risk Analysis":
                output = analyze_kotlin_risks(root)

            else:
                output = f"{phase} not supported for Kotlin."

        # ---------- JS / TS ----------
        elif lang == "javascript":
            if phase == "Structure":
                output = "\n".join(build_tree_text(root))

            elif phase == "Module Classification":
                output = export_js_ts_modules(root)

            elif phase == "Dependency Graph":
                output = export_js_ts_dependency_graph(root)

            elif phase == "Risk Analysis":
                output = analyze_js_ts_risks(root)

            else:
                output = f"{phase} not supported for JS/TS."

        else:
            output = f"{phase} not supported."

        self.workspace.add_output(phase, output)
        self.sidebar.mark_done(self.current_phases.index(phase))

    # ==================================================
    # FINISH
    # ==================================================
    def on_analysis_finished(self):
        summary = build_executive_summary(
            project_name=self.header.text(),
            language=AppState.selected_language
        )
        self.workspace.add_output("Executive Summary", summary)

        if AppState.selected_language == "kotlin":
            self.workspace.add_output(
                "DI Graph (.dot)",
                build_kotlin_di_dot(AppState.tree_root)
            )
            self.workspace.add_output(
                "UI Graph (.dot)",
                build_kotlin_ui_dot(AppState.tree_root)
            )

        if self.cache:
            self.cache.save()

    # ==================================================
    # EXPORT
    # ==================================================
    def export_selected(self):
        phase = self.workspace.current_phase()
        if not phase:
            return

        folder = QFileDialog.getExistingDirectory(self, "Export Folder")
        if not folder:
            return

        OutputRegistry.export_selected(folder, phase)

    def export_all(self):
        folder = QFileDialog.getExistingDirectory(self, "Export Folder")
        if not folder:
            return

        OutputRegistry.export_all(folder)

    def export_zip(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save ZIP", "analysis_outputs.zip", "ZIP (*.zip)"
        )
        if not path:
            return

        OutputRegistry.export_zip(path)
