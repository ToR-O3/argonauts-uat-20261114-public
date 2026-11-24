"""Exercise the README verifier against isolated, real Git states."""

import argparse
import ast
from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess
import tempfile


BASE = "5528aa47cca27a93a6732e914710f2772118a572"
START = "14e6df0700bb19a9e54a0d1b32e0f16f6eced634"
REPORTS_REF = "96c2df6c65af7060baca53fd80d573b3808d3728"
PHASE = ".planning/phases/05-wordfreq-readme-top-three-example"
VERIFIER = f"{PHASE}/verify_readme_top_three.py"
HARNESS = f"{PHASE}/test_verify_readme_top_three_scope.py"
SECURITY = f"{PHASE}/05-SECURITY.md"
OPEN_SPEC = ".planning/argonauts/t_40ba151e/openspec-verify.md"
NEW_REPORT = ".planning/argonauts/t_0a1b2c3d/openspec-verify.md"
VALIDATION = f"{PHASE}/05-VALIDATION.md"
REPORTS = (SECURITY, OPEN_SPEC, f"{PHASE}/05-VERIFICATION.md", f"{PHASE}/05-CLI-EVIDENCE.md", NEW_REPORT)
EXPECTED = [{"word": "alpha", "count": 4}, {"word": "beta", "count": 3}, {"word": "gamma", "count": 2}]
COMMAND = ["python", VERIFIER]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def run(cwd, *argv, check=True):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(
        argv, cwd=cwd, env=env, shell=False, check=check, capture_output=True, timeout=30,
    )


def git(cwd, *args):
    return run(cwd, "git", *args).stdout


@contextmanager
def checkout():
    source = Path(os.fsdecode(git(Path(__file__).resolve().parent, "rev-parse", "--show-toplevel").rstrip(b"\n")))
    temp_root = Path(tempfile.gettempdir()).resolve()
    require(not temp_root.is_relative_to(source), "scratch must be outside the source worktree")
    with tempfile.TemporaryDirectory(prefix="top-three-scope-", dir=temp_root) as scratch:
        root = Path(scratch) / "repo"
        git(scratch, "clone", "--no-local", "--no-checkout", "--template=", "--", str(source), str(root))
        git(root, "config", "core.hooksPath", os.devnull)
        git(root, "config", "user.name", "Verifier Test")
        git(root, "config", "user.email", "verifier-test@example.invalid")
        git(root, "config", "commit.gpgSign", "false")
        git(root, "checkout", "--detach", START)
        git(root, "merge-base", "--is-ancestor", BASE, START)
        git(root, "remote", "remove", "origin")
        require(not (root / ".git/objects/info/alternates").exists(), "clone shares objects")
        (root / VERIFIER).write_bytes((source / VERIFIER).read_bytes())
        yield root, source


def copy_report(root, path, original=None):
    data = git(root, "show", f"{REPORTS_REF}:{original or path}")
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def git_state(root, path):
    status = git(root, "status", "--porcelain=v1", "--untracked-files=all", "--", path)
    index = git(root, "ls-files", "--stage", "--", path)
    head = git(root, "ls-tree", "HEAD", "--", path)
    print(f"{path}: status={status!r}, index={index!r}, HEAD={head!r}")
    return status, index, head


def verify(root):
    head = git(root, "rev-parse", "HEAD").decode().strip()
    print(f"base={BASE}, HEAD={head}, command={COMMAND!r}")
    result = run(root, *COMMAND, check=False)
    print(result.stdout.decode(errors="backslashreplace"), end="")
    print(f"verifier exit: {result.returncode}, verifier stderr: {result.stderr!r}")
    return result


def expect_success(result):
    require(result.returncode == 0 and result.stderr == b"", "expected verifier exit 0 and empty stderr")
    lines = result.stdout.splitlines()
    for marker in (b"placement and scope: PASS", b"CLI: starting", b"CLI exit: 0", b"stderr: b''"):
        require(marker in lines, f"missing {marker!r}")
    outputs = [line.removeprefix(b"stdout: ") for line in lines if line.startswith(b"stdout: ")]
    require(len(outputs) == 1, "expected one CLI stdout record")
    data = json.loads(ast.literal_eval(outputs[0].decode("ascii")))
    require(data == EXPECTED and all(type(row["count"]) is int for row in data), f"unexpected CLI JSON: {data!r}")


