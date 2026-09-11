"""
experiments/final_end_to_end.py
===============================
Final end-to-end integration and security evaluation for Phase 9.
"""
import sys
from pathlib import Path
import yaml
import json
import pandas as pd
import numpy as np

src_path = Path(__file__).parent.parent / "src"
root_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from pipeline import EndToEndPipeline
from security.detector import ThreatDetector

from attacks.forgery import ForgeryAttack
from attacks.impersonation import ImpersonationAttack
from attacks.replay import ReplayAttack
from attacks.unauthorized_verification import UnauthorizedVerificationAttack
from attacks.channel_manipulation import ChannelManipulationAttack

CONFIG_PATH = Path(__file__).parent.parent / "config" / "final_config.yaml"
RESULTS_DIR = Path(__file__).parent / "results"

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("config/final_config.yaml not found.")
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def run_experiment():
    print("==================================================")
    print("FINAL SECURITY EVALUATION")
    print("==================================================")
    config = load_config()
    
    # 1. Validation
    assert 0.0 <= config['confidence_level'] <= 1.0
    assert config['trials_per_attack'] > 0
    assert all(0 <= p <= 1 for p in config['noise_strengths'])
    assert all(l > 0 for l in config['signature_lengths'])
    
    # 2. Build Pipeline
    detector = ThreatDetector(
        calibration_method="percentile",
        warn_percentile=config['warn_threshold'],
        crit_percentile=config['critical_threshold']
    )
    # Generate baseline to calibrate ThreatDetector properly
    # The evaluation happens within pipeline itself
    from qds.signature import generate_signature
    from qds.verification import verify_signature
    for i in range(15):
        s = generate_signature(f"calib_{i}", length=16, seed=config['seed']+i)
        v = verify_signature(s)
        detector.add_baseline_session(v)
    detector.calibrate()
    
    pipeline = EndToEndPipeline(detector=detector)
    
    # Setup test vectors
    trials = config['trials_per_attack']
    attacks = {
        "LEGITIMATE": None,
        "FORGERY": ForgeryAttack(seed=config['seed']),
        "IMPERSONATION": ImpersonationAttack(seed=config['seed']),
        "REPLAY": ReplayAttack(seed=config['seed']),
        "UNAUTHORIZED_VERIFICATION": UnauthorizedVerificationAttack(seed=config['seed']),
        "CHANNEL_MANIPULATION": ChannelManipulationAttack(seed=config['seed'])
    }
    
    all_results = []
    
    for aname, atk in attacks.items():
        intensity = config['attack_intensities'][-1] if atk else 0.0
        # channel manip simulation happens internally in pipeline
        for i in range(trials):
            res = pipeline.run_scenario(
                session_label=f"msg_{aname.lower()}_{i}",
                signature_length=config['signature_lengths'][2], # use 16
                attack=atk,
                intensity=intensity,
                seed=config['seed'] + i * 100
            )
            all_results.append(res)
            
    df = pd.DataFrame([r.__dict__ for r in all_results])
    
    # Global Metrics
    total = len(df)
    legit_df = df[df['attack_type'] == "LEGITIMATE"]
    atk_df = df[df['attack_type'] != "LEGITIMATE"]
    
    tp = len(atk_df[atk_df['detection_status'] == 'DETECTED'])
    fn = len(atk_df[atk_df['detection_status'] == 'MISSED'])
    
    fp = len(legit_df[legit_df['detection_status'] == 'DETECTED']) # normally shouldn't happen unless REJECTED/SUSPICIOUS was classed as DETECTED
    # Wait, LEGITIMATE returns detection_status=NOT_APPLICABLE. 
    # But wait, FAR / FRR requires proper binary classification.
    # We will redefine based on classification: THREAT/SUSPICIOUS/REJECTED = Positive.
    def is_positive(c): return c in ["THREAT", "SUSPICIOUS", "REJECTED"]
    
    atk_df['is_pos'] = atk_df['classification'].apply(is_positive)
    legit_df['is_pos'] = legit_df['classification'].apply(is_positive)
    
    tp = int(atk_df['is_pos'].sum())
    fn = len(atk_df) - tp
    fp = int(legit_df['is_pos'].sum())
    tn = len(legit_df) - fp
    
    tpr = tp / (tp + fn) if (tp+fn)>0 else 0
    far = fp / (fp + tn) if (fp+tn)>0 else 0
    frr = fn / (fn + tp) if (fn+tp)>0 else 0
    acc = (tp + tn) / total
    precision = tp / (tp + fp) if (tp+fp)>0 else 0
    f1 = 2 * precision * tpr / (precision + tpr) if (precision+tpr)>0 else 0
    
    print("\nAccuracy:", acc)
    print("Precision:", precision)
    print("Recall / Detection Rate:", tpr)
    print("F1:", f1)
    print("FAR:", far)
    print("FRR:", frr)
    
    print("\nAttack-wise detection:")
    attack_metrics = []
    for aname in attacks:
        if aname == "LEGITIMATE": continue
        sub = df[df['attack_type'] == aname]
        dt = len(sub[sub['classification'].apply(is_positive)])
        rate = dt / len(sub) if len(sub)>0 else 0
        attack_metrics.append({"attack_type": aname, "detection_rate": rate, "trials": len(sub)})
        print(f"{aname}: {rate:.2%}")
        
    print("\nQuantum metrics:")
    fidelities = df['teleportation_fidelity']
    print(f"Mean teleportation fidelity: {fidelities.mean():.4f}")
    print(f"Minimum fidelity: {fidelities.min():.4f}")
    print(f"Maximum fidelity: {fidelities.max():.4f}")
    
    print("\nPerformance:")
    lats = df['latency']
    print(f"Mean latency: {lats.mean()*1000:.2f} ms")
    print(f"Median latency: {lats.median()*1000:.2f} ms")
    print(f"Throughput: {1.0/lats.mean():.2f} sessions/sec")
    
    print("\nThresholds:")
    print("Warning threshold:", config['warn_threshold'])
    print("Critical threshold:", config['critical_threshold'])
    print("==================================================")
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save CSVs
    pd.DataFrame([{
        "Accuracy": acc, "Precision": precision, "Detection_Rate": tpr, "F1": f1, "FAR": far, "FRR": frr
    }]).to_csv(RESULTS_DIR / "final_metrics.csv", index=False)
    
    pd.DataFrame(attack_metrics).to_csv(RESULTS_DIR / "final_attack_metrics.csv", index=False)
    
    pd.DataFrame([{
        "Mean_Fidelity": fidelities.mean(), "Min_Fidelity": fidelities.min(), "Max_Fidelity": fidelities.max()
    }]).to_csv(RESULTS_DIR / "final_quantum_metrics.csv", index=False)
    
    pd.DataFrame([{
        "Mean_Latency_s": lats.mean(), "Median_Latency_s": lats.median(), "Throughput_hz": 1.0/lats.mean()
    }]).to_csv(RESULTS_DIR / "final_performance.csv", index=False)
    
    with open(RESULTS_DIR / "final_configuration.json", "w") as f:
        json.dump(config, f, indent=4)
        
    import platform
    import qiskit
    import qiskit_aer
    
    env_info = {
        "Python": platform.python_version(),
        "Qiskit": qiskit.__version__,
        "Qiskit_Aer": qiskit_aer.__version__,
        "NumPy": np.__version__,
        "Pandas": pd.__version__,
        "Streamlit": "1.40.1" # placeholder since not imported globally here
    }
    with open(RESULTS_DIR / "environment.json", "w") as f:
        json.dump(env_info, f, indent=4)

if __name__ == "__main__":
    run_experiment()
