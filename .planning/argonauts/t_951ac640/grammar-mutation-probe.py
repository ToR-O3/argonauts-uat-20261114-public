"""Run the authored tests against isolated faulty variants, never product files."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "mutation-results.txt"
VARIANTS = [
    ("no-trim", "exclusions.py", 'word = line.strip()', 'word = line', 'exclude_grammar_trim_comments_newlines'),
    ("no-comments", "exclusions.py", 'if not word or word.startswith("#"):', 'if not word:', 'exclude_grammar_trim_comments_newlines'),
    ("ascii-only", "exclusions.py", 're.fullmatch(r"\\w+", word)', 're.fullmatch(r"\\w+", word, re.ASCII)', 'exclude_grammar_valid_unicode'),
    ("digits-invalid", "exclusions.py", 'if re.fullmatch(r"\\w+", word) is None:', 'if word.isdigit() or re.fullmatch(r"\\w+", word) is None:', 'exclude_grammar_valid_unicode'),
    ("underscore-invalid", "exclusions.py", 'if re.fullmatch(r"\\w+", word) is None:', 'if "_" in word or re.fullmatch(r"\\w+", word) is None:', 'exclude_grammar_valid_unicode'),
    ("lower-not-casefold", "exclusions.py", 'words.add(word.casefold())', 'words.add(word.lower())', 'exclude_grammar_valid_unicode'),
    ("validate-after-fold", "exclusions.py", 're.fullmatch(r"\\w+", word)', 're.fullmatch(r"\\w+", word.casefold())', 'exclude_grammar_valid_unicode'),
    ("partial-not-full", "exclusions.py", 're.fullmatch(r"\\w+", word)', 're.search(r"\\w+", word)', 'exclude_grammar_invalid_original_row'),
    ("ignore-invalid", "exclusions.py", 'raise InvalidExclusion(line_number)', 'continue', 'exclude_grammar_invalid_original_row'),
    ("repair-bom", "exclusions.py", 'word = line.strip()', 'word = line.strip().lstrip("\\ufeff")', 'exclude_grammar_invalid_original_row'),
    ("wrong-original-row", "exclusions.py", 'raise InvalidExclusion(line_number)', 'raise InvalidExclusion(1)', 'exclude_grammar_invalid_original_row'),
    ("lexical-order", "__main__.py", 'counts.items()\n', 'sorted(counts.items())\n', 'exclude_grammar_permutations_and_hashseeds'),
    ("wrong-exclusion-exit", "__main__.py", 'sys.exit(2)', 'sys.exit(1)', 'exclude_tracer_missing_file'),
]


def run():
    with tempfile.TemporaryDirectory(prefix="exclude-mutations-", dir=os.environ["TMPDIR"]) as temp:
        records = []
        for name, filename, original, replacement, selector in VARIANTS:
            destination = Path(temp) / name
            destination.mkdir()
            shutil.copytree(ROOT / "wordfreq", destination / "wordfreq",
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (destination / "tests").mkdir()
            shutil.copy2(ROOT / "tests/test_cli.py", destination / "tests/test_cli.py")
            target = destination / "wordfreq" / filename
            source = target.read_text(encoding="utf-8")
            assert original in source, (name, "mutation seam missing")
            target.write_text(source.replace(original, replacement), encoding="utf-8")
            env = dict(os.environ)
            env.pop("PYTHONPATH", None)
            command = [sys.executable, "-m", "pytest", "tests/test_cli.py", "-q", "-x", "-k", selector]
            result = subprocess.run(command, cwd=destination, env=env, capture_output=True,
                                    text=True, timeout=30)
            records.append(f"## {name}: exit {result.returncode}\n{result.stdout}{result.stderr}")
            # Require an actual behavior assertion, not collection/import/setup failure.
            assert result.returncode == 1 and "AssertionError" in result.stdout, records[-1]
            assert "ERROR collecting" not in result.stdout, records[-1]
        OUT.write_text("\n".join(records), encoding="utf-8")
        print(f"{len(records)} isolated mutants rejected by behavior assertions; {OUT}")


if __name__ == "__main__":
    run()
