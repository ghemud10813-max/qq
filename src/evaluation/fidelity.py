"""
evaluation/fidelity.py
======================
Quantum state fidelity and trace distance calculations.

Implements from Phase 7. Measures how closely a received/reconstructed
quantum state matches the intended state — core metric for assessing
teleportation quality and attack degradation.

    Fidelity   F(ρ, σ) = (Tr √(√ρ σ √ρ))²   ∈ [0, 1]
    Trace dist T(ρ, σ) = ½ Tr|ρ - σ|         ∈ [0, 1]

Phase 0 status: stub only — no implementation.
No AI/ML libraries used.
"""

from __future__ import annotations

__all__: list[str] = ["state_fidelity", "trace_distance"]


def state_fidelity() -> None:
    """Compute fidelity between two quantum states.

    Raises
    ------
    NotImplementedError
        Until Phase 7 is implemented.
    """
    raise NotImplementedError("fidelity.state_fidelity — implemented in Phase 7.")


def trace_distance() -> None:
    """Compute trace distance between two quantum states.

    Raises
    ------
    NotImplementedError
        Until Phase 7 is implemented.
    """
    raise NotImplementedError("fidelity.trace_distance — implemented in Phase 7.")
