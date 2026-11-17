"""Command-line argument parsing and component composition."""
import argparse
import os
import sys
from pathlib import Path

from .aggregator import count_words, top_words
from .formatters import format_html, format_json, format_text
from .sources import FileSource, InputError
from .tokenizer import iter_tokens


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wordfreq")
    parser.add_argument("filename")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--format", choices=["text", "json", "html"], default="text")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.top < 1:
        parser.error("--top must be >= 1")
    try:
        text = FileSource(args.filename).read_text()
    except InputError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
    counts = count_words(iter_tokens(text))
    full_total = sum(counts.values())
    pairs = top_words(counts, args.top)
    if args.format == "html":
        # Sanitize display text only; the original path was used to read input.
        display_name = os.fsencode(Path(args.filename).name).decode(
            sys.getfilesystemencoding(), errors="replace"
        )
        output = format_html(pairs, filename=display_name, total_count=full_total)
    elif args.format == "json":
        output = format_json(pairs)
    else:
        output = format_text(pairs)
    if args.format == "html":
        sys.stdout.buffer.write(output.encode("utf-8"))
        sys.stdout.flush()
    else:
        sys.stdout.write(output)
    sys.exit(0)


if __name__ == "__main__":
    main()
