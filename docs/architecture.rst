Architecture
============

Pattern: Pipeline Pattern + Test Pyramid
-----------------------------------------

ecgvalidator models ECG signal processing as a chain of independent
transformation stages. Each stage receives data, transforms it, and passes it
to the next.

Pipeline flow
-------------

.. code-block:: text

   SignalGenerator (seed=42)
         │  ECGSignal
         ▼
   ISignalProcessor ◄── SignalProcessor
   └── Butterworth bandpass 0.5–40 Hz
   └── QRS detection (find_peaks)
         │  ProcessedSignal
         ▼
   IHeartRateCalculator ◄── HeartRateCalculator
   └── R-R intervals = diff(peaks) / sample_rate
   └── BPM = 60 / mean(R-R)
         │  HeartRate
         ▼
   IAnomalyDetector ◄── AnomalyDetector
   └── BPM > 100 → TACHYCARDIA
   └── BPM < 60  → BRADYCARDIA
   └── else      → NORMAL
         │  AnomalyType
         ▼
   ECGPipeline.run() → PipelineResult

SOLID mapping
-------------

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - Principle
     - Application
   * - **S**
     - ``SignalProcessor`` filters and detects QRS only.
       ``HeartRateCalculator`` computes BPM only.
       ``AnomalyDetector`` classifies only.
       ``ECGPipeline`` orchestrates only — zero signal logic.
   * - **O**
     - Add ``ArrhythmiaDetector`` by implementing ``IAnomalyDetector``.
       No existing file is modified.
   * - **L**
     - Any ``ISignalProcessor`` implementation is substitutable in ``ECGPipeline``.
   * - **I**
     - Three separate interfaces: ``ISignalProcessor``, ``IHeartRateCalculator``,
       ``IAnomalyDetector``. No class depends on methods it does not use.
   * - **D**
     - ``ECGPipeline`` depends on interfaces only.
       Concrete classes are instantiated exclusively in ``conftest.py``.

Dependency rule
---------------

.. code-block:: text

   conftest.py (fixtures + wiring)
         │
         ▼
   ECGPipeline (depends on interfaces only)
         │
   ISignalProcessor   IHeartRateCalculator   IAnomalyDetector
         ▲                    ▲                      ▲
   SignalProcessor  HeartRateCalculator       AnomalyDetector

Clinical thresholds
--------------------

.. list-table::
   :header-rows: 1

   * - Condition
     - Threshold
   * - Tachycardia
     - BPM > 100
   * - Bradycardia
     - BPM < 60
   * - Normal
     - 60 ≤ BPM ≤ 100
   * - Bandpass filter
     - 0.5 Hz – 40 Hz
