from PySide6.QtCore import QThread, Signal


class AnalysisWorker(QThread):
    progress = Signal(int, str)
    finished = Signal()

    def __init__(self, phases, run_phase_cb):
        super().__init__()
        self.phases = phases
        self.run_phase_cb = run_phase_cb

    def run(self):
        total = len(self.phases)

        for idx, phase in enumerate(self.phases):
            self.progress.emit(int((idx / total) * 100), phase)
            self.run_phase_cb(phase)

        self.progress.emit(100, "Completed")
        self.finished.emit()
