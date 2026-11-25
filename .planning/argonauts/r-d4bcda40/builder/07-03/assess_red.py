"""Submit actual unmodified JUnit from this PLAN to the official classifier."""
import json
from pathlib import Path
import sys
here = Path(__file__).resolve().parent
stage, target, expected, actual = sys.argv[1:]
red = here / stage
result = json.loads((red / 'result.json').read_text())
command = json.loads((red / 'command.json').read_text())
record = dict(command=' '.join(command['argv']), exitCode=result['exit'],
              output=(red / 'junit.xml').read_text(), targetTest=target,
              targetFile='tests/test_max_count_verifier.py', expected=expected, actual=actual,
              reportPath=str(red / 'junit.xml'), runStartedAt=result['started'],
              semanticAssessment=actual + '; named assertion failure, no collection/setup errors or skips; product unchanged')
(here / (stage + '-evidence.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
