"""Token extraction and case-insensitive normalization."""

import re
from collections.abc import Callable, Iterator

_WORD_RE = re.compile(r"\w+", re.UNICODE)


def default_tokenizer(text: str) -> list[str]:
    """Extract maximal Unicode word-character sequences."""
    return _WORD_RE.findall(text)


def iter_tokens(
    text: str, tokenizer: Callable[[str], list[str]] = default_tokenizer
) -> Iterator[str]:
    """Yield normalized tokens in their input order."""
    return (token.casefold() for token in tokenizer(text))
