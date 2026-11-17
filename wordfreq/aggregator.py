"""Pure frequency counting, independent of input and output."""
from collections import Counter
from collections.abc import Iterable


def count_words(tokens: Iterable[str]) -> Counter[str]:
    """Count a token iterable without acquiring text."""
    return Counter(tokens)


def top_words(counts: Counter[str], n: int) -> list[tuple[str, int]]:
    """Return up to n pairs by descending count, preserving first-seen ties."""
    return sorted(counts.items(), key=lambda wc: -wc[1])[:n]
