from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ProcessedSignal:
    """ECG signal after bandpass filtering and QRS detection."""

    filtered: np.ndarray
    qrs_peaks: np.ndarray
    sample_rate: float
