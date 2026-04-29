from enum import Enum


class AnomalyType(Enum):
    """Cardiac anomaly classification."""

    NORMAL = "NORMAL"
    TACHYCARDIA = "TACHYCARDIA"
    BRADYCARDIA = "BRADYCARDIA"
