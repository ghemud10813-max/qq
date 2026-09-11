import subprocess
import sys

with open("exp_p7_utf8.txt", "w", encoding="utf-8") as f:
    p = subprocess.run([sys.executable, "experiments/phase7_performance.py"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    f.write(p.stdout)
    f.write(p.stderr)
    
print("Proxy execution finished")
