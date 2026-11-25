"""Run the CLI in a real subprocess with separate output streams."""
import json
from html.parser import HTMLParser
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

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


def test_json_is_machine_readable_in_frequency_then_initial_order(tmp_path):
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
        env=env, capture_output=True, text=True, timeout=10,
    )
    after = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, capture_output=True, check=True).stdout
    assert result.returncode == 0
    assert result.stderr == ""
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


class CLIHTML(HTMLParser):
    """Collect text-only table cells and separately identified metadata."""

    def __init__(self, document):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.values = {}
        self.headers = []
        self.target = None
        self.feed(document)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self.row = []
        if tag in {"td", "th"}:
            self.target = (tag, "")
        elif attrs.get("class") in {"filename-value", "total-value"}:
            self.target = (attrs["class"], "")

    def handle_data(self, data):
        if self.target is not None:
            kind, text = self.target
            self.target = (kind, text + data)

    def handle_endtag(self, tag):
        if self.target is not None:
            kind, text = self.target
            if kind == tag or kind in {"filename-value", "total-value"}:
                if kind == "td":
                    self.row.append(text)
                elif kind == "th":
                    self.headers.append(text)
                else:
                    self.values[kind] = text
                self.target = None
        if tag == "tr" and self.row:
            self.rows.append(self.row)


@pytest.mark.parametrize("top", [1, 2])
@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_normalized_tie_top_is_shared_by_all_formats(tmp_path, top, output_format):
    path = tmp_path / "tie.txt"
    path.write_text("Zoo apple APPLE zoo banana", encoding="utf-8")
    result = run_cli(path, "--top", top, "--format", output_format)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    expected = [("zoo", 2), ("apple", 2)][:top]
    if output_format == "text":
        assert result.stdout == "".join(f"{count}\t{word}\n" for word, count in expected)
    elif output_format == "json":
        assert json.loads(result.stdout) == [{"word": w, "count": c} for w, c in expected]
        assert result.stdout.endswith("\n")
    else:
        parsed = CLIHTML(result.stdout)
        assert parsed.headers == ["順位", "単語", "回数"]
        assert parsed.rows == [[str(i), w, str(c)] for i, (w, c) in enumerate(expected, 1)]
        assert parsed.values == {"filename-value": "tie.txt", "total-value": "5"}
        assert result.stdout.index('class="filename-value"') < result.stdout.index("<table")
        assert result.stdout.index('class="total-value"') < result.stdout.index("<table")
        assert str(tmp_path) not in result.stdout


