from src.processing.signal_processor import SignalProcessor
from src.models.processed_signal import ProcessedSignal


class TestSignalProcessor:
    """Unit tests for SignalProcessor — TDD RED/GREEN/REFACTOR."""

    def setup_method(self) -> None:
        self.processor = SignalProcessor()

    def test_returns_processed_signal_dataclass(self, normal_ecg_signal) -> None:
        """process() must return a ProcessedSignal instance."""
        result = self.processor.process(normal_ecg_signal)
        assert isinstance(result, ProcessedSignal)

    def test_output_shape_matches_input(self, normal_ecg_signal) -> None:
        """Filtered signal must have the same length as input samples."""
        result = self.processor.process(normal_ecg_signal)
        assert len(result.filtered) == len(normal_ecg_signal.samples)

    def test_filtered_signal_reduces_high_frequency_noise(
        self, noisy_ecg_signal
    ) -> None:
        """Bandpass filter must attenuate out-of-band noise (std must decrease)."""
        import numpy as np
        result = self.processor.process(noisy_ecg_signal)
        assert float(np.std(result.filtered)) < float(np.std(noisy_ecg_signal.samples))

    def test_detects_qrs_peaks_in_normal_signal(self, normal_ecg_signal) -> None:
        """At least one QRS peak must be detected in a valid ECG signal."""
        result = self.processor.process(normal_ecg_signal)
        assert len(result.qrs_peaks) > 0

    def test_qrs_count_matches_expected_bpm(self, normal_ecg_signal) -> None:
        """75 BPM over 10 s yields ~12 QRS peaks (±2 tolerance)."""
        result = self.processor.process(normal_ecg_signal)
        expected = int(75.0 * 10.0 / 60.0)
        assert abs(len(result.qrs_peaks) - expected) <= 2
