"""Run the CLI in a real subprocess with separate output streams."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

import pytest

from test_html_output import parse_report

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "wordfreq", *map(str, args)],
        cwd=ROOT, capture_output=True, text=True, timeout=10,
    )


def test_default_text_normalizes_sorts_and_limits_to_ten(tmp_path):
    path = tmp_path / "input.txt"
    path.write_text("Zoo APPLE apple zoo Hello hello HELLO one, two. one b c d e f g h", encoding="utf-8")
    result = run_cli(path)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == "3\thello\n2\tzoo\n2\tapple\n2\tone\n1\ttwo\n1\tb\n1\tc\n1\td\n1\te\n1\tf\n"


def test_top_three_selects_three_sorted_words(tmp_path):
    path = tmp_path / "input.txt"
    path.write_text("zoo apple apple bee cat", encoding="utf-8")
    result = run_cli(path, "--top", "3")
    assert result.returncode == 0, result.stderr
    assert result.stdout == "2\tapple\n1\tzoo\n1\tbee\n"
    assert result.stderr == ""


def test_top_zero_is_usage_error_before_input_read(tmp_path):
    result = run_cli(tmp_path / "missing", "--top", "0")
    assert result.returncode == 2
    assert result.stdout == ""
    assert "--top must be >= 1" in result.stderr
    assert "Traceback" not in result.stderr


def test_json_is_machine_readable_in_frequency_then_first_seen_order(tmp_path):
    path = tmp_path / "input.txt"
    path.write_text("Zoo zoo Apple apple Straße STRASSE 日本語", encoding="utf-8")
    result = run_cli(path, "--format", "json", "--top", "3")
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert json.loads(result.stdout) == [
        {"word": "zoo", "count": 2},
        {"word": "apple", "count": 2},
        {"word": "strasse", "count": 2},
    ]
    assert result.stdout.endswith("\n")
    assert len(result.stdout.splitlines()) == 1


def test_missing_file_is_single_line_error_without_traceback(tmp_path):
    result = run_cli(tmp_path / "missing")
    assert result.returncode == 1
    assert result.stdout == ""
    assert len(result.stderr.splitlines()) == 1
    assert "missing" in result.stderr
    assert "Traceback" not in result.stderr


def test_top_three_outputs_all_when_fewer_words_exist(tmp_path):
    path = tmp_path / "input.txt"
    path.write_text("zoo apple apple", encoding="utf-8")
    result = run_cli(path, "--top", "3")
    assert (result.returncode, result.stdout, result.stderr) == (0, "2\tapple\n1\tzoo\n", "")


def test_top_one_is_smallest_allowed_limit(tmp_path):
    path = tmp_path / "input.txt"
    path.write_text("zoo apple apple", encoding="utf-8")
    result = run_cli(path, "--top", "1")
    assert (result.returncode, result.stdout, result.stderr) == (0, "2\tapple\n", "")


@pytest.mark.parametrize("options", [("--top", "abc"), ("--top=-1",), ("--top", "-1")])
def test_invalid_top_is_usage_error(tmp_path, options):
    result = run_cli(tmp_path / "missing", *options)
    assert result.returncode == 2
    assert result.stdout == ""
    assert "wordfreq: error:" in result.stderr
    assert "Traceback" not in result.stderr


def test_invalid_format_is_usage_error(tmp_path):
    result = run_cli(tmp_path / "missing", "--format", "xml")
    assert result.returncode == 2
    assert result.stdout == ""
    assert "invalid choice" in result.stderr
    assert "Traceback" not in result.stderr


def test_no_file_is_usage_error():
    result = run_cli()
    assert result.returncode == 2
    assert result.stdout == ""
    assert "filename" in result.stderr
    assert "Traceback" not in result.stderr


def test_two_files_are_usage_error(tmp_path):
    result = run_cli(tmp_path / "first", tmp_path / "second")
    assert result.returncode == 2
    assert result.stdout == ""
    assert "unrecognized arguments" in result.stderr
    assert "Traceback" not in result.stderr


def test_invalid_utf8_is_single_line_input_error(tmp_path):
    path = tmp_path / "invalid.txt"
    path.write_bytes(b"hello\xff")
    result = run_cli(path)
    assert result.returncode == 1
    assert result.stdout == ""
    assert len(result.stderr.splitlines()) == 1
    assert "Traceback" not in result.stderr


def test_unopenable_directory_is_single_line_input_error(tmp_path):
    result = run_cli(tmp_path)
    assert result.returncode == 1
    assert result.stdout == ""
    assert len(result.stderr.splitlines()) == 1
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("output_format,expected", [("text", ""), ("json", "[]\n")])
def test_empty_file_is_success(tmp_path, output_format, expected):
    path = tmp_path / "empty.txt"
    path.write_bytes(b"")
    result = run_cli(path, "--format", output_format)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


def test_explicit_text_format_matches_default(tmp_path):
    path = tmp_path / "input.txt"
    path.write_text("hello HELLO world", encoding="utf-8")
    result = run_cli(path, "--format", "text")
    assert (result.returncode, result.stdout, result.stderr) == (0, "2\thello\n1\tworld\n", "")


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_cli_leaves_input_and_git_worktree_unchanged(tmp_path, output_format):
    # A cold package in its own repo prevents earlier tests from hiding writes.
    repo = tmp_path / "repo"
    repo.mkdir()
    shutil.copytree(ROOT / "wordfreq", repo / "wordfreq",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    if (ROOT / ".gitignore").exists():
        shutil.copy2(ROOT / ".gitignore", repo / ".gitignore")
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
    # Track the baseline so content changes show up, not just new paths.
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    path = inputs / "input.txt"
    content = b"hello HELLO world"
    path.write_bytes(content)
    env = os.environ.copy()
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    before = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, capture_output=True, check=True).stdout
    result = subprocess.run(
        [sys.executable, "-m", "wordfreq", str(path), "--format", output_format], cwd=repo,
        env=env, capture_output=True, timeout=10,
    )
    after = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, capture_output=True, check=True).stdout
    assert result.returncode == 0
    assert result.stderr == b""
    if output_format == "html":
        destination = tmp_path / "report.html"
        destination.write_bytes(result.stdout)
        report = parse_report(destination.read_bytes().decode("utf-8"))
        assert report.values["total-count"] == "3"
        assert report.rows[1:] == [["1", "hello", "2"], ["2", "world", "1"]]
    assert path.read_bytes() == content
    assert list(inputs.iterdir()) == [path]
    assert after == before


def test_package_declares_only_development_dependencies():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["project"]["name"] == "wordfreq"
    assert config["project"]["dependencies"] == []
    assert config["project"]["optional-dependencies"] == {"dev": ["pytest"]}
    assert config["build-system"]["build-backend"] == "setuptools.build_meta"
    assert config["tool"]["setuptools"]["packages"] == ["wordfreq"]


def test_readme_runs_as_json_from_repository_without_installation():
    result = run_cli(ROOT / "README.md", "--format", "json")
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert isinstance(json.loads(result.stdout), list)


def assert_format_output(output, output_format, pairs, filename, total):
    """Compare independent oracles, without using production serializers."""
    if output_format == "text":
        assert output == "".join(f"{count}\t{word}\n" for word, count in pairs)
    elif output_format == "json":
        assert json.loads(output) == [{"word": word, "count": count} for word, count in pairs]
        assert output.isascii()
        assert output.count("\n") == 1
        assert output.endswith("\n")
    else:
        report = parse_report(output)
        assert report.declarations == ["DOCTYPE html"]
        assert output.startswith("<!DOCTYPE html>\n")
        assert output.endswith("</html>\n")
        assert sum(tag == "html" for tag, _ in report.tags) == 1
        assert report.rows == [["順位", "単語", "回数"], *[
            [str(i), word, str(count)] for i, (word, count) in enumerate(pairs, 1)
        ]]
        assert report.values == {"filename": filename, "total-count": str(total)}


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("top", [None, 1, 3, 50])
@pytest.mark.parametrize("content,pairs,total", [
    ("one one one two two three", [("one", 3), ("two", 2), ("three", 1)], 6),
    ("", [], 0),
    (" \t\r\n!?。、", [], 0),
    ("日本語 Straße STRASSE café CAFÉ 123 _", [("strasse", 2), ("café", 2), ("日本語", 1), ("123", 1), ("_", 1)], 7),
    ("z a b c d e f g h i j k", [(word, 1) for word in "z a b c d e f g h i j k".split()], 12),
])
def test_all_format_contract_matrix(tmp_path, output_format, top, content, pairs, total):
    path = tmp_path / "資料.txt"
    original = content.encode("utf-8")
    path.write_bytes(original)
    options = [] if top is None else ["--top", str(top)]
    result = run_cli(path, "--format", output_format, *options)
    assert (result.returncode, result.stderr) == (0, "")
    assert_format_output(result.stdout, output_format, pairs[:10 if top is None else top], path.name, total)
    assert path.read_bytes() == original


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("case,code,message", [
    ("zero", 2, "--top must be >= 1"),
    ("negative", 2, "--top must be >= 1"),
    ("noninteger", 2, "invalid int value"),
    ("format", 2, "invalid choice"),
    ("no-file", 2, "filename"),
    ("two-files", 2, "unrecognized arguments"),
    ("missing", 1, "missing.txt"),
    ("directory", 1, "directory"),
    ("utf8", 1, "decode"),
])
def test_all_format_error_matrix(tmp_path, output_format, case, code, message):
    path = tmp_path / "input.txt"
    path.write_bytes(b"hello\xff" if case == "utf8" else b"hello")
    args = [path, "--format", output_format]
    if case in {"zero", "negative", "noninteger"}:
        args += ["--top", {"zero": "0", "negative": "-1", "noninteger": "abc"}[case]]
    elif case == "format":
        args += ["--format", "xml"]
    elif case == "no-file":
        args = ["--format", output_format]
    elif case == "two-files":
        args.append(path)
    elif case == "missing":
        args[0] = tmp_path / "missing.txt"
    elif case == "directory":
        args[0] = tmp_path
    result = run_cli(*args)
    assert result.returncode == code
    assert result.stdout == ""
    assert message in result.stderr
    assert "Traceback" not in result.stderr
    if code == 1:
        assert len(result.stderr.splitlines()) == 1


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("top", [1, 3])
@pytest.mark.parametrize("content,pairs,total", [
    ("Zoo apple zoo APPLE beta", [("zoo", 2), ("apple", 2), ("beta", 1)], 5),
    ("ZOO Straße zoo STRASSE beta", [("zoo", 2), ("strasse", 2), ("beta", 1)], 5),
    ("early late late", [("late", 2), ("early", 1)], 3),
])
def test_all_format_first_seen_and_seed(tmp_path, output_format, top, content, pairs, total):
    path = tmp_path / "input.txt"
    path.write_text(content, encoding="utf-8")
    outputs = []
    for seed in ("1", "777"):
        result = subprocess.run(
            [sys.executable, "-m", "wordfreq", str(path), "--format", output_format, "--top", str(top)],
            cwd=ROOT, capture_output=True, timeout=10,
            env={**os.environ, "PYTHONHASHSEED": seed, "PYTHONIOENCODING": "utf-8"},
        )
        assert (result.returncode, result.stderr) == (0, b"")
        assert_format_output(result.stdout.decode("utf-8"), output_format, pairs[:top], path.name, total)
        outputs.append(result.stdout)
    assert outputs[0] == outputs[1]


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_cli_parallel_distinct_outputs(tmp_path, output_format):
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    path = inputs / "資料.txt"
    original = "Zoo Straße zoo STRASSE 日本語".encode("utf-8")
    path.write_bytes(original)
    args = [sys.executable, "-m", "wordfreq", str(path), "--format", output_format]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    serial = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, timeout=10)
    assert (serial.returncode, serial.stderr) == (0, b"")
    destinations = [tmp_path / f"report-{i}.{output_format}" for i in range(2)]
    with destinations[0].open("wb") as first, destinations[1].open("wb") as second:
        with subprocess.Popen(args, cwd=ROOT, env=env, stdout=first, stderr=subprocess.PIPE) as one, \
             subprocess.Popen(args, cwd=ROOT, env=env, stdout=second, stderr=subprocess.PIPE) as two:
            try:
                for process in (one, two):
                    _, stderr = process.communicate(timeout=10)
                    assert (process.returncode, stderr) == (0, b"")
            finally:
                for process in (one, two):
                    if process.poll() is None:
                        process.kill()
                        process.wait(timeout=10)
    # Observe only completed files; partial stdout is not atomic storage.
    assert all(destination.read_bytes() == serial.stdout for destination in destinations)
    assert path.read_bytes() == original
    assert list(inputs.iterdir()) == [path]
