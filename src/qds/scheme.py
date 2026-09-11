"""
qds/scheme.py
=============
Quantum Digital Signature — high-level scheme orchestration.

Implements from Phase 3. Combines keygen → sign → verify into a single
``QDSScheme`` class that manages state across the full signature lifecycle.

Phase 0 status: stub only — no implementation.
No AI/ML libraries used.
"""

from __future__ import annotations

__all__: list[str] = ["QDSScheme"]


class QDSScheme:
    """High-level orchestrator for the Quantum Digital Signature scheme.

    Instantiated and used from Phase 3 onwards.
    """

    def __init__(self) -> None:
        raise NotImplementedError("QDSScheme — implemented in Phase 3.")
