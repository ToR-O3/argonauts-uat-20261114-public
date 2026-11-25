"""Phase8 before originals: fail-closed contracts, plus explicit real capture."""
import importlib.util
import json
import os
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
BEFORE = ROOT / '.planning/argonauts/r-6ae2cbf2/before'


def driver():
    spec = importlib.util.spec_from_file_location('display_verifier', ROOT / 'tools/verify_wordfreq_displayed_types.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_before_api_and_literal_cases():
    d = driver()
    assert {'build_cases', 'capture_before', 'validate_before'} <= set(dir(d))
    cases = {c['id']: c for c in d.build_cases()}
    assert cases['max2-html']['pairs'] == [['alpha', 2], ['gamma', 1], ['delta', 1]]
    assert cases['triple-html']['pairs'] == [['zoo', 3]]
    assert cases['triple-html']['total'] == 12
    assert len(cases['many-html']['pairs']) == 10
    assert len(cases['many-all-html']['pairs']) == 12
    assert {c['format'] for c in cases.values()} == {'text', 'json', 'html'}


def test_existing_root_and_concurrent_owner_rejected(tmp_path):
    with pytest.raises(FileExistsError):
        driver().capture_before(tmp_path)
    assert list(tmp_path.iterdir()) == []
    owned = tmp_path / 'owned'
    owned.mkdir()
    (owned / 'owner.json').write_text('{"running":true}')
    with pytest.raises(FileExistsError):
        driver().capture_before(owned)


@pytest.mark.parametrize('marker', ['none', 'partial', 'synthetic'])
def test_incomplete_or_synthetic_cannot_validate(tmp_path, marker):
    if marker != 'none':
        (tmp_path / 'index.json').write_text(json.dumps({'verdict': marker, 'synthetic': True}))
    with pytest.raises((ValueError, FileNotFoundError)):
        driver().validate_before(tmp_path)


def test_interrupt_preserves_owned_root_without_completion(monkeypatch, tmp_path):
    d = driver()
    target = tmp_path / 'interrupted'

    def interrupt():
        raise KeyboardInterrupt('injected interruption, synthetic control')

    monkeypatch.setattr(d, 'source_state', interrupt)
    with pytest.raises(KeyboardInterrupt):
        d.capture_before(target)
    assert (target / 'owner.json').is_file()
    assert not (target / 'index.sha256').exists()
    with pytest.raises((ValueError, FileNotFoundError)):
        d.validate_before(target)
    with pytest.raises(FileExistsError):
        d.capture_before(target)


def test_wrong_product_refused_before_browser(monkeypatch, tmp_path):
    d = driver()
    provenance = d.source_state()
    provenance['product_hashes']['wordfreq/formatters.py'] = '0' * 64
    monkeypatch.setattr(d, 'source_state', lambda: provenance)
    target = tmp_path / 'wrong-product'
    with pytest.raises(ValueError, match='unchanged product'):
        d.capture_before(target)
    assert not (target / 'index.sha256').exists()


def test_capture_before_real_browser():
    d = driver()
    if os.environ.get('WORDFREQ_DISPLAY_CAPTURE') == 'before':
        d.capture_before(BEFORE)
        d.validate_before(BEFORE)
    elif BEFORE.exists():
        d.validate_before(BEFORE)
    else:
        # Ordinary suite never captures implicitly; absence is not browser success.
        assert not (BEFORE / 'index.json').exists()


@pytest.mark.parametrize('damage', ['missing', 'bytes', 'head', 'product', 'viewport', 'dpr', 'synthetic', 'interrupted', 'inventory'])
def test_saved_original_tamper_rejected(tmp_path, damage):
    d = driver()
    if not BEFORE.exists():
        with pytest.raises(FileNotFoundError):
            d.validate_before(BEFORE)
        return
    copy = tmp_path / 'copy'
    shutil.copytree(BEFORE, copy)
    index = json.loads((copy / 'index.json').read_text())
    if damage in {'missing', 'bytes'}:
        path = copy / next(iter(index['artifacts']))
        if damage == 'missing':
            path.unlink()
        else:
            path.write_bytes(b'corrupt')
    elif damage in {'head', 'product'}:
        index['provenance']['head' if damage == 'head' else 'product_hashes'] = 'wrong'
    elif damage in {'viewport', 'dpr'}:
        case = next(c for c in index['cases'] if c['format'] == 'html')
        view = case['views'][0]
        view['browser']['viewport']['width' if damage == 'viewport' else 'dpr'] = 42
    elif damage == 'synthetic':
        index['synthetic'] = True
    elif damage == 'inventory':
        index['artifacts'].pop(next(iter(index['artifacts'])))
    else:
        index['verdict'] = 'collecting'
    d.save_json(copy / 'index.json', index)
    (copy / 'index.sha256').write_text(d.digest(copy / 'index.json') + '\n')
    with pytest.raises((ValueError, FileNotFoundError)):
        d.validate_before(copy)
