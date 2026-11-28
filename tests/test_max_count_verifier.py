"""Read-only integrity checks for the max-count oracle and pre-feature RED."""
import importlib.util
import json
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("max_verifier", ROOT / "tools/verify_wordfreq_max_count.py")


def driver():
    module = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(module)
    return module


def test_browser_free_capture_api():
    d = driver()
    required = {'build_capture_cases', 'capture', 'validate_capture', 'review_session', 'finalize'}
    assert required <= set(dir(d)), 'max-specific capture and independent review API missing'


def test_browser_free_capture_cases():
    d = driver()
    assert hasattr(d, 'build_capture_cases'), 'max-specific cases missing'
    cases = {c['id']: c for c in d.build_capture_cases()}
    assert cases['max2-html']['pairs'] == [['alpha', 2], ['gamma', 1], ['delta', 1]]
    assert cases['triple-html']['pairs'] == [['zoo', 3]]
    assert cases['triple-html']['total'] == 12
    assert len(cases['many-html']['pairs']) == 10
    assert len(cases['many-all-html']['pairs']) == 12
    assert cases['min2max2-html']['pairs'] == [['alpha', 2]]
    assert cases['unicode-empty-html']['pairs'] == []
    assert cases['negative-html']['pairs'] == []
    assert len(cases) == len(d.build_capture_cases())
    assert all(c['format'] in ('text', 'json', 'html') for c in cases.values())


def test_browser_free_quality_role_cannot_be_flag_only(monkeypatch, tmp_path):
    d = driver()
    assert hasattr(d, 'capture'), 'capture API missing'
    monkeypatch.setenv('HERMES_PROFILE', 'argonauts-uat-builder')
    with pytest.raises(ValueError, match='profile'):
        d.capture(tmp_path / 'not-created', 'quality', ROOT / d.BASELINE)
    assert not (tmp_path / 'not-created').exists()


def test_browser_free_case_contract():
    cases = driver().build_baseline_cases()
    assert len({c['id'] for c in cases}) == len(cases)
    assert {c['format'] for c in cases} == {'text', 'json', 'html'}
    assert {'default-text', 'min-top-html', 'excluded-html', 'unicode-html',
            'long-html', 'hostile-html', 'cr-html'} <= {c['id'] for c in cases}
    assert all('--max-count' not in c['options'] for c in cases)


def test_browser_free_existing_root_rejected(tmp_path):
    with pytest.raises(FileExistsError):
        driver().capture_baseline(tmp_path)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize('damage', ['stdout', 'input', 'argv', 'environment', 'head', 'hash', 'html', 'synthetic'])
def test_browser_free_tamper_rejected(tmp_path, damage):
    d = driver()
    source = ROOT / d.BASELINE
    target = tmp_path / 'copy'
    shutil.copytree(source, target)
    index = json.loads((target / 'index.json').read_text())
    case = index['cases'][0]
    if damage == 'stdout':
        (target / case['stdout']).write_bytes(b'corrupt')
    elif damage == 'input':
        (target / case['input']).write_bytes(b'corrupt')
    elif damage == 'html':
        html_case = next(c for c in index['cases'] if c['format'] == 'html')
        (target / html_case['html']).unlink()
    else:
        if damage == 'argv':
            case['argv'].append('--max-count=0')
        elif damage == 'environment':
            index['environment']['PYTHONHASHSEED'] = '42'
        elif damage == 'head':
            index['head'] = '0' * 40
        elif damage == 'synthetic':
            index['synthetic'] = True
        else:
            index['artifacts'][case['stdout']] = '0' * 64
        d.save_json(target / 'index.json', index)
        # Even with an updated outer checksum, inner/provenance contracts fail.
        (target / 'index.sha256').write_text(d.digest(target / 'index.json') + '\n')
    with pytest.raises((ValueError, FileNotFoundError)):
        d.validate_baseline(target)


@pytest.fixture(scope='module')
def collected_capture(tmp_path_factory):
    # Fixture only: real CLI bytes, deliberately incomplete suite, never acceptance.
    from unittest.mock import patch
    d = driver()
    target = tmp_path_factory.mktemp('max-contract') / 'capture'
    with patch.dict('os.environ', HERMES_PROFILE='argonauts-uat-builder',
                    HERMES_HOME='/fixture/argonauts-uat-builder'):
        # Damage fixture is not an acceptance run. Avoid historical Git reads
        # here; real scope discrimination runs in the separate cold repository.
        with patch.object(d, 'validate_scope', return_value={'fixture_only': True}):
            d.collect_capture(target, 'builder', ROOT / d.BASELINE)
    return target


