import subprocess
import sys

with open("test_err_utf8.txt", "w", encoding="utf-8") as f:
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests/evaluation/"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    f.write(p.stdout)
    f.write(p.stderr)
    
p2 = subprocess.run([sys.executable, "experiments/phase6_security_evaluation.py"], capture_output=True, text=True, encoding="utf-8", errors="replace")
with open("exp_err_utf8.txt", "w", encoding="utf-8") as f:
    f.write(p2.stdout)
    f.write(p2.stderr)
