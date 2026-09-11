import subprocess
import sys

with open("exp_err_utf8.txt", "w", encoding="utf-8") as f:
    p = subprocess.run([sys.executable, "experiments/phase65_detector_hardening.py"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    f.write(p.stdout)
    f.write(p.stderr)
    
print("Proxy execution finished")
