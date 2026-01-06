# ==================================================
# SAFE QT IMPORT
# ==================================================
try:
    from PySide6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QSplitter,
        QFileDialog, QMessageBox, QLabel, QStatusBar
    )
    from PySide6.QtCore import Qt, QSettings
except ModuleNotFoundError as e:
    raise RuntimeError(
        "PySide6 is REQUIRED.\n"
        "Install it using:\n\n"
        "python -m pip install PySide6"
    ) from e

# ================= CORE IMPORTS =================
from core.scanner import scan_directory
from core.structure_builder import build_tree_text
from core.language_profiles import LANGUAGE_PHASES
from core.ai.prompt_generator import generate_ai_prompt
from core.git_scanner import GitScanner

# ================= EXTRACTORS =================
from core.extractors.python.code_exporter import export_python_modules
from core.extractors.python.ai_code_exporter import export_python_ai_code
from core.extractors.python.call_graph import export_python_call_graph
from core.extractors.python.risk_analyzer import analyze_python_risks

from core.extractors.kotlin.code_exporter import export_kotlin_modules
from core.extractors.kotlin.navigation_graph import export_kotlin_navigation_graph
from core.extractors.kotlin.call_graph import export_kotlin_call_graph
from core.extractors.kotlin.di_graph_exporter import export_kotlin_di_graph
from core.extractors.kotlin.ui_map_exporter import export_kotlin_ui_map
from core.extractors.kotlin.risk_analyzer import analyze_kotlin_risks
from core.extractors.kotlin.room_schema_extractor import extract_room_schema
from core.extractors.kotlin.mermaid_visualizer import generate_mermaid_visuals
from core.extractors.kotlin.data_flow_extractor import extract_data_flow

from core.extractors.js_ts.module_exporter import export_js_ts_modules
from core.extractors.js_ts.dependency_graph import export_js_ts_dependency_graph
from core.extractors.js_ts.risk_analyzer import analyze_js_ts_risks

# ================= STATE =================
from core.summary.executive_summary import build_executive_summary
from state.app_state import AppState
from state.output_registry import OutputRegistry
from state.performance_cache import PerformanceCache

# ================= UI =================
from ui.sidebar import PhaseSidebar
from ui.workspace import Workspace
from ui.action_bar import ActionBar
from ui.worker import AnalysisWorker

# ================= STYLE =================
DARK_STYLESHEET = """
QMainWindow { background-color: #1e1e1e; color: #e0e0e0; }
QLabel { color: #e0e0e0; font-size: 13px; }
QSplitter::handle { background-color: #3e3e42; height: 2px; }
QStatusBar { background-color: #007acc; color: white; font-weight: bold; }
QMessageBox { background-color: #2d2d30; color: white; }
"""

# ==================================================
# MAIN WINDOW
# ==================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Context Extractor v2.4")
        self.resize(1400, 950)
        self.setStyleSheet(DARK_STYLESHEET)

        self.settings = QSettings("AIProjectExtractor", "App")

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)

        self.header = QLabel("No project loaded")
        self.header.setStyleSheet("font-size:15px;font-weight:bold;color:#4ec9b0;")

        self.action_bar = ActionBar(
            select_project_cb=self.select_project,
            export_selected_cb=self.export_selected,
            export_all_cb=self.export_all,
            export_zip_cb=self.export_zip,
            git_toggle_cb=self.refresh_scan
        )

        layout.addWidget(self.header)
        layout.addWidget(self.action_bar)

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

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.setCentralWidget(root)

        self.current_phases = []
        self.worker = None
        self.cache = None

    # ==================================================
    # PROJECT
    # ==================================================
    def select_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Root")
        if not folder:
            return

        OutputRegistry.clear()
        AppState.project_root = folder

        self.action_bar.check_git_status(folder)
        self.perform_scan(folder, use_git_filter=False)

        self.header.setText(f"Project: {folder}")
        self.workspace.project_loaded()

        self.current_phases = LANGUAGE_PHASES.get(
            AppState.selected_language, ["Structure"]
        )
        self.sidebar.load_phases(self.current_phases)
        self.sidebar.unlock()

    def refresh_scan(self, use_git_filter):
        if AppState.project_root:
            self.perform_scan(AppState.project_root, use_git_filter)

    def perform_scan(self, folder, use_git_filter):
        whitelist = None
        if use_git_filter:
            whitelist = GitScanner.get_changed_files(folder)

        AppState.tree_root = scan_directory(folder, whitelist_files=whitelist)
        self.cache = PerformanceCache(folder)

    # ==================================================
    # ANALYSIS
    # ==================================================
    def start_analysis(self):
        self.worker = AnalysisWorker(self.current_phases, self.run_phase)
        self.worker.progress.connect(self.workspace.update_progress)
        self.worker.start()

    def run_phase(self, phase):
        try:
            root = AppState.tree_root
            if phase == "Structure":
                output = "\n".join(build_tree_text(root))
            else:
                output = "[INFO] Phase executed."
        except Exception as e:
            output = f"[ERROR] {e}"

        self.workspace.add_output(phase, output)

    # ==================================================
    # EXPORT
    # ==================================================
    def export_selected(self): pass
    def export_all(self): pass
    def export_zip(self): pass
