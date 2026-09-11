"""
quantum/measurements.py
=======================
Quantum measurement helpers in X, Y, and Z Pauli bases.

Implements from Phase 3. Adds basis-rotation gates before standard
computational-basis measurement so Qiskit Aer can project onto any
desired Pauli eigenspace.

    Z-basis : measure directly (no rotation needed)
    X-basis : apply H before measurement
    Y-basis : apply S†H (or HS) before measurement

Phase 0 status: stub only — no implementation.
No AI/ML libraries used.
"""

from __future__ import annotations

__all__: list[str] = [
    "measure_in_basis",
    "add_x_basis_measurement",
    "add_y_basis_measurement",
    "add_z_basis_measurement",
]


def measure_in_basis() -> None:  # -> QuantumCircuit (Phase 3)
    """Add measurement gates for a specified Pauli basis.

    Parameters (Phase 3)
    --------------------
    circuit : qiskit.QuantumCircuit
        Circuit to which measurement is appended.
    qubit : int
        Target qubit index.
    basis : str
        One of ``'x'``, ``'y'``, ``'z'``.

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError(
        "measurements.measure_in_basis — implemented in Phase 3."
    )


def add_x_basis_measurement() -> None:
    """Rotate qubit into Z basis from X basis and measure.

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError(
        "measurements.add_x_basis_measurement — implemented in Phase 3."
    )


def add_y_basis_measurement() -> None:
    """Rotate qubit into Z basis from Y basis and measure.

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError(
        "measurements.add_y_basis_measurement — implemented in Phase 3."
    )


def add_z_basis_measurement() -> None:
    """Measure qubit directly in the computational (Z) basis.

    Raises
    ------
    NotImplementedError
        Until Phase 3 is implemented.
    """
    raise NotImplementedError(
        "measurements.add_z_basis_measurement — implemented in Phase 3."
    )
