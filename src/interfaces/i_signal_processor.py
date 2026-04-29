from abc import ABC, abstractmethod

from src.models.ecg_signal import ECGSignal
from src.models.processed_signal import ProcessedSignal


class ISignalProcessor(ABC):
    """Contract for ECG signal filtering and QRS detection."""

    @abstractmethod
    def process(self, signal: ECGSignal) -> ProcessedSignal:
        """Filter raw ECG signal and detect QRS complexes.

        Args:
            signal: Raw ECG signal with samples and sample rate.

        Returns:
            ProcessedSignal with filtered data and QRS peak indices.
        """
