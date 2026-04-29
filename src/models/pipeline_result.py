from dataclasses import dataclass
from datetime import datetime

from src.models.ecg_signal import ECGSignal
from src.models.processed_signal import ProcessedSignal
from src.models.heart_rate import HeartRate
from src.models.anomaly_type import AnomalyType


@dataclass(frozen=True)
class PipelineResult:
    """Full result of one ECG pipeline execution."""

    signal: ECGSignal
    processed: ProcessedSignal
    heart_rate: HeartRate
    anomaly: AnomalyType
    timestamp: datetime
