"""Controlled encoding seams, not an OS-locale emulation or installed CLI.

Real raw-byte argv/file lookup, FileSource, tokenizer and formatter remain intact.
Only display decoding and the stdout TextIOWrapper encoding are controlled.
"""
import io
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from wordfreq.__main__ import main


def probe():
    diagnostic, filesystem_encoding, stdout_encoding, *argv = sys.argv[1:]
    raw_path = os.fsencode(argv[0])
    # os.fsencode uses the startup filesystem codec, not this display seam.
    sys.getfilesystemencoding = lambda: filesystem_encoding
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=stdout_encoding)
    Path(diagnostic).write_text(json.dumps({
        "kind": "controlled-seam-not-native-locale",
        "filesystem_display_encoding": sys.getfilesystemencoding(),
        "stdout_encoding": sys.stdout.encoding,
        "raw_path_hex": raw_path.hex(),
        "roundtrip_path_hex": os.fsencode(argv[0]).hex(),
    }), encoding="utf-8")
    main(argv)


if __name__ == "__main__":
    probe()
