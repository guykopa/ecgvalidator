from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ECGSignal:
    """Raw ECG signal acquired from the device."""

    samples: np.ndarray
    sample_rate: float
    duration: float
