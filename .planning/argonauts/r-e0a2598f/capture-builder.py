"""Actual binary CLI captures and isolated baseline discrimination controls."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path.cwd()
OUT = ROOT / ".planning/argonauts/r-e0a2598f"
spec = importlib.util.spec_from_file_location("cli_tests", ROOT / "tests/test_cli.py")
assert spec is not None and spec.loader is not None
tests = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tests)


def capture(argv, cwd, env):
    r = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=30)
    return {"argv": argv, "cwd": str(cwd), "exit": r.returncode,
            "stdout": repr(r.stdout), "stderr": repr(r.stderr),
            "stdout_hex": r.stdout.hex(), "stderr_hex": r.stderr.hex()}


with tempfile.TemporaryDirectory(prefix="exclude08-") as temp:
    scratch = Path(temp)
    old, new, env = tests.exclude_baseline_roots.__wrapped__(scratch)
    controlled_env = {k: env.get(k) for k in ["PYTHONPATH", "PYTHONDONTWRITEBYTECODE", "PYTHONHASHSEED", "PYTHONIOENCODING", "PYTHONNOUSERSITE", "LANG", "LC_ALL", "LC_CTYPE"]}
    records = []
    body = scratch / "同じ入力.txt"
    for text in ["Zoo apple APPLE zoo Straße STRASSE Café CAFÉ 日本語 日本語 zeta yak xray wolf vole urn tiger snake rabbit quail penguin otter", ""]:
        body.write_bytes(text.encode())
        for fmt in [None, "text", "json", "html"]:
            for options in [[], ["--top", "1"], ["--top", "2"], ["--top", "99"], ["--min-count", "1"], ["--min-count", "2"], ["--min-count", "3"], ["--min-count", "2", "--top", "2"]]:
                argv = [sys.executable, "-m", "wordfreq", str(body), *options]
                if fmt:
                    argv += ["--format", fmt]
                a, b = capture(argv, old, env), capture(argv, new, env)
                assert a["exit"] == b["exit"] == 0 and a["stderr_hex"] == b["stderr_hex"] == ""
                assert a["stdout_hex"] == b["stdout_hex"] and body.read_bytes() == text.encode()
                records.append({"input_path": str(body), "input_hex": text.encode().hex(), "historical": a, "candidate": b, "expected_vs_actual": "exact bytes/status/stderr equal; input unchanged"})
    (OUT / "baseline-captures.json").write_text(json.dumps({"baseline": tests.EXCLUDE_BASELINE, "interpreter": sys.executable, "version": sys.version, "environment": controlled_env, "cases": records}, ensure_ascii=False, indent=2) + "\n")
    body.write_bytes(b"Zoo apple APPLE zoo banana")
    excluded = scratch / "excluded.txt"
    cli = []
    for label, exclusion, options, status in [
        ("AC1", b"apple\n", [], 0),
        ("AC2", b" \r\n  #banana\r\n apple ", [], 0),
        ("AC3", b"\n #comment\napple\nfoo bar", [], 2),
        ("AC4", b"apple\xff", [], 2),
        ("selection", b"zoo\n", ["--min-count", "2", "--top", "1"], 0),
        ("all-excluded", b"zoo\napple\nbanana\n", [], 0),
    ]:
        for fmt in ["text", "json", "html"]:
            excluded.write_bytes(exclusion)
            r = capture([sys.executable, "-m", "wordfreq", str(body), "--exclude", str(excluded), "--format", fmt, *options], new, env)
            assert r["exit"] == status
            assert body.read_bytes() == b"Zoo apple APPLE zoo banana" and excluded.read_bytes() == exclusion
            if status:
                assert r["stdout_hex"] == "" and str(excluded) in r["stderr"]
            else:
                expected = [("apple", 2)] if label == "selection" else [] if label == "all-excluded" else [("zoo", 2), ("banana", 1)]
                tests.assert_output_bytes(bytes.fromhex(r["stdout_hex"]), fmt, expected, body.name, 5)
                assert r["stderr_hex"] == ""
            cli.append({"label": label, "format": fmt, "body_hex": body.read_bytes().hex(), "exclusion_hex": exclusion.hex(), "result": r, "expected_exit": status, "expected_vs_actual": "asserted exit/output/total/input immutability"})
    (OUT / "cli-captures.json").write_text(json.dumps({"interpreter": sys.executable, "environment": controlled_env, "cases": cli}, ensure_ascii=False, indent=2) + "\n")
    mutants = [
        ("default", "wordfreq/__main__.py", "default=10", "default=1"),
        ("lexical-ties", "wordfreq/aggregator.py", "key=lambda wc: -wc[1]", "key=lambda wc: (-wc[1], wc[0])"),
        ("json-newline", "wordfreq/formatters.py", 'ensure_ascii=True) + "\\n"', 'ensure_ascii=True) + ""'),
        ("html-template", "wordfreq/formatters.py", "<title>単語の出現頻度</title>", "<title>changed</title>"),
    ]
    controls = []
    for name, filename, before, after in mutants:
        repo = scratch / name
        subprocess.run(["git", "clone", "--shared", "--no-checkout", "--quiet", str(ROOT), str(repo)], check=True)
        shutil.copytree(ROOT / "wordfreq", repo / "wordfreq", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (repo / "tests").mkdir()
        shutil.copy2(ROOT / "tests/test_cli.py", repo / "tests/test_cli.py")
        path = repo / filename
        text = path.read_text()
        assert before in text
        path.write_text(text.replace(before, after))
        argv = [sys.executable, "-m", "pytest", "tests/test_cli.py", "-q", "-x", "-k", "exclude_baseline"]
        r = subprocess.run(argv, cwd=repo, env=env, capture_output=True, timeout=90)
        console = r.stdout + r.stderr
        (OUT / f"baseline-mutant-{name}.txt").write_bytes(console)
        assert r.returncode == 1 and b"fixed historical stdout bytes differ" in console and b"AssertionError" in console, console.decode(errors="replace")
        controls.append({"mutation": name, "argv": argv, "cwd": str(repo), "exit": r.returncode, "diagnostic": "fixed historical stdout bytes differ", "console": f"baseline-mutant-{name}.txt"})
    (OUT / "baseline-controls.json").write_text(json.dumps(controls, indent=2) + "\n")
print(f"Captured {len(records)} historical pairs, {len(cli)} real exclusion cases; {len(controls)} mutants assertion-rejected")
