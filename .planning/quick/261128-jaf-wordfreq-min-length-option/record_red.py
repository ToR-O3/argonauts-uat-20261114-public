"""Package unchanged actual JUnit reports for the official RED classifier."""
import json
import os
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
name, target, expected, actual = sys.argv[1:]
report = root / f"{name}.xml"
record = {
    "command": f"{os.environ['PY']} -m pytest tests/test_cli.py -k {target.removeprefix('test_')} -q" + (" -s" if name.startswith("tracer") else "") + f" --junitxml={os.environ['Q']}/{name}.xml",
    "exitCode": 1,
    "output": report.read_text(encoding="utf-8"),
    "targetTest": target,
    "targetFile": "tests/test_cli.py",
    "expected": expected,
    "actual": actual,
    "reportPath": str(report),
    "reportModifiedAt": report.stat().st_mtime,
    "semanticAssessment": "Named test executed and failed on the planned missing behavior; no collection, import or setup failure. See unchanged XML and console log.",
}
(root / f"{name}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
