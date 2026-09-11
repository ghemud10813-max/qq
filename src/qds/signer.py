"""
qds/signer.py
=============
Quantum Digital Signature — message signing.

Implements from Phase 3. Encodes a message hash into Pauli eigenstate
sequences and produces a quantum signature (list of prepared circuits).

Phase 0 status: stub only — no implementation.
No AI/ML libraries used.
"""

from __future__ import annotations

__all__: list[str] = ["sign_message"]


def sign_message() -> None:  # -> QuantumSignature (Phase 3)
    """Sign a message using the signer's private key.

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError("signer.sign_message — implemented in Phase 3.")
