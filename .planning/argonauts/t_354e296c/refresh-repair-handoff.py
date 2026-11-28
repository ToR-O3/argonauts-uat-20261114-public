"""Refresh current content manifest, preserving old observations as historical."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path.cwd()
data_dir = root / ".planning/argonauts/r-e0a2598f"
repair = root / ".planning/argonauts/t_354e296c"
subprocess.run([sys.executable, str(data_dir / "prepare-handoff.py")], check=True)
path = data_dir / "quality-handoff.json"
data = json.loads(path.read_text())
files = ["CI-REPAIR.md", "shallow-red.txt", "shallow-green-final.txt", "shallow-suite.json",
         "shallow-suite-stdout.txt", "shallow-suite-stderr.txt", "exclude-repair-green.txt",
         "handoff-tests-repair.txt", "verification-status-repair.json", "state-repair.json"]
for name in files:
    original = repair / name
    data["originals"].append({"path": str(original.relative_to(root)), "sha256": hashlib.sha256(original.read_bytes()).hexdigest()})
info = json.loads((repair / "shallow-suite.json").read_text())
links = [str((repair / name).relative_to(root)) for name in ["CI-REPAIR.md", "shallow-suite.json", "shallow-suite-stdout.txt", "shallow-suite-stderr.txt"]]
data["executions"].append({"command": "python -m pytest (disconnected depth1 checkout)",
    "argv": info["argv"], "input": ["committed fixed historical raw Git objects; existing test suite and fixtures"],
    "environment": {"python": info["python"], "shallow": info["shallow"], "origin": info["origin"], "PYTHONPATH": "removed"},
    "stdout": (repair / "shallow-suite-stdout.txt").read_text(), "stderr": "", "exit": info["exit"],
    "expected_vs_actual": "1159 passed; baseline absent before/after; all original 64 comparisons retained; no skip", "originals": links})
data["ac_mapping"]["AC6"].extend(links)
data["repair_evidence"] = {"report": links[0], "previous_observations": "Historical originals retained; fresh repaired-target full-suite observation is the final execution record."}
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
text_path = data_dir / "quality-handoff.md"
text_path.write_text(text_path.read_text() + "\n## 品質差戻し後の浅い取得への対応\n\n" +
    "現在の内容対象は上のtarget。修正前の実測原本は履歴として保持。最新の全件確認はoriginを切断したdepth1 checkoutで1159件成功、固定commit欠落は実行前後とも確認。基準のGit object chainを同梱原本で認証するためfetch/skip/自己goldenを使わない。\n" +
    "必須のCI不具合だけ修正。記録のみのWR-01/WR-02/IN-01〜05は未変更。独立品質・OpenSpec3.2はpending。\n" +
    "\n".join("- " + row["path"] + " SHA-256 " + row["sha256"] for row in data["originals"] if row["path"].startswith(".planning/argonauts/t_354e296c/")) + "\n")
print("Current repair target", data["target_head"], "with actual shallow-suite original and pending quality")
