# Use this in your MainWindow class to integrate Phase 1 Visibility
from core.intelligence.role_auditor import RoleAuditor
from core.intelligence.heatmap_generator import RiskHeatmap
from core.summary.executive_summary_v2 import ExecutiveSummaryV2
from state.app_state import AppState

def run_rocket_analysis(self):
    # This replaces parts of your current 'run_phase' or adds new steps
    root = AppState.tree_root
    lang = AppState.selected_language
    
    # 1. Visibility: Perform Role Audit
    self.status_bar.showMessage("Rocket Mode: Performing Role Audit...")
    metrics = RoleAuditor.audit_project(root, lang)
    
    # 2. Intelligence: Risk Heatmap
    heatmap = RiskHeatmap.generate(metrics)
    self.workspace.add_output("Architecture Heatmap", heatmap)
    
    # 3. Layer Violations
    violations = RoleAuditor.detect_violations(metrics)
    
    # 4. Executive Summary v2
    summary = ExecutiveSummaryV2.build("Context Project", metrics, violations)
    self.workspace.add_output("Executive Summary 2.0", summary)
    
    self.status_bar.showMessage("Rocket Analysis Complete!")