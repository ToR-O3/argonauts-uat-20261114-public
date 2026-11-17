"""Command-line argument parsing and component composition."""
import argparse
import sys

from .aggregator import count_words, top_words
from .formatters import format_json, format_text
from .sources import FileSource
from .tokenizer import iter_tokens


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wordfreq")
    parser.add_argument("filename")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.top < 1:
        parser.error("--top must be >= 1")
    text = FileSource(args.filename).read_text()
    pairs = top_words(count_words(iter_tokens(text)), args.top)
    output = format_json(pairs) if args.format == "json" else format_text(pairs)
    sys.stdout.write(output)
    sys.exit(0)


if __name__ == "__main__":
    main()
