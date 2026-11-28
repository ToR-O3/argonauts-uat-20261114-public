"""Command-line argument parsing and component composition."""
import argparse
from collections import Counter
import os
import sys

from .aggregator import count_words, top_words
from .formatters import format_html, format_json, format_text
from .sources import FileSource, InputError
from .tokenizer import iter_tokens


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wordfreq")
    parser.add_argument("filename")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--min-count", type=int, default=1)
    parser.add_argument("--min-length", type=int, default=1)
    parser.add_argument("--max-count", type=int, default=None)
    parser.add_argument("--format", choices=["text", "json", "html"], default="text")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.top < 1:
        parser.error("--top must be >= 1")
    if args.min_count < 1:
        parser.error("--min-count must be >= 1")
    if args.min_length < 1:
        parser.error("--min-length must be >= 1")
    try:
        text = FileSource(args.filename).read_text()
    except InputError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
    counts = count_words(iter_tokens(text))
    total = sum(counts.values())
    selected_counts = Counter({word: count for word, count in counts.items()
                               if count >= args.min_count
                               and len(word) >= args.min_length
                               and (args.max_count is None or count <= args.max_count)})
    pairs = top_words(selected_counts, args.top)
    if args.format == "html":
        # argv uses filesystem surrogateescape; HTML needs displayable Unicode.
        basename = os.fsencode(os.path.basename(args.filename)).decode(
            sys.getfilesystemencoding(), errors="replace"
        )
        output = format_html(pairs, basename, total)
    elif args.format == "json":
        output = format_json(pairs)
    else:
        output = format_text(pairs)
    if args.format == "html":
        # The document declares UTF-8, independently of the terminal locale.
        sys.stdout.buffer.write(output.encode("utf-8"))
    else:
        sys.stdout.write(output)
    sys.exit(0)


if __name__ == "__main__":
    main()
