"""Pure text and JSON output contracts."""
import importlib
import importlib.util
import json
from html.parser import HTMLParser
import re


def test_format_text_count_tab_word_lines():
    assert importlib.util.find_spec("wordfreq.formatters") is not None, "formatting module is required"
    from wordfreq.formatters import format_text

    pairs = [("hello", 3), ("world", 1)]
    assert format_text(pairs) == "3\thello\n1\tworld\n"
    assert pairs == [("hello", 3), ("world", 1)]
    assert format_text([]) == ""
    assert format_text([("日本語", 1)]) == "1\t日本語\n"


def test_format_json_preserves_order_and_integer_counts():
    formatters = importlib.import_module("wordfreq.formatters")
    assert callable(getattr(formatters, "format_json", None)), "format_json is required"
    pairs = [("hello", 10**100), ("world", 1)]
    output = formatters.format_json(pairs)
    assert json.loads(output) == [
        {"word": "hello", "count": 10**100}, {"word": "world", "count": 1}
    ]
    assert output.endswith("\n")
    assert output.count("\n") == 1
    assert pairs == [("hello", 10**100), ("world", 1)]


def test_format_json_empty_array_has_one_newline():
    from wordfreq.formatters import format_json

    assert format_json([]) == "[]\n"
    assert json.loads(format_json([])) == []


def test_format_json_escapes_unicode_and_round_trips():
    from wordfreq.formatters import format_json

    word = '日本語"\\\n'
    output = format_json([(word, 3)])
    assert "\\u65e5" in output
    assert output.isascii()
    assert output.count("\n") == 1
    assert json.loads(output) == [{"word": word, "count": 3}]


class HTMLDocument(HTMLParser):
    """Strictly collect the document tree, without a browser dependency."""

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.stack = []
        self.declarations = []
        self.feed(source)
        self.close()
        assert self.stack == []

    def handle_decl(self, decl):
        self.declarations.append(decl)

    def handle_starttag(self, tag, attrs):
        assert len(attrs) == len(dict(attrs)), "duplicate attributes"
        node = {"tag": tag, "attrs": dict(attrs), "text": "",
                "ancestors": list(self.stack)}
        self.nodes.append(node)
        if tag != "meta":
            self.stack.append(node)

    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1]["tag"] == tag
        self.stack.pop()

    def handle_data(self, data):
        if self.stack:
            self.stack[-1]["text"] += data
        else:
            assert not data.strip()

    def handle_comment(self, data):
        raise AssertionError("no comments in the fixed document")

    def tagged(self, tag):
        return [node for node in self.nodes if node["tag"] == tag]

    def classified(self, name):
        return [node for node in self.nodes if node["attrs"].get("class") == name]


def assert_static_document(document):
    assert document.declarations == ["doctype html"]
    allowed = {
        "html": {"lang"}, "head": set(), "meta": {"charset", "name", "content"},
        "title": set(), "style": set(), "body": set(), "main": set(),
        "h1": set(), "div": {"class"}, "table": set(), "caption": set(),
        "thead": set(), "tbody": set(), "tr": set(), "th": {"class", "scope"},
        "td": {"class"}, "p": {"class"},
    }
    classes = {"metadata", "metadata-item", "label", "filename-value",
               "total-value", "rank", "word", "count", "empty-message"}
    for node in document.nodes:
        assert node["tag"] in allowed
        assert set(node["attrs"]) <= allowed[node["tag"]]
        if "class" in node["attrs"]:
            assert node["attrs"]["class"] in classes
    for tag in ["html", "head", "body", "main", "style", "title", "h1",
                "table", "caption", "thead", "tbody"]:
        assert len(document.tagged(tag)) == 1
    assert document.tagged("html")[0]["attrs"] == {"lang": "ja"}
    assert [node["attrs"] for node in document.tagged("meta")] == [
        {"charset": "utf-8"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ]
    assert document.tagged("title")[0]["text"] == "単語の出現頻度"
    assert document.tagged("h1")[0]["text"] == "単語の出現頻度"
    assert document.tagged("caption")[0]["text"] == "集計結果"
    headers = document.tagged("th")
    assert [node["text"] for node in headers] == ["順位", "単語", "回数"]
    assert [node["attrs"] for node in headers] == [
        {"class": name, "scope": "col"} for name in ["rank", "word", "count"]
    ]
    assert all(node["ancestors"][-2]["tag"] == "thead" for node in headers)
    table_position = document.nodes.index(document.tagged("table")[0])
    for name in ["filename-value", "total-value"]:
        assert len(document.classified(name)) == 1
        assert document.nodes.index(document.classified(name)[0]) < table_position
    css = document.tagged("style")[0]["text"]
    assert not re.search(r"url\s*\(|@import|expression\s*\(|javascript:|https?:|//", css, re.I)
    assert "\\" not in css  # No escaped CSS identifiers hiding resource paths.


def test_html_hostile_values_round_trip_once_as_text_only():
    from wordfreq.formatters import format_html

    # These deliberately bypass tokenizer: formatter must be independently safe.
    words = ['& < > " \'', '<img src=x onerror=alert(1)>',
             '</td><script>alert("x")</script>', '&lt;literal&gt;  \n\t日本語']
    pairs = [(word, count) for word, count in zip(words, [1, 9, 2, 4])]
    original = list(pairs)
    basename = '検査  &<>"\'\n次\t終.txt'
    output = format_html(pairs, basename, 200)
    document = HTMLDocument(output)
    assert_static_document(document)
    assert document.classified("filename-value")[0]["text"] == basename
    assert document.classified("total-value")[0]["text"] == "200"
    cells = document.tagged("td")
    assert [cell["text"] for cell in cells] == [
        value for i, (word, count) in enumerate(original, 1)
        for value in [str(i), word, str(count)]
    ]
    assert all(cell["ancestors"][-2]["tag"] == "tbody" for cell in cells)
    assert [cell["attrs"] for cell in cells] == [
        {"class": name} for _ in pairs for name in ["rank", "word", "count"]
    ]
    assert document.classified("empty-message") == []
    assert pairs == original  # Neither sorting nor aggregation nor mutation.
    assert "&quot;" in output and "&#x27;" in output  # quote=True, even in text.


def test_empty_html_keeps_metadata_and_headers_without_a_fake_row():
    from wordfreq.formatters import format_html

    pairs = []
    document = HTMLDocument(format_html(pairs, "empty.txt", 0))
    assert_static_document(document)
    assert document.classified("filename-value")[0]["text"] == "empty.txt"
    assert document.classified("total-value")[0]["text"] == "0"
    assert document.tagged("td") == []
    assert len(document.tagged("tr")) == 1  # Only the header row.
    message, = document.classified("empty-message")
    assert message["text"] == "集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。"
    assert all(node["tag"] != "tbody" for node in message["ancestors"])
    assert document.nodes.index(message) > document.nodes.index(document.tagged("table")[0])
    assert pairs == []
