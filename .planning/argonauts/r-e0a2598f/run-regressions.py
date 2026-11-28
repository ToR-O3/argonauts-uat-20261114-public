"""Capture the assigned task02 regression commands without synthesized reports."""
import json
from pathlib import Path
import subprocess
import sys

root = Path.cwd()
out = root / ".planning/argonauts/r-e0a2598f"
executions = []
for name, command in [
    ("exclude-final", ["uv", "run", "--extra", "dev", "python", "-m", "pytest", "tests/test_cli.py", "-q", "-x", "-k", "exclude"]),
    ("suite-final", ["uv", "run", "--extra", "dev", "python", "-m", "pytest", "-q"]),
]:
    result = subprocess.run(command, capture_output=True, cwd=root, timeout=360)
    (out / f"{name}-stdout.txt").write_bytes(result.stdout)
    (out / f"{name}-stderr.txt").write_bytes(result.stderr)
    executions.append({"command": " ".join(command), "argv": command, "input": ["repository tests and tmp_path fixtures"],
                       "environment": {"runner": "existing uv dev extra; see captures for actual CLI environment"},
                       "stdout": result.stdout.decode(), "stderr": result.stderr.decode(), "exit": result.returncode,
                       "expected_vs_actual": "expected exit0 with nonzero collected cases; actual output captured verbatim",
                       "originals": [f".planning/argonauts/r-e0a2598f/{name}-stdout.txt", f".planning/argonauts/r-e0a2598f/{name}-stderr.txt"]})
    print(name, result.returncode, result.stdout.decode(), result.stderr.decode())
    if result.returncode:
        sys.exit(result.returncode)
(out / "regression-executions.json").write_text(json.dumps(executions, indent=2) + "\n")
