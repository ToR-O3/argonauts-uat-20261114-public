"""Run copied tests against isolated wrong implementations; never edit live sources."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
cli = (ROOT / "wordfreq/__main__.py").read_text()
source = (ROOT / "wordfreq/sources.py").read_text()
body_read = '        text = FileSource(args.filename).read_text()\n'
mutations = [
    ("exclusion-exit-one", "wordfreq/__main__.py", cli.replace('            sys.exit(2)', '            sys.exit(1)'), 'exclude_failures_role_mapping'),
    ("body-exit-two", "wordfreq/__main__.py", cli.replace('        sys.exit(1)', '        sys.exit(2)'), 'exclude_failures_role_mapping'),
    ("body-first", "wordfreq/__main__.py", cli.replace('    excluded = set()', '    FileSource(args.filename).read_text()\n    excluded = set()'), 'exclude_precedence_failed_exclusion'),
    ("late-validation", "wordfreq/__main__.py", cli.replace('            excluded = parse_exclusions(exclusion_text)', '            FileSource(args.filename).read_text()\n            excluded = parse_exclusions(exclusion_text)'), 'exclude_precedence_failed_exclusion'),
    ("read-before-numeric", "wordfreq/__main__.py", cli.replace('    if args.top < 1:', '    FileSource(args.filename).read_text()\n    if args.top < 1:'), 'exclude_precedence_argv'),
    ("lost-path-reason", "wordfreq/sources.py", source.replace('raise InputError(f"{self._path}: {error}") from error', 'raise InputError("input failed") from error'), 'exclude_failures_role_mapping'),
    ("lost-cause", "wordfreq/sources.py", source.replace('from error', 'from None'), 'exclude_failures_role_mapping'),
    ("ignore-late-invalid", "wordfreq/__main__.py", cli.replace('            excluded = parse_exclusions(exclusion_text)', '            excluded = parse_exclusions(exclusion_text.split("apple banana")[0])'), 'exclude_precedence_failed_exclusion'),
]
results = []
for name, target, changed, selector in mutations:
    with tempfile.TemporaryDirectory(prefix="wf-mutation-", dir=os.environ["TMPDIR"]) as directory:
        isolated = Path(directory)
        shutil.copytree(ROOT / "wordfreq", isolated / "wordfreq", ignore=shutil.ignore_patterns("__pycache__"))
        (isolated / "tests").mkdir()
        for test_file in ("test_cli.py", "test_formatters.py"):
            shutil.copy2(ROOT / "tests" / test_file, isolated / "tests" / test_file)
        assert changed != (ROOT / target).read_text(), name
        (isolated / target).write_text(changed)
        argv = [sys.executable, "-m", "pytest", "tests/test_cli.py", "-q", "-x", "-k", selector]
        completed = subprocess.run(argv, cwd=isolated, env=dict(os.environ, PYTHONPATH=str(isolated)),
                                   capture_output=True, text=True, timeout=60)
        report = completed.stdout + completed.stderr
        (OUT / f"mutation-{name}.txt").write_text(report)
        rejected = (completed.returncode == 1 and "AssertionError" in report and "1 failed" in report
                    and "ERROR collecting" not in report)
        results.append({"name": name, "target": target, "selector": selector, "argv": argv,
                        "exit": completed.returncode, "assertion_rejected": rejected,
                        "report": f"mutation-{name}.txt"})
        print(f"{name}: exit={completed.returncode}, assertion_rejected={rejected}", flush=True)
(OUT / "failure-mutation-results.json").write_text(json.dumps(results, indent=2) + "\n")
assert all(result["assertion_rejected"] for result in results)
