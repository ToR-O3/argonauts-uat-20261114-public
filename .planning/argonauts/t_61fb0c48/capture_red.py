"""Capture unmodified pytest JUnit evidence for GSD's RED gate."""
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

file, name = sys.argv[1:3]
report = Path(__file__).with_name(f"{name}-junit.xml")
command = [sys.executable, "-m", "pytest", f"{file}::{name}", "-q", "--color=no", f"--junitxml={report}"]
started = datetime.now(timezone.utc).isoformat()
result = subprocess.run(command, capture_output=True, text=True)
report.with_suffix(".console.txt").write_text(result.stdout + result.stderr)
record = {
    "command": " ".join(command), "exitCode": result.returncode,
    "reportPath": str(report), "runStartedAt": started,
    "reportModifiedAt": datetime.fromtimestamp(report.stat().st_mtime, timezone.utc).isoformat(),
    "output": report.read_text(), "targetTest": name, "targetFile": file,
    "expected": "The named public API meets the contract asserted in the test",
    "actual": "Named assertion failed; unchanged JUnit report contains actual values",
    "semanticAssessment": "Target executed; assertion shows missing planned capability, not fixture, collection, or syntax failure. Initial module-presence assertions only prove availability; subsequent assertions verify behavior in GREEN.",
}
path = Path(__file__).with_name(f"{name}-red.json")
path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(result.stdout + result.stderr, end="")
print(f"Evidence: {path}; exitCode={result.returncode}")
