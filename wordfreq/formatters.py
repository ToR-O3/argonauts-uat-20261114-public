"""Pure output formatting; callers own writing and exit decisions."""
import json


def format_text(pairs: list[tuple[str, int]]) -> str:
    """Format count-first tab-separated lines, or nothing for no pairs."""
    return "".join(f"{count}\t{word}\n" for word, count in pairs)


def format_json(pairs: list[tuple[str, int]]) -> str:
    """Format ordered word/count objects as one ASCII-safe JSON line."""
    items = [{"word": word, "count": count} for word, count in pairs]
    return json.dumps(items, ensure_ascii=True) + "\n"
