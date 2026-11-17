"""Pure frequency counting, independent of input and output."""
from collections import Counter
from collections.abc import Iterable


def count_words(tokens: Iterable[str]) -> Counter[str]:
    """Count a token iterable without acquiring text."""
    return Counter(tokens)


def top_words(counts: Counter[str], n: int) -> list[tuple[str, int]]:
    """Rank by descending count, preserving insertion order for ties.

    Callers must supply counts in normalized first-occurrence order.
    Stable sorting happens before limiting; counts are not mutated.
    """
    return sorted(counts.items(), key=lambda wc: -wc[1])[:n]
