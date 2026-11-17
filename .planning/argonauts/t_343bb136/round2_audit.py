"""Recheck fresh originals and exercise missing-channel/text rejection in Chromium."""
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path.cwd()
spec = importlib.util.spec_from_file_location('v', ROOT / 'tools/verify_wordfreq_html.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
output = ROOT / '.planning/argonauts/r-50053edc/builder/round2-capture'
manifest = json.loads((output / 'manifest.json').read_text())
counts = dict(cli_cases=len(manifest['cases']), views=0, images=0, rejected_ready_deletions=0,
              rejected_text_deletions=0)
for case in manifest['cases']:
    for view in case['views']:
        counts['views'] += 1
        counts['images'] += len(view['images'])
        raw = json.loads(Path(view['raw']).read_text())
        net = json.loads(Path(view['network']).read_text())
        url = Path(case['stdout']).as_uri()
        assert v.network_errors(net, url) == []
        assert v.geometry_errors(raw) == []
        for kind in ('browser-autoattach-ready', 'page-cdp-ready'):
            bad = copy.deepcopy(net)
            bad['events'] = [e for e in bad['events'] if e['kind'] != kind]
            assert v.network_errors(bad, url)
            counts['rejected_ready_deletions'] += 1
        for el in raw['elements']:
            if el['tag'] == 'td' or el['className'] in {'filename-value', 'total-value'}:
                bad = copy.deepcopy(raw)
                bad['texts'] = [t for t in bad['texts'] if t['owner'] != el['id']]
                assert any('text not fully measured' in e for e in v.geometry_errors(bad))
                counts['rejected_text_deletions'] += 1
assert v.capture_errors(manifest, output) == []

# Browser-owned probe, not a modification of product HTML or its capture evidence.
from playwright.sync_api import sync_playwright
nested = []
with sync_playwright() as pw, v.instrumented_browser(pw, '/usr/bin/chromium-browser') as browser:
    context = browser.new_context(viewport=dict(width=320, height=900), device_scale_factor=1)
    page = context.new_page()
    for name, markup in (
        ('td', '<table><tr><td class="word"><div>wrapped</div></td><td>control</td></tr></table>'),
        ('filename-value', '<div class="filename-value"><div>wrapped</div></div><h1>control</h1>'),
        ('total-value', '<div class="total-value"><div>123</div></div><h1>control</h1>')):
        assert v.Document(markup).errors == []
        page.set_content(markup)
        raw = page.evaluate((ROOT / 'tools/wordfreq_html_geometry.js').read_text())
        errors = v.geometry_errors(raw)
        assert any('text not fully measured' in e for e in errors), errors
        nested.append(dict(case=name, raw=raw, errors=errors))
    context.close()
v.save_json(ROOT / '.planning/argonauts/t_343bb136/round2-audit.json', dict(counts=counts, nested_probes=nested,
    verdict='tooling checks passed; readability and independent acceptance pending'))
print(json.dumps(counts))
