"""Verify the one-line README change and execute the command as published."""

import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile


BASE = "5528aa47cca27a93a6732e914710f2772118a572"
README = "README.md"
TASKS = "openspec/changes/r-864b299c-readme-top-three/tasks.md"
PHASE_DIR = ".planning/phases/05-wordfreq-readme-top-three-example"
# Existing tests read fixtures under .planning/, so only these exact
# workflow artifacts are exempt from the product diff check.
WORKFLOW_PATHS = {
    ".planning/INGEST-CONFLICTS.md",
    ".planning/REQUIREMENTS.md",
    ".planning/ROADMAP.md",
    ".planning/STATE.md",
    ".planning/state.json",
    ".planning/argonauts/r-864b299c-learnings.md",
    ".planning/argonauts/r-864b299c-manifest.yaml",
    ".planning/argonauts/r-864b299c-prd.md",
    ".planning/intel/SYNTHESIS.md",
    ".planning/intel/classifications/brief-wordfreq-top-three-3adfe49d.json",
    ".planning/intel/classifications/prd-wordfreq-top-three-73325b60.json",
    ".planning/intel/classifications/proposal-4146fcc0.json",
    ".planning/intel/classifications/spec-67452c5a.json",
    ".planning/intel/classifications/tasks-e477c401.json",
    ".planning/intel/constraints.md",
    ".planning/intel/context.md",
    ".planning/intel/decisions.md",
    ".planning/intel/requirements.md",
    *(f"{PHASE_DIR}/{name}" for name in (
        ".gitkeep", "05-01-PLAN.md", "05-01-SUMMARY.md", "05-CONTEXT.md",
        "05-PATTERNS.md", "05-RESEARCH.md", "05-VALIDATION.md", "05-REVIEW.md",
        "05-VERIFICATION.md", "05-CLI-EVIDENCE.md", "verify_readme_top_three.py",
    )),
}
ANCHOR = b"python -m wordfreq input.txt --top 2 --format json"
EXAMPLE = b"python -m wordfreq input.txt --top 3 --format json"
INPUT = "delta gamma beta alpha beta gamma alpha beta alpha alpha"
EXPECTED = [
    {"word": "alpha", "count": 4},
    {"word": "beta", "count": 3},
    {"word": "gamma", "count": 2},
]


def git(cwd, *args):
    result = subprocess.run(
        ["git", "-c", "core.fileMode=true", *args], cwd=cwd,
        check=True, capture_output=True, timeout=10,
    )
    return result.stdout


def anchor_index(data):
    lines = data.splitlines(keepends=True)
    heading = "## wordfreq の実行".encode()
    positions = [i for i, line in enumerate(lines) if line.rstrip(b"\r\n") == heading]
    if len(positions) != 1:
        raise ValueError("expected one wordfreq usage section")
    anchors = []
    fence = None
    for i in range(positions[0] + 1, len(lines)):
        line = lines[i].rstrip(b"\r\n")
        if fence is None and line.startswith(b"## "):
            break
        if line.startswith(b"```"):
            if fence is None:
                fence = line
            elif line == b"```":
                fence = None
        elif fence == b"```sh" and line == ANCHOR:
            anchors.append(i)
    if fence is not None or len(anchors) != 1:
        raise ValueError("expected one top-2 JSON anchor in a closed sh block")
    return lines, anchors[0]


def diff_entries(raw):
    fields = raw.split(b"\0")[:-1]
    for meta, path in zip(fields[::2], fields[1::2], strict=True):
        old_mode, new_mode, _, _, status = meta.removeprefix(b":").split()
        yield os.fsdecode(path), old_mode, new_mode, status