def untracked_previous():
    with checkout() as (root, _):
        for path in (SECURITY, OPEN_SPEC):
            copy_report(root, path)
            require(git_state(root, path) == (f"?? {path}\n".encode(), b"", b""), "expected untracked original")
        expect_success(verify(root))


def expect_rejection(result, path, reason):
    lines = result.stdout.splitlines()
    failures = [line for line in lines if line.startswith(b"verification: FAIL")]
    require(result.returncode == 1 and result.stderr == b"", "expected scope rejection, not process failure")
    require(len(failures) == 1 and path.encode() in failures[0] and reason.encode() in failures[0],
            f"expected {reason!r} for {path!r}, got {failures!r}")
    require(b"CLI: not run" in lines, "expected no CLI attempt")
    require(not any(line.startswith((b"published:", b"argv:", b"CLI: starting", b"CLI exit:", b"stdout:"))
                    for line in lines), "unexpected CLI launch evidence")


def commit_paths(root, subject, *paths):
    git(root, "add", "--", *paths)
    git(root, "commit", "-m", subject)


def prepare_reports(root, source, state):
    (root / HARNESS).write_bytes((source / HARNESS).read_bytes())
    copy_report(root, VALIDATION)
    commit_paths(root, "Prepare verifier and tracked validation update", VERIFIER, HARNESS, VALIDATION)
    validation_diff = git(root, "diff", "--raw", "--no-renames", START, "HEAD", "--", VALIDATION)
    require(validation_diff.startswith(b":100644 100644 ") and b" M\t" in validation_diff,
            "VALIDATION must be a same-mode tracked update from START")
    print(f"tracked preparation: {validation_diff!r}")
    for path in REPORTS:
        require(git_state(root, path) == (b"", b"", b""), f"unexpected pre-existing report: {path}")
        require(not git(root, "ls-tree", BASE, "--", path), f"report already in base: {path}")
        copy_report(root, path, OPEN_SPEC if path == NEW_REPORT else None)
    if state == "staged":
        git(root, "add", "--", *REPORTS)
    elif state == "committed":
        commit_paths(root, "Save the added reports", *REPORTS)
        require(not git(root, "status", "--porcelain=v1", "--untracked-files=all"), "expected clean committed state")
        added = git(root, "diff", "--no-renames", "--name-status", BASE, "HEAD", "--", *REPORTS)
        require(set(added.splitlines()) == {f"A\t{path}".encode() for path in REPORTS}, "not all reports added from base")
        print(f"committed additions from base: {added!r}")
    for path in REPORTS:
        status, index, head = git_state(root, path)
        prefix = {"untracked": "??", "staged": "A ", "committed": ""}[state]
        require(status == (f"{prefix} {path}\n".encode() if prefix else b""), f"wrong report status: {path}")
        require(index.startswith(b"100644 ") if state != "untracked" else not index, f"wrong index: {path}")
        require(head.startswith(b"100644 blob ") if state == "committed" else not head, f"wrong HEAD: {path}")


def positive(state):
    with checkout() as (root, source):
        prepare_reports(root, source, state)
        expect_success(verify(root))


