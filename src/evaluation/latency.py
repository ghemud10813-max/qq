"""
evaluation/latency.py
=====================
Circuit execution and end-to-end timing benchmarks.

Implements from Phase 7. Measures wall-clock and CPU time for:
    - Qiskit circuit transpilation
    - Aer simulator job execution
    - Full QDS sign + verify cycle
    - Threat detection pipeline

Phase 0 status: stub only — no implementation.
No AI/ML libraries used.
"""

from __future__ import annotations

__all__: list[str] = ["time_circuit_execution", "time_qds_cycle"]


def time_circuit_execution() -> None:
    """Measure execution time of a single Qiskit circuit on Aer.

    Raises
    ------
    NotImplementedError
        Until Phase 7 is implemented.
    """
    raise NotImplementedError("latency.time_circuit_execution — implemented in Phase 7.")


def time_qds_cycle() -> None:
    """Measure end-to-end latency of a full QDS sign-then-verify cycle.

    Raises
    ------
    NotImplementedError
        Until Phase 7 is implemented.
    """
    raise NotImplementedError("latency.time_qds_cycle — implemented in Phase 7.")
