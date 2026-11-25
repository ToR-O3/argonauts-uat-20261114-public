"""One-shot launch and image-capability probe, not acceptance evidence."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent
with sync_playwright() as pw:
    with pw.chromium.launch(executable_path="/home/Yuki/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome", headless=True) as browser:
        page = browser.new_page(viewport={"width": 320, "height": 900}, device_scale_factor=1)
        page.goto((root / "launch.html").as_uri())
        page.screenshot(path=str(root / "launch.png"), full_page=True)
        print(browser.version)
        print(page.title())
