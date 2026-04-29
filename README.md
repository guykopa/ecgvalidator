# ecgvalidator

![CI](https://github.com/guykopa/ecgvalidator/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://guykopa.github.io/ecgvalidator/)

Test automation framework for an ECG signal acquisition and analysis pipeline,
built with strict TDD and SOLID principles in a regulated medical environment
(IEC 62304 awareness).

**Documentation complète :** https://guykopa.github.io/ecgvalidator/

---

## Installation

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v --cov=src --cov-report=html --cov-fail-under=90
```

---

## Test campaign output

```
24 passed in 2.79s — coverage: 100%

tests/unit/test_signal_processor.py         5 tests  ✓
tests/unit/test_heart_rate_calculator.py    4 tests  ✓
tests/unit/test_anomaly_detector.py        11 tests  ✓  (7 parametrized boundary values)
tests/integration/test_ecg_pipeline.py      3 tests  ✓
tests/non_regression/test_signal_stability  1 test   ✓
```

---

## Algorithm

1. **Acquisition** — `SignalGenerator` produces a synthetic ECG (P wave + QRS + T wave) at a target BPM using NumPy. Accepts a `seed` for fully deterministic output.
2. **Filtering** — `SignalProcessor` applies a 4th-order Butterworth bandpass filter (0.5–40 Hz) via `scipy.signal.sosfilt`, then detects R peaks with `scipy.signal.find_peaks`.
3. **Heart rate** — `HeartRateCalculator` derives R-R intervals from peak spacing and computes BPM = 60 / mean(R-R).
4. **Classification** — `AnomalyDetector` labels the result: BPM > 100 → TACHYCARDIA, BPM < 60 → BRADYCARDIA, otherwise NORMAL.
5. **Orchestration** — `ECGPipeline` wires the stages by constructor injection and returns a `PipelineResult` dataclass.

---

## IEC 62304 test strategy

| Level | Files | Purpose |
|---|---|---|
| Unit | `tests/unit/` | Each algorithm in isolation |
| Integration | `tests/integration/` | Full pipeline end-to-end |
| Non-regression | `tests/non_regression/` | Stability guarantee across releases (seed=42) |

Coverage enforced ≥ 90% on every CI run.

---

## Non-regression reference

```json
{
  "bpm": 75.03126302626093,
  "anomaly": "NORMAL",
  "qrs_count": 13
}
```

Generated with `seed=42`, `bpm=75`, `sample_rate=250 Hz`, `duration=10 s`.
Any unintended change to filtering or peak detection logic will break `test_signal_stability.py`.
