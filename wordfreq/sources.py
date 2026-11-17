"""Input acquisition boundary; no command-line exit decisions."""
from typing import Protocol


class TextSource(Protocol):
    def read_text(self) -> str: ...


class FileSource:
    def __init__(self, path: str) -> None:
        self._path = path

    def read_text(self) -> str:
        with open(self._path, "r", encoding="utf-8") as source:
            return source.read()
