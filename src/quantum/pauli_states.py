"""
quantum/pauli_states.py
=======================
Pauli eigenstate preparation circuits.

Implements from Phase 3. Prepares the six Pauli eigenstates used as the
quantum key material in the QDS scheme:

    +X  |+⟩ = (|0⟩ + |1⟩) / √2     (H|0⟩)
    -X  |-⟩ = (|0⟩ - |1⟩) / √2     (H|1⟩)
    +Y  |i⟩ = (|0⟩ + i|1⟩) / √2    (HS†|0⟩  or SH|0⟩ depending on convention)
    -Y  |-i⟩= (|0⟩ - i|1⟩) / √2
    +Z  |0⟩                          (computational basis 0)
    -Z  |1⟩                          (computational basis 1)

Phase 0 status: stub only — no implementation.
No AI/ML libraries used.
"""

from __future__ import annotations

__all__: list[str] = [
    "prepare_plus_x",
    "prepare_minus_x",
    "prepare_plus_y",
    "prepare_minus_y",
    "prepare_plus_z",
    "prepare_minus_z",
]


def prepare_plus_x() -> None:
    """Prepare |+⟩ (positive X eigenstate).

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError("pauli_states.prepare_plus_x — implemented in Phase 3.")


def prepare_minus_x() -> None:
    """Prepare |-⟩ (negative X eigenstate).

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError("pauli_states.prepare_minus_x — implemented in Phase 3.")


def prepare_plus_y() -> None:
    """Prepare |i⟩ (positive Y eigenstate).

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError("pauli_states.prepare_plus_y — implemented in Phase 3.")


def prepare_minus_y() -> None:
    """Prepare |-i⟩ (negative Y eigenstate).

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError("pauli_states.prepare_minus_y — implemented in Phase 3.")


def prepare_plus_z() -> None:
    """Prepare |0⟩ (positive Z eigenstate).

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError("pauli_states.prepare_plus_z — implemented in Phase 3.")


def prepare_minus_z() -> None:
    """Prepare |1⟩ (negative Z eigenstate).

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError("pauli_states.prepare_minus_z — implemented in Phase 3.")
