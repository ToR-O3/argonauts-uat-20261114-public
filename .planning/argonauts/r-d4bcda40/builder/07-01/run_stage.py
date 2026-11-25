"""Finite execution recorder for this PLAN; not a product entry point."""
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location('max_verifier', ROOT/'tools/verify_wordfreq_max_count.py')
assert spec and spec.loader
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
stage, *arguments = sys.argv[1:]
folder = ROOT/d.EVIDENCE/stage
folder.mkdir(parents=True, exist_ok=False)
argv = [sys.executable, '-m', 'pytest', *arguments, '--junitxml='+str(folder/'junit.xml')]
env = os.environ.copy()
env['PYTHONPATH'] = '/home/Yuki/.local/lib/python3.12/site-packages'
command = dict(argv=argv, cwd=str(ROOT), environment={k: env.get(k) for k in d.ENV_KEYS})
d.save_json(folder/'command.json', command)
result = dict(head=d.git('rev-parse', 'HEAD'), product_blobs=d.product_blobs(),
              started=datetime.now(timezone.utc).isoformat(), python=sys.version,
              task=os.environ.get('HERMES_KANBAN_TASK'), profile=os.environ.get('HERMES_PROFILE'))
(folder/'test_cli.py.original').write_bytes((ROOT/'tests/test_cli.py').read_bytes())
start = time.monotonic()
run = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=600)
(folder/'stdout.txt').write_bytes(run.stdout)
(folder/'stderr.txt').write_bytes(run.stderr)
suite = ET.parse(folder/'junit.xml').getroot().find('testsuite')
assert suite is not None
result.update(exit=run.returncode, duration_seconds=time.monotonic()-start,
              product_after=d.product_blobs(), tests=int(suite.get('tests', '0')),
              failures=int(suite.get('failures', '0')), errors=int(suite.get('errors', '0')),
              skipped=int(suite.get('skipped', '0')),
              ended=datetime.now(timezone.utc).isoformat())
result['case_results'] = [dict(name=c.get('name'), status='failed' if c.find('failure') is not None else
                             'error' if c.find('error') is not None else 'skipped' if c.find('skipped') is not None
                             else 'passed') for c in suite.findall('testcase')]
result['artifacts'] = {str(p.relative_to(folder)): d.digest(p) for p in folder.iterdir() if p.is_file()}
d.save_json(folder/'result.json', result)
print(json.dumps({k: result[k] for k in ('head', 'exit', 'tests', 'failures', 'errors', 'skipped', 'duration_seconds')}))
print('stdout/stderr/JUnit originals: '+str(folder))
sys.exit(run.returncode)
