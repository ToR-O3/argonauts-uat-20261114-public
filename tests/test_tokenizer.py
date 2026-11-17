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


def test_preserves_underscores_and_digits_as_word_characters():
    from wordfreq.tokenizer import iter_tokens

    assert list(iter_tokens("snake_case abc123 _ 123")) == [
        "snake_case", "abc123", "_", "123"
    ]


def test_japanese_tokens_are_maximal_and_repeatable():
    from wordfreq.tokenizer import iter_tokens

    text = "日本語のテキスト。東京、ひらがな"
    expected = ["日本語のテキスト", "東京", "ひらがな"]
    assert list(iter_tokens(text)) == expected
    assert list(iter_tokens(text)) == expected


def test_empty_text_has_no_tokens():
    from wordfreq.tokenizer import default_tokenizer, iter_tokens

    assert default_tokenizer("") == []
    assert list(iter_tokens("")) == []


def test_injected_tokenizer_receives_text_and_its_output_is_casefolded():
    from wordfreq.tokenizer import iter_tokens

    received = []

    def custom_tokenizer(text: str) -> list[str]:
        received.append(text)
        return ["CUSTOM-TOKEN", "Straße", "CUSTOM-TOKEN"]

    tokens = iter_tokens("ignored by custom tokenizer", tokenizer=custom_tokenizer)
    assert iter(tokens) is tokens
    assert list(tokens) == ["custom-token", "strasse", "custom-token"]
    assert received == ["ignored by custom tokenizer"]
