"""
qds/verifier.py
===============
Quantum Digital Signature — signature verification.

Implements from Phase 3. Measures received quantum signature states in the
correct Pauli bases and computes a verification score against threshold.

Phase 0 status: stub only — no implementation.
No AI/ML libraries used.
"""

from __future__ import annotations

__all__: list[str] = ["verify_signature"]


def verify_signature() -> None:  # -> VerificationResult (Phase 3)
    """Verify a quantum signature against a public key.

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError("verifier.verify_signature — implemented in Phase 3.")
