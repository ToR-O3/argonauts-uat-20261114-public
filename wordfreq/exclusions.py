"""Pure, eager interpretation of exclusion text; no acquisition or exit policy."""
import re


class InvalidExclusion(ValueError):
    """An invalid original exclusion row, numbered before any rows are ignored."""

    def __init__(self, line_number: int) -> None:
        self.line_number = line_number
        super().__init__(f"line {line_number}: expected one Unicode word")


def parse_exclusions(text: str) -> set[str]:
    """Validate original words before normalizing the complete membership set."""
    words = set()
    for line_number, line in enumerate(text.split("\n"), 1):
        word = line.strip()
        if not word or word.startswith("#"):
            continue
        if re.fullmatch(r"\w+", word) is None:
            raise InvalidExclusion(line_number)
        words.add(word.casefold())
    return words
