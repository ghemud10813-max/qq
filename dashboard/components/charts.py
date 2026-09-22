"""
dashboard/components/charts.py
==============================
Threat-analytics charts, read from the canonical experiment output.

SIH26141 | Blockchain & Cybersecurity.

Every chart here is backed by `experiments/results/final/`, which only
`experiments/run_final_experiment.py` writes. This module loads and
renders; it computes no security metric of its own.

An earlier revision read whichever CSVs happened to sit in
`experiments/results/`, mixing per-phase development diagnostics with
final results and silently showing a stale figure when a file was absent.
Now a missing input says so explicitly -- a blank panel is better than a
number nobody can trace to a run.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (_ROOT / "src", _ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from dashboard.data_source import (  # noqa: E402
    load_attack_metrics,
    load_comparison,
    load_confusion_matrix,
    load_intensity,
    load_metrics,
    load_threshold_analysis,
    missing_results_message,
    plot_path,
    results_available,
)

RESULTS_DIR = _ROOT / "experiments" / "results" / "final"


def _require_results() -> bool:
    """Show the regeneration instruction when no canonical run exists."""
    if results_available():
        return True
    st.warning(missing_results_message())
    return False


def _show_plot(name: str, caption: str = "") -> None:
    """Render a generated figure, or say why it is absent."""
    p = plot_path(name)
    if p:
        st.image(p, width="stretch")
        if caption:
            st.caption(caption)
    else:
        st.info(f"`{name}` not found — re-run the canonical experiment.")


# ---------------------------------------------------------------------------
# Attack comparison
# ---------------------------------------------------------------------------

def render_attack_comparison() -> None:
    """Per-attack detection rates with confidence intervals."""
    st.subheader("Attack Detection Performance")
    if not _require_results():
        return

    df = load_attack_metrics()
    if df is None or df.empty:
        st.info("No attack metrics in the canonical results.")
        return

    show = df.copy()
    show["detection_rate"] = (show["detection_rate"] * 100).round(2)
    show["95% CI"] = [
        f"[{lo * 100:.2f}, {hi * 100:.2f}]"
        for lo, hi in zip(show["ci_lower"], show["ci_upper"])
    ]
    show["classified"] = (show["classification_accuracy"] * 100).round(1)
    st.dataframe(
        show[["attack_type", "trials", "detected", "missed",
              "detection_rate", "95% CI", "classified",
              "mean_anomaly_score", "mean_fidelity", "mean_purity"]],
        width="stretch", hide_index=True,
    )
    st.caption(
        "Detection rate is the fraction flagged as SUSPICIOUS or THREAT. "
        "`classified` is how often the engine also named the correct attack. "
        "Intervals are 95% Clopper-Pearson."
    )
    _show_plot("attack_comparison.png")

    st.divider()
    st.markdown("#### Normal vs Attack Telemetry")
    comp = load_comparison()
    if comp is not None and not comp.empty:
        cols = ["condition", "fidelity", "purity", "trace_distance",
                "entropy", "mismatch_rate", "anomaly_score"]
        st.dataframe(comp[[c for c in cols if c in comp.columns]].round(4),
                     width="stretch", hide_index=True)
        st.caption(
            "Purity is the discriminator between forgery and channel noise: "
            "substituting an eigenstate leaves the state pure, while a "
            "depolarizing channel decoheres it."
        )
    _show_plot("normal_vs_attack.png")


# ---------------------------------------------------------------------------
# Threshold analysis
# ---------------------------------------------------------------------------

def render_threshold_analysis() -> None:
    """Threshold sweep, confusion matrix and detection-vs-intensity."""
    st.subheader("Threshold & Error-Rate Analysis")
    if not _require_results():
        return

    m = load_metrics() or {}
    df = load_threshold_analysis()

    if df is not None and not df.empty:
        st.markdown("#### FAR / FRR vs Threshold")
        chart = df[["threshold", "far", "frr"]].set_index("threshold")
        st.line_chart(chart)
        st.caption(
            f"Selected operating point: {m.get('threshold', float('nan')):.6f}. "
            "FAR is attacks that passed; FRR is legitimate sessions denied."
        )
        _show_plot("far_frr_vs_threshold.png")

    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Confusion Matrix")
        cm = load_confusion_matrix()
        if cm is not None:
            st.dataframe(cm, width="stretch")
        _show_plot("confusion_matrix.png")

    with c2:
        st.markdown("#### Detection vs Attack Intensity")
        inten = load_intensity()
        if inten is not None and not inten.empty:
            pivot = inten.pivot_table(
                index="intensity", columns="attack_type",
                values="detection_rate", aggfunc="mean",
            )
            st.line_chart(pivot)
        _show_plot("detection_vs_intensity.png")

    st.divider()
    st.markdown("#### Fidelity vs Channel Noise")
    _show_plot(
        "fidelity_vs_noise.png",
        "Measured on the live teleportation channel: injected depolarizing "
        "noise degrades the fidelity of the state the verifier receives.",
    )


# ---------------------------------------------------------------------------
# Performance / scalability
# ---------------------------------------------------------------------------

def render_performance_analytics() -> None:
    """Latency, throughput and scaling behaviour."""
    st.subheader("Performance & Scalability")
    if not _require_results():
        return

    m = load_metrics() or {}
    lat = m.get("latency_ms", {})

    cols = st.columns(5)
    cols[0].metric("Signature gen", f"{lat.get('signature_generation_mean', 0):.2f} ms")
    cols[1].metric("Quantum channel", f"{lat.get('quantum_channel_mean', 0):.2f} ms")
    cols[2].metric("Verification", f"{lat.get('verification_mean', 0):.2f} ms")
    cols[3].metric("Detection", f"{lat.get('detection_mean', 0):.2f} ms")
    cols[4].metric("Throughput",
                   f"{m.get('throughput_sessions_per_sec', 0):.1f}/s")
    st.caption(
        f"End-to-end mean {lat.get('end_to_end_mean', 0):.2f} ms, "
        f"median {lat.get('end_to_end_median', 0):.2f} ms."
    )

    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Latency vs Signature Length")
        path = RESULTS_DIR / "scalability_length.csv"
        if path.exists():
            df = pd.read_csv(path)
            st.dataframe(
                df[["signature_length", "total_ms", "throughput_per_sec",
                    "mean_fidelity"]].round(3),
                width="stretch", hide_index=True,
            )
        _show_plot("latency_vs_length.png",
                   "Stacked by pipeline stage, measured on the real pipeline.")

    with c2:
        st.markdown("#### Throughput vs Signature Length")
        _show_plot("throughput_vs_length.png")

    st.divider()
    st.markdown("#### Shot Count: Cost vs Statistical Precision")
    path = RESULTS_DIR / "scalability_shots.csv"
    if path.exists():
        st.dataframe(pd.read_csv(path).round(5), width="stretch", hide_index=True)
    _show_plot(
        "scalability_vs_shots.png",
        "More shots per element cost time but tighten the baseline anomaly-score "
        "spread, which is what lets the detector run a tighter threshold.",
    )
