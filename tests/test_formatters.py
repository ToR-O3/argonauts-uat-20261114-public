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
