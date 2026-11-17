"""Token extraction and case-insensitive normalization."""

from collections.abc import Callable, Iterator


def default_tokenizer(text: str) -> list[str]:
    """Extract words from text."""
    return text.split()


def iter_tokens(
    text: str, tokenizer: Callable[[str], list[str]] = default_tokenizer
) -> Iterator[str]:
    """Yield normalized tokens in their input order."""
    return (token.casefold() for token in tokenizer(text))
