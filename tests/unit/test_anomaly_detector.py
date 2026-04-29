import pytest
import numpy as np

from src.analysis.anomaly_detector import AnomalyDetector
from src.models.anomaly_type import AnomalyType
from src.models.heart_rate import HeartRate


class TestAnomalyDetector:
    """Unit tests for AnomalyDetector — TDD RED/GREEN/REFACTOR."""

    def setup_method(self) -> None:
        self.detector = AnomalyDetector()

    def test_invalid_heart_rate_raises_value_error(self) -> None:
        """valid=False must raise ValueError containing 'invalid'."""
        invalid = HeartRate(
            bpm=0.0, rr_intervals=np.array([], dtype=np.float64), valid=False
        )
        with pytest.raises(ValueError, match="invalid"):
            self.detector.detect(invalid)

    def test_detects_normal_heart_rate(self, normal_heart_rate) -> None:
        """75 BPM must be classified as NORMAL."""
        assert self.detector.detect(normal_heart_rate) == AnomalyType.NORMAL

    def test_detects_tachycardia(self, tachycardia_heart_rate) -> None:
        """120 BPM must be classified as TACHYCARDIA."""
        result = self.detector.detect(tachycardia_heart_rate)
        assert result == AnomalyType.TACHYCARDIA

    def test_detects_bradycardia(self, bradycardia_heart_rate) -> None:
        """45 BPM must be classified as BRADYCARDIA."""
        result = self.detector.detect(bradycardia_heart_rate)
        assert result == AnomalyType.BRADYCARDIA

    @pytest.mark.parametrize("bpm,expected", [
        (45.0,  AnomalyType.BRADYCARDIA),
        (59.9,  AnomalyType.BRADYCARDIA),
        (60.0,  AnomalyType.NORMAL),
        (75.0,  AnomalyType.NORMAL),
        (100.0, AnomalyType.NORMAL),
        (100.1, AnomalyType.TACHYCARDIA),
        (150.0, AnomalyType.TACHYCARDIA),
    ])
    def test_boundary_values(self, bpm: float, expected: AnomalyType) -> None:
        """Boundary values must map to the correct AnomalyType."""
        hr = HeartRate(
            bpm=bpm,
            rr_intervals=np.array([60.0 / bpm], dtype=np.float64),
            valid=True,
        )
        assert self.detector.detect(hr) == expected
