"""Record real subprocess outputs for this quick task, not independent acceptance."""
import json
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
root = Path.cwd()
cases = [
    ("default", "a bb ccc bb", []),
    ("explicit-one", "a bb ccc bb", ["--min-length", "1"]),
    ("boundary", "a bb ccc bb", ["--min-length", "2"]),
    ("casefold", "ß ss a", ["--min-length", "2"]),
    ("unicode", "日 日本 日本語 _ 12", ["--min-length", "2"]),
    ("composition", "a a a bb cc bb cc dddd",
     ["--min-length", "2", "--min-count", "2", "--max-count", "2", "--top", "1"]),
    ("tie", "a zz aa zz aa", ["--min-length", "2", "--top", "1"]),
    ("empty", "a bb", ["--min-length", "3"]),
]
records = []
for name, body, options in cases:
    folder = out / "outputs" / name
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "input.txt"
    path.write_text(body, encoding="utf-8")
    for fmt in ("text", "json", "html"):
        argv = [sys.executable, "-m", "wordfreq", str(path), *options, "--format", fmt]
        result = subprocess.run(argv, cwd=root, capture_output=True, timeout=10)
        (folder / f"{fmt}.stdout").write_bytes(result.stdout)
        (folder / f"{fmt}.stderr").write_bytes(result.stderr)
        records.append(dict(case=name, input=body, argv=argv, exit=result.returncode,
                            stdout=result.stdout.decode("utf-8"), stderr=result.stderr.decode("utf-8")))
        assert result.returncode == 0 and result.stderr == b""
help_result = subprocess.run([sys.executable, "-m", "wordfreq", "--help"], capture_output=True, timeout=10)
records.append(dict(case="help", argv=[sys.executable, "-m", "wordfreq", "--help"],
                    exit=help_result.returncode, stdout=help_result.stdout.decode("utf-8"),
                    stderr=help_result.stderr.decode("utf-8")))
assert help_result.returncode == 0 and help_result.stderr == b""
(out / "actual-outputs.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Recorded {len(records)} real CLI subprocess outputs")
