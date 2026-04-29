import numpy as np

from src.calculation.heart_rate_calculator import HeartRateCalculator
from src.models.processed_signal import ProcessedSignal


class TestHeartRateCalculator:
    """Unit tests for HeartRateCalculator — TDD RED/GREEN/REFACTOR."""

    def setup_method(self) -> None:
        self.calculator = HeartRateCalculator()

    def _make_processed(
        self, peaks: np.ndarray, sample_rate: float = 250.0
    ) -> ProcessedSignal:
        """Build a minimal ProcessedSignal from peak indices."""
        n = int(peaks[-1] + 1) if len(peaks) > 0 else 100
        return ProcessedSignal(
            filtered=np.zeros(n, dtype=np.float64),
            qrs_peaks=peaks.astype(np.int64),
            sample_rate=sample_rate,
        )

    def test_returns_invalid_if_less_than_two_peaks(self) -> None:
        """Fewer than 2 QRS peaks must yield valid=False."""
        peaks = np.array([100], dtype=np.int64)
        processed = self._make_processed(peaks)
        result = self.calculator.calculate(processed)
        assert result.valid is False

    def test_rr_intervals_calculated_correctly(self) -> None:
        """Peaks spaced 250 samples at 250 Hz → R-R = 1.0 s exactly."""
        peaks = np.array([0, 250, 500, 750], dtype=np.int64)
        processed = self._make_processed(peaks, sample_rate=250.0)
        result = self.calculator.calculate(processed)
        assert np.allclose(result.rr_intervals, 1.0, atol=1e-6)

    def test_calculates_correct_bpm_from_peaks(self) -> None:
        """Peaks spaced 200 samples at 250 Hz → BPM = 75 (±1)."""
        peaks = np.arange(0, 2001, 200, dtype=np.int64)
        processed = self._make_processed(peaks, sample_rate=250.0)
        result = self.calculator.calculate(processed)
        assert abs(result.bpm - 75.0) <= 1.0

    def test_bpm_within_physiological_range(self, normal_ecg_signal) -> None:
        """BPM calculated from a real generated signal must be in 30–300."""
        from src.processing.signal_processor import SignalProcessor
        processed = SignalProcessor().process(normal_ecg_signal)
        result = self.calculator.calculate(processed)
        if result.valid:
            assert 30.0 <= result.bpm <= 300.0
