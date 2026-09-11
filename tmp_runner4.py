import subprocess
import sys

with open("test_p7_utf8.txt", "w", encoding="utf-8") as f:
    p = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", 
         "tests/evaluation/test_complexity.py", 
         "tests/evaluation/test_performance.py", 
         "tests/evaluation/test_scalability.py"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    f.write(p.stdout)
    f.write(p.stderr)
print("Finished proxy test run")
