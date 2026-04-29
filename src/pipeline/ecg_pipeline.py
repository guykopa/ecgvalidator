from datetime import datetime

from src.interfaces.i_signal_processor import ISignalProcessor
from src.interfaces.i_heart_rate_calculator import IHeartRateCalculator
from src.interfaces.i_anomaly_detector import IAnomalyDetector
from src.models.ecg_signal import ECGSignal
from src.models.pipeline_result import PipelineResult


class ECGPipeline:
    """Orchestrates the ECG analysis pipeline via constructor injection.

    Depends exclusively on interfaces — never on concrete stage classes.
    Concrete classes are instantiated only by the caller (conftest.py or main).
    """

    def __init__(
        self,
        processor: ISignalProcessor,
        calculator: IHeartRateCalculator,
        detector: IAnomalyDetector,
    ) -> None:
        """Inject all pipeline stages.

        Args:
            processor: ECG signal filter and QRS detector.
            calculator: Heart rate calculator from QRS peaks.
            detector: Cardiac anomaly classifier.
        """
        self._processor = processor
        self._calculator = calculator
        self._detector = detector

    def run(self, signal: ECGSignal) -> PipelineResult:
        """Execute the full ECG analysis pipeline.

        Args:
            signal: Raw ECG signal to analyse.

        Returns:
            PipelineResult with all intermediate and final outputs.
        """
        processed = self._processor.process(signal)
        heart_rate = self._calculator.calculate(processed)
        anomaly = self._detector.detect(heart_rate)

        return PipelineResult(
            signal=signal,
            processed=processed,
            heart_rate=heart_rate,
            anomaly=anomaly,
            timestamp=datetime.now(),
        )
