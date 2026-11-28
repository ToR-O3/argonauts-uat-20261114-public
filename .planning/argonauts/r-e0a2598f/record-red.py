"""Preserve actual runner reports for the official RED classifier."""
import json
from pathlib import Path
import sys

root = Path(__file__).parent
kind = sys.argv[1]
if kind == "docs":
    report = root / "docs-red.xml"
    record = dict(command="uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_docs --junitxml=.planning/argonauts/r-e0a2598f/docs-red.xml", exitCode=1,
                  output=report.read_text(), targetTest="test_exclude_docs_complete_contract_and_literal_example", targetFile="tests/test_cli.py",
                  expected="README explicitly states no automatic exclusion dictionary", actual="AssertionError: missing no-automatic-dictionary statement", reportPath=str(report),
                  semanticAssessment="Target executes; topic assertions pass, then fails on missing approved non-goal documentation, not import/setup.")
else:
    report = root / "checker-red.txt"
    record = dict(command="python3 -m unittest discover -s .planning/argonauts/r-e0a2598f -p test_quality_handoff.py -v", exitCode=1,
                  output=report.read_text(), targetTest="test_complete_pending_package_passes", targetFile="test_quality_handoff.py",
                  expected="complete pending handoff exits0 without future quality reports", actual="loadable fail-closed skeleton exits2: implementation pending",
                  semanticAssessment="Entrypoint loaded; subprocess returned named implementation-pending diagnostic, target status assertion failed.")
(root / f"{kind}-red.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
