import io
import json
import time
import unittest
from pathlib import Path

from diagnostics.network_diagnostics import collect_linux_network_state

ROOT = Path(__file__).parent
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

suite = unittest.defaultTestLoader.discover("tests", pattern="test_*.py")

buffer = io.StringIO()
start = time.perf_counter()
result = unittest.TextTestRunner(stream=buffer, verbosity=2).run(suite)
elapsed = time.perf_counter() - start

text_output = buffer.getvalue()
print(text_output)

total = result.testsRun
failed = len(result.failures)
errors = len(result.errors)
passed = total - failed - errors
pass_rate = round((passed / total) * 100, 1) if total else 0.0

summary = {
    "total_tests": total,
    "passed": passed,
    "failed": failed,
    "errors": errors,
    "pass_rate": pass_rate,
    "duration_seconds": round(elapsed, 3),
    "network_diagnostics": collect_linux_network_state(),
}

summary_text = f"""
========================================
 Linux Network Validation Framework
========================================
Total tests : {total}
Passed      : {passed}
Failed      : {failed}
Errors      : {errors}
Pass rate   : {pass_rate}%
Duration    : {elapsed:.3f}s
========================================
"""

print(summary_text)

(REPORT_DIR / "test_report.txt").write_text(
    text_output + "\n" + summary_text,
    encoding="utf-8"
)

(REPORT_DIR / "test_report.json").write_text(
    json.dumps(summary, indent=2),
    encoding="utf-8"
)

print(f"Reports saved to: {REPORT_DIR}")
raise SystemExit(0 if result.wasSuccessful() else 1)
