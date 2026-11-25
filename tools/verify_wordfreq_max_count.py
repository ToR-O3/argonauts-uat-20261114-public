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
    return {p: hashlib.sha256(subprocess.run(['git', 'show', f'{START}:{p}'], cwd=ROOT,
            capture_output=True, check=True, timeout=20).stdout).hexdigest() for p in PRODUCT}


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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['baseline'], required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    capture_baseline(args.output_dir)


if __name__ == '__main__':
    main()
