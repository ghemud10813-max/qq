import subprocess
import sys

with open("test_err_utf8.txt", "w", encoding="utf-8") as f:
    p = subprocess.run([sys.executable, "-m", "pytest", "-v", "tests/security/test_calibration.py", "tests/evaluation/test_threshold_optimization.py"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    f.write(p.stdout)
    f.write(p.stderr)
