from src.pipeline.ecg_pipeline import ECGPipeline
from src.processing.signal_processor import SignalProcessor
from src.calculation.heart_rate_calculator import HeartRateCalculator
from src.analysis.anomaly_detector import AnomalyDetector
from src.models.anomaly_type import AnomalyType
from src.models.pipeline_result import PipelineResult


class TestECGPipeline:
    """Integration tests — full pipeline end-to-end, TDD RED/GREEN/REFACTOR."""

    def setup_method(self) -> None:
        self.pipeline = ECGPipeline(
            processor=SignalProcessor(),
            calculator=HeartRateCalculator(),
            detector=AnomalyDetector(),
        )

    def test_full_pipeline_normal_signal_returns_normal(
        self, normal_ecg_signal
    ) -> None:
        """75 BPM signal must produce a PipelineResult with anomaly=NORMAL."""
        result = self.pipeline.run(normal_ecg_signal)
        assert isinstance(result, PipelineResult)
        assert result.anomaly == AnomalyType.NORMAL

    def test_full_pipeline_tachycardia_signal_detected(
        self, tachycardia_ecg_signal
    ) -> None:
        """120 BPM signal must produce anomaly=TACHYCARDIA."""
        result = self.pipeline.run(tachycardia_ecg_signal)
        assert result.anomaly == AnomalyType.TACHYCARDIA

    def test_full_pipeline_bradycardia_signal_detected(
        self, bradycardia_ecg_signal
    ) -> None:
        """45 BPM signal must produce anomaly=BRADYCARDIA."""
        result = self.pipeline.run(bradycardia_ecg_signal)
        assert result.anomaly == AnomalyType.BRADYCARDIA
