"""
qds/keygen.py
=============
Quantum Digital Signature — key generation.

Implements from Phase 3. Generates private/public key pairs by preparing
sequences of Pauli eigenstate circuits that encode the signer's key material
into quantum states.

Phase 0 status: stub only — no implementation.
No AI/ML libraries used.
"""

from __future__ import annotations

__all__: list[str] = ["generate_key_pair"]


def generate_key_pair() -> None:  # -> tuple[PrivateKey, PublicKey] (Phase 3)
    """Generate a QDS private/public key pair.

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError("keygen.generate_key_pair — implemented in Phase 3.")
