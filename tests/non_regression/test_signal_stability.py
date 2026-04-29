import json
from pathlib import Path

from src.acquisition.signal_generator import SignalGenerator
from src.processing.signal_processor import SignalProcessor
from src.calculation.heart_rate_calculator import HeartRateCalculator
from src.analysis.anomaly_detector import AnomalyDetector
from src.pipeline.ecg_pipeline import ECGPipeline

REFERENCE_PATH = Path("fixtures/reference_output.json")
SEED = 42


class TestSignalStability:
    """Non-regression tests — pipeline output must remain stable across releases.

    Any unintended change in processing logic will break these tests.
    Reference generated with seed=42, stored in fixtures/reference_output.json.
    """

    def test_pipeline_output_matches_reference(self) -> None:
        """Full pipeline output must match the stored reference (seed=42)."""
        pipeline = ECGPipeline(
            processor=SignalProcessor(),
            calculator=HeartRateCalculator(),
            detector=AnomalyDetector(),
        )
        signal = SignalGenerator(seed=SEED).generate(
            bpm=75.0, sample_rate=250.0, duration=10.0
        )
        result = pipeline.run(signal)
        reference = json.loads(REFERENCE_PATH.read_text())

        assert abs(result.heart_rate.bpm - reference["bpm"]) < 0.1
        assert result.anomaly.value == reference["anomaly"]
        assert len(result.processed.qrs_peaks) == reference["qrs_count"]
