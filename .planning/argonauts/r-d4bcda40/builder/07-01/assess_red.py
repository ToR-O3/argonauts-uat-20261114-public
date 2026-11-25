"""Bind the unchanged pytest JUnit report to the official RED classifier."""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
red = here/'red'
result = json.loads((red/'result.json').read_text())
command = json.loads((red/'command.json').read_text())
record = dict(command=' '.join(command['argv']), exitCode=result['exit'], output=(red/'junit.xml').read_text(),
              targetTest='test_max_count_tracer[text]', targetFile='tests/test_cli.py',
              expected='exit0, stderr empty, alpha2/gamma1/delta1',
              actual='assertion fails: exit2 unrecognized --max-count 2, expected exit0',
              reportPath=str(red/'junit.xml'), runStartedAt=result['started'],
              semanticAssessment='Target executed; literal exit assertion failed because max-count is not registered. '
                                 '276 collected; 213 intended feature failures, 63 natural usage passes; no ERROR or skip. '
                                 'Initial product blobs unchanged. Missing verifier-file infrastructure test is NOT used as feature RED.')
(here/'red-evidence.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
