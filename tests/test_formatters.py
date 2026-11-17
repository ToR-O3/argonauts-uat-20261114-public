"""Pure text and JSON output contracts."""
import importlib
import importlib.util
import json


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