@pytest.mark.parametrize('damage', ['head', 'argv', 'case', 'input', 'stdout', 'html',
                                   'synthetic', 'acceptance', 'profile', 'hash'])
def test_browser_free_capture_damage_rejected(collected_capture, tmp_path, damage):
    d = driver()
    root = tmp_path / 'copy'
    shutil.copytree(collected_capture, root)
    m = json.loads((root / 'manifest.json').read_text())
    case = m['cases'][0]
    if damage == 'head':
        m['head'] = '0' * 40
    elif damage == 'argv':
        case['argv'].append('--max-count=0')
    elif damage == 'case':
        m['cases'].pop()
    elif damage in ('input', 'stdout'):
        (root / case[damage]).write_bytes(b'bad')
    elif damage == 'html':
        c = next(c for c in m['cases'] if c['format'] == 'html')
        (root / c['html']).unlink()
    elif damage == 'synthetic':
        m['synthetic'] = True
    elif damage == 'acceptance':
        m['independent_acceptance'] = True
        m['verdict'] = 'accepted'
    elif damage == 'profile':
        m['provenance']['profile'] = 'argonauts-uat-quality'
    else:
        m['artifacts'][case['stdout']] = '0' * 64
    d.save_json(root / 'manifest.json', m)
    (root / 'manifest.sha256').write_text(d.digest(root / 'manifest.json') + '\n')
    with pytest.raises((ValueError, FileNotFoundError)):
        d.validate_collection(root, ROOT / d.BASELINE)


def test_browser_free_partial_cannot_pass(collected_capture):
    d = driver()
    with pytest.raises(ValueError, match='incomplete'):
        d.validate_capture(collected_capture, ROOT / d.BASELINE)


@pytest.mark.parametrize('tests,failures,errors,skipped,exit_code', [
    (0, 0, 0, 0, 0), (1, 1, 0, 0, 0), (1, 0, 1, 0, 0),
    (1, 0, 0, 1, 0), (1, 0, 0, 0, 1), (2, 0, 0, 0, 0),
])
def test_browser_free_bad_suite_rejected(tmp_path, tests, failures, errors, skipped, exit_code):
    d = driver()
    xml = tmp_path / 'bad.xml'
    xml.write_text(f'<testsuites><testsuite tests="{tests}" failures="{failures}" '
                   f'errors="{errors}" skipped="{skipped}"><testcase name="fixture"/>'
                   '</testsuite></testsuites>')
    with pytest.raises(ValueError, match='suite'):
        d.suite_counts(xml, exit_code)


def test_saved_builder_capture():
    import os
    d = driver()
    active = os.environ.get('WORDFREQ_MAX_ACTIVE_ROOT')
    root = Path(active) if active else ROOT / d.CAPTURE
    # Only the actual capture owner's direct pytest child may inspect the sealed
    # collection without requiring its own (still running) suite to be complete.
    m = json.loads((root / 'manifest.json').read_text())
    if active and m['provenance']['pid'] == os.getppid() and m['phase'] == 'collected':
        d.validate_collection(root, ROOT / d.BASELINE, active_owner=True)
    else:
        d.validate_capture(root, ROOT / d.BASELINE)


def test_evidence_contract_runbook_exists():
    assert (ROOT / 'docs/wordfreq-max-count-verification.md').is_file(), 'max runbook missing'


def test_scope_contract_api():
    assert hasattr(driver(), 'validate_scope'), 'scope validator missing'


def runbook_contract(text):
    required = ['OpenSpec2.2は未完了', 'pending-review', '1795609328', '画像取得0枚',
                'PMに画像や圧縮物の閲覧を求めない', 'VERIFICATION.md', 'cli-ci-proof.md',
                'kanban_attach', 'kanban_attachments', 'SHA-256', 'read_file',
                '未報告CIは未確認', 'fresh root', '既存試験保持', '元Counter不変',
                'original-Counter/total -> AND -> top -> shared-pairs',
                '--mode review-session --role quality', '--mode finalize --role quality',
                '--mode validate', '--baseline-dir', '--review-ledger', '非0/ERROR/skip',
                *[f'AC{i}' for i in range(1, 7)], *[f'REQ-{i}' for i in range(23, 29)]]
    for term in required:
        assert term in text, 'missing runbook obligation: '+term
    assert 'verify_wordfreq_min_count.py --mode' not in text
    assert '--browser' not in text


