from abc import ABC, abstractmethod

from src.models.processed_signal import ProcessedSignal
from src.models.heart_rate import HeartRate


class IHeartRateCalculator(ABC):
    """Contract for heart rate calculation from a processed ECG signal."""

    @abstractmethod
    def calculate(self, processed: ProcessedSignal) -> HeartRate:
        """Calculate heart rate from QRS peak positions.

        Args:
            processed: Processed signal with detected QRS peaks.

        Returns:
            HeartRate with BPM value, R-R intervals, and validity flag.

        Raises:
            InsufficientPeaksError: if fewer than 2 QRS peaks detected.
        """
