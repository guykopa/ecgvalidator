from src.interfaces.i_anomaly_detector import IAnomalyDetector
from src.models.heart_rate import HeartRate
from src.models.anomaly_type import AnomalyType


class AnomalyDetector(IAnomalyDetector):
    """Classifies heart rate as NORMAL, TACHYCARDIA, or BRADYCARDIA."""

    _TACHYCARDIA_THRESHOLD: float = 100.0
    _BRADYCARDIA_THRESHOLD: float = 60.0

    def detect(self, heart_rate: HeartRate) -> AnomalyType:
        """Classify heart rate as normal or anomalous.

        Args:
            heart_rate: Calculated heart rate with BPM value.

        Returns:
            AnomalyType: NORMAL, TACHYCARDIA, or BRADYCARDIA.

        Raises:
            ValueError: if heart_rate.valid is False.
        """
        if not heart_rate.valid:
            raise ValueError("invalid heart rate: cannot classify")

        if heart_rate.bpm > self._TACHYCARDIA_THRESHOLD:
            return AnomalyType.TACHYCARDIA
        if heart_rate.bpm < self._BRADYCARDIA_THRESHOLD:
            return AnomalyType.BRADYCARDIA
        return AnomalyType.NORMAL
