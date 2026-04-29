"""Generate ECG pipeline visualization figures for Sphinx documentation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from src.acquisition.signal_generator import SignalGenerator
from src.processing.signal_processor import SignalProcessor
from src.calculation.heart_rate_calculator import HeartRateCalculator
from src.analysis.anomaly_detector import AnomalyDetector
from src.pipeline.ecg_pipeline import ECGPipeline
from src.models.anomaly_type import AnomalyType

IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

SAMPLE_RATE = 250.0
DURATION = 10.0
SEED = 42

COLORS = {
    "raw": "#4C72B0",
    "filtered": "#55A868",
    "peaks": "#C44E52",
    "rr": "#8172B2",
    AnomalyType.NORMAL: "#55A868",
    AnomalyType.TACHYCARDIA: "#C44E52",
    AnomalyType.BRADYCARDIA: "#4C72B0",
}

ANOMALY_LABELS = {
    AnomalyType.NORMAL: "Normal — 75 BPM",
    AnomalyType.TACHYCARDIA: "Tachycardie — 120 BPM",
    AnomalyType.BRADYCARDIA: "Bradycardie — 45 BPM",
}

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#F8F8F8",
    "axes.grid": True,
    "grid.color": "white",
    "grid.linewidth": 1.2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 11,
})


def _time_axis(n_samples: int) -> np.ndarray:
    return np.linspace(0.0, DURATION, n_samples)


def _run_pipeline(bpm: float):
    """Return (signal, processed, heart_rate, anomaly) for a given BPM."""
    pipeline = ECGPipeline(
        processor=SignalProcessor(),
        calculator=HeartRateCalculator(),
        detector=AnomalyDetector(),
    )
    signal = SignalGenerator(seed=SEED).generate(
        bpm=bpm, sample_rate=SAMPLE_RATE, duration=DURATION
    )
    result = pipeline.run(signal)
    return signal, result.processed, result.heart_rate, result.anomaly


def generate_pipeline_stages() -> None:
    """One figure showing all pipeline stages for a normal 75 BPM signal."""
    signal, processed, heart_rate, anomaly = _run_pipeline(75.0)
    t = _time_axis(len(signal.samples))
    peak_times = processed.qrs_peaks / SAMPLE_RATE

    fig = plt.figure(figsize=(14, 10))
    fig.suptitle(
        "Pipeline ECG — étapes de traitement (75 BPM, seed=42)",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )
    gs = gridspec.GridSpec(3, 1, hspace=0.55)

    # --- Étape 1 : signal brut ---
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(t, signal.samples, color=COLORS["raw"], linewidth=0.8)
    ax1.set_title("Étape 1 — Signal brut (acquisition)", fontweight="bold")
    ax1.set_ylabel("Amplitude (mV)")
    ax1.set_xlabel("Temps (s)")

    # --- Étape 2 : signal filtré + pics QRS ---
    ax2 = fig.add_subplot(gs[1])
    ax2.plot(
        t, processed.filtered,
        color=COLORS["filtered"], linewidth=0.9, label="Signal filtré",
    )
    ax2.scatter(
        peak_times,
        processed.filtered[processed.qrs_peaks],
        color=COLORS["peaks"], zorder=5, s=60, label="Pics QRS détectés",
    )
    ax2.set_title(
        "Étape 2 — Signal filtré (passe-bande 0.5–40 Hz) + détection QRS",
        fontweight="bold",
    )
    ax2.set_ylabel("Amplitude (mV)")
    ax2.set_xlabel("Temps (s)")
    ax2.legend(loc="upper right", framealpha=0.8)

    # --- Étape 3 : intervalles R-R + résultat ---
    ax3 = fig.add_subplot(gs[2])
    rr_times = peak_times[:-1] + np.diff(peak_times) / 2
    ax3.bar(
        rr_times,
        heart_rate.rr_intervals,
        width=np.diff(peak_times) * 0.6,
        color=COLORS[anomaly], alpha=0.8, label="Intervalle R-R (s)",
    )
    ax3.axhline(
        np.mean(heart_rate.rr_intervals),
        color="black", linestyle="--", linewidth=1.2,
        label=f"Moyenne R-R = {np.mean(heart_rate.rr_intervals):.3f} s",
    )
    ax3.set_title(
        f"Étape 3 — Intervalles R-R → {heart_rate.bpm:.1f} BPM"
        f" → {anomaly.value}",
        fontweight="bold",
    )
    ax3.set_ylabel("Intervalle R-R (s)")
    ax3.set_xlabel("Temps (s)")
    ax3.legend(loc="upper right", framealpha=0.8)

    fig.savefig(IMAGES_DIR / "pipeline_stages.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  pipeline_stages.png")


def generate_anomaly_comparison() -> None:
    """One figure comparing normal, tachycardia and bradycardia signals."""
    scenarios = [
        (75.0, AnomalyType.NORMAL),
        (120.0, AnomalyType.TACHYCARDIA),
        (45.0, AnomalyType.BRADYCARDIA),
    ]

    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle(
        "Comparaison des anomalies cardiaques — signal filtré + pics QRS",
        fontsize=14, fontweight="bold", y=0.98,
    )

    for ax, (bpm, expected_anomaly) in zip(axes, scenarios):
        signal, processed, heart_rate, anomaly = _run_pipeline(bpm)
        t = _time_axis(len(signal.samples))
        peak_times = processed.qrs_peaks / SAMPLE_RATE

        color = COLORS[anomaly]
        ax.plot(
            t, processed.filtered,
            color=color, linewidth=0.9,
        )
        ax.scatter(
            peak_times,
            processed.filtered[processed.qrs_peaks],
            color=COLORS["peaks"], zorder=5, s=50,
        )
        ax.set_title(
            f"{ANOMALY_LABELS[anomaly]} — {len(processed.qrs_peaks)} pics"
            f" en {DURATION:.0f} s",
            fontweight="bold", color=color,
        )
        ax.set_ylabel("Amplitude (mV)")
        ax.set_xlabel("Temps (s)")

    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(
        IMAGES_DIR / "anomaly_comparison.png", dpi=150, bbox_inches="tight"
    )
    plt.close(fig)
    print("  anomaly_comparison.png")


def generate_result_summary() -> None:
    """Gauge-style summary card for a normal 75 BPM result."""
    _, _, heart_rate, anomaly = _run_pipeline(75.0)

    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.axis("off")

    color = COLORS[anomaly]
    bpm_str = f"{heart_rate.bpm:.1f} BPM"
    anomaly_str = anomaly.value

    ax.text(
        0.5, 0.72, bpm_str,
        ha="center", va="center", fontsize=52, fontweight="bold",
        color=color, transform=ax.transAxes,
    )
    ax.text(
        0.5, 0.32, anomaly_str,
        ha="center", va="center", fontsize=26, fontweight="bold",
        color="white", transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=color, linewidth=0),
    )
    ax.text(
        0.5, 0.08,
        f"Référence : seed=42 — {len(heart_rate.rr_intervals)} intervalles R-R",
        ha="center", va="center", fontsize=10, color="#666666",
        transform=ax.transAxes,
    )
    fig.patch.set_facecolor("white")

    fig.savefig(
        IMAGES_DIR / "result_summary.png", dpi=150, bbox_inches="tight"
    )
    plt.close(fig)
    print("  result_summary.png")


if __name__ == "__main__":
    print("Generating figures...")
    generate_pipeline_stages()
    generate_anomaly_comparison()
    generate_result_summary()
    print("Done — images saved to docs/images/")
