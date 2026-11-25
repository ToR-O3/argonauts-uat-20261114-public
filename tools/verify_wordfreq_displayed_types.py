"""Request-local, immutable before originals. Collection is never acceptance.

Only explicit before mode launches a browser. Historical validation is read-only
and compares captured sources with Git at their execution head, not today's code.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('html_parts', ROOT / 'tools/verify_wordfreq_html.py')
parts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(parts)
save_json = parts.save_json
PRODUCT = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'wordfreq').glob('*.py')) + ['README.md']
DRIVERS = ['tools/verify_wordfreq_displayed_types.py', 'tools/verify_wordfreq_html.py', 'tools/wordfreq_html_geometry.js']
BROWSER = '/home/Yuki/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_bytes(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, check=True).stdout


def build_cases():
    """Literals independent of formatter/aggregator code."""
    cases = []
    normal = 'beta beta beta alpha gamma alpha delta'
    three = 'beta beta beta beta zoo zoo zoo apple apple pear pear single'
    many_words = ['zoo', 'apple', 'pear', 'mango', 'lime', 'kiwi', 'plum', 'berry', 'melon', 'peach', 'grape', 'fig']
    many = ' '.join(w for w in many_words for _ in range(2)) + ' beta beta beta'
    definitions = [
        ('max2', normal, ['--max-count', '2'], [['alpha', 2], ['gamma', 1], ['delta', 1]], 7),
        ('top1', normal, ['--max-count', '2', '--top', '1'], [['alpha', 2]], 7),
        ('top99', normal, ['--max-count', '2', '--top', '99'], [['alpha', 2], ['gamma', 1], ['delta', 1]], 7),
        ('min2max2', normal, ['--min-count', '2', '--max-count', '2'], [['alpha', 2]], 7),
        ('triple', three, ['--min-count', '2', '--max-count', '3', '--top', '1'], [['zoo', 3]], 12),
        ('many', many, ['--max-count', '2'], [[w, 2] for w in many_words[:10]], 27),
        ('many-all', many, ['--max-count', '2', '--top', '99'], [[w, 2] for w in many_words], 27),
        ('empty', '', [], [], 0), ('whitespace', ' \t\n\r', [], [], 0),
        ('punctuation', '!?... --', [], [], 0),
        ('excluded', normal, ['--max-count', '0'], [], 7),
        ('negative', normal, ['--max-count', '-1'], [], 7),
        ('contradictory', normal, ['--min-count', '3', '--max-count', '2'], [], 7),
        ('min4', normal, ['--min-count', '4'], [], 7),
        ('unicode', 'Straße STRASSE', ['--min-count', '2', '--max-count', '2'], [['strasse', 2]], 2),
        ('long', 'w' * 256, [], [['w' * 256, 1]], 1),
        ('escape', 'Café CAFÉ Straße STRASSE 日本語', [], [['café', 2], ['strasse', 2], ['日本語', 1]], 5),
        ('cr', 'alpha\r\nbeta', [], [['alpha', 1], ['beta', 1]], 2),
    ]
    for name, body, options, pairs, total in definitions:
        basename = name + '.txt'
        if name == 'long':
            basename = '集計  ' + 'n' * 176 + '\n続き\t終わり  &<>"\'.txt'
        elif name in {'escape', 'cr'}:
            basename = '検査\r\n&<>"\'.txt'
        for fmt in ('html', 'text', 'json'):
            cases.append(dict(id=f'{name}-{fmt}', body=body, basename=basename,
                              options=options + ['--format', fmt], pairs=pairs, total=total, format=fmt))
    return cases


def source_state():
    return dict(head=git_bytes('rev-parse', 'HEAD').decode().strip(),
                product_hashes={p: digest(ROOT / p) for p in PRODUCT},
                driver_hashes={p: digest(ROOT / p) for p in DRIVERS})


def assert_pre_product(provenance):
    if {p: digest(ROOT / p) for p in PRODUCT} != provenance['product_hashes']:
        raise ValueError('pre-product source hash mismatch')


def audit_cli(case, stdout):
    if case['format'] == 'text':
        expected = ''.join(f'{n}\t{w}\n' for w, n in case['pairs']).encode()
        if stdout != expected:
            raise ValueError('text bytes differ')
    elif case['format'] == 'json':
        expected = (json.dumps([dict(word=w, count=n) for w, n in case['pairs']], ensure_ascii=True) + '\n').encode()
        if stdout != expected:
            raise ValueError('json bytes differ')
    else:
        doc = parts.Document(stdout.decode('utf-8'))
        cells = [str(x) for i, (w, n) in enumerate(case['pairs'], 1) for x in (i, w, n)]
        if (doc.errors or doc.texts('td') != cells or doc.texts('th') != ['順位', '単語', '回数']
                or doc.texts('div', 'filename-value') != [case['basename']]
                or doc.texts('div', 'total-value') != [str(case['total'])]
                or doc.texts('div', 'displayed-types')):
            raise ValueError('unchanged HTML/static oracle differs')
        if b'private-source-directory' in stdout:
            raise ValueError('directory disclosure')


def controls(browser, output):
    """Real clean and blocked-at-network resource canaries, outside product HTML."""
    folder = output / 'canaries'
    folder.mkdir()
    results = []
    for name, markup in [('clean', '<!doctype html><title>clean</title><p>clean</p>'),
                         ('violating', '<!doctype html><title>violating</title><img src="http://wordfreq-canary.invalid:9/attempt">')]:
        path = folder / (name + '.html')
        path.write_text(markup)
        context = browser.new_context()
        observer = parts.Observer(browser, context)
        # Attempt is observed but never allowed to leave this process.
        context.route('http://**/*', lambda route: route.abort())
        page = context.new_page()
        observer.attach(page)
        try:
            page.goto(path.as_uri(), wait_until='load')
        finally:
            page.wait_for_timeout(100)
            net = observer.finish()
            save_json(folder / (name + '-network.json'), net)
            observer.browser_cdp.detach()
            context.close()
        errors = parts.network_errors(net, path.as_uri())
        if (name == 'clean' and errors) or (name == 'violating' and not any('external/unexpected attempt' in e for e in errors)):
            raise ValueError(f'canary {name}: observer discrimination failed: {errors}')
        if name == 'violating' and any(not e.startswith('external/unexpected attempt') for e in errors):
            raise ValueError(f'canary observer coverage failed: {errors}')
        results.append(dict(id=name, errors=errors, rejected=bool(errors)))
    save_json(folder / 'results.json', results)
    return results


def capture_before(output):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)  # atomic exclusive ownership, no resume
    save_json(output / 'owner.json', dict(pid=os.getpid(), started=parts.now()))
    initial = source_state()
    for p, sha in initial['product_hashes'].items():
        if hashlib.sha256(git_bytes('show', initial['head'] + ':' + p)).hexdigest() != sha:
            raise ValueError('capture requires committed unchanged product')
    provenance = dict(initial, cwd=str(ROOT), executable=sys.executable, python=sys.version,
                      os=platform.platform(), profile=os.environ.get('HERMES_PROFILE'),
                      task=os.environ.get('HERMES_KANBAN_TASK'), run=os.environ.get('HERMES_KANBAN_RUN_ID'),
                      environment={k: os.environ.get(k) for k in ('TMPDIR', 'PYTHONPATH', 'PYTHONUTF8')})
    save_json(output / 'provenance.json', provenance)
    index = dict(version=1, verdict='collecting', synthetic=False, independent_acceptance=False,
                 reviewed_images=[], provenance=provenance, execution_head=initial['head'], report_head=None,
                 root=str(output), cases=[], artifacts={})
    save_json(output / 'partial.json', index)
    try:
        from playwright.sync_api import sync_playwright
        for oracle in build_cases():
            folder = output / oracle['id']
            source = folder / 'private-source-directory' / oracle['basename']
            source.parent.mkdir(parents=True)
            source.write_bytes(oracle['body'].encode())
            argv = [sys.executable, '-m', 'wordfreq', str(source), *oracle['options']]
            env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
            run = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=30)
            stdout, stderr = folder / ('stdout.html' if oracle['format'] == 'html' else 'stdout.bin'), folder / 'stderr.bin'
            stdout.write_bytes(run.stdout)
            stderr.write_bytes(run.stderr)
            case = dict(oracle, argv=argv, input=str(source), stdout=str(stdout), stderr=str(stderr),
                        exit=run.returncode, environment={k: env[k] for k in ('PYTHONIOENCODING', 'PYTHONUTF8', 'PYTHONDONTWRITEBYTECODE')}, views=[])
            index['cases'].append(case)
            save_json(folder / 'cli.json', case)
            if run.returncode or run.stderr:
                raise ValueError(f'{oracle["id"]}: CLI failure')
            audit_cli(case, run.stdout)
        with sync_playwright() as pw, parts.instrumented_browser(pw, BROWSER) as browser:
            index['browser'] = dict(version=browser.version, executable=BROWSER, launch=browser.launch_record)
            index['controls'] = controls(browser, output)
            for case in index['cases']:
                if case['format'] != 'html':
                    continue
                for width in parts.WIDTHS:
                    view = parts.collect_view(browser, case, width, output)
                    case['views'].append(view)
                    save_json(output / 'partial.json', index)
                    if view['errors']:
                        raise ValueError(f'{case["id"]}/{width}: {view["errors"]}')
        if source_state() != initial:
            raise ValueError('source/head changed during capture')
        index['verdict'] = 'pending-review'
        index['ended'] = parts.now()
        # Include every original and sidecar; no file is claimed viewed.
        index['artifacts'] = {p.relative_to(output).as_posix(): digest(p) for p in sorted(output.rglob('*')) if p.is_file() and p.name != 'partial.json'}
        save_json(output / 'index.json', index)
        (output / 'index.sha256').write_text(digest(output / 'index.json') + '\n')
        validate_before(output)
        return index
    except BaseException as exc:
        index['verdict'] = 'failed'
        index['failure'] = f'{type(exc).__name__}: {exc}'
        save_json(output / 'partial.json', index)
        # A failed collection never retains its completion marker.
        (output / 'index.sha256').unlink(missing_ok=True)
        raise


def local(root, historical, original_root):
    rel = Path(historical).relative_to(original_root)
    target = (root / rel).resolve()
    target.relative_to(root.resolve())
    return target


def validate_before(root):
    root = Path(root).resolve()
    index_path = root / 'index.json'
    index = json.loads(index_path.read_text())
    if (root / 'index.sha256').read_text() != digest(index_path) + '\n':
        raise ValueError('index seal mismatch')
    if index.get('verdict') != 'pending-review' or index.get('synthetic') is not False or index.get('independent_acceptance') is not False or index.get('reviewed_images') != []:
        raise ValueError('invalid collection/acceptance state')
    provenance = index['provenance']
    if provenance != json.loads((root / 'provenance.json').read_text()) or index['execution_head'] != provenance['head']:
        raise ValueError('provenance mismatch')
    for p, sha in provenance['product_hashes'].items():
        if hashlib.sha256(git_bytes('show', provenance['head'] + ':' + p)).hexdigest() != sha:
            raise ValueError('historical product hash differs')
    if set(provenance['product_hashes']) != set(PRODUCT):
        raise ValueError('missing product hashes')
    for rel, sha in index['artifacts'].items():
        path = (root / rel).resolve()
        path.relative_to(root)
        if digest(path) != sha:
            raise ValueError(f'artifact altered: {rel}')
    expected = build_cases()
    if len(index['cases']) != len(expected) or index['controls'] != json.loads((root / 'canaries/results.json').read_text()):
        raise ValueError('case/control coverage missing')
    if [c['rejected'] for c in index['controls']] != [False, True]:
        raise ValueError('canary controls invalid')
    for case, oracle in zip(index['cases'], expected):
        if any(case[k] != v for k, v in oracle.items()) or case['exit'] != 0:
            raise ValueError('case oracle differs')
        source = local(root, case['input'], index['root'])
        stdout = local(root, case['stdout'], index['root'])
        stderr = local(root, case['stderr'], index['root'])
        if source.read_bytes() != oracle['body'].encode() or stderr.read_bytes():
            raise ValueError('input/stderr differs')
        if case['argv'] != [provenance['executable'], '-m', 'wordfreq', case['input'], *oracle['options']]:
            raise ValueError('argv differs')
        audit_cli(case, stdout.read_bytes())
        if len(case['views']) != (2 if case['format'] == 'html' else 0):
            raise ValueError('missing browser views')
        for width, view in zip(parts.WIDTHS, case['views']):
            if view['errors'] or view['reviewed_images'] or view['verdict'] != 'pending-review':
                raise ValueError('invalid view state')
            raw = json.loads(local(root, view['raw'], index['root']).read_text())
            viewport = dict(width=width, height=900, dpr=1, scale=1)
            if view['browser']['viewport'] != viewport or raw['viewport'] != viewport or not raw.get('platformFonts'):
                raise ValueError('viewport/DPR/fonts differ')
            if parts.geometry_errors(raw) or parts.dom_errors(raw, case):
                raise ValueError('raw geometry/DOM invalid')
            network = json.loads(local(root, view['network'], index['root']).read_text())
            if parts.network_errors(network, Path(case['stdout']).as_uri()):
                raise ValueError('network coverage invalid')
            if not view['images'] or view['images'][0]['type'] != 'full':
                raise ValueError('missing images')
            for image in view['images']:
                path = local(root, image['path'], index['root'])
                if parts.png_size(path) != (image['width'], image['height']):
                    raise ValueError('image dimensions differ')
    return index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['before', 'validate-before'], required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = capture_before(args.output) if args.mode == 'before' else validate_before(args.output)
    print(json.dumps(dict(verdict=result['verdict'], cases=len(result['cases']), independent_acceptance=False)))


if __name__ == '__main__':
    main()
