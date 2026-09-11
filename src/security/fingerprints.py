"""
security/fingerprints.py
========================
Quantum state fingerprinting from measurement distributions.

Implements from Phase 4. A fingerprint is a compact, deterministic
representation of a quantum state's measurement statistics across all
three Pauli bases (X, Y, Z), used as the reference for anomaly detection.

Phase 0 status: stub only — no implementation.
No AI/ML libraries used.
"""

from __future__ import annotations

__all__: list[str] = ["build_fingerprint", "compare_fingerprints"]


def build_fingerprint() -> None:
    """Build a quantum state fingerprint from multi-basis measurement counts.

    Raises
    ------
    NotImplementedError
        Until Phase 4 is implemented.
    """
    raise NotImplementedError("fingerprints.build_fingerprint — Phase 4.")


def compare_fingerprints() -> None:
    """Compare two fingerprints and return a similarity score.

    Raises
    ------
    NotImplementedError
        Until Phase 4 is implemented.
    """
    raise NotImplementedError("fingerprints.compare_fingerprints — Phase 4.")
