"""Pure frequency counting, independent of input and output."""
from collections import Counter
from collections.abc import Iterable


def count_words(tokens: Iterable[str]) -> Counter[str]:
    """Count a token iterable without acquiring text."""
    return Counter(tokens)
