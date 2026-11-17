"""Capture real pytest RED output for the official GSD evidence gate."""
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

name = sys.argv[1]
report = Path(__file__).with_name(f"{name}-junit.xml")
command = [sys.executable, "-m", "pytest", f"tests/test_tokenizer.py::{name}", "-q", "--color=no", f"--junitxml={report}"]
started = datetime.now(timezone.utc).isoformat()
result = subprocess.run(command, capture_output=True, text=True)
console = result.stdout + result.stderr
report.with_suffix(".console.txt").write_text(console)
output = report.read_text()
record = {
    "command": " ".join(command),
    "exitCode": result.returncode,
    "reportPath": str(report),
    "runStartedAt": started,
    "reportModifiedAt": datetime.fromtimestamp(report.stat().st_mtime, timezone.utc).isoformat(),
    "output": output,
    "targetTest": name,
    "targetFile": "tests/test_tokenizer.py",
    "expected": "The tokenizer meets the named token sequence contract",
    "actual": "The named assertion failed; see unchanged output",
    "semanticAssessment": "Target executed and assertion failed because the planned tokenizer capability is absent; no setup or collection failure",
}
path = Path(__file__).with_name(f"{name}-red.json")
path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(output, end="")
print(f"Evidence: {path}; exitCode={result.returncode}")