def scope(root):
    work = list(diff_entries(git(root, "diff", "--raw", "--no-renames", "-z", BASE, "--")))
    staged = list(diff_entries(git(root, "diff", "--cached", "--raw", "--no-renames", "-z", BASE, "--")))
    untracked = [os.fsdecode(p) for p in git(root, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p]
    for label, entries in (("base → worktree", work), ("base → index", staged)):
        print(label + ":")
        for path, old_mode, new_mode, status in entries:
            print(f"  {status.decode()} {old_mode.decode()}→{new_mode.decode()} {path!r}")
    print(f"untracked: {untracked!r}")
    raw = git(root, "diff", "--no-ext-diff", "--no-textconv", BASE, "--", README)
    print("README diff:\n" + (raw.decode("utf-8", errors="backslashreplace") if raw else "(none)"))
    return work, staged, untracked


def verify_scope(root, work, staged, untracked, expected_readme):
    touched = set()
    for entries, index in ((work, False), (staged, True)):
        for path, old_mode, new_mode, status in entries:
            if path in WORKFLOW_PATHS:
                continue
            if path not in {README, TASKS} or status != b"M" or old_mode != new_mode:
                raise ValueError(f"out-of-scope change: {path!r} ({status!r})")
            touched.add(path)
            if path == README:
                if index and git(root, "show", f":{README}") != expected_readme:
                    raise ValueError("staged README is not the exact approved insertion")
            else:
                baseline = git(root, "show", f"{BASE}:{TASKS}")
                unchecked = b"\n- [ ] 1.1 "
                actual = git(root, "show", f":{TASKS}") if index else (root / TASKS).read_bytes()
                if baseline.count(unchecked) != 1 or actual != baseline.replace(unchecked, b"\n- [x] 1.1 ", 1):
                    raise ValueError("OpenSpec change must only check task 1.1")
    outside = [path for path in untracked if path not in WORKFLOW_PATHS]
    if outside:
        raise ValueError(f"out-of-scope untracked paths: {outside!r}")
    if not any(entry[0] == README for entry in work) or README not in touched:
        raise ValueError("README insertion not found in worktree diff")
    if git(root, "diff", "--numstat", BASE, "--", README) != b"1\t0\tREADME.md\n":
        raise ValueError("README diff must report one addition and zero deletions")


def verify_cli(root, published):
    argv = shlex.split(published.decode("ascii"))
    if argv != EXAMPLE.decode("ascii").split():
        raise ValueError("published argv does not match the approved command")
    temp_root = Path(tempfile.gettempdir()).resolve()
    if temp_root.is_relative_to(root):
        raise ValueError("temporary input directory must be outside the worktree")
    with tempfile.TemporaryDirectory(prefix="wordfreq-top-three-", dir=temp_root) as tmp:
        path = Path(tmp) / "input.txt"
        path.write_text(INPUT, encoding="utf-8")
        argv[3] = str(path)
        print(f"published: {published.decode('ascii')}\nargv: {argv!r}\ninput (UTF-8): {INPUT}")
        print("CLI: starting")
        result = subprocess.run(
            argv, cwd=root, shell=False, capture_output=True, timeout=10,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        )
    print(f"CLI exit: {result.returncode}\nstdout: {result.stdout!r}\nstderr: {result.stderr!r}")
    if result.returncode:
        raise ValueError("published CLI returned nonzero")
    data = json.loads(result.stdout)
    if data != EXPECTED or any(type(item["count"]) is not int for item in data):
        raise ValueError(f"expected exactly {EXPECTED!r} with integer counts")


def main():
    cli_started = False
    try:
        root = Path(os.fsdecode(git(Path(__file__).resolve().parent, "rev-parse", "--show-toplevel").rstrip(b"\n"))).resolve()
        head = git(root, "rev-parse", "HEAD").decode("ascii").strip()
        dirty = git(root, "status", "--porcelain=v1", "--untracked-files=all")
        print(f"base: {BASE}\nHEAD: {head}\ntarget: {'working tree (not a committed result)' if dirty else 'clean HEAD'}")
        git(root, "cat-file", "-e", f"{BASE}^{{commit}}")
        git(root, "merge-base", "--is-ancestor", BASE, head)
        work, staged, untracked = scope(root)
        readme = root / README
        if readme.is_symlink() or not readme.is_file():
            raise ValueError("README must be a regular file")
        current = readme.read_bytes()
        lines, anchor = anchor_index(current)
        published = lines[anchor + 1].rstrip(b"\r\n") if anchor + 1 < len(lines) else b""
        if published != EXAMPLE:
            raise ValueError("top-three example missing immediately after the top-2 JSON example")
        if sum(line.rstrip(b"\r\n") == EXAMPLE for line in lines) != 1:
            raise ValueError("top-three example must appear exactly once")
        original, at = anchor_index(git(root, "show", f"{BASE}:{README}"))
        eol = original[at][len(ANCHOR):]
        expected = b"".join([*original[:at + 1], EXAMPLE + eol, *original[at + 1:]])
        if current != expected:
            raise ValueError("README differs from a single exact insertion at the approved anchor")
        verify_scope(root, work, staged, untracked, expected)
        print("placement and scope: PASS")
        cli_started = True
        verify_cli(root, published)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        if not cli_started:
            print("CLI: not run")
        print(f"verification: FAIL (exit 1): {exc}")
        if isinstance(exc, (subprocess.CalledProcessError, subprocess.TimeoutExpired)):
            print(f"subprocess stdout: {exc.stdout!r}\nsubprocess stderr: {exc.stderr!r}")
        return 1
    print("verification: PASS (exit 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
