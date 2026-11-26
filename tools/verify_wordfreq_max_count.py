"""Request r-d4bcda40: one-shot pre-feature byte oracle and read-only checks.

Images/browser omitted by the human decision on t_87068596, 1795609328.
No independent-quality claim is made by this builder utility.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
START = '8efbfaa1907ace272a4f685e2659144a4085d303'
BASELINE = Path('.planning/argonauts/r-d4bcda40/baseline')
EVIDENCE = Path('.planning/argonauts/r-d4bcda40/builder/07-01')
PRODUCT = ('wordfreq/__init__.py', 'wordfreq/__main__.py', 'wordfreq/aggregator.py',
           'wordfreq/formatters.py', 'wordfreq/sources.py', 'wordfreq/tokenizer.py')
ENV_KEYS = ('PATH', 'PYTHONPATH', 'PYTHONHASHSEED', 'PYTHONIOENCODING', 'PYTHONUTF8',
            'PYTHONDONTWRITEBYTECODE', 'LANG', 'LC_ALL', 'TMPDIR')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, check=True,
                          text=True, timeout=20).stdout.strip()


def product_blobs():
    return {p: digest(ROOT / p) for p in PRODUCT}


def start_blobs():
    # Pinned SHA-256 values from START, checked against the sealed provenance
    # and Git blobs when recorded. Read-only verification must also work in
    # shallow checkouts where START is absent; never derive these from the
    # evidence being validated or from the current product.
    return {
        'wordfreq/__init__.py': '8004295c8623cc0913025efb31807353a72698470a9497cf8dee95ed6e7d7239',
        'wordfreq/__main__.py': 'ab897f8838a423de2a2c466cb6937e05a60100d29f4f260587f80943b0f0cf3d',
        'wordfreq/aggregator.py': '33c40f5d0c5bbc7c8e185bbc8a25051ef7d381ebd42c9ed42c35b4ec7cbbbd35',
        'wordfreq/formatters.py': '184bb48ae6badf9c7fedc874e55bf163e4bd576c0a234a0ccffa37c49056f726',
        'wordfreq/sources.py': '8800710801b75e5e87e085471f4fca7d8079dcf924e125da9536259bbda67f58',
        'wordfreq/tokenizer.py': 'beb26f7b2713dde42d6532397df50bec22a5676969ecbc3fdd7c1762e8668dc6',
    }


def environment():
    # Explicit, non-secret execution environment; never persist inherited tokens.
    env = {k: os.environ[k] for k in ENV_KEYS if k in os.environ}
    env.update(PYTHONHASHSEED='0', PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
    return env


def build_baseline_cases():
    cases = []

    def add(name, body, pairs, total, options=(), basename='input.txt', default=False):
        for fmt in ('text', 'json', 'html'):
            opts = list(options) + ([] if default and fmt == 'text' else ['--format', fmt])
            cases.append(dict(id=name+'-'+fmt, body=body, pairs=[list(p) for p in pairs],
                              total=total, options=opts, basename=basename, format=fmt))

    body = 'Zoo APPLE apple zoo Hello hello HELLO one, two. one b c d e f g h'
    pairs = [('hello', 3), ('zoo', 2), ('apple', 2), ('one', 2), ('two', 1),
             ('b', 1), ('c', 1), ('d', 1), ('e', 1), ('f', 1)]
    add('default', body, pairs, 17, default=True)
    add('explicit-min', body, pairs, 17, ('--min-count', '1'))
    normal = 'beta beta beta alpha gamma alpha delta'
    add('min-top', normal, [('beta', 3)], 7, ('--min-count', '2', '--top', '1'))
    add('excluded', normal, [], 7, ('--min-count', '4'))
    for name, text in [('empty', ''), ('whitespace', ' \t\n\r  '), ('punctuation', '!?,.;: --')]:
        add(name, text, [], 0)
    add('unicode', 'Straße STRASSE 日本語 日本語 Café CAFÉ',
        [('strasse', 2), ('日本語', 2), ('café', 2)], 6)
    long_pairs = [('w'*256, 123)] + [(f'row{i:02d}', 13-i) for i in range(1, 12)]
    long_body = ' '.join(w for w, n in long_pairs for _ in range(n))
    long_name = '集計  ' + 'n'*176 + '\n続き\t終わり  &<>"\'.txt'
    for name, top in [('long', '12'), ('long-large', '99')]:
        add(name, long_body, long_pairs, 200, ('--top', top), long_name)
    add('long-default', long_body, long_pairs[:10], 200, basename=long_name)
    add('hostile', 'Café CAFÉ Straße STRASSE 日本語', [('café', 2), ('strasse', 2), ('日本語', 1)],
        5, basename='検査  &<>"\'\n次\t終.txt')
    add('cr', long_body, long_pairs, 200, ('--top', '12'), 'a\rb\r\nc  \n\t.txt')
    return cases


class Content(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.rows, self.headers, self.values = [], [], {}
        self.target = None
        self.feed(raw.decode('utf-8'))
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = []
        cls = dict(attrs).get('class')
        if tag in ('td', 'th') or cls in ('filename-value', 'total-value'):
            self.target = (tag, cls, '')

    def handle_data(self, data):
        if self.target:
            tag, cls, text = self.target
            self.target = tag, cls, text + data

    def handle_endtag(self, tag):
        if self.target and tag == self.target[0]:
            _, cls, text = self.target
            if tag == 'td':
                self.row.append(text)
            elif tag == 'th':
                self.headers.append(text)
            else:
                self.values[cls] = text
            self.target = None
        if tag == 'tr' and self.row:
            self.rows.append(self.row)


def check_output(raw, case):
    pairs = case['pairs']
    if case['format'] == 'text':
        good = raw == ''.join(f'{n}\t{w}\n' for w, n in pairs).encode('utf-8')
    elif case['format'] == 'json':
        good = raw == (json.dumps([dict(word=w, count=n) for w, n in pairs])+'\n').encode('utf-8')
    else:
        doc = Content(raw)
        good = (doc.rows == [[str(i), w, str(n)] for i, (w, n) in enumerate(pairs, 1)]
                and doc.headers == ['順位', '単語', '回数']
                and doc.values == {'filename-value': case['basename'], 'total-value': str(case['total'])})
    if not good:
        raise ValueError('literal content oracle mismatch: ' + case['id'])


def seal(root, index):
    index['artifacts'] = {str(p.relative_to(root)): digest(p)
                          for p in sorted(root.rglob('*')) if p.is_file()}
    save_json(root/'index.json', index)
    (root/'index.sha256').write_text(digest(root/'index.json')+'\n', encoding='ascii')


def capture_baseline(output):
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError('no overwrite/resume/recapture of an existing baseline root')
    if product_blobs() != start_blobs():
        raise ValueError('product changed before baseline')
    before = product_blobs()
    started = time.monotonic()
    env = environment()
    output.mkdir(parents=True)
    provenance = dict(head=git('rev-parse', 'HEAD'), product_blobs=before,
                      status=git('status', '--porcelain'), root=str(ROOT), start=START)
    save_json(output/'provenance.json', provenance)
    index = dict(request='r-d4bcda40', head=START, synthetic=False,
                 independent_acceptance=False, browser='not run: human decision 1795609328',
                 root=str(output), cwd=str(ROOT), executable=sys.executable, python=sys.version,
                 os=platform.platform(), environment=env, provenance=provenance,
                 started=datetime.now(timezone.utc).isoformat(), timeout_seconds=600, cases=[])
    for case in build_baseline_cases():
        if time.monotonic()-started > 600:
            raise TimeoutError('baseline deadline; preserve partial root')
        folder = output/case['id']
        (folder/'input').mkdir(parents=True)
        path = folder/'input'/case['basename']
        path.write_bytes(case['body'].encode('utf-8'))
        argv = [sys.executable, '-m', 'wordfreq', str(path), *case['options']]
        run = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=20)
        (folder/'stdout.bin').write_bytes(run.stdout)
        (folder/'stderr.bin').write_bytes(run.stderr)
        record = dict(case, input=str(path.relative_to(output)),
                      stdout=str((folder/'stdout.bin').relative_to(output)),
                      stderr=str((folder/'stderr.bin').relative_to(output)), argv=argv, exit=run.returncode)
        if case['format'] == 'html':
            (folder/'stdout.html').write_bytes(run.stdout)
            record['html'] = str((folder/'stdout.html').relative_to(output))
        index['cases'].append(record)
        if run.returncode != 0 or run.stderr:
            raise ValueError(f'baseline CLI failed: {case["id"]} exit={run.returncode}')
        check_output(run.stdout, case)
    if before != product_blobs():
        raise ValueError('product changed during baseline')
    index['duration_seconds'] = time.monotonic()-started
    index['cli_cases'], index['views'], index['images'] = len(index['cases']), 0, 0
    seal(output, index)
    validate_baseline(output)
    print(json.dumps({k: index[k] for k in ('cli_cases', 'views', 'images', 'duration_seconds')}))


def validate_baseline(root):
    root = Path(root)
    index = json.loads((root/'index.json').read_text(encoding='utf-8'))
    if (root/'index.sha256').read_text().strip() != digest(root/'index.json'):
        raise ValueError('index checksum mismatch')
    if (index['head'] != START or index['synthetic'] or index['independent_acceptance']
            or index['request'] != 'r-d4bcda40' or index['environment']['PYTHONHASHSEED'] != '0'
            or index['provenance']['product_blobs'] != start_blobs()):
        raise ValueError('baseline provenance mismatch')
    if index['provenance'] != json.loads((root/'provenance.json').read_text()):
        raise ValueError('provenance copy mismatch')
    definitions = build_baseline_cases()
    if len(index['cases']) != len(definitions):
        raise ValueError('case count mismatch')
    for case, expected in zip(index['cases'], definitions):
        if any(case[k] != v for k, v in expected.items()):
            raise ValueError('case definition mismatch')
        if case['argv'] != [index['executable'], '-m', 'wordfreq',
                            str(Path(index['root'])/case['input']), *case['options']]:
            raise ValueError('argv mismatch')
        if (root/case['input']).read_bytes() != case['body'].encode('utf-8'):
            raise ValueError('input mismatch')
        raw = (root/case['stdout']).read_bytes()
        if case['exit'] != 0 or (root/case['stderr']).read_bytes():
            raise ValueError('exit/stderr mismatch')
        check_output(raw, case)
        if case['format'] == 'html' and (root/case['html']).read_bytes() != raw:
            raise ValueError('HTML original mismatch')
    actual = {str(p.relative_to(root)): digest(p) for p in root.rglob('*')
              if p.is_file() and p.name not in ('index.json', 'index.sha256')}
    if actual != index['artifacts']:
        raise ValueError('artifact completeness/hash mismatch')
    return index


def validate_red(root):
    root = Path(root)
    result = json.loads((root/'result.json').read_text())
    command = json.loads((root/'command.json').read_text())
    suite = ET.parse(root/'junit.xml').getroot().find('testsuite')
    cases = suite.findall('testcase')
    if (result['exit'] != 1 or result['product_blobs'] != start_blobs()
            or result['product_after'] != start_blobs() or result['head'] != START
            or '-x' in command['argv'] or command['argv'][1:6] !=
            ['-m', 'pytest', 'tests/test_cli.py', '-k', 'max_count']):
        raise ValueError('not a full preimplementation RED')
    if (not cases or int(suite.get('errors')) or int(suite.get('skipped'))
            or not int(suite.get('failures')) or len(cases) != result['tests']):
        raise ValueError('invalid RED count/errors/skip')
    required = {'tracer', 'parser', 'help', 'selection', 'internal_order', 'saved_bytes',
                'hashseed', 'empty', 'invalid_before_read', 'input_failure', 'read_only'}
    found = {name for name in required if any('test_max_count_'+name in c.get('name') for c in cases)}
    if found != required:
        raise ValueError('missing 1.1 test group')
    for c in cases:
        if c.find('error') is not None:
            raise ValueError('environment error is not feature RED')
        failure = c.find('failure')
        if failure is not None and not any(term in (failure.text or '') for term in
                                           ('AssertionError', 'SystemExit', 'AttributeError')):
            raise ValueError('unexpected RED failure')
    if not all(any('test_max_count_'+name in c.get('name') and c.find('failure') is not None
                   for c in cases) for name in ('tracer', 'parser', 'help', 'selection', 'empty', 'input_failure')):
        raise ValueError('missing intended feature assertion RED')
    for name, sha in result['artifacts'].items():
        if digest(root/name) != sha:
            raise ValueError('RED original changed')
    return result


CAPTURE = Path('.planning/argonauts/r-d4bcda40/builder/07-03/capture')
DECISION = 't_87068596/default/1795609328'
AC_REQ = {'AC1': ['REQ-23', 'REQ-26'], 'AC2': ['REQ-24', 'REQ-25'],
          'AC3': ['REQ-24', 'REQ-25', 'REQ-26'], 'AC4': ['REQ-27'],
          'AC5': ['REQ-28'], 'AC6': ['REQ-26', 'REQ-27']}


def build_capture_cases():
    # Literal spec oracles, independent of product parsing, sorting and formatting.
    cases = []
    for baseline in build_baseline_cases():
        cases.append(dict(baseline, oracle=baseline['id']))
        cases.append(dict(baseline, id='large-'+baseline['id'],
                          options=baseline['options']+['--max-count', '1000000'],
                          oracle=baseline['id']))

    def add(name, body, pairs, total, options):
        for fmt in ('text', 'json', 'html'):
            cases.append(dict(id=name+'-'+fmt, body=body, pairs=[list(p) for p in pairs],
                              total=total, options=[*options, '--format', fmt],
                              basename='input.txt', format=fmt))

    normal = 'beta beta beta alpha gamma alpha delta'
    add('max1', normal, [('gamma', 1), ('delta', 1)], 7, ['--max-count', '1'])
    add('max2', normal, [('alpha', 2), ('gamma', 1), ('delta', 1)], 7, ['--max-count', '2'])
    for maximum, pairs in [('2', [('alpha', 2)]), ('3', [('beta', 3), ('alpha', 2)])]:
        for reverse in (False, True):
            options = ['--min-count', '2', '--max-count', maximum]
            if reverse:
                options = options[2:]+options[:2]
            add('min2max'+maximum+('-reverse' if reverse else ''), normal, pairs, 7, options)
    add('top1', normal, [('alpha', 2)], 7, ['--max-count', '2', '--top', '1'])
    add('triple', 'beta beta beta beta zoo zoo zoo apple apple pear pear single',
        [('zoo', 3)], 12, ['--min-count', '2', '--max-count', '3', '--top', '1'])
    for name, options in [('zero', ['--max-count', '0']),
                          ('negative', ['--max-count=-1']),
                          ('inverted', ['--min-count', '3', '--max-count', '2'])]:
        add(name, normal, [], 7, options)
    for name, text in [('empty-max', ''), ('whitespace-max', ' \t\n\r  '),
                       ('punctuation-max', '!?,.;: --')]:
        add(name, text, [], 0, ['--max-count', '2'])
    for top in ('1', '2'):
        add('tie'+top, 'Zoo apple APPLE zoo banana', [('zoo', 2), ('apple', 2)][:int(top)],
            5, ['--min-count', '2', '--max-count', '2', '--top', top])
    unicode_body = 'Straße STRASSE 日本語 日本語'
    add('unicode-empty', unicode_body, [], 4, ['--max-count', '1'])
    add('unicode-selected', unicode_body, [('strasse', 2), ('日本語', 2)], 4,
        ['--min-count', '2', '--max-count', '2'])
    words = ['zoo', 'apple', 'pear', 'cherry', 'dog', 'eel', 'fox', 'goat', 'horse', 'ibis', 'jay', 'koala']
    many = ' '.join(['excluded']*3 + [w for w in words for _ in range(2)])
    for name, options, selected in [('many', [], words[:10]), ('many-all', ['--top', '99'], words)]:
        add(name, many, [(w, 2) for w in selected], 27, ['--max-count', '2', *options])
    return cases


def runtime_snapshot():
    paths = [ROOT/'README.md', ROOT/'pyproject.toml', ROOT/'.planning/config.json']
    for folder in ('wordfreq', 'tools', 'tests'):
        paths.extend((ROOT/folder).rglob('*.py'))
    return {str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)}


def actor(role):
    expected = 'argonauts-uat-'+role
    if (role not in ('builder', 'quality') or os.environ.get('HERMES_PROFILE') != expected
            or Path(os.environ.get('HERMES_HOME', '')).name != expected):
        raise ValueError('actual profile and home must match role, not only the flag')
    return expected


def capture_seal(root, manifest):
    manifest['artifacts'] = {str(p.relative_to(root)): digest(p)
                             for p in sorted(root.rglob('*'))
                             if p.is_file() and p.name not in ('manifest.json', 'manifest.sha256')}
    save_json(root/'manifest.json', manifest)
    (root/'manifest.sha256').write_text(digest(root/'manifest.json')+'\n', encoding='ascii')


def collect_capture(output, role, baseline):
    profile = actor(role)
    output, baseline = Path(output).resolve(), Path(baseline).resolve()
    if output.exists():
        raise FileExistsError('fresh root required; preserve partial evidence')
    fixed = validate_baseline(baseline)
    before = runtime_snapshot()
    head = git('rev-parse', 'HEAD')
    started = time.monotonic()
    env = environment()
    output.mkdir(parents=True)
    save_json(output/'scope.json', validate_scope())
    provenance = dict(head=head, profile=profile, role=role, pid=os.getpid(),
                      runtime=before, baseline_sha256=digest(baseline/'index.json'),
                      decision=DECISION, status=git('status', '--porcelain'))
    save_json(output/'provenance.json', provenance)
    manifest: dict[str, Any] = dict(request='r-d4bcda40', head=head, provenance=provenance,
                    root=str(output), cwd=str(ROOT), executable=sys.executable,
                    python=sys.version, os=platform.platform(), environment=env,
                    synthetic=False, independent_acceptance=False, verdict='pending-review',
                    phase='collecting', started=datetime.now(timezone.utc).isoformat(),
                    timeout_seconds=600, browser='not run: '+DECISION,
                    views=0, images=0, cases=[], ac_index=AC_REQ)
    fixed_cases = {c['id']: c for c in fixed['cases']}
    for case in build_capture_cases():
        remaining = 600-(time.monotonic()-started)
        if remaining <= 0:
            raise TimeoutError('capture deadline; preserve partial originals')
        folder = output/case['id']
        (folder/'input').mkdir(parents=True)
        source = folder/'input'/case['basename']
        source.write_bytes(case['body'].encode('utf-8'))
        argv = [sys.executable, '-m', 'wordfreq', str(source), *case['options']]
        run = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=min(20, remaining))
        (folder/'stdout.bin').write_bytes(run.stdout)
        (folder/'stderr.bin').write_bytes(run.stderr)
        record = dict(case, input=str(source.relative_to(output)), argv=argv,
                      stdout=case['id']+'/stdout.bin', stderr=case['id']+'/stderr.bin', exit=run.returncode)
        if case['format'] == 'html':
            (folder/'stdout.html').write_bytes(run.stdout)
            record['html'] = case['id']+'/stdout.html'
        manifest['cases'].append(record)
        save_json(output/'partial.json', dict(head=head, last_case=case['id'], exit=run.returncode))
        if run.returncode or run.stderr:
            raise ValueError('CLI failed: '+case['id'])
        check_output(run.stdout, case)
        if 'oracle' in case and run.stdout != (baseline/fixed_cases[case['oracle']]['stdout']).read_bytes():
            raise ValueError('pre-feature bytes differ: '+case['id'])
    if before != runtime_snapshot() or head != git('rev-parse', 'HEAD'):
        raise ValueError('execution surface changed during capture')
    manifest.update(phase='collected', cli_cases=len(manifest['cases']),
                    collection_seconds=time.monotonic()-started)
    capture_seal(output, manifest)
    validate_collection(output, baseline)
    return manifest


def validate_collection(root, baseline, active_owner=False):
    root = Path(root)
    m = json.loads((root/'manifest.json').read_text())
    if (root/'manifest.sha256').read_text().strip() != digest(root/'manifest.json'):
        raise ValueError('manifest checksum mismatch')
    if (m['request'] != 'r-d4bcda40' or m['synthetic'] or m['independent_acceptance']
            or m['verdict'] != 'pending-review' or m['images'] != 0 or m['views'] != 0
            or m['ac_index'] != AC_REQ or m['browser'] != 'not run: '+DECISION):
        raise ValueError('capture cannot claim independent acceptance or browser success')
    p = m['provenance']
    if (p != json.loads((root/'provenance.json').read_text()) or p['head'] != m['head']
            or len(m['head']) != 40 or any(c not in '0123456789abcdef' for c in m['head'])
            or p['role'] not in ('builder', 'quality') or p['profile'] != 'argonauts-uat-'+p['role']
            or p['decision'] != DECISION):
        raise ValueError('head/profile provenance mismatch')
    fixed = validate_baseline(baseline)
    if p['baseline_sha256'] != digest(Path(baseline)/'index.json'):
        raise ValueError('wrong baseline')
    definitions = build_capture_cases()
    if len(m['cases']) != len(definitions) or m['cli_cases'] != len(definitions):
        raise ValueError('missing capture case')
    baseline_cases = {c['id']: c for c in fixed['cases']}
    for c, expected in zip(m['cases'], definitions):
        if any(c[k] != v for k, v in expected.items()):
            raise ValueError('capture case definition mismatch')
        if (c['input'] != c['id']+'/input/'+c['basename']
                or c['stdout'] != c['id']+'/stdout.bin' or c['stderr'] != c['id']+'/stderr.bin'
                or c['argv'] != [m['executable'], '-m', 'wordfreq', str(Path(m['root'])/c['input']), *c['options']]):
            raise ValueError('capture argv/path mismatch')
        if (root/c['input']).read_bytes() != c['body'].encode('utf-8'):
            raise ValueError('capture input mismatch')
        raw = (root/c['stdout']).read_bytes()
        if c['exit'] or (root/c['stderr']).read_bytes():
            raise ValueError('capture exit/stderr mismatch')
        check_output(raw, c)
        if c['format'] == 'html' and (root/c['html']).read_bytes() != raw:
            raise ValueError('capture HTML original mismatch')
        if 'oracle' in c and raw != (Path(baseline)/baseline_cases[c['oracle']]['stdout']).read_bytes():
            raise ValueError('capture fixed bytes differ')
    actual = {str(f.relative_to(root)): digest(f) for f in root.rglob('*')
              if f.is_file() and f.name not in ('manifest.json', 'manifest.sha256')}
    if active_owner:
        if (p['pid'] != os.getppid() or m['phase'] != 'collected'
                or os.environ.get('WORDFREQ_MAX_ACTIVE_ROOT') != str(root.resolve())):
            raise ValueError('only direct pytest child of live capture owner may inspect collection')
        for name in ('suite-command.json', 'suite.xml'):
            actual.pop(name, None)
    if actual != m['artifacts']:
        raise ValueError('capture artifact completeness/hash mismatch')
    return m


def validate_scope(repo=ROOT, base=START):
    repo = Path(repo)

    def run(*args):
        return subprocess.run(['git', *args], cwd=repo, capture_output=True,
                              check=True, timeout=20).stdout

    changed = run('diff', '--name-only', '-z', '--no-renames', base).decode().split('\0')
    changed += run('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')
    changed = sorted(set(p for p in changed if p))
    exact = {'wordfreq/__main__.py', 'tests/test_cli.py', 'README.md',
             'tools/verify_wordfreq_max_count.py', 'tests/test_max_count_verifier.py',
             'docs/wordfreq-max-count-verification.md', '.planning/STATE.md',
             '.planning/ROADMAP.md', '.planning/REQUIREMENTS.md', '.planning/state.json'}
    prefixes = ('.planning/argonauts/r-d4bcda40', '.planning/phases/07-wordfreq-max-count/',
                'openspec/changes/r-d4bcda40-max-count/')
    for path in changed:
        if path not in exact and not path.startswith(prefixes):
            raise ValueError('out-of-scope path: '+path)
        if not (repo/path).is_file() or (repo/path).is_symlink():
            raise ValueError('deleted/symlink path: '+path)
    # Entire inherited tests/helpers remain byte-for-byte; append-only additions.
    original = run('show', base+':tests/test_cli.py')
    if not (repo/'tests/test_cli.py').read_bytes().startswith(original):
        raise ValueError('existing tests changed/deleted/relaxed')
    approved = {'wordfreq/__main__.py': '9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba',
                'README.md': 'e8c2babfe5371cd4cbce3fe5f67d7e5887a236fd59eedb91b3c77d696ccb9696'}
    for path, sha in approved.items():
        if digest(repo/path) != sha:
            raise ValueError('unapproved product/README change: '+path)
    return dict(base=base, paths=changed, product_blobs={p: digest(repo/p) for p in PRODUCT},
                existing_tests_preserved=True, approved_product_and_readme=True)


def suite_counts(path, exit_code):
    suites = ET.parse(path).getroot()
    cases = suites.findall('.//testcase')
    counts = {key: sum(int(s.get(key, 0)) for s in suites.findall('testsuite'))
              for key in ('tests', 'failures', 'errors', 'skipped')}
    if (exit_code != 0 or counts['tests'] <= 0 or counts['tests'] != len(cases)
            or any(counts[k] for k in ('failures', 'errors', 'skipped'))
            or any(c.find(tag) is not None for c in cases for tag in ('failure', 'error', 'skipped'))):
        raise ValueError('suite is not a nonempty complete success')
    return counts


def capture(output, role, baseline):
    started = time.monotonic()
    m = collect_capture(output, role, baseline)
    output = Path(output).resolve()
    env = dict(os.environ, WORDFREQ_MAX_ACTIVE_ROOT=str(output))
    argv = [sys.executable, '-m', 'pytest', 'tests/', '-q', '--junitxml='+str(output/'suite.xml')]
    save_json(output/'suite-command.json', dict(argv=argv, cwd=str(ROOT), environment=environment()))
    before = runtime_snapshot()
    run = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True,
                         timeout=max(1, 600-(time.monotonic()-started)))
    (output/'suite.stdout.txt').write_bytes(run.stdout)
    (output/'suite.stderr.txt').write_bytes(run.stderr)
    counts = suite_counts(output/'suite.xml', run.returncode)
    if before != runtime_snapshot() or m['head'] != git('rev-parse', 'HEAD'):
        raise ValueError('execution surface changed during suite')
    save_json(output/'suite.json', dict(counts, exit=run.returncode, head=m['head'],
                                      duration_seconds=time.monotonic()-started-m['collection_seconds']))
    m.update(phase='complete', duration_seconds=time.monotonic()-started,
             ended=datetime.now(timezone.utc).isoformat())
    capture_seal(output, m)
    validate_capture(output, baseline)
    return m


def validate_capture(root, baseline):
    m = validate_collection(root, baseline)
    root = Path(root)
    if m['phase'] != 'complete':
        raise ValueError('suite incomplete')
    suite = json.loads((root/'suite.json').read_text())
    counts = suite_counts(root/'suite.xml', suite['exit'])
    if any(suite[k] != v for k, v in counts.items()) or suite['head'] != m['head']:
        raise ValueError('suite record mismatch')
    command = json.loads((root/'suite-command.json').read_text())
    if command['argv'] != [m['executable'], '-m', 'pytest', 'tests/', '-q',
                           '--junitxml='+str(Path(m['root'])/'suite.xml')]:
        raise ValueError('not the standard full suite')
    return m


def review_session(output, role, baseline):
    if role != 'quality':
        raise ValueError('review-session requires quality profile')
    # No live browser/session or image ledger: explicitly superseded by DECISION.
    return capture(output, role, baseline)


def finalize(output, role, baseline, ledger):
    actor(role)
    m = validate_capture(output, baseline)
    if role != 'quality' or m['provenance']['role'] != 'quality':
        raise ValueError('builder capture cannot become quality acceptance')
    if m['head'] != git('rev-parse', 'HEAD') or m['provenance']['runtime'] != runtime_snapshot():
        raise ValueError('quality must regenerate for current head and source')
    review = json.loads(Path(ledger).read_text())
    if (review.get('head') != m['head'] or review.get('profile') != actor(role)
            or review.get('capture_sha256') != digest(Path(output)/'manifest.json')
            or set(review.get('ac_reviews', {})) != set(AC_REQ)
            or not all(isinstance(v, str) and v.strip() for v in review['ac_reviews'].values())
            or review.get('source_sha256') != digest(ROOT/'wordfreq/__main__.py')
            or review.get('source_order') != 'original-Counter/total -> AND -> top -> shared-pairs'
            or not review.get('source_notes', '').strip()):
        raise ValueError('incomplete independent CLI/HTML/source review ledger')
    # Do not mutate sealed originals or auto-complete OpenSpec2.2/CI/PM delivery.
    return dict(head=m['head'], verdict='quality-content-reviewed',
                ledger_sha256=digest(ledger), independent_acceptance=False,
                remaining=['quality VERIFICATION.md', 'CLI/CI text attachments', 'PM readback', 'OpenSpec2.2 judgement'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['baseline', 'capture', 'review-session', 'finalize', 'validate'], required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--role', choices=['builder', 'quality'])
    parser.add_argument('--baseline-dir', type=Path)
    parser.add_argument('--review-ledger', type=Path)
    args = parser.parse_args()
    if args.mode == 'baseline':
        capture_baseline(args.output_dir)
        return
    if args.baseline_dir is None:
        parser.error('--baseline-dir required')
    if args.mode != 'validate' and args.role is None:
        parser.error('--role required')
    if args.mode == 'finalize' and args.review_ledger is None:
        parser.error('--review-ledger required')
    if args.mode == 'validate':
        result = validate_capture(args.output_dir, args.baseline_dir)
    elif args.mode == 'capture':
        result = capture(args.output_dir, args.role, args.baseline_dir)
    elif args.mode == 'review-session':
        result = review_session(args.output_dir, args.role, args.baseline_dir)
    else:
        result = finalize(args.output_dir, args.role, args.baseline_dir, args.review_ledger)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
