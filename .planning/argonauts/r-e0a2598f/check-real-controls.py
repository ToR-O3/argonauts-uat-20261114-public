"""Exercise actual package and separately damaged scratch copies, never live edits."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path.cwd()
out = root / ".planning/argonauts/r-e0a2598f"
checker = out / "check_quality_handoff.py"
relative = ".planning/argonauts/r-e0a2598f/quality-handoff.json"
source = json.loads((root / relative).read_text())
results = []
for kind, expected, diagnostic in [("valid", 0, "HANDOFF_READY_ONLY"), ("missing-original", 2, "original_missing"), ("stale-head", 2, "target_stale"), ("missing-obligation", 2, "obligation:Q6")]:
    with tempfile.TemporaryDirectory(prefix="real-handoff-control-") as temp:
        repo = Path(temp) / "repo"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", "--quiet", str(root), str(repo)], check=True)
        subprocess.run(["git", "read-tree", "HEAD"], cwd=repo, check=True)
        names = {row["path"] for group in ["manifest", "sources", "originals"] for row in source[group]}
        names.update([relative, source["handoff_text"], "openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md"])
        for name in names:
            target = repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / name, target)
        data = json.loads((repo / relative).read_text())
        if kind == "missing-original":
            (repo / ".planning/argonauts/r-e0a2598f/cli-captures.json").unlink()
        elif kind == "stale-head":
            data["target_head"] = data["baseline"]
        elif kind == "missing-obligation":
            data["obligations"].pop()
        (repo / relative).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        argv = [sys.executable, str(checker), "--repo-root", str(repo), "--handoff", relative]
        r = subprocess.run(argv, capture_output=True, timeout=30)
        (out / f"real-control-{kind}.txt").write_bytes(r.stdout + r.stderr)
        assert r.returncode == expected and diagnostic.encode() in r.stdout + r.stderr, (kind, r.stdout, r.stderr)
        results.append({"case": kind, "argv": argv, "exit": r.returncode, "expected_exit": expected, "diagnostic": diagnostic, "stdout": r.stdout.decode(), "stderr": r.stderr.decode(), "source_handoff_sha256": hashlib.sha256((root / relative).read_bytes()).hexdigest()})
(out / "real-package-controls.json").write_text(json.dumps(results, indent=2) + "\n")
print("Actual-package copy accepted; missing original, stale head and missing Q6 rejected with intended diagnostics")
