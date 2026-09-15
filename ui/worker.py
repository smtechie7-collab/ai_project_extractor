import time

from PySide6.QtCore import QThread, Signal


class AnalysisWorker(QThread):
    progress = Signal(int, str)
    finished = Signal()
    cancelled = Signal()

    def __init__(self, phases, run_phase_cb):
        super().__init__()
        self.phases = phases
        self.run_phase_cb = run_phase_cb
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        total = len(self.phases)
        if total == 0:
            self.progress.emit(100, "No phases to execute")
            self.finished.emit()
            return

        start_time = time.monotonic()

        for idx, phase in enumerate(self.phases):
            if self._is_cancelled:
                self.progress.emit(int((idx / total) * 100), "Cancelled by user")
                self.cancelled.emit()
                return

            elapsed = time.monotonic() - start_time
            avg_per_phase = elapsed / idx if idx > 0 else 0.0
            remaining_phases = total - idx
            est_remaining = avg_per_phase * remaining_phases

            eta_str = f" (~{int(est_remaining)}s left)" if idx > 0 and est_remaining > 1 else ""
            status_text = f"{phase}{eta_str}"

            self.progress.emit(int((idx / total) * 100), status_text)
            self.run_phase_cb(phase)

        if self._is_cancelled:
            self.cancelled.emit()
            return

        self.progress.emit(100, "Completed")
        self.finished.emit()
