import numpy as np

from src.models.ecg_signal import ECGSignal


class SignalGenerator:
    """Synthetic ECG signal generator for deterministic test data.

    Generates a realistic ECG waveform (P wave + QRS complex + T wave)
    at a given heart rate. Used exclusively as test infrastructure —
    not part of the production pipeline under test.
    """

    def __init__(self, seed: int = 42) -> None:
        """Initialise the generator with a fixed random seed.

        Args:
            seed: Seed for the NumPy RNG — guarantees deterministic output.
        """
        self._rng = np.random.default_rng(seed)

    def generate(
        self,
        bpm: float,
        sample_rate: float,
        duration: float,
        noise_level: float = 0.05,
    ) -> ECGSignal:
        """Generate a synthetic ECG signal.

        Args:
            bpm: Target heart rate in beats per minute.
            sample_rate: Sampling frequency in Hz.
            duration: Signal duration in seconds.
            noise_level: Standard deviation of additive Gaussian noise.

        Returns:
            ECGSignal with dtype=float64 samples.
        """
        n_samples = int(sample_rate * duration)
        t = np.linspace(0.0, duration, n_samples, dtype=np.float64)
        signal = np.zeros(n_samples, dtype=np.float64)

        beat_period = 60.0 / bpm
        beat_times = np.arange(0.0, duration, beat_period)

        for bt in beat_times:
            signal += 0.15 * np.exp(-((t - (bt + 0.10)) ** 2) / (2 * 0.010 ** 2))
            signal += 1.00 * np.exp(-((t - (bt + 0.20)) ** 2) / (2 * 0.005 ** 2))
            signal += 0.30 * np.exp(-((t - (bt + 0.35)) ** 2) / (2 * 0.020 ** 2))

        noise = self._rng.normal(0.0, noise_level, n_samples).astype(np.float64)
        samples = (signal + noise).astype(np.float64)

        return ECGSignal(samples=samples, sample_rate=sample_rate, duration=duration)
