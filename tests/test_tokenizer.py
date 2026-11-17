"""Behavior checks for the standalone tokenizer."""

from importlib.util import find_spec


def test_casefolds_tokens_in_input_order():
    assert find_spec("wordfreq") is not None, "wordfreq package must exist"
    from wordfreq.tokenizer import iter_tokens

    assert list(iter_tokens("Hello hello HELLO world Straße STRASSE")) == [
        "hello", "hello", "hello", "world", "strasse", "strasse"
    ]


def test_excludes_punctuation_symbols_and_whitespace():
    from wordfreq.tokenizer import default_tokenizer, iter_tokens

    assert default_tokenizer("one, two. one!\tthree—four🙂five") == [
        "one", "two", "one", "three", "four", "five"
    ]
    assert list(iter_tokens("one, two. one")) == ["one", "two", "one"]
