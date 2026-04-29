ecgvalidator
============

.. image:: https://github.com/guykopa/ecgvalidator/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/guykopa/ecgvalidator/actions
   :alt: CI

.. image:: https://img.shields.io/badge/coverage-100%25-brightgreen
   :alt: Coverage

.. image:: https://img.shields.io/badge/python-3.11%2B-blue
   :alt: Python

Test automation framework for an ECG signal acquisition and analysis pipeline,
built with strict TDD and SOLID principles in a regulated medical environment
(**IEC 62304** awareness).

.. toctree::
   :maxdepth: 2
   :caption: Contents

   visualization
   architecture
   testing
   api/index

Quick start
-----------

.. code-block:: bash

   python3.11 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   pytest tests/ -v --cov=src --cov-fail-under=90

Non-regression reference (seed=42)
-----------------------------------

.. code-block:: json

   {
     "bpm": 75.03126302626093,
     "anomaly": "NORMAL",
     "qrs_count": 13
   }
