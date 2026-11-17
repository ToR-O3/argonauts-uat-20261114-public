"""Input acquisition boundary; no command-line exit decisions."""
from typing import Protocol


class InputError(Exception):
    """Environment error raised while acquiring input text."""


class TextSource(Protocol):
    def read_text(self) -> str: ...


class FileSource:
    def __init__(self, path: str) -> None:
        self._path = path

    def read_text(self) -> str:
        try:
            with open(self._path, "r", encoding="utf-8") as source:
                return source.read()
        except (OSError, UnicodeDecodeError) as error:
            raise InputError(f"{self._path}: {error}") from error
