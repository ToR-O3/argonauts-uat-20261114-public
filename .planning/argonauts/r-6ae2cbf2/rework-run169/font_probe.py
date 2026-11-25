"""Read-only real CLI page probe with platform-font evidence, not acceptance."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'before/max2-html/stdout.html'
with sync_playwright() as pw:
    with pw.chromium.launch(executable_path='/home/Yuki/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome', headless=True) as browser:
        page = browser.new_page(viewport={'width': 320, 'height': 900}, device_scale_factor=1)
        page.goto(SOURCE.as_uri(), wait_until='load')
        page.evaluate('document.fonts.ready')
        cdp = page.context.new_cdp_session(page)
        cdp.send('DOM.enable')
        cdp.send('CSS.enable')
        doc = cdp.send('DOM.getDocument')
        node = cdp.send('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': 'h1'})
        fonts = cdp.send('CSS.getPlatformFontsForNode', {'nodeId': node['nodeId']})
        report = {'browser': browser.version, 'source': str(SOURCE), 'heading': page.locator('h1').inner_text(), 'fonts': fonts}
        page.screenshot(path=str(ROOT / 'font-probe.png'), full_page=True)
        (ROOT / 'font-probe.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(report, ensure_ascii=False))
        assert any(f['familyName'] == 'Noto Sans JP' and f['glyphCount'] > 0 for f in fonts['fonts']), 'Japanese heading has no Noto Sans JP glyphs'
