"""Behavior checks for the standalone tokenizer."""

from importlib.util import find_spec


def test_casefolds_tokens_in_input_order():
    assert find_spec("wordfreq") is not None, "wordfreq package must exist"
    from wordfreq.tokenizer import iter_tokens

    assert list(iter_tokens("Hello hello HELLO world Straße STRASSE")) == [
        "hello", "hello", "hello", "world", "strasse", "strasse"
    ]
