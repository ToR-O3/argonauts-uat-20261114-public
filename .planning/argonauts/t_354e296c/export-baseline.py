"""Export only the fixed commit's authenticated wordfreq object closure."""
import base64
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASELINE = "79d83ba14dd59d289d2ecd3e33c85e8de437972e"

def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout

root_tree = git("rev-parse", BASELINE + "^{tree}").decode().strip()
package_tree = git("rev-parse", BASELINE + ":wordfreq").decode().strip()
objects = [("commit", BASELINE), ("tree", root_tree), ("tree", package_tree)]
for line in git("ls-tree", "-r", BASELINE, "--", "wordfreq").decode().splitlines():
    mode, kind, oid_name = line.split(" ", 2)
    oid, name = oid_name.split("\t", 1)
    assert mode == "100644" and kind == "blob" and name.endswith(".py")
    objects.append((kind, oid))
data = {"commit": BASELINE, "objects": [
    {"type": kind, "oid": oid, "base64": base64.b64encode(git("cat-file", kind, oid)).decode("ascii")}
    for kind, oid in objects
]}
path = ROOT / "tests/fixtures/exclude-baseline-git-objects.json"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
print(path, len(data["objects"]), path.stat().st_size)
