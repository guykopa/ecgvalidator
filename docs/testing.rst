Test strategy
=============

IEC 62304 requires a documented test strategy with multiple validation levels.
ecgvalidator implements the **Test Pyramid** with three levels.

Test pyramid
------------

.. code-block:: text

        ▲  tests/non_regression/  (1 test)
       / \   seed=42 → pipeline → compare to reference
      /───\
      tests/integration/  (3 tests)
      └── ECGPipeline full run, 3 clinical scenarios
   /─────────────────────────────────────\
     tests/unit/  (20 tests)
     ├── test_signal_processor.py    (5)
     ├── test_heart_rate_calculator.py (4)
     └── test_anomaly_detector.py   (11 — 7 parametrized boundary values)

Coverage
--------

Enforced ≥ 90% on every CI run via ``--cov-fail-under=90``.
Current coverage: **100%** across all 21 source files.

Unit tests
----------

One test class per production class. All fixtures from ``conftest.py`` only.
No mocks — pipeline stages are pure functions.

.. list-table::
   :header-rows: 1

   * - Class under test
     - Tests
     - Key scenarios
   * - ``SignalProcessor``
     - 5
     - shape, noise reduction, QRS detection, BPM count
   * - ``HeartRateCalculator``
     - 4
     - correct BPM, R-R intervals, <2 peaks → invalid
   * - ``AnomalyDetector``
     - 11
     - NORMAL / TACHYCARDIA / BRADYCARDIA + 7 boundary values

Integration tests
-----------------

``ECGPipeline`` wired with real concrete classes (as in production).
Validates clinical correctness end-to-end.

Non-regression tests
--------------------

Reference output generated with ``seed=42``, ``bpm=75``, ``sample_rate=250 Hz``,
``duration=10 s`` and stored in ``fixtures/reference_output.json``.

Any unintended change in filtering or peak detection logic will break
``test_signal_stability.py``.

Running the campaign
--------------------

.. code-block:: bash

   pytest tests/ -v --cov=src --cov-report=html --cov-fail-under=90
