import numpy as np

from src.interfaces.i_heart_rate_calculator import IHeartRateCalculator
from src.models.processed_signal import ProcessedSignal
from src.models.heart_rate import HeartRate


class HeartRateCalculator(IHeartRateCalculator):
    """Calculates BPM and R-R intervals from detected QRS peaks."""

    def calculate(self, processed: ProcessedSignal) -> HeartRate:
        """Calculate heart rate from QRS peak positions.

        Args:
            processed: Processed signal with detected QRS peaks.

        Returns:
            HeartRate with BPM, R-R intervals, and validity flag.
            valid=False when fewer than 2 peaks are detected.
        """
        if len(processed.qrs_peaks) < 2:
            return HeartRate(
                bpm=0.0,
                rr_intervals=np.array([], dtype=np.float64),
                valid=False,
            )

        rr_intervals = (
            np.diff(processed.qrs_peaks).astype(np.float64) / processed.sample_rate
        )
        bpm = float(60.0 / np.mean(rr_intervals))

        return HeartRate(bpm=bpm, rr_intervals=rr_intervals, valid=True)
