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
               "total-value", "total-summary", "displayed-types",
               "rank", "word", "count", "empty-message"}
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


def test_html_preserves_cr_without_html_input_newline_normalization():
    from wordfreq.formatters import format_html

    basename = "a\rb\r\nc  \n\t.txt"
    word = "&<\r>\r\n'\"  \t"
    output = format_html([(word, 123)], basename, 123)
    # HTML input preprocessing normalizes raw CR/CRLF before tokenization;
    # Python's HTMLParser alone does not model that browser step.
    browser_input = output.replace("\r\n", "\n").replace("\r", "\n")
    document = HTMLDocument(browser_input)
    assert document.classified("filename-value")[0]["text"] == basename
    assert document.classified("word")[-1]["text"] == word
    assert_static_document(document)
    assert "\r" not in output
    assert output.count("&#13;") == 4


def test_long_whitespace_and_multidigit_values_survive_without_truncation():
    from wordfreq.formatters import format_html

    basename = '集計  ' + 'n' * 176 + '\n続き\t終わり  &<>"\'.txt'
    pairs = [("w" * 256, 123)] + [(f"row{i:02d}", 13 - i) for i in range(1, 12)]
    document = HTMLDocument(format_html(pairs, basename, 200))
    assert_static_document(document)
    assert document.classified("filename-value")[0]["text"] == basename
    assert document.classified("total-value")[0]["text"] == "200"
    assert [node["text"] for node in document.classified("rank")[1:]] == list(map(str, range(1, 13)))
    assert [node["text"] for node in document.classified("word")[1:]] == [word for word, _ in pairs]
    assert [node["text"] for node in document.classified("count")[1:]] == list(map(str, [123, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]))
    assert document.classified("empty-message") == []
    huge = 10**100
    document = HTMLDocument(format_html([("huge", huge)], basename, huge))
    assert document.classified("total-value")[0]["text"] == str(huge)
    assert document.classified("count")[-1]["text"] == str(huge)
    assert document.classified("rank")[-1]["text"] == "1"


def test_complete_fixed_css_contract_is_static_not_browser_acceptance():
    from wordfreq.formatters import format_html

    document = HTMLDocument(format_html([], "empty.txt", 0))
    assert_static_document(document)
    assert [node["text"] for node in document.classified("label")] == ["ファイル名", "総出現回数"]
    css = document.tagged("style")[0]["text"]
    # Exact fixed declarations reject additional theme branches, clipping,
    # scrolling, shrink-to-fit, animation and encoded communication paths.
    # This checks source declarations only; real geometry/images remain pending.
    narrow = '@media (max-width: 480px) { main { padding: 16px; } }'
    assert css.count(narrow) == 1
    rules = re.findall(r'([^{}]+)\{([^{}]*)\}', css.replace(narrow, ""))
    parsed = {}
    for selector, block in rules:
        selector = selector.strip()
        assert selector not in parsed
        parsed[selector] = dict(part.strip().split(":", 1) for part in block.split(";") if part.strip())
        parsed[selector] = {key.strip(): value.strip() for key, value in parsed[selector].items()}
    assert parsed == {
        ":root": {"color-scheme": "light"},
        "body": {"margin": "0", "background": "#FFFFFF", "color": "#0F172A",
                 "font-family": 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                 "font-size": "16px", "font-weight": "400", "line-height": "1.5"},
        "main": {"width": "100%", "max-width": "960px", "box-sizing": "border-box",
                 "margin": "0 auto", "padding": "32px"},
        "h1": {"margin": "0 0 16px", "color": "#1D4ED8", "font-size": "24px",
               "font-weight": "600", "line-height": "1.25", "overflow-wrap": "anywhere"},
        ".metadata": {"margin": "0 0 24px"},
        ".metadata-item + .metadata-item": {"margin-top": "8px"},
        ".label, caption, th": {"font-size": "14px", "font-weight": "600", "line-height": "1.5"},
        ".label": {"margin-bottom": "4px", "color": "#475569"},
        ".filename-value, .word": {"white-space": "break-spaces", "overflow-wrap": "anywhere",
                                    "word-break": "normal", "tab-size": "4"},
        ".total-value": {"color": "#1D4ED8"},
        ".total-summary": {"display": "flex", "flex-wrap": "wrap", "gap": "8px", "align-items": "baseline"},
        ".displayed-types": {"white-space": "pre-wrap", "overflow-wrap": "anywhere"},
        "table": {"width": "100%", "table-layout": "fixed", "border-collapse": "collapse"},
        "caption": {"text-align": "left", "color": "#475569", "margin-bottom": "8px"},
        "th, td": {"box-sizing": "border-box", "padding": "8px", "vertical-align": "top",
                   "text-align": "left", "overflow-wrap": "anywhere", "border-bottom": "1px solid #CBD5E1"},
        "th": {"background": "#F1F5F9"}, "td": {"background": "#FFFFFF"},
        ".rank, .count": {"text-align": "right", "font-variant-numeric": "tabular-nums"},
        ".rank": {"width": "56px"}, ".count": {"width": "64px"},
        ".empty-message": {"margin": "24px 0 0", "color": "#475569", "overflow-wrap": "anywhere"},
    }
    assert not re.search(r'overflow\s*:|hidden|clip|ellipsis|nowrap|min-width|(?<![-\w])height\s*:|clamp\(|scale\(|zoom\s*:|@font|@keyframes', css, re.I)


def assert_displayed_types(document, expected, total, basename):
    """Exact leaves, ancestry and source order; not a claim of horizontal render."""
    leaves = document.classified('displayed-types')
    assert len(leaves) == 1, 'missing unique displayed-types leaf'
    count, = leaves
    summary, = document.classified('total-summary')
    total_leaf, = document.classified('total-value')
    assert count['tag'] == total_leaf['tag'] == summary['tag'] == 'div'
    assert count['text'] == f'表示 {len(expected)} 種類'
    assert total_leaf['text'] == str(total)
    assert document.classified('filename-value')[0]['text'] == basename
    assert count['ancestors'][-1] is summary and total_leaf['ancestors'][-1] is summary
    children = [n for n in document.nodes if n['ancestors'] and n['ancestors'][-1] is summary]
    assert children == [total_leaf, count]
    assert document.nodes.index(total_leaf) < document.nodes.index(count) < document.nodes.index(document.tagged('table')[0])
    assert [n['text'] for n in document.tagged('td')] == [str(x) for i, (w, n) in enumerate(expected, 1) for x in (i, w, n)]
    assert len(document.tagged('tr')) == len(expected) + 1
    assert all(n['ancestors'][-2]['tag'] == 'tbody' for n in document.tagged('td'))
    assert_static_document(document)


def test_html_displayed_types():
    from wordfreq.formatters import format_html

    # Unsorted pairs and unrelated original totals distinguish len from sums/top.
    matrix = [([], 0), ([], 7), ([('zoo', 3)], 12),
              ([('alpha', 2), ('gamma', 1), ('delta', 1)], 7),
              ([(f'row{i}', 2) for i in range(10)], 27),
              ([(f'row{i}', 2) for i in range(12)], 27),
              ([('low', 1), ('high', 99)], 10**100),
              ([('&<\r>\"\'', 2)], 2)]
    for pairs, total in matrix:
        original = list(pairs)
        basename = '集計\r\n&<>\"\'.txt'
        document = HTMLDocument(format_html(pairs, basename, total))
        assert_displayed_types(document, original, total, basename)
        assert pairs == original
