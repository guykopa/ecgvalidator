import numpy as np
from scipy.signal import butter, sosfilt, find_peaks

from src.interfaces.i_signal_processor import ISignalProcessor
from src.models.ecg_signal import ECGSignal
from src.models.processed_signal import ProcessedSignal


class SignalProcessor(ISignalProcessor):
    """Bandpass filter and QRS detector implementing ISignalProcessor."""

    def process(self, signal: ECGSignal) -> ProcessedSignal:
        """Filter raw ECG signal and detect QRS complexes.

        Args:
            signal: Raw ECG signal with samples and sample rate.

        Returns:
            ProcessedSignal with filtered data and QRS peak indices.
        """
        sos = butter(
            4, [0.5, 40.0], btype="band", fs=signal.sample_rate, output="sos"
        )
        filtered = sosfilt(sos, signal.samples).astype(np.float64)

        min_distance = int(signal.sample_rate * 0.5)
        peaks, _ = find_peaks(
            filtered,
            height=0.5 * float(np.max(filtered)),
            distance=min_distance,
        )

        return ProcessedSignal(
            filtered=filtered,
            qrs_peaks=peaks.astype(np.int64),
            sample_rate=signal.sample_rate,
        )