@pytest.mark.skipif(os.name != "posix", reason="POSIX byte filenames")
@pytest.mark.parametrize("locale_name", ["en_US.utf8", "C.UTF-8"])
def test_html_replaces_non_utf8_basename_bytes(tmp_path, locale_name):
    path = os.fsencode(tmp_path) + b"/bad\xff.txt"
    with open(path, "wb") as source:
        source.write(b"hello hello world")
    env = os.environ.copy()
    env.pop("PYTHONIOENCODING", None)
    env.update(LC_ALL=locale_name, PYTHONUTF8="0", PYTHONCOERCECLOCALE="0")
    charmap = subprocess.run(["locale", "charmap"], env=env, capture_output=True, check=True, timeout=10)
    assert (charmap.stdout.strip(), charmap.stderr) == (b"UTF-8", b"")
    result = subprocess.run(
        [sys.executable, "-m", "wordfreq", path, "--format", "html"],
        cwd=ROOT, env=env, capture_output=True, timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    document = result.stdout.decode("utf-8", errors="strict")
    parsed = CLIHTML(document)
    assert parsed.values == {"filename-value": "bad\ufffd.txt", "total-value": "3"}
    assert parsed.rows == [["1", "hello", "2"], ["2", "world", "1"]]
    assert str(tmp_path) not in document


def encoding_probe(tmp_path, path, filesystem_encoding, stdout_encoding):
    diagnostic = tmp_path / "encoding-diagnostic.json"
    result = subprocess.run(
        [sys.executable, str(ROOT / "tests/fixtures/encoding_cli_probe.py"),
         str(diagnostic), filesystem_encoding, stdout_encoding, path, "--format", "html"],
        cwd=ROOT, capture_output=True, timeout=10)
    recorded = json.loads(diagnostic.read_text(encoding="utf-8"))
    assert recorded == {
        "kind": "controlled-seam-not-native-locale",
        "filesystem_display_encoding": filesystem_encoding,
        "stdout_encoding": stdout_encoding,
        "raw_path_hex": os.fsencode(path).hex(),
        "roundtrip_path_hex": os.fsencode(path).hex(),
    }
    return result


def native_encoding_env(locale_name):
    env = os.environ.copy()
    env.pop("PYTHONIOENCODING", None)
    env.update(LC_ALL=locale_name, PYTHONUTF8="0", PYTHONCOERCECLOCALE="0")
    charmap = subprocess.run(["locale", "charmap"], env=env, capture_output=True, check=True, timeout=10)
    expected = b"ANSI_X3.4-1968" if locale_name == "C" else b"ISO-8859-15"
    assert (charmap.stdout.strip(), charmap.stderr) == (expected, b"")
    return env


@pytest.mark.parametrize("available", [False, True])
def test_native_encoding_availability_and_charmap_mismatch(monkeypatch, available):
    # Deterministic native-present mismatch must fail, never silently fall back.
    real_run = subprocess.run

    def mismatch(argv, **kwargs):
        if argv == ["locale", "-a"]:
            return subprocess.CompletedProcess(argv, 0, b"en_GB.iso885915\n" if available else b"C\n", b"")
        if argv == ["locale", "charmap"]:
            return subprocess.CompletedProcess(argv, 0, b"UTF-8\n", b"")
        return real_run(argv, **kwargs)

    monkeypatch.setattr(subprocess, "run", mismatch)
    names = subprocess.run(["locale", "-a"], capture_output=True).stdout.splitlines()
    if b"en_GB.iso885915" in names:
        with pytest.raises(AssertionError):
            native_encoding_env("en_GB.iso885915")
    else:
        assert names == [b"C"]


def test_encoding_obligations_run_without_native_locale(tmp_path, monkeypatch):
    real_run = subprocess.run

    def without_iso(argv, **kwargs):
        if argv == ["locale", "-a"]:
            return subprocess.CompletedProcess(argv, 0, b"C\nC.utf8\n", b"")
        return real_run(argv, **kwargs)

    monkeypatch.setattr(subprocess, "run", without_iso)
    test_html_preserves_basename_in_filesystem_encoding(tmp_path)
    test_html_bytes_are_utf8_independent_of_stdout_encoding(tmp_path, "en_GB.iso885915", None)


@pytest.mark.skipif(os.name != "posix", reason="POSIX byte filenames")
def test_html_preserves_basename_in_filesystem_encoding(tmp_path):
    locale_name = "en_GB.iso885915"
    available = subprocess.run(
        ["locale", "-a"], capture_output=True, check=True, timeout=10,
    ).stdout.decode("ascii").splitlines()
    path = os.fsencode(tmp_path) + b"/caf\xe9.txt"
    with open(path, "wb") as source:
        source.write(b"hello hello world")
    controlled = encoding_probe(tmp_path, path, "iso8859-15", "latin-1")
    results = [controlled]
    if locale_name in available:
        env = native_encoding_env(locale_name)
        results.append(subprocess.run(
            [sys.executable, "-m", "wordfreq", path, "--format", "html"],
            cwd=ROOT, env=env, capture_output=True, timeout=10))
        print("native ISO-8859-15 filesystem check executed")
    else:
        print("native ISO-8859-15 unavailable; controlled byte check executed")
    for result in results:
        assert (result.returncode, result.stderr) == (0, b"")
        document = result.stdout.decode("utf-8", errors="strict")
        parsed = CLIHTML(document)
        assert parsed.values == {"filename-value": "café.txt", "total-value": "3"}
        assert parsed.rows == [["1", "hello", "2"], ["2", "world", "1"]]
        assert parsed.headers == ["順位", "単語", "回数"]
        assert str(tmp_path) not in document
        assert result.stdout == controlled.stdout
    with open(path, "rb") as source:
        assert source.read() == b"hello hello world"


@pytest.mark.parametrize("locale_name,io_encoding", [
    ("en_GB.iso885915", None),
    ("C", "latin-1"),
])
def test_html_bytes_are_utf8_independent_of_stdout_encoding(tmp_path, locale_name, io_encoding):
    path = tmp_path / "input.txt"
    path.write_text("hello hello 日本語", encoding="utf-8")
    controlled = encoding_probe(tmp_path, str(path), "utf-8", io_encoding or "iso8859-15")
    assert (controlled.returncode, controlled.stderr) == (0, b"")
    available = subprocess.run(["locale", "-a"], capture_output=True, check=True, timeout=10).stdout.decode("ascii").splitlines()
    result = controlled
    if locale_name == "C" or locale_name in available:
        env = native_encoding_env(locale_name)
        if io_encoding is not None:
            env["PYTHONIOENCODING"] = io_encoding
        result = subprocess.run(
            [sys.executable, "-m", "wordfreq", str(path), "--format", "html"],
            cwd=ROOT, env=env, capture_output=True, timeout=10)
        print(f"native {locale_name} stdout check executed")
    else:
        print("native ISO-8859-15 unavailable; controlled stdout check executed")
    assert path.read_bytes() == "hello hello 日本語".encode("utf-8")
    saved = tmp_path / "encoding-output.html"
    saved.write_bytes(result.stdout)
    assert saved.read_bytes() == controlled.stdout
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    document = result.stdout.decode("utf-8", errors="strict")
    assert '<meta charset="utf-8">' in document
    parsed = CLIHTML(document)
    assert parsed.headers == ["順位", "単語", "回数"]
    assert parsed.values == {"filename-value": "input.txt", "total-value": "3"}
    assert parsed.rows == [["1", "hello", "2"], ["2", "日本語", "1"]]


def run_cli_bytes(*args, env=None):
    return subprocess.run(
        [sys.executable, "-m", "wordfreq", *map(str, args)],
        cwd=ROOT, env=env, capture_output=True, timeout=10,
    )


def assert_output_bytes(raw, output_format, expected, basename, total):
    document = raw.decode("utf-8", errors="strict")
    if output_format == "text":
        assert document == "".join(f"{c}\t{w}\n" for w, c in expected)
    elif output_format == "json":
        assert raw.isascii()
        assert document.count("\n") == 1 and document.endswith("\n")
        assert json.loads(document) == [{"word": w, "count": c} for w, c in expected]
    else:
        parsed = CLIHTML(document)
        assert document.startswith('<!doctype html>\n')
        assert '<meta charset="utf-8">' in document
        assert parsed.headers == ["順位", "単語", "回数"]
        assert parsed.rows == [[str(i), w, str(c)] for i, (w, c) in enumerate(expected, 1)]
        assert parsed.values == {"filename-value": basename, "total-value": str(total)}
        for name in ["filename-value", "total-value"]:
            assert document.index(f'class="{name}"') < document.index("<table")


LONG_PAIRS = [("w" * 256, 123)] + [(f"row{i:02d}", 13 - i) for i in range(1, 12)]
LONG_CONTENT = " ".join(w for w, c in LONG_PAIRS for _ in range(c)) + "\n"


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("content,top,expected,total", [
    ("zoo apple zoo banana apple cherry", 1, [("zoo", 2)], 6),
    ("zoo apple zoo banana apple cherry", 2, [("zoo", 2), ("apple", 2)], 6),
    ("zoo apple zoo banana apple cherry", 10,
     [("zoo", 2), ("apple", 2), ("banana", 1), ("cherry", 1)], 6),
    ("beta beta beta alpha gamma alpha delta", 2, [("beta", 3), ("alpha", 2)], 7),
    ("", 10, [], 0),
    (LONG_CONTENT, None, LONG_PAIRS[:10], 200),
    (LONG_CONTENT, 99, LONG_PAIRS, 200),
    (LONG_CONTENT, 12, LONG_PAIRS, 200),
])
def test_all_format_explicit_metadata_matrix(tmp_path, output_format, content, top, expected, total):
    from html import escape

    parent = tmp_path / 'private-parent-&-marker' / 'nested-secret'
    parent.mkdir(parents=True)
    path = parent / "通常.txt"
    path.write_bytes(content.encode("utf-8"))
    args = [path, "--format", output_format]
    if top is not None:
        args += ["--top", top]
    result = run_cli_bytes(*args)
    assert (result.returncode, result.stderr) == (0, b"")
    assert_output_bytes(result.stdout, output_format, expected, path.name, total)
    if output_format == "html":
        document = result.stdout.decode("utf-8", errors="strict")
        for secret in [str(parent), str(path), parent.name, parent.parent.name]:
            assert secret not in document
            assert escape(secret, quote=True) not in document
    assert path.read_bytes() == content.encode("utf-8")


def test_saved_html_hostile_basename_utf8_privacy_and_static_safety(tmp_path):
    from html import escape
    from test_formatters import HTMLDocument, assert_static_document

    parent = tmp_path / 'unique-private-&-parent' / 'nested-sensitive'
    parent.mkdir(parents=True)
    basename = '検査  &<>"\'\n次\t終.txt'
    path = parent / basename
    path.write_bytes("Café CAFÉ Straße STRASSE 日本語".encode("utf-8"))
    result = run_cli_bytes(path, "--format", "html")
    assert (result.returncode, result.stderr) == (0, b"")
    saved = tmp_path / "saved.html"
    saved.write_bytes(result.stdout)
    assert saved.read_bytes() == result.stdout
    document = saved.read_bytes().decode("utf-8", errors="strict")
    assert_output_bytes(result.stdout, "html", [("café", 2), ("strasse", 2), ("日本語", 1)], basename, 5)
    assert_static_document(HTMLDocument(document))
    for secret in [str(parent), str(path), parent.name, parent.parent.name]:
        assert secret not in document
        assert escape(secret, quote=True) not in document


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("failure", ["missing", "directory", "decode", "permission"])
def test_real_input_failure_matrix(tmp_path, output_format, failure):
    path = tmp_path / "input.txt"
    if failure == "directory":
        path.mkdir()
    elif failure == "decode":
        path.write_bytes(b"hello\xff")
    elif failure == "permission":
        path.write_bytes(b"hello")
        path.chmod(0)
    try:
        if failure == "permission":
            # Prove EACCES under the same effective user, not just chmod intent.
            with pytest.raises(PermissionError, match="Permission denied"):
                path.read_bytes()
        result = run_cli_bytes(path, "--format", output_format)
        assert result.returncode == 1
        assert result.stdout == b""
        assert result.stderr and b"Traceback" not in result.stderr
        if failure == "permission":
            assert b"Permission denied" in result.stderr
    finally:
        if failure == "permission":
            path.chmod(0o600)


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("options", [("--top", "0"), ("--top", "-1"), ("--top", "abc"),
                                     ("--format", "xml"), ("extra.txt",)])
def test_real_usage_failure_matrix(tmp_path, output_format, options):
    result = run_cli_bytes(tmp_path / "missing", "--format", output_format, *options)
    assert result.returncode == 2
    assert result.stdout == b""
    assert result.stderr and b"Traceback" not in result.stderr


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_missing_argument_for_each_format(output_format):
    result = run_cli_bytes("--format", output_format)
    assert result.returncode == 2
    assert result.stdout == b""
    assert result.stderr and b"Traceback" not in result.stderr


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_permission_exception_maps_to_cli_exit_one(monkeypatch, capsys, output_format):
    from wordfreq.__main__ import main
    from wordfreq.sources import FileSource, InputError

    def denied(source):
        raise InputError("explicit permission denial") from PermissionError("denied")

    monkeypatch.setattr(FileSource, "read_text", denied)
    with pytest.raises(SystemExit) as caught:
        main(["input.txt", "--format", output_format])
    assert caught.value.code == 1
    output = capsys.readouterr()
    assert output.out == "" and output.err == "explicit permission denial\n"


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_hash_seed_does_not_change_output_bytes(tmp_path, output_format):
    path = tmp_path / "deterministic.txt"
    path.write_bytes("Zoo apple APPLE zoo banana Café CAFÉ 日本語".encode("utf-8"))
    outputs = []
    for seed in ["0", "1", "42"]:
        env = os.environ.copy()
        env["PYTHONHASHSEED"] = seed
        result = run_cli_bytes(path, "--format", output_format, env=env)
        assert (result.returncode, result.stderr) == (0, b"")
        assert_output_bytes(result.stdout, output_format,
                            [("zoo", 2), ("apple", 2), ("café", 2), ("banana", 1), ("日本語", 1)],
                            path.name, 8)
        outputs.append(result.stdout)
    assert outputs[0] == outputs[1] == outputs[2]


@pytest.mark.parametrize("basename", [
    '集計  ' + 'n' * 176 + '\n続き\t終わり  &<>"\'.txt',
    'a\rb\r\nc  \n\t.txt',
])
def test_real_html_preserves_full_long_and_cr_basename(tmp_path, basename):
    path = tmp_path / basename
    path.write_bytes(LONG_CONTENT.encode("utf-8"))
    result = run_cli_bytes(path, "--format", "html", "--top", "12")
    assert (result.returncode, result.stderr) == (0, b"")
    assert_output_bytes(result.stdout, "html", LONG_PAIRS, basename, 200)
    document = result.stdout.decode("utf-8", errors="strict")
    assert "\r" not in document
    browser_input = document.replace("\r\n", "\n").replace("\r", "\n")
    assert CLIHTML(browser_input).values["filename-value"] == basename
    assert path.read_bytes() == LONG_CONTENT.encode("utf-8")


# 04-02 tracer: argument acceptance and pre-I/O rejection (OpenSpec 1.2).
@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_min_count_argument_tracer(tmp_path, output_format):
    path = tmp_path / "input.txt"
    path.write_text("Zoo apple APPLE zoo banana", encoding="utf-8")
    default = run_cli_bytes(path, "--format", output_format)
    explicit = run_cli_bytes(path, "--format", output_format, "--min-count", "1")
    assert (explicit.returncode, explicit.stderr) == (0, b"")
    assert explicit.stdout == default.stdout
    assert_output_bytes(explicit.stdout, output_format,
                        [("zoo", 2), ("apple", 2), ("banana", 1)], path.name, 5)


@pytest.mark.parametrize("value", ["1", "2", "999999999999999999999999999999999999", "+2", "02"])
def test_min_count_parser_positive_integer(value):
    from wordfreq.__main__ import build_parser
    parser = build_parser()
    assert parser.parse_args(["input.txt"]).min_count == 1
    assert parser.parse_args(["input.txt", "--min-count", value]).min_count == int(value)


MIN_COUNT_INVALID = [("--min-count", "0"), ("--min-count", "-1"),
                     ("--min-count=-1",), ("--min-count", "1.5"),
                     ("--min-count", "abc"), ("--min-count",)]


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("options", MIN_COUNT_INVALID)
def test_min_count_invalid_before_read(tmp_path, monkeypatch, capsys, output_format, options):
    from wordfreq.__main__ import main
    from wordfreq.sources import FileSource
    calls = []

    def spy(source):
        calls.append(source)
        raise AssertionError("invalid threshold must not read input")

    monkeypatch.setattr(FileSource, "read_text", spy)
    with pytest.raises(SystemExit) as caught:
        main([str(tmp_path / "missing"), "--format", output_format, *options])
    assert caught.value.code == 2
    assert calls == []
    output = capsys.readouterr()
    assert output.out == "" and "--min-count" in output.err
    real = run_cli_bytes(tmp_path / "missing", "--format", output_format, *options)
    assert real.returncode == 2 and real.stdout == b""
    assert b"--min-count" in real.stderr and b"Traceback" not in real.stderr


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("failure", ["missing", "directory", "decode", "permission"])
def test_min_count_valid_input_failure(tmp_path, output_format, failure):
    path = tmp_path / "input.txt"
    if failure == "directory":
        path.mkdir()
    elif failure == "decode":
        path.write_bytes(b"hello\xff")
    elif failure == "permission":
        path.write_bytes(b"hello")
        path.chmod(0)
    try:
        if failure == "permission":
            with pytest.raises(PermissionError, match="Permission denied"):
                path.read_bytes()
        result = run_cli_bytes(path, "--min-count", "2", "--format", output_format)
        assert result.returncode == 1 and result.stdout == b""
        assert result.stderr and b"Traceback" not in result.stderr
        if failure == "permission":
            assert b"Permission denied" in result.stderr
    finally:
        if failure == "permission":
            path.chmod(0o600)


def test_min_count_help_and_readme_example(tmp_path):
    help_result = run_cli_bytes("--help")
    assert help_result.returncode == 0 and help_result.stderr == b""
    assert b"--min-count MIN_COUNT" in help_result.stdout
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python -m wordfreq input.txt --min-count 2 --top 1 --format json" in readme
    path = tmp_path / "input.txt"
    path.write_text("beta beta beta alpha gamma alpha delta", encoding="utf-8")
    result = run_cli_bytes(path, "--min-count", "2", "--top", "1", "--format", "json")
    assert (result.returncode, result.stdout, result.stderr) == (
        0, b'[{"word": "beta", "count": 3}]\n', b"")


# Both groups are authored/run before the common filter (OpenSpec 1.3/1.4).
@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("content,minimum,expected,total", [
    ("beta beta beta alpha gamma alpha delta", 1,
     [("beta", 3), ("alpha", 2), ("gamma", 1), ("delta", 1)], 7),
    ("beta beta beta alpha gamma alpha delta", 2, [("beta", 3), ("alpha", 2)], 7),
    ("beta beta beta alpha gamma alpha delta", 3, [("beta", 3)], 7),
    ("Zoo apple APPLE zoo banana", 2, [("zoo", 2), ("apple", 2)], 5),
    ("Straße STRASSE", 2, [("strasse", 2)], 2),
    ("日本語 日本語 Café CAFÉ banana", 2, [("日本語", 2), ("café", 2)], 5),
])
@pytest.mark.parametrize("top", [None, 1, 3, 10, 99])
@pytest.mark.parametrize("reverse", [False, True])
def test_min_count_selection(tmp_path, output_format, content, minimum, expected, total, top, reverse):
    path = tmp_path / "input.txt"
    path.write_text(content, encoding="utf-8")
    options = ["--min-count", str(minimum)]
    if top is not None:
        top_options = ["--top", str(top)]
        options = top_options + options if reverse else options + top_options
    result = run_cli_bytes(path, "--format", output_format, *options)
    assert (result.returncode, result.stderr) == (0, b"")
    assert_output_bytes(result.stdout, output_format,
                        expected[:10 if top is None else top], path.name, total)


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("content,minimum,top,expected,total", [
    ("beta beta beta alpha gamma alpha delta", 4, None, [], 7),
    ("beta beta beta alpha gamma alpha delta", 2, 1, [("beta", 3)], 7),
    ("Zoo apple APPLE zoo banana", 3, 10, [], 5),
    ("beta beta beta alpha gamma alpha delta", 10**100, 99, [], 7),
    ("", 2, None, [], 0), (" \t\r\n  ", 2, None, [], 0),
    ("!?,.;: --", 2, None, [], 0),
])
def test_min_count_empty_total(tmp_path, output_format, content, minimum, top, expected, total):
    from test_formatters import HTMLDocument, assert_static_document
    path = tmp_path / "empty-or-filtered.txt"
    path.write_text(content, encoding="utf-8")
    options = ["--min-count", str(minimum), "--format", output_format]
    if top is not None:
        options += ["--top", str(top)]
    result = run_cli_bytes(path, *options)
    assert (result.returncode, result.stderr) == (0, b"")
    assert_output_bytes(result.stdout, output_format, expected, path.name, total)
    if not expected:
        if output_format == "text":
            assert result.stdout == b""
        elif output_format == "json":
            assert result.stdout == b"[]\n"
        else:
            doc = HTMLDocument(result.stdout.decode("utf-8"))
            assert_static_document(doc)
            assert doc.tagged("td") == []
            assert len(doc.tagged("tr")) == 1
            assert doc.classified("empty-message")[0]["text"] == (
                "集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。")


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_min_count_selection_hashseed(tmp_path, output_format):
    path = tmp_path / "seed.txt"
    path.write_text("Zoo apple APPLE zoo banana Café CAFÉ 日本語", encoding="utf-8")
    outputs = []
    for seed in ["0", "1", "42"]:
        result = run_cli_bytes(path, "--min-count", "2", "--format", output_format,
                               env=dict(os.environ, PYTHONHASHSEED=seed))
        assert (result.returncode, result.stderr) == (0, b"")
        assert_output_bytes(result.stdout, output_format,
                            [("zoo", 2), ("apple", 2), ("café", 2)], path.name, 8)
        outputs.append(result.stdout)
    assert outputs[0] == outputs[1] == outputs[2]


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_min_count_selection_preserves_counter_and_shared_pairs(tmp_path, monkeypatch, output_format):
    from collections import Counter
    import wordfreq.__main__ as cli
    original_counts = Counter({"zoo": 2, "banana": 1, "apple": 2})
    original_items = list(original_counts.items())
    monkeypatch.setattr(cli, "count_words", lambda tokens: original_counts)
    selected = []
    real_top = cli.top_words
    real_formatter = getattr(cli, "format_" + output_format)
    calls = []

    def top_spy(counts, n):
        assert counts is not original_counts
        assert list(counts.items()) == [("zoo", 2), ("apple", 2)]
        pairs = real_top(counts, n)
        selected.append(pairs)
        return pairs

    def formatter_spy(pairs, *metadata):
        assert pairs is selected[0]
        assert pairs == [("zoo", 2)]
        assert metadata == (("input.txt", 5) if output_format == "html" else ())
        calls.append(True)
        return real_formatter(pairs, *metadata)

    monkeypatch.setattr(cli, "top_words", top_spy)
    monkeypatch.setattr(cli, "format_" + output_format, formatter_spy)
    path = tmp_path / "input.txt"
    path.write_text("Zoo banana apple APPLE zoo", encoding="utf-8")
    with pytest.raises(SystemExit) as caught:
        cli.main([str(path), "--min-count", "2", "--top", "1", "--format", output_format])
    assert caught.value.code == 0 and calls == [True]
    assert original_counts == Counter({"zoo": 2, "banana": 1, "apple": 2})
    assert list(original_counts.items()) == original_items


@pytest.mark.parametrize("case_index", range(12))
def test_min_count_saved_default_bytes(case_index):
    root = ROOT / ".planning/argonauts/r-e476c11d/baseline"
    index = json.loads((root / "index.json").read_text(encoding="utf-8"))
    case = index["cases"][case_index]
    capture_root = Path(index["root"])
    path = root / Path(case["input"]).relative_to(capture_root)
    expected = (root / Path(case["stdout"]).relative_to(capture_root)).read_bytes()
    assert path.read_bytes() == case["body"].encode("utf-8")
    options = ["--format", case["format"]] if case["explicit_format"] else []
    if case["top"] is not None:
        options += ["--top", str(case["top"])]
    env = os.environ.copy()
    for key, value in case["environment"].items():
        if value is None:
            env.pop(key, None)
        else:
            env[key] = value
    for minimum in [[], ["--min-count", "1"]]:
        result = run_cli_bytes(path, *options, *minimum, env=env)
        assert (result.returncode, result.stderr) == (0, b"")
        assert result.stdout == expected


# Phase 7 / OpenSpec 1.1: all groups below are authored and run before product edits.
MAX_NORMAL = "beta beta beta alpha gamma alpha delta"
MAX_THREE = "beta beta beta beta zoo zoo zoo apple apple pear pear single"
MAX_MANY_PAIRS = [(f"eligible{i:02d}", 2) for i in range(12)]
MAX_MANY_BODY = "over over over " + " ".join(w for w, n in MAX_MANY_PAIRS for _ in range(n))


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_max_count_tracer(tmp_path, output_format):
    path = tmp_path / "input.txt"
    path.write_text(MAX_NORMAL, encoding="utf-8")
    result = run_cli_bytes(path, "--max-count", "2", "--format", output_format)
    assert (result.returncode, result.stderr) == (0, b"")
    assert_output_bytes(result.stdout, output_format,
                        [("alpha", 2), ("gamma", 1), ("delta", 1)], path.name, 7)


@pytest.mark.parametrize("value", [None, "0", "-1", "+2", "02", str(10**100), str(-10**100)])
def test_max_count_parser(value):
    from wordfreq.__main__ import build_parser
    parser = build_parser()
    args = ["input.txt"] + ([] if value is None else ["--max-count=" + value])
    actual = parser.parse_args(args).max_count
    assert actual == (None if value is None else int(value))
    assert actual is None or type(actual) is int


def test_max_count_parser_equals_negative():
    from wordfreq.__main__ import build_parser
    assert build_parser().parse_args(["input.txt", "--max-count=-1"]).max_count == -1


def test_max_count_help():
    result = run_cli_bytes("--help")
    assert (result.returncode, result.stderr) == (0, b"")
    assert b"--max-count MAX_COUNT" in result.stdout


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("content,minimum,maximum,top,expected,total", [
    (MAX_NORMAL, 1, 2, None, [("alpha", 2), ("gamma", 1), ("delta", 1)], 7),
    (MAX_NORMAL, 1, 1, 3, [("gamma", 1), ("delta", 1)], 7),
    (MAX_NORMAL, 2, 2, None, [("alpha", 2)], 7),
    (MAX_NORMAL, 2, 3, None, [("beta", 3), ("alpha", 2)], 7),
    (MAX_NORMAL, 1, 2, 1, [("alpha", 2)], 7),
    (MAX_THREE, 2, 3, 1, [("zoo", 3)], 12),
    ("Straße STRASSE 日本語 日本語", 1, 1, None, [], 4),
    ("Straße STRASSE 日本語 日本語", 2, 2, None, [("strasse", 2), ("日本語", 2)], 4),
    ("Zoo apple APPLE zoo banana", 2, 2, 1, [("zoo", 2)], 5),
    ("Zoo apple APPLE zoo banana", 2, 2, 2, [("zoo", 2), ("apple", 2)], 5),
    ("zoo apple zoo apple zoo apple zoo apple zoo apple", 1, 5, None, [("zoo", 5), ("apple", 5)], 10),
    (MAX_MANY_BODY, 2, 2, None, MAX_MANY_PAIRS[:10], 27),
    (MAX_MANY_BODY, 2, 2, 3, MAX_MANY_PAIRS[:3], 27),
    (MAX_MANY_BODY, 2, 2, 99, MAX_MANY_PAIRS, 27),
    ("one", 1, 1, 3, [("one", 1)], 1),
])
def test_max_count_selection(tmp_path, output_format, reverse, content, minimum, maximum, top, expected, total):
    path = tmp_path / "input.txt"
    path.write_text(content, encoding="utf-8")
    low, high = ["--min-count", str(minimum)], ["--max-count", str(maximum)]
    options = high + low if reverse else low + high
    if top is not None:
        options += ["--top", str(top)]
    result = run_cli_bytes(path, "--format", output_format, *options)
    assert (result.returncode, result.stderr) == (0, b"")
    assert_output_bytes(result.stdout, output_format, expected, path.name, total)


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("content,minimum,maximum,total", [
    (MAX_NORMAL, 1, 0, 7), (MAX_NORMAL, 1, -1, 7),
    (MAX_NORMAL, 1, -10**100, 7), (MAX_NORMAL, 3, 2, 7),
    ("one", 1, 0, 1), ("", 1, 2, 0), (" \t\r\n  ", 1, 2, 0),
    ("!?,.;: --", 1, 2, 0), ("Zoo apple APPLE zoo banana", 3, 3, 5),
])
def test_max_count_empty(tmp_path, output_format, content, minimum, maximum, total):
    from test_formatters import HTMLDocument, assert_static_document
    path = tmp_path / "empty-or-filtered.txt"
    path.write_text(content, encoding="utf-8")
    result = run_cli_bytes(path, "--min-count", minimum, "--max-count", maximum, "--format", output_format)
    assert (result.returncode, result.stderr) == (0, b"")
    assert_output_bytes(result.stdout, output_format, [], path.name, total)
    if output_format == "html":
        document = HTMLDocument(result.stdout.decode("utf-8"))
        assert_static_document(document)
        assert document.tagged("td") == []
        assert document.classified("empty-message")[0]["text"] == (
            "集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。")


MAX_USAGE = [("--max-count", "abc"), ("--max-count", "1.5"), ("--max-count",)] + [
    ("--max-count", maximum, option, bad)
    for maximum in ("0", "-1") for option in ("--min-count", "--top") for bad in ("0", "-1", "abc", "1.5")
] + [("--max-count", "0", "--min-count"), ("--max-count", "-1", "--top")]


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("options", MAX_USAGE)
def test_max_count_invalid_before_read(tmp_path, monkeypatch, capsys, output_format, options):
    from wordfreq.__main__ import main
    from wordfreq.sources import FileSource
    calls = []

    def spy(source):
        calls.append(source)
        raise AssertionError("usage must not acquire input")

    monkeypatch.setattr(FileSource, "read_text", spy)
    args = [str(tmp_path / "missing"), "--format", output_format, *options]
    with pytest.raises(SystemExit) as caught:
        main(args)
    assert caught.value.code == 2 and calls == []
    output = capsys.readouterr()
    assert output.out == "" and "wordfreq: error:" in output.err
    assert "Traceback" not in output.err
    real = run_cli_bytes(*args)
    assert real.returncode == 2 and real.stdout == b""
    assert b"wordfreq: error:" in real.stderr and b"Traceback" not in real.stderr


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("options", [("--max-count", "0"), ("--max-count", "-1"),
                                      ("--min-count", "3", "--max-count", "2")])
@pytest.mark.parametrize("failure", ["missing", "directory", "decode", "permission"])
def test_max_count_input_failure(tmp_path, output_format, options, failure):
    path = tmp_path / "input.txt"
    if failure == "directory":
        path.mkdir()
    elif failure == "decode":
        path.write_bytes(b"hello\xff")
    elif failure == "permission":
        path.write_bytes(b"hello")
        path.chmod(0)
    try:
        if failure == "permission":
            with pytest.raises(PermissionError, match="Permission denied"):
                path.read_bytes()
        result = run_cli_bytes(path, "--format", output_format, *options)
        assert result.returncode == 1 and result.stdout == b""
        assert result.stderr and b"Traceback" not in result.stderr
        if failure == "permission":
            assert b"Permission denied" in result.stderr
    finally:
        if failure == "permission":
            path.chmod(0o600)


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_max_count_internal_order(tmp_path, monkeypatch, output_format):
    from collections import Counter
    import wordfreq.__main__ as cli
    original = Counter({"beta": 4, "zoo": 3, "apple": 2, "pear": 2, "single": 1})
    before = list(original.items())
    monkeypatch.setattr(cli, "count_words", lambda tokens: original)
    real_top = cli.top_words
    real_formatter = getattr(cli, "format_" + output_format)
    selected, formatted = [], []

    def top_spy(counts, n):
        assert counts is not original
        assert list(counts.items()) == [("zoo", 3), ("apple", 2), ("pear", 2)]
        pairs = real_top(counts, n)
        selected.append(pairs)
        return pairs

    def formatter_spy(pairs, *metadata):
        assert pairs is selected[0]
        assert pairs == [("zoo", 3)]
        assert metadata == (("input.txt", 12) if output_format == "html" else ())
        formatted.append(True)
        return real_formatter(pairs, *metadata)

    monkeypatch.setattr(cli, "top_words", top_spy)
    monkeypatch.setattr(cli, "format_" + output_format, formatter_spy)
    path = tmp_path / "input.txt"
    path.write_text(MAX_THREE, encoding="utf-8")
    with pytest.raises(SystemExit) as caught:
        cli.main([str(path), "--min-count", "2", "--max-count", "3", "--top", "1", "--format", output_format])
    assert caught.value.code == 0 and formatted == [True]
    assert list(original.items()) == before


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_max_count_hashseed(tmp_path, output_format):
    path = tmp_path / "seed.txt"
    path.write_text("Zoo apple APPLE zoo banana Café CAFÉ 日本語", encoding="utf-8")
    outputs = []
    for seed in ["0", "1", "42"]:
        result = run_cli_bytes(path, "--min-count", "2", "--max-count", "2", "--format", output_format,
                               env=dict(os.environ, PYTHONHASHSEED=seed))
        assert (result.returncode, result.stderr) == (0, b"")
        assert_output_bytes(result.stdout, output_format, [("zoo", 2), ("apple", 2), ("café", 2)], path.name, 8)
        outputs.append(result.stdout)
    assert outputs[0] == outputs[1] == outputs[2]


@pytest.mark.parametrize("case_index", range(39))
def test_max_count_saved_bytes(case_index):
    root = ROOT / ".planning/argonauts/r-d4bcda40/baseline"
    index = json.loads((root / "index.json").read_text(encoding="utf-8"))
    case = index["cases"][case_index]
    path = root / case["input"]
    assert path.read_bytes() == case["body"].encode("utf-8")
    expected = (root / case["stdout"]).read_bytes()
    for extra in [[], ["--max-count", str(10**100)], ["--min-count", "1"]
                  if "--min-count" not in case["options"] else []]:
        result = run_cli_bytes(path, *case["options"], *extra, env=index["environment"])
        assert (result.returncode, result.stderr) == (case["exit"], (root / case["stderr"]).read_bytes())
        assert result.stdout == expected


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_max_count_read_only(tmp_path, output_format):
    repo = tmp_path / "repo"
    repo.mkdir()
    shutil.copytree(ROOT / "wordfreq", repo / "wordfreq",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(ROOT / ".gitignore", repo / ".gitignore")
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    path = inputs / "input.txt"
    body = MAX_NORMAL.encode("utf-8")
    path.write_bytes(body)
    env = os.environ.copy()
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    before = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"],
                            cwd=repo, capture_output=True, check=True).stdout
    result = subprocess.run([sys.executable, "-m", "wordfreq", str(path), "--max-count", "2",
                             "--format", output_format], cwd=repo, env=env, capture_output=True, timeout=10)
    assert (result.returncode, result.stderr) == (0, b"")
    assert path.read_bytes() == body and list(inputs.iterdir()) == [path]
    after = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"],
                           cwd=repo, capture_output=True, check=True).stdout
    assert before == after


