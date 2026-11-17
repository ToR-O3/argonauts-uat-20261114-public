"""Static HTML contracts; real-browser acceptance is a separate phase gate."""
from html.parser import HTMLParser
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
