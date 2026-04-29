from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class HeartRate:
    """Heart rate calculated from QRS peak intervals."""

    bpm: float
    rr_intervals: np.ndarray
    valid: bool