@pytest.mark.parametrize("mutation", ["ignore-upper", "exclusive", "or", "top-first",
                                     "destroy-counter", "recalculate-total", "lexical-ties"])
def test_max_count_discrimination(tmp_path, mutation):
    # Each single mutation runs only in a cold package copy under managed pytest scratch.
    repo = tmp_path / "mutant"
    repo.mkdir()
    shutil.copytree(ROOT / "wordfreq", repo / "wordfreq",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (repo / "tests").mkdir()
    shutil.copy2(ROOT / "tests/test_cli.py", repo / "tests/test_cli.py")
    source = repo / "wordfreq/__main__.py"
    original = source.read_text(encoding="utf-8")
    upper = "and (args.max_count is None or count <= args.max_count)"
    if mutation == "ignore-upper":
        changed = original.replace(upper, "")
    elif mutation == "exclusive":
        changed = original.replace("count <= args.max_count", "count < args.max_count")
    elif mutation == "or":
        changed = original.replace(upper, upper.replace("and", "or", 1))
    elif mutation == "top-first":
        start = original.index("    selected_counts = Counter(")
        end = original.index('    if args.format == "html":', start)
        changed = original[:start] + (
            "    pairs = [(word, count) for word, count in top_words(counts, args.top)\n"
            "             if count >= args.min_count and (args.max_count is None or count <= args.max_count)]\n"
        ) + original[end:]
    elif mutation == "destroy-counter":
        changed = original.replace("    pairs = top_words", "    counts.clear()\n    pairs = top_words")
    elif mutation == "recalculate-total":
        changed = original.replace("    pairs = top_words", "    total = sum(selected_counts.values())\n    pairs = top_words")
    else:
        source = repo / "wordfreq/aggregator.py"
        original = source.read_text(encoding="utf-8")
        changed = original.replace("key=lambda wc: -wc[1]", "key=lambda wc: (-wc[1], wc[0])")
    assert changed != original, "mutation must hit exactly the current implementation seam"
    source.write_text(changed, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_cli.py", "-k",
         "max_count_tracer or max_count_selection or max_count_internal_order", "-q"],
        cwd=repo, env=dict(os.environ, PYTHONPATH=os.environ.get("PYTHONPATH", "")),
        capture_output=True, timeout=90,
    )
    print("MUTATION", mutation, "exit", result.returncode)
    print(result.stdout.decode("utf-8"))
    print(result.stderr.decode("utf-8"))
    assert result.returncode == 1
    assert b"AssertionError" in result.stdout
    assert b"ERROR collecting" not in result.stdout and b"SyntaxError" not in result.stdout

