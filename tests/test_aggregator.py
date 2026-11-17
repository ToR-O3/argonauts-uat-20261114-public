"""Standalone frequency aggregation contracts; no input source involved."""
from collections import Counter
import importlib
import importlib.util


def test_count_words_counts_an_iterator():
    assert importlib.util.find_spec("wordfreq.aggregator") is not None, "aggregation module is required"
    from wordfreq.aggregator import count_words

    result = count_words(iter(["hello", "world", "hello"]))
    assert isinstance(result, Counter)
    assert result == Counter({"hello": 2, "world": 1})
    assert count_words(iter([])) == Counter()
