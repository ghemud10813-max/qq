"""
dashboard/components/metrics.py
===============================
KPI metrics and event log visualization.
"""
import pandas as pd
import streamlit as st
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent.parent / "experiments" / "results"

# Every KPI below is loaded from the canonical experiment output via the
# dashboard data contract. Nothing here computes a security metric, and
# nothing falls back to a plausible-looking placeholder: if a run has not
# been performed, the UI says so rather than showing a number that no
# measurement produced.
from dashboard.data_source import (  # noqa: E402
    load_experiment_config,
    load_metrics,
    missing_results_message,
    pct,
    pct_ci,
    results_available,
)


def render_top_kpis():
    """Render the top dashboard KPIs from the canonical experiment run."""
    st.markdown("### System Security Posture")

    if not results_available():
        st.warning(missing_results_message())
        st.divider()
        return

    m = load_metrics() or {}
    cfg = load_experiment_config() or {}

    cols = st.columns(6)

    # 1. Overall status, derived from the measured F1.
    with cols[0]:
        f1 = m.get("f1")
        if f1 is not None and f1 > 0.90:
            st.metric("Status", "SECURE", "Operational")
        elif f1 is not None:
            st.metric("Status", "DEGRADED", f"F1 {pct(f1)}")
        else:
            st.metric("Status", "UNKNOWN", "-")

    with cols[1]:
        st.metric("Global Accuracy", pct(m.get("accuracy")))

    with cols[2]:
        st.metric(
            "Detection Rate (TPR)",
            pct(m.get("detection_rate")),
            pct_ci(m.get("detection_rate"), m.get("detection_rate_ci")),
            help="95% Clopper-Pearson interval shown below the value.",
        )

    with cols[3]:
        st.metric(
            "False Acceptance Rate",
            pct(m.get("far")),
            pct_ci(m.get("far"), m.get("far_ci")),
            delta_color="off",
            help=f"Attacks that passed, over n={m.get('far_n', '?')} attack sessions.",
        )

    with cols[4]:
        st.metric(
            "False Rejection Rate",
            pct(m.get("frr")),
            pct_ci(m.get("frr"), m.get("frr_ci")),
            delta_color="off",
            help=f"Legitimate sessions denied, over n={m.get('frr_n', '?')}.",
        )

    with cols[5]:
        th = m.get("threshold")
        st.metric(
            "Calibrated Threshold",
            f"{th:.5f}" if isinstance(th, (int, float)) else "N/A",
            "experimentally selected",
            delta_color="off",
            help=cfg.get("threshold_rule", ""),
        )

    # Provenance: make it obvious which run these numbers came from.
    ts = cfg.get("timestamp_utc", "unknown")
    trials = cfg.get("trials_per_class", "?")
    seed = cfg.get("seed", "?")
    commit = cfg.get("git_commit") or "n/a"
    st.caption(
        f"Source: experiments/results/final - run {ts} - "
        f"{trials} sessions/class - seed {seed} - commit {commit} - "
        f"mean teleportation fidelity {m.get('mean_teleportation_fidelity', float('nan')):.4f}"
    )

    st.divider()


def log_event(event_type: str, action: str, score: float, decision: str):
    """Log an interactive event to session state."""
    import datetime
    import uuid
    if "event_logs" not in st.session_state:
        st.session_state.event_logs = []

    st.session_state.event_logs.insert(0, {
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "session_id": str(uuid.uuid4())[:8],
        "event_type": event_type,
        "action": action,
        "anomaly_score": round(score, 4),
        "decision": decision
    })


def render_event_log():
    """Render the chronological event log from dashboard interactions."""
    st.subheader("Live Event Log")
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.caption("Live interactions with the verification and attack engines.")
    with col2:
        if st.button("Clear Log"):
            st.session_state.event_logs = []

    if not st.session_state.get("event_logs"):
        st.info("No events logged yet. Perform verification or launch an attack to see live logs.")
    else:
        df = pd.DataFrame(st.session_state.event_logs)
        def color_decision(val):
            color = "#00FF41" if val in ("NORMAL", "ACCEPTED") else "#FF073A" if val in ("THREAT", "DENIED") else "#FFBF00"
            return f'color: {color}'
        st.dataframe(df.style.map(color_decision, subset=['decision']), use_container_width=True, hide_index=True)
