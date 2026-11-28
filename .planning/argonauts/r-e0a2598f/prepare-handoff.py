"""Assemble real Builder observations; fixture helper only projects source inventories."""
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("handoff_schema", Path(__file__).with_name("test_quality_handoff.py"))
assert spec is not None and spec.loader is not None
schema = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schema)

root = Path.cwd()
out = root / schema.DATA
data = schema.make_package(root)
data["originals"] = []
original_names = ["builder-evidence.md", "baseline-captures.json", "cli-captures.json", "baseline-controls.json", "integration-green.xml", "suite-green.xml", "checker-green.txt", "regression-executions.json", "exclude-final-stdout.txt", "exclude-final-stderr.txt", "suite-final-stdout.txt", "suite-final-stderr.txt"]
for name in original_names:
    path = f"{schema.DATA}/{name}"
    data["originals"].append({"path": path, "sha256": schema.digest(root / path)})
data["executions"] = json.loads((out / "regression-executions.json").read_text())
base = json.loads((out / "baseline-captures.json").read_text())
data["interpreter"] = {"path": base["interpreter"], "version": base["version"]}
data["environment"] = base["environment"]
for case in base["cases"]:
    for role in ["historical", "candidate"]:
        result = case[role]
        data["executions"].append({"command": " ".join(result["argv"]), "argv": result["argv"], "input": [{"path": case["input_path"], "hex": case["input_hex"]}],
                                   "environment": base["environment"], "stdout": result["stdout"], "stderr": result["stderr"], "exit": result["exit"],
                                   "expected_vs_actual": case["expected_vs_actual"], "originals": [f"{schema.DATA}/baseline-captures.json"]})
cli = json.loads((out / "cli-captures.json").read_text())
for case in cli["cases"]:
    result = case["result"]
    data["executions"].append({"command": " ".join(result["argv"]), "argv": result["argv"], "input": [{"body_hex": case["body_hex"], "exclusion_hex": case["exclusion_hex"]}],
                               "environment": cli["environment"], "stdout": result["stdout"], "stderr": result["stderr"], "exit": result["exit"],
                               "expected_vs_actual": case["expected_vs_actual"], "originals": [f"{schema.DATA}/cli-captures.json"]})
data["ac_mapping"] = {f"AC{i}": [f"{schema.DATA}/builder-evidence.md", f"{schema.DATA}/suite-final-stdout.txt", f"{schema.DATA}/cli-captures.json"] for i in range(1, 7)}
data["ac_mapping"]["AC5"].append(f"{schema.DATA}/integration-green.xml")
data["ac_mapping"]["AC6"].extend([f"{schema.DATA}/baseline-captures.json", f"{schema.DATA}/baseline-controls.json"])
(out / "quality-handoff.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
lines = ["# 品質担当への引渡し — 独立検証は未実施", "",
         "Builder原本と対象の内容を検査した引渡しです。独立品質・フェーズ・PMの合格ではありません。OpenSpec3.2は未完です。",
         "", f"初期の製品内容対象: `{data['target_head']}`。依頼branch: `{data['branch']}`。固定過去版と依頼起点: `{data['baseline']}`。",
         "報告ファイルは自分自身のcommit hashを持てません。checkerは最新の製品/試験/README/pyproject変更commitをtargetとして固定し、その全Git bytesと現在のworktreeを照合します。報告だけの後続commitは許可しますが、品質のexact-head合格を引き継ぐものではありません。品質は報告時の実HEADを新しく解決し、必要な検査を独立再実行してください。",
         "", "## 実行コマンド（repo直下）", "```sh", *data["commands"],
         "python3 -m unittest discover -s .planning/argonauts/r-e0a2598f -p test_quality_handoff.py -v",
         "python3 .planning/argonauts/r-e0a2598f/check_quality_handoff.py --repo-root . --handoff .planning/argonauts/r-e0a2598f/quality-handoff.json", "```",
         "", "## 読む原本", *["- " + p for p in schema.CANON],
         "- _bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md",
         "- _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md",
         "- _bmad-output/initiative-r-e0a2598f/architecture/architecture.md",
         "- openspec/changes/r-e0a2598f-wordfreq-exclude/{proposal.md,design.md,specs/wordfreq-cli/spec.md,tasks.md}",
         "", "## Builder文字原本", *["- " + row["path"] + " SHA-256 " + row["sha256"] for row in data["originals"]],
         "", "全6ACとREQ/FR/RULE/AD/EXへの根拠はbuilder-evidence.md。全26edge/14UI/2prohibitionと各predicate/source/dispositionはJSONに個別記録し、checkerがPLAN/raw probeから独立導出して比較します。5 concurrency backstopはhuman_needed/insufficient_spec、descriptor-less禁止2件はflagged-unverifiedを保持します。画像閲覧0枚、geometry/可読性/実通信は新規実測していません。未確認をgreenにしません。",
         "", "## 後続品質の全義務（原本をそのまま転記、すべてpending）",
         *[row["statement"] for row in data["obligations"]],
         "", "## 実在する公式手順（参照のみ、Builderは実行しない）",
         *[f"- {row['id']}: {row['path']} (SHA-256 {row['sha256']})" for row in data["procedures"]],
         "GSDは公式execute-phaseの検証経路（verify:post/security→code-review→regression→verifier→fingerprint→verification.status）を品質が実行。OpenSpecはstatus/instructions applyから完全性・正確性・整合性を品質が確認。公式ランチャーは同じ端末内のgsd_run関数からshで起動し、gsd-tools.cjs直実行はしません。",
         "後続成果物: .planning/phases/08-wordfreq-exclude/08-VERIFICATION.md、.planning/argonauts/r-e0a2598f/quality-evidence.md と読みやすい文字原本。品質は標準添付とSHA-256照合で配送し、PMが条件ごとにread_fileできる索引を渡します。後続品質をこのBuilderから起動/予約しません。archive/最終化/PR ready/マージは対象外。"]
(out / "quality-handoff.md").write_text("\n".join(lines) + "\n")
print("Prepared actual pending-quality handoff", data["target_head"], "executions", len(data["executions"]))
