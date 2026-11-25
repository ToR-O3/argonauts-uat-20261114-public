"""Bind the README test's original JUnit to the official RED classifier."""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
red = here / 'red'
result = json.loads((red / 'result.json').read_text())
command = json.loads((red / 'command.json').read_text())
record = dict(command=' '.join(command['argv']), exitCode=result['exit'],
              output=(red / 'junit.xml').read_text(),
              targetTest='test_max_count_readme_example', targetFile='tests/test_cli.py',
              expected='README contains the specified max-count example exactly once',
              actual='readme.count(command) is 0, expected 1; AssertionError at tests/test_cli.py',
              reportPath=str(red / 'junit.xml'), runStartedAt=result['started'],
              semanticAssessment='The named test executed and failed at the first assertion because the README example is absent. One failure, no errors or skips. README and product are unchanged at RED. This is README 1.3 RED, not a replacement for the preserved pre-feature 1.1 RED.')
(here / 'red-evidence.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
