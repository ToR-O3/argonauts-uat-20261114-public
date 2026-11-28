"""Process-only controls: fixture observations are NOT product/quality evidence."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).parent
CHECKER = HERE / "check_quality_handoff.py"
PHASE = ".planning/phases/08-wordfreq-exclude"
DATA = ".planning/argonauts/r-e0a2598f"
CANON = [f"{PHASE}/08-{n:02}-PLAN.md" for n in (1, 2, 3)] + [
    f"{PHASE}/08-UI-SPEC.md", ".planning/argonauts/t_b046d7f7-edge-probe.json",
    ".planning/argonauts/t_b046d7f7-ui-probe.json"]
PROCEDURES = {
    "gsd": str(Path.home() / ".hermes/profiles/argonauts-uat-builder/gsd-core/workflows/execute-phase/steps/verify-phase-goal.md"),
    "openspec": str(Path.home() / ".hermes/plugin-data/agent-plugin-argonauts-55aeafc7/openspec/.agents/skills/openspec-verify-change/SKILL.md"),
}


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=True).stdout


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventories(root):
    """Independently project identities/predicates from actual approved originals."""
    predicates = {}
    prohibitions = []
    for n in (1, 2, 3):
        path = f"{PHASE}/08-{n:02}-PLAN.md"
        for line in (root / path).read_text().splitlines():
            value = line.strip()
            for prefix in ["- statement: '", "- '"]:
                if value.startswith(prefix):
                    text = value[len(prefix):].removesuffix("'")
                    if text.startswith(("REQ-", "UI-E")) and ": " in text:
                        key = text.split(": ", 1)[0]
                        predicates[key] = (text, path)
                    elif text.startswith("P-08-"):
                        prohibitions.append({"key": text.split(":", 1)[0], "predicate": text, "source": path, "disposition": "flagged-unverified"})
                    break
    result = {"prohibitions": prohibitions}
    for kind, filename, prefix in [
        ("edges", "t_b046d7f7-edge-probe.json", ""),
        ("ui", "t_b046d7f7-ui-probe.json", "UI-"),
    ]:
        probe = json.loads((root / ".planning/argonauts" / filename).read_text())
        rows = []
        for item in probe["items"]:
            key = prefix + item["requirement_id"] + "/" + item["category"]
            text, source = predicates[key]
            disposition = "human_needed/insufficient_spec" if key.endswith("/concurrency") else "pending-independent-quality"
            rows.append({"key": key, "predicate": text, "source": source, "disposition": disposition})
        result[kind] = rows
    result["trace"] = [{"key": key, "source": source, "disposition": "pending-independent-quality"} for family, first, end, source in [
        ("REQ", 28, 34, ".planning/REQUIREMENTS.md"),
        ("FR", 1, 8, "_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md"),
        ("RULE", 1, 5, "_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md"),
        ("AD", 1, 5, "_bmad-output/initiative-r-e0a2598f/architecture/architecture.md"),
        ("EX", 1, 6, "openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md"),
        ("AC", 1, 7, f"{PHASE}/08-03-PLAN.md"),
    ] for key in [f"{family}-{i}" if family != "AC" else f"AC{i}" for i in range(first, end)]]
    return result


def obligations(root):
    text = (root / PHASE / "08-03-PLAN.md").read_text()
    section = text.split("## Mandatory later independent quality phase-verification card", 1)[1].split("<threat_model>", 1)[0]
    return [{"id": f"Q{i}", "statement": next(line for line in section.splitlines() if line.startswith(f"{i}. ")), "status": "pending"} for i in range(1, 7)]


def make_package(root):
    head = git(root, "log", "-1", "--format=%H", "--", "wordfreq", "tests", "README.md", "pyproject.toml").decode().strip()
    names = git(root, "ls-tree", "-rz", "--name-only", head, "--", "wordfreq", "tests", "README.md", "pyproject.toml").decode().strip("\0").split("\0")
    original = f"{DATA}/builder-evidence.md"
    sources = CANON + [".planning/REQUIREMENTS.md", "_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md", "_bmad-output/initiative-r-e0a2598f/architecture/architecture.md", "openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md"]
    manifest = [{"path": name, "sha256": digest(root / name)} for name in names]
    ac = {f"AC{i}": [original] for i in range(1, 7)}
    return {"request": "r-e0a2598f", "branch": "argonauts/r-e0a2598f", "target_head": head,
            "request_start": "79d83ba14dd59d289d2ecd3e33c85e8de437972e", "baseline": "79d83ba14dd59d289d2ecd3e33c85e8de437972e",
            "quality_status": "pending", "openspec_3_2": "pending", "manifest": manifest,
            "sources": [{"path": p, "sha256": digest(root / p)} for p in sources],
            "originals": [{"path": original, "sha256": digest(root / original)}],
            "executions": [{"command": "fixture command (not real product proof)", "argv": [sys.executable, "fixture"], "input": ["fixture bytes"], "environment": {"fixture": "only"}, "stdout": "", "stderr": "", "exit": 0, "expected_vs_actual": "fixture valid process state", "originals": [original]}],
            "ac_mapping": ac, "inventories": inventories(root), "obligations": obligations(root),
            "procedures": [{"id": k, "path": v, "sha256": digest(Path(v))} for k, v in PROCEDURES.items()],
            "commands": ["uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude", "uv run --extra dev python -m pytest -q"],
            "handoff_text": f"{DATA}/quality-handoff.md"}


def save_package(root, data):
    path = root / DATA / "quality-handoff.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    (root / data["handoff_text"]).write_text("# Fixture pending quality\n" + "\n".join(data["commands"]) + "\n" + "\n".join(x["statement"] for x in data["obligations"]))
    return path


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="handoff-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        git(ROOT, "clone", "--shared", "--no-checkout", "--quiet", str(ROOT), str(self.root))
        git(self.root, "checkout", "HEAD", "--", "wordfreq", "tests", "README.md", "pyproject.toml", *CANON, ".planning/REQUIREMENTS.md", "_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md", "_bmad-output/initiative-r-e0a2598f/architecture/architecture.md", "openspec/changes/r-e0a2598f-wordfreq-exclude", f"{DATA}/builder-evidence.md")
        self.data = make_package(self.root)

    def check(self, expected, diagnostic=""):
        path = save_package(self.root, self.data)
        result = subprocess.run([sys.executable, str(CHECKER), "--repo-root", str(self.root), "--handoff", str(path)], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertIn(diagnostic, result.stdout + result.stderr)

    def test_complete_pending_package_passes(self):
        self.check(0, "HANDOFF_READY_ONLY")
        self.assertFalse((self.root / PHASE / "08-VERIFICATION.md").exists())

    def test_original_missing(self):
        (self.root / self.data["originals"][0]["path"]).unlink()
        self.check(2, "original_missing")

    def test_original_empty(self):
        (self.root / self.data["originals"][0]["path"]).write_bytes(b"")
        self.check(2, "original_empty")

    def test_original_unreadable(self):
        path = self.root / self.data["originals"][0]["path"]
        path.chmod(0)
        self.addCleanup(path.chmod, 0o644)
        self.check(2, "original_unreadable")

    def test_original_wrong_digest(self):
        self.data["originals"][0]["sha256"] = "0" * 64
        self.check(2, "original_digest")

    def test_missing_execution_fields(self):
        for key in ["command", "argv", "input", "environment", "stdout", "stderr", "exit", "expected_vs_actual", "originals"]:
            with self.subTest(key=key):
                original = self.data["executions"][0].pop(key)
                self.check(2, "evidence_field:" + key)
                self.data["executions"][0][key] = original

    def test_missing_ac_mapping(self):
        del self.data["ac_mapping"]["AC6"]
        self.check(2, "AC_mapping")

    def test_bad_target_format(self):
        self.data["target_head"] = "d30dd31"
        self.check(2, "target_head_format")

    def test_nonexistent_target(self):
        self.data["target_head"] = "f" * 40
        self.check(2, "target_head_missing")

    def test_stale_target(self):
        self.data["target_head"] = self.data["baseline"]
        self.check(2, "target_stale")

    def test_omitted_scoped_path(self):
        self.data["manifest"].pop()
        self.check(2, "manifest_paths")

    def test_changed_worktree(self):
        (self.root / "wordfreq/__main__.py").write_bytes(b"# changed\n")
        self.check(2, "manifest_worktree")

    def test_wrong_git_digest(self):
        self.data["manifest"][0]["sha256"] = "0" * 64
        self.check(2, "manifest_digest")

    def test_omitted_or_duplicate_inventory(self):
        for kind in ["edges", "ui", "prohibitions", "trace"]:
            for mutation in ["omit", "duplicate", "predicate", "false-green"]:
                with self.subTest(kind=kind, mutation=mutation):
                    original = copy.deepcopy(self.data["inventories"][kind])
                    if mutation == "omit":
                        self.data["inventories"][kind].pop()
                    elif mutation == "duplicate":
                        self.data["inventories"][kind].append(copy.deepcopy(original[0]))
                    elif mutation == "predicate":
                        self.data["inventories"][kind][0]["source"] = "README.md"
                    else:
                        self.data["inventories"][kind][-1]["disposition"] = "passed"
                    self.check(2, "inventory:" + kind)
                    self.data["inventories"][kind] = original

    def test_missing_quality_obligation(self):
        self.data["obligations"].pop()
        self.check(2, "obligation:Q6")

    def test_missing_procedure(self):
        self.data["procedures"].pop()
        self.check(2, "procedure:openspec")

    def test_premature_quality_pass(self):
        self.data["quality_status"] = "passed"
        self.check(2, "quality_pending")

    def test_premature_task_checkoff(self):
        path = self.root / "openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md"
        path.write_text(path.read_text().replace("- [ ] 3.2", "- [x] 3.2"))
        self.check(2, "task_3_2")

    def test_report_only_descendant_is_not_new_product_acceptance(self):
        # No hash self-reference: target is latest scoped commit, reports are separate.
        (self.root / "report.md").write_text("report only")
        git(self.root, "add", "report.md")
        git(self.root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "report-only fixture")
        self.check(0, "HANDOFF_READY_ONLY")


def load_tests(loader, suite, pattern):
    if suite.countTestCases() == 0:
        raise RuntimeError("zero discovered handoff tests")
    return suite
