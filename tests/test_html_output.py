"""Static HTML contracts; real-browser acceptance is a separate phase gate."""
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.declarations = []
        self.headers = []
        self.rows = []
        self.values = {}
        self.stack = []

    def handle_decl(self, decl):
        self.declarations.append(decl)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "tr":
            self.rows.append([])
        if tag in ("th", "td"):
            self.rows[-1].append("")
        if tag == "th":
            self.headers.append(attrs)
        if "id" in attrs:
            self.values[attrs["id"]] = ""
        if tag not in ("meta", "col"):
            self.stack.append((tag, attrs))

    def handle_endtag(self, tag):
        assert self.stack[-1][0] == tag
        self.stack.pop()

    def handle_data(self, data):
        for tag, attrs in self.stack:
            if "id" in attrs:
                self.values[attrs["id"]] += data
        if self.stack and self.stack[-1][0] in ("th", "td"):
            self.rows[-1][-1] += data


def parse_report(document):
    parser = ReportParser()
    parser.feed(document)
    parser.close()
    assert not parser.stack
    return parser


def run_html_cli(path, *args):
    return subprocess.run(
        [sys.executable, "-m", "wordfreq", str(path), "--format", "html", *args],
        cwd=ROOT, capture_output=True, timeout=10,
    )


@pytest.mark.parametrize("stdio_encoding", ["cp932", "ascii"])
def test_cli_html_is_utf8_regardless_of_stdio_encoding(tmp_path, stdio_encoding):
    path = tmp_path / "資料.txt"
    original = "日本語 Zoo zoo".encode("utf-8")
    path.write_bytes(original)
    result = subprocess.run(
        [sys.executable, "-m", "wordfreq", str(path), "--format", "html"],
        cwd=ROOT, capture_output=True, timeout=10,
        env={**os.environ, "PYTHONIOENCODING": stdio_encoding},
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    destination = tmp_path / "report.html"
    destination.write_bytes(result.stdout)
    report = parse_report(destination.read_bytes().decode("utf-8"))
    assert ("meta", {"charset": "utf-8"}) in report.tags
    assert report.values["filename"] == "資料.txt"
    assert report.rows[1:] == [["1", "zoo", "2"], ["2", "日本語", "1"]]
    assert path.read_bytes() == original


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX byte filenames")
def test_cli_html_replaces_undecodable_basename_only_for_display(tmp_path):
    raw_path = os.fsencode(tmp_path) + b"/x\xff<&.txt"
    original = "日本語 Zoo zoo".encode("utf-8")
    try:
        with open(raw_path, "wb") as source:
            source.write(original)
    except (OSError, UnicodeError) as error:
        pytest.skip(f"filesystem rejects byte filename: {error}")
    path = os.fsdecode(raw_path)
    result = run_html_cli(path)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    document = result.stdout.decode("utf-8")
    report = parse_report(document)
    assert report.values["filename"] == "x\ufffd<&.txt"
    assert "x\ufffd&lt;&amp;.txt" in document
    assert str(tmp_path) not in document
    assert report.rows[1:] == [["1", "zoo", "2"], ["2", "日本語", "1"]]
    with open(raw_path, "rb") as source:
        assert source.read() == original


def test_cli_html_saved_document(tmp_path):
    inputs = tmp_path / "private-directory"
    inputs.mkdir()
    path = inputs / "資料.txt"
    original = b"one one one two two three"
    path.write_bytes(original)
    result = run_html_cli(path)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    destination = tmp_path / "report.html"
    destination.write_bytes(result.stdout)
    document = destination.read_bytes().decode("utf-8")
    report = parse_report(document)
    assert report.declarations == ["DOCTYPE html"]
    for tag in ("html", "head", "body", "main", "table", "thead", "tbody", "title", "h1"):
        assert sum(t == tag for t, _ in report.tags) == 1
    assert ("html", {"lang": "ja"}) in report.tags
    assert ("meta", {"charset": "utf-8"}) in report.tags
    assert ("meta", {"name": "viewport", "content": "width=device-width, initial-scale=1"}) in report.tags
    assert report.rows == [["順位", "単語", "回数"], ["1", "one", "3"], ["2", "two", "2"], ["3", "three", "1"]]
    assert report.headers == [{"scope": "col"}] * 3
    assert report.values["filename"] == path.name
    assert report.values["total-count"] == "6"
    assert document.index('id="filename"') < document.index('<table')
    assert document.index('id="total-count"') < document.index('<table')
    assert "private-directory" not in document
    assert path.read_bytes() == original


@pytest.mark.parametrize("content,expected,total", [("", [], "0"), (" !? \t\n", [], "0"), ("日本語", [["1", "日本語", "1"]], "1")])
def test_html_empty_and_single(tmp_path, content, expected, total):
    path = tmp_path / "入力.txt"
    path.write_text(content, encoding="utf-8")
    before = path.read_bytes()
    result = run_html_cli(path)
    assert result.returncode == 0
    assert result.stderr == b""
    report = parse_report(result.stdout.decode("utf-8"))
    assert report.rows == [["順位", "単語", "回数"], *expected]
    assert report.values["total-count"] == total
    assert path.read_bytes() == before


@pytest.mark.parametrize("value", [
    '& < > " \' &amp; &#13; <script>alert(1)</script>',
    " 日本語  \t\n\r\r\n終端 ",
])
def test_html_safe_text(value):
    from wordfreq.formatters import format_html

    pairs = [(value, 2), ("last", 9)]
    original = pairs.copy()
    document = format_html(pairs, filename=value, total_count=123)
    # Simulate HTML input-stream newline processing before character references.
    report = parse_report(document.replace("\r\n", "\n").replace("\r", "\n"))
    assert report.values["filename"] == value
    assert report.values["total-count"] == "123"
    assert report.rows[1:] == [["1", value, "2"], ["2", "last", "9"]]
    assert pairs == original
    assert not any(tag in {"script", "img", "a", "link", "iframe", "svg"} for tag, _ in report.tags)
    assert not any(key.startswith("on") or key in {"href", "src"} for _, attrs in report.tags for key in attrs)
    assert "\r" not in document
    assert "&#13;" in document if "\r" in value else True


def test_html_metadata_top1(tmp_path):
    path = tmp_path / "nested"
    path.mkdir()
    path = path / "資料.txt"
    path.write_text("Zoo apple zoo APPLE beta", encoding="utf-8")
    result = run_html_cli(path, "--top", "1")
    assert result.returncode == 0
    assert result.stderr == b""
    report = parse_report(result.stdout.decode("utf-8"))
    assert report.values["total-count"] == "5"
    assert report.values["filename"] == "資料.txt"
    assert report.rows[1:] == [["1", "zoo", "2"]]


@pytest.mark.parametrize("content,pairs", [
    ("Zoo apple zoo APPLE beta", [("zoo", 2), ("apple", 2), ("beta", 1)]),
    ("ZOO Straße zoo STRASSE beta", [("zoo", 2), ("strasse", 2), ("beta", 1)]),
    ("early late late", [("late", 2), ("early", 1)]),
])
@pytest.mark.parametrize("output_format", ["text", "json", "html"])
@pytest.mark.parametrize("top", [1, 10])
def test_html_first_seen_cases(tmp_path, content, pairs, output_format, top):
    path = tmp_path / "input.txt"
    path.write_text(content, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "wordfreq", str(path), "--format", output_format, "--top", str(top)],
        cwd=ROOT, capture_output=True, timeout=10,
    )
    assert result.returncode == 0
    assert result.stderr == b""
    selected = pairs[:top]
    if output_format == "html":
        report = parse_report(result.stdout.decode("utf-8"))
        assert report.rows[1:] == [[str(i), word, str(count)] for i, (word, count) in enumerate(selected, 1)]
        assert report.values["total-count"] == str(sum(count for _, count in pairs))
    elif output_format == "json":
        assert json.loads(result.stdout) == [{"word": word, "count": count} for word, count in selected]
    else:
        assert result.stdout == "".join(f"{count}\t{word}\n" for word, count in selected).encode("utf-8")


@pytest.mark.parametrize("output_format", ["text", "json", "html"])
def test_all_format_seed_bytes(tmp_path, output_format):
    path = tmp_path / "input.txt"
    path.write_text("Zoo Straße APPLE zoo STRASSE apple 日本語", encoding="utf-8")
    outputs = []
    for seed in ("1", "777"):
        result = subprocess.run(
            [sys.executable, "-m", "wordfreq", str(path), "--format", output_format],
            cwd=ROOT, capture_output=True, timeout=10,
            env={**os.environ, "PYTHONHASHSEED": seed, "PYTHONIOENCODING": "utf-8"},
        )
        assert result.returncode == 0
        assert result.stderr == b""
        outputs.append(result.stdout)
    assert outputs[0] == outputs[1]
