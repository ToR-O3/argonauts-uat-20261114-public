"""Validate Builder handoff bytes and pending obligations, NOT quality acceptance."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

PHASE = ".planning/phases/08-wordfreq-exclude"
DATA = ".planning/argonauts/r-e0a2598f"
SCOPE = ("wordfreq", "tests", "README.md", "pyproject.toml")
BASELINE = "79d83ba14dd59d289d2ecd3e33c85e8de437972e"
SOURCES = {f"{PHASE}/08-{n:02}-PLAN.md" for n in (1, 2, 3)} | {
    f"{PHASE}/08-UI-SPEC.md", ".planning/argonauts/t_b046d7f7-edge-probe.json",
    ".planning/argonauts/t_b046d7f7-ui-probe.json", ".planning/REQUIREMENTS.md",
    "_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md",
    "_bmad-output/initiative-r-e0a2598f/architecture/architecture.md",
    "openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md",
}
COMMANDS = {"uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude",
            "uv run --extra dev python -m pytest -q"}


class InvalidHandoff(ValueError):
    pass


def require(ok, diagnostic):
    if not ok:
        raise InvalidHandoff(diagnostic)


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=True).stdout


def sha(data):
    return hashlib.sha256(data).hexdigest()


def local(root, name):
    path = Path(name)
    require(not path.is_absolute() and ".." not in path.parts and ".git" not in path.parts, "unsafe_path:" + str(name))
    target = root / path
    require(target.resolve().is_relative_to(root), "unsafe_path:" + str(name))
    return target


def readable(path, label):
    require(path.is_file(), label + "_missing:" + str(path))
    require(path.stat().st_mode & 0o444 != 0, label + "_unreadable:" + str(path))
    value = path.read_bytes()
    require(bool(value.strip()), label + "_empty:" + str(path))
    return value


def keyed(rows, field, label):
    require(isinstance(rows, list) and bool(rows), label)
    require(all(isinstance(row, dict) and isinstance(row.get(field), str) for row in rows), label)
    result = {row[field]: row for row in rows}
    require(len(result) == len(rows), label)
    return result


def expected_inventory(root):
    # Project from all original PLAN truth strings; no aggregate count shortcuts.
    predicates = {}
    prohibitions = {}
    pattern = re.compile(r"^\s+- (?:statement: )?'((?:REQ-|UI-E|P-08-).*)'$", re.M)
    for n in (1, 2, 3):
        source = f"{PHASE}/08-{n:02}-PLAN.md"
        for match in pattern.finditer((root / source).read_text()):
            text = match.group(1)
            key = text.split(": ", 1)[0]
            row = {"key": key, "predicate": text, "source": source}
            if key.startswith("P-08-"):
                row["disposition"] = "flagged-unverified"
                prohibitions[key] = row
            else:
                row["disposition"] = "human_needed/insufficient_spec" if key.endswith("/concurrency") else "pending-independent-quality"
                predicates[key] = row
    result = {"prohibitions": prohibitions}
    for kind, filename, prefix in [("edges", "t_b046d7f7-edge-probe.json", ""), ("ui", "t_b046d7f7-ui-probe.json", "UI-")]:
        probe = json.loads((root / ".planning/argonauts" / filename).read_text())
        keys = [prefix + item["requirement_id"] + "/" + item["category"] for item in probe["items"]]
        require(len(keys) == len(set(keys)), "source_inventory_duplicate:" + kind)
        result[kind] = {key: predicates[key] for key in keys}
    # Confirm probes and lifted predicates agree, rather than trusting just one.
    require(set(predicates) == set(result["edges"]) | set(result["ui"]), "source_inventory_predicates")
    trace = {}
    for family, numbers, source in [
        ("REQ", range(28, 34), ".planning/REQUIREMENTS.md"),
        ("FR", range(1, 8), "_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md"),
        ("RULE", range(1, 5), "_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md"),
        ("AD", range(1, 5), "_bmad-output/initiative-r-e0a2598f/architecture/architecture.md"),
        ("EX", range(1, 6), "openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md"),
        ("AC", range(1, 7), f"{PHASE}/08-03-PLAN.md"),
    ]:
        text = (root / source).read_text()
        for number in numbers:
            key = f"{family}{number}" if family == "AC" else f"{family}-{number}"
            require(key in text, "source_trace:" + key)
            trace[key] = {"key": key, "source": source, "disposition": "pending-independent-quality"}
    result["trace"] = trace
    return result


def validate(root, handoff):
    data = json.loads(readable(handoff, "handoff"))
    require(data.get("request") == "r-e0a2598f" and data.get("branch") == "argonauts/r-e0a2598f", "request_branch")
    require(data.get("baseline") == BASELINE and data.get("request_start") == BASELINE, "baseline_revision")
    require(data.get("quality_status") == "pending", "quality_pending")
    require(data.get("openspec_3_2") == "pending", "task_3_2")
    tasks = (root / "openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md").read_text()
    require("- [ ] 3.2 " in tasks and "- [x] 3.2 " not in tasks, "task_3_2")
    target = data.get("target_head", "")
    require(isinstance(target, str) and re.fullmatch("[0-9a-f]{40}", target) is not None, "target_head_format")
    try:
        require(git(root, "rev-parse", "--verify", target + "^{commit}").decode().strip() == target, "target_head_missing")
    except subprocess.CalledProcessError as error:
        raise InvalidHandoff("target_head_missing") from error
    # A report cannot contain its own hash. Pin the latest content-scope commit,
    # permit only report-only descendants, and never call that final-head acceptance.
    latest = git(root, "log", "-1", "--format=%H", "HEAD", "--", *SCOPE).decode().strip()
    require(target == latest, "target_stale: latest scoped commit differs")
    git(root, "merge-base", "--is-ancestor", target, "HEAD")
    names = set(git(root, "ls-tree", "-rz", "--name-only", target, "--", *SCOPE).decode().strip("\0").split("\0"))
    manifest = keyed(data.get("manifest"), "path", "manifest_paths")
    require(set(manifest) == names, "manifest_paths")
    require(set(git(root, "ls-files", "-z", "--", *SCOPE).decode().strip("\0").split("\0")) == names, "manifest_paths: index additions/deletions")
    require(not git(root, "ls-files", "--others", "--exclude-standard", "--", *SCOPE), "manifest_paths: untracked scoped content")
    for name, row in manifest.items():
        expected = git(root, "show", f"{target}:{name}")
        require(row.get("sha256") == sha(expected), "manifest_digest:" + name)
        path = local(root, name)
        require(path.is_file() and path.read_bytes() == expected, "manifest_worktree:" + name)
    sources = keyed(data.get("sources"), "path", "source_paths")
    require(set(sources) == SOURCES, "source_paths")
    for name, row in sources.items():
        value = readable(local(root, name), "source")
        require(row.get("sha256") == sha(value) == sha(git(root, "show", f"{target}:{name}")), "source_digest:" + name)
    originals = keyed(data.get("originals"), "path", "original_paths")
    for name, row in originals.items():
        value = readable(local(root, name), "original")
        require(row.get("sha256") == sha(value), "original_digest:" + name)
        value.decode("utf-8")  # readable text originals, not an archive/image surrogate
    executions = data.get("executions")
    require(isinstance(executions, list) and bool(executions), "executions_missing")
    types = {"command": str, "argv": list, "input": list, "environment": dict,
             "stdout": str, "stderr": str, "exit": int, "expected_vs_actual": str, "originals": list}
    for run in executions:
        for key, kind in types.items():
            require(key in run and type(run[key]) is kind, "evidence_field:" + key)
            require(key in {"stdout", "stderr", "exit"} or bool(run[key]), "evidence_field:" + key)
        require(set(run["originals"]) <= set(originals), "evidence_field:originals")
    mapping = data.get("ac_mapping", {})
    require(set(mapping) == {f"AC{i}" for i in range(1, 7)}, "AC_mapping")
    for key, links in mapping.items():
        require(isinstance(links, list) and bool(links) and set(links) <= set(originals), "AC_mapping:" + key)
    expected = expected_inventory(root)
    for kind, rows in expected.items():
        actual = keyed(data.get("inventories", {}).get(kind), "key", "inventory:" + kind)
        require(actual == rows, "inventory:" + kind)
    section = (root / PHASE / "08-03-PLAN.md").read_text().split("## Mandatory later independent quality phase-verification card", 1)[1].split("<threat_model>", 1)[0]
    obligations = keyed(data.get("obligations"), "id", "obligation:identities")
    require(set(obligations) <= {f"Q{i}" for i in range(1, 7)}, "obligation:identities")
    for i in range(1, 7):
        key = f"Q{i}"
        statement = next(line for line in section.splitlines() if line.startswith(f"{i}. "))
        require(obligations.get(key) == {"id": key, "statement": statement, "status": "pending"}, "obligation:" + key)
    procedures = keyed(data.get("procedures"), "id", "procedure:identities")
    suffixes = {"gsd": "gsd-core/workflows/execute-phase/steps/verify-phase-goal.md",
                "openspec": "openspec/.agents/skills/openspec-verify-change/SKILL.md"}
    for key, suffix in suffixes.items():
        require(key in procedures, "procedure:" + key)
        path = Path(procedures[key]["path"])
        require(str(path).endswith(suffix), "procedure:" + key)
        require(sha(readable(path, "procedure")) == procedures[key].get("sha256"), "procedure:" + key)
    commands = data.get("commands", [])
    require(isinstance(commands, list) and set(commands) >= COMMANDS, "quality_commands")
    text = readable(local(root, data.get("handoff_text", "")), "handoff_text").decode()
    require(all(command in text for command in commands), "handoff_text_commands")
    require(all(row["statement"] in text for row in obligations.values()), "handoff_text_obligations")
    return {"result": "HANDOFF_READY_ONLY", "target_head": target,
            "reporting_head": git(root, "rev-parse", "HEAD").decode().strip(),
            "scoped_files": len(names), "edges": len(expected["edges"]), "ui": len(expected["ui"]),
            "prohibitions": len(expected["prohibitions"]), "quality_status": "pending", "openspec_3_2": "pending"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--handoff", required=True)
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    path = Path(args.handoff)
    if not path.is_absolute():
        path = root / path
    try:
        print(json.dumps(validate(root, path), sort_keys=True))
        return 0
    except (InvalidHandoff, OSError, ValueError, KeyError, TypeError, StopIteration, subprocess.CalledProcessError) as error:
        print(f"HANDOFF_INVALID: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
