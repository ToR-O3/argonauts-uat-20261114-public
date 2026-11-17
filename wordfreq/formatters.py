"""Pure output formatting; callers own writing and exit decisions."""


def format_text(pairs: list[tuple[str, int]]) -> str:
    """Format count-first tab-separated lines, or nothing for no pairs."""
    return "".join(f"{count}\t{word}\n" for word, count in pairs)
