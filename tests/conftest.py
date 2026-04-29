import pytest
import numpy as np

from src.acquisition.signal_generator import SignalGenerator
from src.models.ecg_signal import ECGSignal
from src.models.heart_rate import HeartRate

SAMPLE_RATE = 250.0
DURATION = 10.0


@pytest.fixture
def normal_ecg_signal() -> ECGSignal:
    """Normal ECG signal — 75 BPM, seed=42."""
    return SignalGenerator(seed=42).generate(
        bpm=75.0, sample_rate=SAMPLE_RATE, duration=DURATION
    )


@pytest.fixture
def tachycardia_ecg_signal() -> ECGSignal:
    """Tachycardia ECG signal — 120 BPM, seed=42."""
    return SignalGenerator(seed=42).generate(
        bpm=120.0, sample_rate=SAMPLE_RATE, duration=DURATION
    )


@pytest.fixture
def bradycardia_ecg_signal() -> ECGSignal:
    """Bradycardia ECG signal — 45 BPM, seed=42."""
    return SignalGenerator(seed=42).generate(
        bpm=45.0, sample_rate=SAMPLE_RATE, duration=DURATION
    )


@pytest.fixture
def noisy_ecg_signal() -> ECGSignal:
    """ECG signal with high noise — 75 BPM, noise_level=0.5, seed=42."""
    return SignalGenerator(seed=42).generate(
        bpm=75.0, sample_rate=SAMPLE_RATE, duration=DURATION, noise_level=0.5
    )


@pytest.fixture
def normal_heart_rate() -> HeartRate:
    """Normal heart rate fixture — 75 BPM."""
    rr = np.array([0.8, 0.8, 0.8, 0.8, 0.8], dtype=np.float64)
    return HeartRate(bpm=75.0, rr_intervals=rr, valid=True)


@pytest.fixture
def tachycardia_heart_rate() -> HeartRate:
    """Tachycardia heart rate fixture — 120 BPM."""
    rr = np.array([0.5, 0.5, 0.5, 0.5, 0.5], dtype=np.float64)
    return HeartRate(bpm=120.0, rr_intervals=rr, valid=True)


@pytest.fixture
def bradycardia_heart_rate() -> HeartRate:
    """Bradycardia heart rate fixture — 45 BPM."""
    rr = np.array([1.33, 1.33, 1.33, 1.33], dtype=np.float64)
    return HeartRate(bpm=45.0, rr_intervals=rr, valid=True)
