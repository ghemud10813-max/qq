"""
dashboard/components/metrics.py
===============================
KPI metrics and event log visualization.
"""
import pandas as pd
import streamlit as st
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent.parent / "experiments" / "results"

def load_security_summary():
    """Load latest security overview metrics."""
    try:
        df = pd.read_csv(RESULTS_DIR / "security_summary.csv")
        return pd.Series(
            df.Value.values, index=df.Metric
        ).to_dict()
    except Exception:
        return {}
        
def load_performance_summary():
    """Load performance benchmarks."""
    try:
        import json
        with open(RESULTS_DIR / "benchmark_config.json", "r") as f:
            return json.load(f)
    except Exception:
        return {}


def render_top_kpis():
    """Render the top dashboard key performance indicators."""
    summary = load_security_summary()
    perf = load_performance_summary()
    
    st.markdown("### System Security Posture")
    cols = st.columns(6)
    
    # 1. Overall Security Status
    with cols[0]:
        val = summary.get("F1 Score", "N/A")
        if isinstance(val, float) and val > 0.90:
            st.metric("Status", "SECURE", "Operational")
        else:
            st.metric("Status", "DEGRADED", "-")
            
    # 2. Latest Accuracy
    with cols[1]:
        acc = summary.get("Accuracy", "N/A")
        try:
            acc = f"{acc:.2%}" if isinstance(acc, float) else acc
        except Exception:
            pass
        st.metric("Global Accuracy", acc)
        
    # 3. Detection Rate
    with cols[2]:
        dr = summary.get("Detection Rate", "N/A")
        try:
            dr = f"{dr:.2%}" if isinstance(dr, float) else dr
        except Exception:
            pass
        st.metric("Detection Rate (TPR)", dr)
        
    # 4. False Acceptance Rate
    with cols[3]:
        far = summary.get("FAR", "N/A")
        try:
            far = f"{far:.2%}" if isinstance(far, float) else far
        except Exception:
            pass
        st.metric("False Acceptance Rate", far)
        
    # 5. False Rejection Rate
    with cols[4]:
        frr = summary.get("FRR", "N/A")
        try:
            frr = f"{frr:.2%}" if isinstance(frr, float) else frr
        except Exception:
            pass
        st.metric("False Rejection Rate", frr)
        
    # 6. Current Median Threshold
    with cols[5]:
        th = summary.get("Threshold_Critical", "N/A")
        try:
            th = f"{th:.4f}" if isinstance(th, float) else th
        except Exception:
            pass
        st.metric("Current Def. Threshold", th)
        
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
