"""
qds -- Quantum Digital Signature package.

Phase 3 -- SIH26141 | Blockchain & Cybersecurity.

Modules
-------
pauli_states  : Six Pauli eigenstates, projectors, measurement (Phase 3)
signature     : QDS signature generation, SignatureElement, QDSSignature (Phase 3)
verification  : Projective verification, VerificationResult, accept/reject (Phase 3)
keygen        : Key-generation stub (Phase 3+)
signer        : Signing stub (Phase 3+)
verifier      : Verifier stub (Phase 3+)
scheme        : High-level scheme stub (Phase 3+)
"""

# ----- Phase 3: Pauli eigenstates -----
from qds.pauli_states import (
    SIGMA_X,
    SIGMA_Y,
    SIGMA_Z,
    IDENTITY,
    PAULI_MATRICES,
    PROJECTOR_PLUS,
    PROJECTOR_MINUS,
    EIGENSTATE_LABELS,
    PauliEigenstate,
    make_ket_0,
    make_ket_1,
    make_ket_plus,
    make_ket_minus,
    make_ket_plus_i,
    make_ket_minus_i,
    get_eigenstate,
    all_eigenstates,
    projective_measurement_probs,
    measure_eigenstate,
    validate_statevector_norm,
    validate_eigenvalue_equation,
)

# ----- Phase 3: Signature -----
from qds.signature import (
    SignatureElement,
    QDSSignature,
    DEFAULT_SIGNATURE_LENGTH,
    generate_signature,
    signature_summary,
)

# ----- Phase 3: Verification -----
from qds.verification import (
    ElementVerificationResult,
    VerificationResult,
    DEFAULT_ACCEPT_THRESHOLD,
    verify_element,
    verify_signature,
)

__all__: list[str] = [
    # pauli_states
    "SIGMA_X", "SIGMA_Y", "SIGMA_Z", "IDENTITY",
    "PAULI_MATRICES", "PROJECTOR_PLUS", "PROJECTOR_MINUS",
    "EIGENSTATE_LABELS",
    "PauliEigenstate",
    "make_ket_0", "make_ket_1", "make_ket_plus", "make_ket_minus",
    "make_ket_plus_i", "make_ket_minus_i",
    "get_eigenstate", "all_eigenstates",
    "projective_measurement_probs", "measure_eigenstate",
    "validate_statevector_norm", "validate_eigenvalue_equation",
    # signature
    "SignatureElement", "QDSSignature",
    "DEFAULT_SIGNATURE_LENGTH",
    "generate_signature", "signature_summary",
    # verification
    "ElementVerificationResult", "VerificationResult",
    "DEFAULT_ACCEPT_THRESHOLD",
    "verify_element", "verify_signature",
]