def test_evidence_contract_complete():
    runbook_contract((ROOT / 'docs/wordfreq-max-count-verification.md').read_text())


@pytest.mark.parametrize('missing', ['AC6', 'REQ-28', 'kanban_attachments', '元Counter不変',
                                     '未報告CIは未確認', '--review-ledger', '1795609328'])
def test_evidence_contract_omission_detected(missing):
    text = (ROOT / 'docs/wordfreq-max-count-verification.md').read_text()
    with pytest.raises(AssertionError, match='missing runbook obligation'):
        runbook_contract(text.replace(missing, 'REMOVED'))


@pytest.fixture
def scope_repo(tmp_path):
    import subprocess
    d = driver()
    repo = tmp_path / 'cold'
    repo.mkdir()
    for name in (*d.PRODUCT, 'README.md', 'tests/test_cli.py', 'pyproject.toml'):
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        # Historical max-count scope, not the current product (which may evolve).
        # Snapshot: 31953e1c3f1bd0b5da09484f079f0027976ec737:wordfreq/__main__.py
        # SHA-256: 9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba
        source = (ROOT / 'tests/fixtures/max_count_scope/__main__.py'
                  if name == 'wordfreq/__main__.py' else ROOT / name)
        path.write_bytes(source.read_bytes())
    def git(*args):
        return subprocess.run(['git', *args], cwd=repo, capture_output=True, check=True,
                              text=True, timeout=20).stdout.strip()
    git('init', '-q')
    git('add', '.')
    git('-c', 'user.name=Scope Fixture', '-c', 'user.email=scope@example.invalid',
        'commit', '-qm', 'cold baseline')
    return repo, git('rev-parse', 'HEAD')


def test_scope_contract_clean_and_append_only(scope_repo):
    d = driver()
    repo, base = scope_repo
    with (repo / 'tests/test_cli.py').open('a') as stream:
        stream.write('\ndef test_addition():\n    assert True\n')
    result = d.validate_scope(repo, base)
    assert result['paths'] == ['tests/test_cli.py']
    assert result['existing_tests_preserved']


@pytest.mark.parametrize('damage', ['unrelated', 'dependency', 'delete', 'relax', 'formatter', 'readme', 'workflow'])
def test_scope_contract_cold_damage_rejected(scope_repo, damage):
    repo, base = scope_repo
    if damage == 'delete':
        (repo / 'tests/test_cli.py').unlink()
    elif damage == 'relax':
        p = repo / 'tests/test_cli.py'
        p.write_text(p.read_text().replace('assert ', 'pass # assert ', 1))
    else:
        name = {'unrelated': 'unrelated.txt', 'dependency': 'pyproject.toml',
                'formatter': 'wordfreq/formatters.py', 'readme': 'README.md',
                'workflow': '.github/workflows/injected.yml'}[damage]
        p = repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('a') as stream:
            stream.write('\n# unrelated\n')
    with pytest.raises(ValueError):
        driver().validate_scope(repo, base)


def test_browser_free_foreign_owner_rejected(collected_capture):
    d = driver()
    with pytest.raises(ValueError, match='direct pytest child'):
        d.validate_collection(collected_capture, ROOT / d.BASELINE, active_owner=True)


def test_saved_baseline():
    d = driver()
    root = ROOT / d.BASELINE
    before = {p: d.digest(p) for p in root.rglob('*') if p.is_file()}
    d.validate_baseline(root)
    assert before == {p: d.digest(p) for p in root.rglob('*') if p.is_file()}


def test_saved_preimplementation_red():
    d = driver()
    d.validate_red(ROOT / d.EVIDENCE / 'red')


@pytest.mark.parametrize('evidence', ['baseline', 'red'])
def test_saved_evidence_without_git_history(monkeypatch, evidence):
    d = driver()

    def unavailable_history(*args, **kwargs):
        raise AssertionError('saved evidence verification must not read Git history')

    monkeypatch.setattr(d.subprocess, 'run', unavailable_history)
    if evidence == 'baseline':
        d.validate_baseline(ROOT / d.BASELINE)
    else:
        d.validate_red(ROOT / d.EVIDENCE / 'red')
