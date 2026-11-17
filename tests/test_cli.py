"""Run the CLI in a real subprocess with separate output streams."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

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
    assert result.stdout == "3\thello\n2\tapple\n2\tone\n2\tzoo\n1\tb\n1\tc\n1\td\n1\te\n1\tf\n1\tg\n"


def test_top_three_selects_three_sorted_words(tmp_path):
    path = tmp_path / "input.txt"
    path.write_text("zoo apple apple bee cat", encoding="utf-8")
    result = run_cli(path, "--top", "3")
    assert result.returncode == 0, result.stderr
    assert result.stdout == "2\tapple\n1\tbee\n1\tcat\n"
    assert result.stderr == ""


def test_top_zero_is_usage_error_before_input_read(tmp_path):
    result = run_cli(tmp_path / "missing", "--top", "0")
    assert result.returncode == 2
    assert result.stdout == ""
    assert "--top must be >= 1" in result.stderr
    assert "Traceback" not in result.stderr


def test_json_is_machine_readable_in_frequency_then_word_order(tmp_path):
    path = tmp_path / "input.txt"
    path.write_text("Zoo zoo Apple apple Straße STRASSE 日本語", encoding="utf-8")
    result = run_cli(path, "--format", "json", "--top", "3")
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert json.loads(result.stdout) == [
        {"word": "apple", "count": 2},
        {"word": "strasse", "count": 2},
        {"word": "zoo", "count": 2},
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


def test_cli_leaves_input_and_git_worktree_unchanged(tmp_path):
    path = tmp_path / "input.txt"
    content = b"hello HELLO world"
    path.write_bytes(content)
    before = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=ROOT, capture_output=True, check=True).stdout
    result = run_cli(path)
    after = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=ROOT, capture_output=True, check=True).stdout
    assert result.returncode == 0
    assert result.stderr == ""
    assert path.read_bytes() == content
    assert list(tmp_path.iterdir()) == [path]
    assert after == before

