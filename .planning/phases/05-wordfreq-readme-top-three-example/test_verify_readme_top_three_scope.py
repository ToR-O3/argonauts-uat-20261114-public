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
SECURITY = f"{PHASE}/05-SECURITY.md"
OPEN_SPEC = ".planning/argonauts/t_40ba151e/openspec-verify.md"
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
        yield root


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
    with checkout() as root:
        for path in (SECURITY, OPEN_SPEC):
            copy_report(root, path)
            require(git_state(root, path) == (f"?? {path}\n".encode(), b"", b""), "expected untracked original")
        expect_success(verify(root))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=["untracked-previous"])
    parser.parse_args()
    untracked_previous()
    print("PASS: untracked-previous")


if __name__ == "__main__":
    main()