def mutate(root, case):
    tracked = {
        "tracked-change": "CONCEPTS.md",
        "tracked-fixture": ".planning/argonauts/r-e476c11d/baseline/index.json",
        "report-in-base": ".planning/argonauts/t_419e62f7/openspec-verify.md",
    }
    unknown = {
        "unrelated-untracked": ".planning/unrelated.md",
        "wrong-id-length": ".planning/argonauts/t_0a1b2c3/openspec-verify.md",
        "wrong-id-case": ".planning/argonauts/t_0A1b2c3d/openspec-verify.md",
        "extra-level": ".planning/argonauts/t_0a1b2c3d/nested/openspec-verify.md",
        "wrong-filename": ".planning/argonauts/t_0a1b2c3d/other.md",
    }
    if case in tracked:
        path = tracked[case]
        require(git(root, "ls-tree", BASE, "--", path).startswith(b"100644 blob "), "missing base file")
        target = root / path
        target.write_bytes(target.read_bytes() + b"\nchanged in test\n")
        if case != "tracked-change":
            git(root, "add", "--", path)
        prefix = " M" if case == "tracked-change" else "M "
        require(git_state(root, path)[0] == f"{prefix} {path}\n".encode(), "missing expected tracked change")
        return path, "already tracked at base" if case == "report-in-base" else "out-of-scope change"
    if case in unknown:
        path = unknown[case]
        copy_report(root, path, OPEN_SPEC)
        require(git_state(root, path) == (f"?? {path}\n".encode(), b"", b""), "missing unknown untracked path")
        return path, "out-of-scope untracked paths"
    if case == "staged-deletion":
        path = OPEN_SPEC
        git(root, "rm", "--", path)
        status, index, head = git_state(root, path)
        require(status == f"D  {path}\n".encode() and not index and head.startswith(b"100644 blob ")
                and not (root / path).exists(), "expected staged deletion of a regular HEAD report")
        for args in ((BASE,), ("--cached", BASE)):
            require(not git(root, "diff", "--name-only", "--no-renames", *args, "--", path), "not absent from old diff")
        require(not git(root, "ls-files", "--others", "--exclude-standard", "--", path), "not absent from untracked")
        for args, prefix in (((BASE, "HEAD"), "A"), (("--cached", "HEAD"), "D")):
            diff = git(root, "diff", "--name-status", "--no-renames", *args, "--", path)
            require(diff == f"{prefix}\t{path}\n".encode(), "missing addition or deletion in extra diff")
            print(f"diff {args}: {diff!r}")
        return path, "staged deletion"
    if case == "fixed-mode-change":
        (root / VALIDATION).chmod(0o755)
        require(git_state(root, VALIDATION)[0] == f" M {VALIDATION}\n".encode(), "missing tracked mode change")
        return VALIDATION, "file mode change"
    if case == "symlink-parent":
        parent = (root / NEW_REPORT).parent
        moved = parent.rename(root.parent / "moved-report-directory")
        parent.symlink_to(moved, target_is_directory=True)
        status = git(root, "status", "--porcelain=v1", "--untracked-files=all")
        print(f"parent symlink: {status!r}")
        require(f" D {NEW_REPORT}\n".encode() in status and parent.is_symlink()
                and (root / NEW_REPORT).is_file(), "expected a symlink parent reaching the original report")
        return NEW_REPORT, "symlink parent"
    path = ".planning/argonauts/t_11112222/openspec-verify.md"
    if case == "fixed-symlink":
        path = f"{PHASE}/05-REVIEW.md"
    target = root / path
    require(not target.exists(), f"non-regular scenario needs a new path: {path}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(root / SECURITY)
    if case in {"symlink-index", "symlink-head"}:
        if case == "symlink-head":
            commit_paths(root, "Save a non-regular report", path)
        else:
            git(root, "add", "--", path)
        target.unlink()
        copy_report(root, path, OPEN_SPEC)
        if case == "symlink-head":
            git(root, "add", "--", path)
        status, index, head = git_state(root, path)
        if case == "symlink-index":
            require(status == f"AT {path}\n".encode() and index.startswith(b"120000 ") and not head,
                    "expected a staged symlink masked by a regular worktree file")
            return path, "non-regular or conflicted entry in index"
        require(status == f"T  {path}\n".encode() and index.startswith(b"100644 ") and head.startswith(b"120000 blob "),
                "expected a HEAD symlink masked by regular index and worktree files")
        return path, "non-regular or conflicted entry in HEAD"
    require(target.is_symlink() and git_state(root, path) == (f"?? {path}\n".encode(), b"", b""),
            "expected an untracked symlink")
    return path, "non-regular file in worktree"


def negative(case):
    with checkout() as (root, source):
        prepare_reports(root, source, "committed")
        path, reason = mutate(root, case)
        expect_rejection(verify(root), path, reason)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    states = ("untracked", "staged", "committed")
    negatives = ("tracked-change", "unrelated-untracked", "tracked-fixture", "wrong-id-length", "wrong-id-case",
                 "extra-level", "wrong-filename", "report-in-base", "symlink-worktree", "symlink-index",
                 "symlink-head", "staged-deletion", "fixed-mode-change", "fixed-symlink", "symlink-parent")
    cases = ("untracked-previous", *states, *negatives)
    parser.add_argument("--case", choices=cases)
    selection = parser.parse_args().case
    for case in (selection,) if selection else cases:
        print(f"\n=== {case} ===", flush=True)
        if case == "untracked-previous":
            untracked_previous()
        elif case in states:
            positive(case)
        else:
            negative(case)
        print(f"PASS: {case}")


if __name__ == "__main__":
    main()
