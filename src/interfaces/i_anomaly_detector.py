from abc import ABC, abstractmethod

from src.models.heart_rate import HeartRate
from src.models.anomaly_type import AnomalyType


class IAnomalyDetector(ABC):
    """Contract for cardiac anomaly classification."""

    @abstractmethod
    def detect(self, heart_rate: HeartRate) -> AnomalyType:
        """Classify heart rate as normal or anomalous.

        Args:
            heart_rate: Calculated heart rate with BPM value.

        Returns:
            AnomalyType: NORMAL, TACHYCARDIA, or BRADYCARDIA.

        Raises:
            ValueError: if heart_rate.valid is False.
        """
