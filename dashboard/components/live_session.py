"""
dashboard/components/live_session.py
====================================
Live end-to-end session panel, driven by the real engine.

SIH26141 | Blockchain & Cybersecurity.

Runs an actual ``SessionRunner`` session in front of the user -- message
binding, signature, Bell pair, teleportation, Pauli correction, projective
measurement, verification, threat decision -- and shows what was measured
at each stage: real shot counts, real fidelity, the security timeline, and
the forensic report.

Nothing on this page is precomputed or illustrative. The attack controls
perturb the pipeline before transmission, and whatever the physics does
next is what appears.
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

ATTACK_CHOICES = (
    "NONE (legitimate)",
    "FORGERY",
    "IMPERSONATION",
    "REPLAY",
    "UNAUTHORIZED_VERIFICATION",
    "CHANNEL_MANIPULATION",
)


@st.cache_resource(show_spinner="Calibrating baseline from legitimate sessions...")
def _get_runner(signature_length: int, shots: int, seed: int):
    """Build and calibrate a session runner once, then reuse it.

    Calibration measures what an undisturbed session looks like on this
    machine; it is the reference every deviation metric is relative to, so
    it must happen before any attack is scored.
    """
    from session import SessionRunner

    r = SessionRunner(
        signature_length=signature_length,
        shots=shots,
        teleport_shots=128,
        seed=seed,
    )
    r.setup(private_seed=bytes([seed % 256]) * 32)
    r.calibrate_baseline(n_sessions=15)
    return r


def _run(runner, message: bytes, attack: str, intensity: float):
    """Execute one session for the chosen attack scenario."""
    import copy

    from attacks.forgery import ForgeryAttack
    from attacks.unauthorized_verification import UnauthorizedVerificationAttack
    from qds.keygen import generate_key_pair

    if attack.startswith("NONE"):
        return runner.run(message=message)

    if attack == "FORGERY":
        return runner.run(
            message=message, attack=ForgeryAttack(seed=7),
            attack_type=attack, intensity=intensity,
        )

    if attack == "UNAUTHORIZED_VERIFICATION":
        return runner.run(
            message=message, attack=UnauthorizedVerificationAttack(seed=7),
            attack_type=attack, intensity=intensity,
        )

    if attack == "IMPERSONATION":
        priv, _ = generate_key_pair(
            signer_id="attacker_mallory", table_size=runner.table_size
        )
        return runner.run(
            message=message, attack_type=attack,
            intensity=intensity, signing_key=priv,
        )

    if attack == "CHANNEL_MANIPULATION":
        return runner.run(
            message=message, attack_type=attack, intensity=intensity,
            channel_noise="depolarizing", channel_noise_level=intensity,
        )

    if attack == "REPLAY":
        ctx = runner.next_context("live_replay")
        runner.run(message=message, context=copy.deepcopy(ctx), detect=False)
        return runner.run(
            message=message, attack_type=attack, intensity=intensity,
            context=copy.deepcopy(ctx),
        )

    raise ValueError(f"Unknown attack {attack!r}")


def render_live_session() -> None:
    """Render the live verification / attack-lab panel."""
    st.subheader("Live Verification Session")
    st.caption(
        "Runs the real pipeline: message binding -> QDS signature -> Bell pair "
        "-> teleportation -> Pauli correction -> projective measurement -> "
        "verification -> threat decision. Every number below is measured."
    )

    ctrl, out = st.columns([0.32, 0.68])

    with ctrl:
        message = st.text_input("Message to sign", "transfer 100 to bob")
        attack = st.selectbox("Attack scenario", ATTACK_CHOICES)
        intensity = st.slider("Attack intensity", 0.0, 1.0, 0.5, 0.05,
                              disabled=attack.startswith("NONE"))
        sig_len = st.slider("Signature length", 4, 32, 8, 4)
        shots = st.select_slider("Shots per element", [64, 128, 256, 512], 128)
        run = st.button("RUN SESSION", type="primary")

    if not run:
        with out:
            st.info("Configure a scenario and run a session.")
        return

    runner = _get_runner(sig_len, shots, 42)
    with st.spinner("Executing quantum session..."):
        res = _run(runner, message.encode(), attack, intensity)

    with out:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Verification", f"{res.verification_score:.3f}",
                  f"{res.matches}/{res.total_elements} matched")
        c2.metric("Teleportation F", f"{res.telemetry.mean_fidelity:.4f}")
        c3.metric("Anomaly score", f"{res.anomaly_score:.4f}",
                  f"threshold {res.threshold:.4f}", delta_color="off")
        colour = {"LEGITIMATE": "green", "SUSPICIOUS": "orange", "THREAT": "red"}
        c4.markdown(
            f"**DECISION**<br><span style='color:{colour.get(res.decision,'grey')};"
            f"font-size:1.4rem;font-weight:700'>{res.decision}</span><br>"
            f"<small>{res.detected_attack}</small>",
            unsafe_allow_html=True,
        )

    st.divider()
    t_explain, t_measure, t_bloch, t_timeline, t_forensics = st.tabs(
        ["Explanation", "Measurements", "Quantum State", "Timeline", "Forensics"]
    )

    from security.threat_engine import ThreatEngine

    engine = ThreatEngine(runner.baseline)

    with t_explain:
        st.code(engine.explain(res), language="text")

    with t_measure:
        st.caption(
            "Per-element projective measurement. Counts are sampled from the "
            "state that actually arrived over the channel."
        )
        rows = [{
            "pos": e.position,
            "expected": e.expected_label,
            "basis": e.expected_basis.upper(),
            "exp. eigenvalue": e.expected_eigenvalue,
            "counts 0": e.counts.get("0", 0),
            "counts 1": e.counts.get("1", 0),
            "p0": round(e.p0, 4),
            "measured": e.measured_eigenvalue,
            "fidelity": round(e.fidelity, 4),
            "trace dist": round(e.trace_distance, 4),
            "purity": round(e.purity, 4),
            "match": "yes" if e.match else "NO",
        } for e in res.elements]
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

        b1, b2, b3 = st.columns(3)
        b1.metric("Trace distance", f"{res.telemetry.mean_trace_distance:.4f}")
        b2.metric("Purity", f"{res.telemetry.mean_purity:.4f}")
        b3.metric("Measurement entropy", f"{res.telemetry.measurement_entropy:.4f}")

        devs = {
            b.upper(): getattr(res.telemetry, f"{b}_deviation")
            for b in ("x", "y", "z")
        }
        shown = {k: v for k, v in devs.items() if v is not None}
        if shown:
            st.caption("Per-basis deviation from the expected distribution "
                       "(bases unused by this signature are omitted):")
            st.dataframe(
                pd.DataFrame([{"basis": k, "deviation": round(v, 4)}
                              for k, v in shown.items()]),
                width="stretch", hide_index=True,
            )

    with t_bloch:
        from dashboard.components.bloch_view import render_bloch_panel

        render_bloch_panel(res)

    with t_timeline:
        st.caption("Security event timeline. Anomalous stages are marked.")
        st.code(res.timeline(), language="text")

    with t_forensics:
        if res.decision == "LEGITIMATE":
            st.success("No incident: session verified cleanly.")
        st.code(engine.forensics(res), language="text")
