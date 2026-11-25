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
