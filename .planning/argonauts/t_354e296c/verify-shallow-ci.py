"""Run the unchanged CI test command in an isolated depth-one checkout."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path.cwd()
out = root / ".planning/argonauts/t_354e296c"
with tempfile.TemporaryDirectory(prefix="shallow-ci-") as temp:
    repo = Path(temp) / "repo"
    subprocess.run(["git", "clone", "--no-local", "--depth", "1", str(root), str(repo)], check=True, capture_output=True)
    shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=repo, capture_output=True, check=True).stdout
    absent = subprocess.run(["git", "cat-file", "-e", "79d83ba14dd59d289d2ecd3e33c85e8de437972e"], cwd=repo, capture_output=True)
    assert shallow == b"true\n" and absent.returncode != 0
    shutil.copy2(root / "tests/test_cli.py", repo / "tests/test_cli.py")
    shutil.copytree(root / "tests/fixtures", repo / "tests/fixtures", dirs_exist_ok=True)
    # A disconnected origin makes accidental remote acquisition fail immediately.
    subprocess.run(["git", "remote", "set-url", "origin", str(Path(temp) / "absent-origin")], cwd=repo, check=True)
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    argv = [sys.executable, "-m", "pytest"]
    result = subprocess.run(argv, cwd=repo, env=env, capture_output=True, timeout=480)
    (out / "shallow-suite-stdout.txt").write_bytes(result.stdout)
    (out / "shallow-suite-stderr.txt").write_bytes(result.stderr or b"(empty stderr)\n")
    after = subprocess.run(["git", "cat-file", "-e", "79d83ba14dd59d289d2ecd3e33c85e8de437972e"], cwd=repo, capture_output=True)
    info = {"argv": argv, "cwd": str(repo), "python": sys.version, "shallow": shallow.decode().strip(),
            "baseline_absent_before": absent.returncode, "baseline_absent_after": after.returncode,
            "origin": "disconnected local path", "exit": result.returncode,
            "stdout": str(out / "shallow-suite-stdout.txt"), "stderr": str(out / "shallow-suite-stderr.txt")}
    (out / "shallow-suite.json").write_text(json.dumps(info, indent=2) + "\n")
    print(result.stdout.decode())
    print(info)
    assert result.returncode == 0 and after.returncode != 0
