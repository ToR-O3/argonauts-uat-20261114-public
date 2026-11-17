"""Real Chromium regression: full capture must match the measured viewport pixels.
Run with the existing CPython3.12/Playwright environment. Not quality acceptance.
"""
import base64
import importlib.util
import json
from pathlib import Path
import sys

import struct
import zlib
from playwright.sync_api import sync_playwright


def pixels(data):
    """Decode Chromium's non-interlaced RGB/RGBA PNG with stdlib only."""
    offset, compressed = 8, bytearray()
    while offset < len(data):
        length = int.from_bytes(data[offset:offset+4], "big")
        tag, payload = data[offset+4:offset+8], data[offset+8:offset+8+length]
        if tag == b"IHDR":
            width, height, depth, color, _, _, interlace = struct.unpack(">IIBBBBB", payload)
            assert depth == 8 and color in (2, 6) and interlace == 0
            channels = 3 if color == 2 else 4
        if tag == b"IDAT":
            compressed.extend(payload)
        offset += length + 12
    raw, stride, rows = zlib.decompress(compressed), width * channels, []
    previous = bytearray(stride)
    for y in range(height):
        start = y * (stride + 1)
        mode, row = raw[start], bytearray(raw[start+1:start+1+stride])
        for x in range(stride):
            a = row[x-channels] if x >= channels else 0
            b, c = previous[x], previous[x-channels] if x >= channels else 0
            if mode == 1:
                predictor = a
            elif mode == 2:
                predictor = b
            elif mode == 3:
                predictor = (a+b)//2
            elif mode == 4:
                p = a+b-c
                distances = (abs(p-a), abs(p-b), abs(p-c))
                predictor = (a, b, c)[distances.index(min(distances))]
            else:
                assert mode == 0
                predictor = 0
            row[x] = (row[x]+predictor) & 255
        rows.append(bytes(value for x, value in enumerate(row) if x % channels < 3))
        previous = row
    return width, height, rows


def difference(a, b, y=0):
    aw, ah, ar = a
    bw, bh, br = b
    assert aw <= bw and ah <= bh-y
    return sum(ar[i] != br[i+y][:aw*3] for i in range(ah))

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("verifier", ROOT / "tools/verify_wordfreq_html.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
output = Path(sys.argv[1]).resolve()
output.mkdir(parents=True, exist_ok=False)
cases = v.generate_cases(output)
original_attach = v.Observer.attach
references = []


def attach(self, page):
    cdp = original_attach(self, page)
    original_send = cdp.send

    def send(method, params=None):
        if method == "Page.captureScreenshot" and params.get("clip", {}).get("y") == 0:
            # This viewport-only reference retains the current scrollbar/layout.
            # It is captured BEFORE the collector's potentially reflowing call.
            reference = original_send("Page.captureScreenshot", dict(format="png", captureBeyondViewport=False))
            references.append(pixels(base64.b64decode(reference["data"])))
        return original_send(method, params) if params is not None else original_send(method)

    cdp.send = send
    return cdp


v.Observer.attach = attach
results = []
with sync_playwright() as pw, v.instrumented_browser(pw, "/usr/bin/chromium-browser") as browser:
    for case_id in ("long-12", "long-99", "long-default", "normal-2"):
        case = next(c for c in cases if c["id"] == case_id)
        for width in (320, 1280):
            start = len(references)
            view = v.collect_view(browser, case, width, output)
            raw = json.loads(Path(view["raw"]).read_text())
            full = pixels(Path(view["images"][0]["path"]).read_bytes())
            reference = references[start]
            top = (full[0], min(full[1], 900), full[2][:900])
            diff = difference(top, reference)
            tile_diffs = []
            for tile in view["images"][1:]:
                image = pixels(Path(tile["path"]).read_bytes())
                tile_diffs.append(difference(image, full, tile["y"]))
            item = dict(case=case_id, width=width, clientWidth=raw["document"]["clientWidth"],
                        scrollHeight=raw["document"]["scrollHeight"], viewport_difference=diff,
                        tile_differences=tile_diffs, errors=view["errors"])
            results.append(item)
            print(json.dumps(item), flush=True)
v.save_json(output / "pixel-comparison.json", results)
assert all(r["viewport_difference"] == 0 and not any(r["tile_differences"]) and not r["errors"] for r in results), "capture reflow: full/tile pixels differ from the measured viewport"
