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


def test_top_words_sorts_frequency_then_first_seen():
    aggregator = importlib.import_module("wordfreq.aggregator")
    assert callable(getattr(aggregator, "top_words", None)), "top_words is required"
    counts = Counter({"zoo": 5, "rare": 1, "middle": 3, "apple": 5})
    original = counts.copy()
    assert aggregator.top_words(counts, 3) == [("zoo", 5), ("apple", 5), ("middle", 3)]
    assert counts == original


def test_top_words_handles_result_limits_and_empty_input():
    from wordfreq.aggregator import top_words

    counts = Counter({"zoo": 5, "apple": 5})
    assert top_words(counts, 10) == [("zoo", 5), ("apple", 5)]
    assert top_words(counts, 2) == [("zoo", 5), ("apple", 5)]
    assert top_words(counts, 1) == [("zoo", 5)]
    assert top_words(Counter(), 10) == []


def test_top_words_preserves_large_integer_counts():
    from wordfreq.aggregator import top_words

    huge = 10**100
    assert top_words(Counter({"zoo": huge, "apple": huge + 1}), 2) == [
        ("apple", huge + 1), ("zoo", huge)
    ]


def test_first_seen_after_casefold():
    from wordfreq.aggregator import count_words, top_words
    from wordfreq.tokenizer import iter_tokens

    for text, expected in [
        ("Zoo apple zoo APPLE beta", [("zoo", 2), ("apple", 2), ("beta", 1)]),
        ("ZOO Straße zoo STRASSE beta", [("zoo", 2), ("strasse", 2), ("beta", 1)]),
        ("early late late", [("late", 2), ("early", 1)]),
    ]:
        counts = count_words(iter_tokens(text))
        before = list(counts.items())
        assert top_words(counts, 10) == expected
        assert top_words(counts, 1) == expected[:1]
        assert list(counts.items()) == before
