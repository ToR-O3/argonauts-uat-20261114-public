"""Command-line argument parsing and component composition."""
import argparse
import sys

from .aggregator import count_words, top_words
from .formatters import format_text
from .sources import FileSource
from .tokenizer import iter_tokens


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wordfreq")
    parser.add_argument("filename")
    parser.add_argument("--top", type=int, default=10)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    text = FileSource(args.filename).read_text()
    pairs = top_words(count_words(iter_tokens(text)), args.top)
    sys.stdout.write(format_text(pairs))
    sys.exit(0)


if __name__ == "__main__":
    main()
