"""Real-file CLI/browser evidence. Capture never claims visual acceptance.

Browser dependencies are imported only by explicit browser operations.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (1280, 320)


def fixed_cases():
    """Independent input/oracle literals; never ask product code for expectations."""
    cases = []

    def add(name, basename, body, pairs, total, top=10, fmt="html"):
        cases.append(dict(id=name, basename=basename, body=body, pairs=pairs,
                          total=total, top=top, format=fmt))

    add("empty", "empty.txt", "", [], 0)
    for top in (1, 2, 10):
        add(f"normal-{top}", "通常.txt", "zoo apple zoo banana apple cherry",
            [("zoo", 2), ("apple", 2), ("banana", 1), ("cherry", 1)][:top], 6, top)
    add("frequency", "frequency.txt", "beta beta beta alpha gamma alpha delta",
        [("beta", 3), ("alpha", 2)], 7, 2)
    for fmt in ("text", "json", "html"):
        for top in (1, 2):
            add(f"tie-{fmt}-{top}", "tie.txt", "Zoo apple APPLE zoo banana",
                [("zoo", 2), ("apple", 2)][:top], 5, top, fmt)
    pairs = [("w" * 256, 123)] + [(f"row{i:02}", 13-i) for i in range(1, 12)]
    body = " ".join(word for word, count in pairs for _ in range(count)) + "\n"
    basename = '集計  ' + 'n' * 176 + '\n続き\t終わり  &<>"\'.txt'
    for label, top in (("12", 12), ("default", None), ("99", 99)):
        add(f"long-{label}", basename, body, pairs[:10 if top is None else top], 200, top)
    add("injection", '検査  &<>"\'\n次\t終.txt', "Café CAFÉ Straße STRASSE 日本語",
        [("café", 2), ("strasse", 2), ("日本語", 1)], 5)
    return cases


def now():
    return datetime.now(timezone.utc).isoformat()


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class Document(HTMLParser):
    """Fixed-document model and static executable/resource allow-list."""
    allowed = {"div", "html", "head", "meta", "title", "style", "body", "main", "h1", "dl", "dt", "dd", "table", "caption", "colgroup", "col", "thead", "tr", "th", "tbody", "td", "p"}

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.nodes, self.stack, self.errors = [], [], []
        self.feed(source)
        self.close()
        if self.stack:
            self.errors.append("unclosed markup")

    def handle_starttag(self, tag, attrs):
        node = dict(tag=tag, attrs=dict(attrs), text="")
        self.nodes.append(node)
        if tag not in self.allowed:
            self.errors.append(f"forbidden tag {tag}")
        for key, value in attrs:
            if key not in {"lang", "charset", "name", "content", "class", "scope"}:
                self.errors.append(f"forbidden attribute {tag}.{key}")
            if key == "name" and value != "viewport":
                self.errors.append("unknown meta")
        if tag not in {"meta", "col"}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1]["tag"] != tag:
            self.errors.append(f"unbalanced {tag}")
        else:
            self.stack.pop()

    def handle_data(self, data):
        for node in self.stack:
            node["text"] += data
        if self.stack and self.stack[-1]["tag"] == "style":
            if re.search(r"url\s*\(|@import|expression\s*\(", data, re.I) or "\\" in data:
                self.errors.append("CSS executable/resource path")

    def texts(self, tag, cls=None):
        return [n["text"] for n in self.nodes if n["tag"] == tag and
                (cls is None or n["attrs"].get("class") == cls)]


def generate_cases(output):
    records = []
    for case in fixed_cases():
        folder = output / case["id"]
        source_dir = folder / "private-source-directory"
        source_dir.mkdir(parents=True, exist_ok=False)
        source = source_dir / case["basename"]
        source.write_bytes(case["body"].encode("utf-8"))
        argv = [sys.executable, "-m", "wordfreq", str(source), "--format", case["format"]]
        if case["top"] is not None:
            argv += ["--top", str(case["top"])]
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=20)
        stdout = folder / ("stdout.html" if case["format"] == "html" else "stdout.txt")
        stderr = folder / "stderr.bin"
        stdout.write_bytes(result.stdout)
        stderr.write_bytes(result.stderr)
        record = dict(case, input=str(source), basename_repr=repr(case["basename"]),
                      argv=argv, cwd=str(ROOT), executable=sys.executable,
                      environment={key: env[key] for key in ("PYTHONIOENCODING", "PYTHONUTF8", "PYTHONDONTWRITEBYTECODE")},
                      exit=result.returncode, stdout=str(stdout), stderr=str(stderr), views=[])
        records.append(record)
        save_json(folder / "cli.json", record)
        if result.returncode or result.stderr:
            raise ValueError(f"{case['id']}: CLI exit/stderr {result.returncode}: {result.stderr!r}")
        text = result.stdout.decode("utf-8", errors="strict")
        if case["format"] == "text":
            if text != "".join(f"{count}\t{word}\n" for word, count in case["pairs"]):
                raise ValueError(f"{case['id']}: text oracle")
        elif case["format"] == "json":
            if json.loads(text) != [dict(word=w, count=n) for w, n in case["pairs"]]:
                raise ValueError(f"{case['id']}: JSON oracle")
        else:
            model = Document(text)
            expected_cells = [str(value) for i, (word, count) in enumerate(case["pairs"], 1) for value in (i, word, count)]
            if model.errors or model.texts("td") != expected_cells:
                raise ValueError(f"{case['id']}: static/row oracle {model.errors}")
            if model.texts("th") != ["順位", "単語", "回数"]:
                raise ValueError(f"{case['id']}: headers")
            if model.texts("div", "filename-value") != [case["basename"]] or model.texts("div", "total-value") != [str(case["total"])]:
                raise ValueError(f"{case['id']}: metadata")
            if "private-source-directory" in text or str(source_dir) in text or escape(str(source_dir)) in text:
                raise ValueError(f"{case['id']}: directory disclosure")
            record["static_audit"] = "passed"
    return records


def geometry_errors(raw):
    """Derive failures separately; never mutate, round or clamp original rectangles."""
    errors = []
    try:
        viewport = raw["viewport"]
        if viewport["dpr"] != 1 or viewport["scale"] != 1:
            errors.append("DPR/zoom differs")
        if raw["document"]["scrollWidth"] > viewport["width"]:
            errors.append("document horizontal overflow")
        elements = {e["id"]: e for e in raw["elements"]}
        if not elements or not raw["texts"]:
            return errors + ["missing element/text measurements"]
        glyphs = []
        for text in raw["texts"]:
            owner = elements[text["owner"]]
            chars = text["characters"]
            if len(chars) != len(text["text"]) or not isinstance(text["fullRects"], list):
                errors.append(f"{text['id']}: missing character/full Range")
                continue
            offset = 0
            for i, (char, item) in enumerate(zip(text["text"], chars)):
                end = offset + len(char.encode("utf-16-le")) // 2
                if (item["index"], item["utf16Start"], item["utf16End"], item["char"], item["codepoint"]) != (i, offset, end, char, ord(char)):
                    errors.append(f"{text['id']}[{i}]: codepoint/UTF16 mismatch")
                offset = end
                if not isinstance(item["rects"], list) or (not char.isspace() and not item["rects"]):
                    errors.append(f"{text['id']}[{i}]: missing visible Range")
                for r in item["rects"]:
                    if r["width"] <= 0 or r["height"] <= 0:
                        continue  # Raw retains zero-area rectangles; no visible ink.
                    if r["left"] < 0 or r["right"] > viewport["width"]:
                        errors.append(f"{text['id']}[{i}]: outside viewport")
                    if r["left"] < owner["rect"]["left"] or r["right"] > owner["rect"]["right"]:
                        errors.append(f"{text['id']}[{i}]: outside column")
                    for ancestor in owner["ancestors"]:
                        clip = ancestor["clip"]
                        if ancestor["overflowX"] in {"hidden", "clip", "auto", "scroll"} and (r["left"] < clip["left"] or r["right"] > clip["right"]):
                            errors.append(f"{text['id']}[{i}]: clipped X by {ancestor['id']}")
                        if ancestor["overflowY"] in {"hidden", "clip", "auto", "scroll"} and (r["top"] < clip["top"] or r["bottom"] > clip["bottom"]):
                            errors.append(f"{text['id']}[{i}]: clipped Y by {ancestor['id']}")
                    if not char.isspace():
                        glyphs.append((text["id"], r))
        for i, (tid, a) in enumerate(glyphs):
            for uid, b in glyphs[i+1:]:
                if tid != uid and min(a["right"], b["right"]) > max(a["left"], b["left"]) and min(a["bottom"], b["bottom"]) > max(a["top"], b["top"]):
                    errors.append(f"text overlap {tid}/{uid}")
                    break
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"missing/malformed geometry: {exc}")
    return list(dict.fromkeys(errors))


def capture_errors(manifest, output):
    errors = []
    cases = manifest.get("cases", [])
    if [c.get("id") for c in cases] != [c["id"] for c in fixed_cases()]:
        errors.append("missing/reordered fixed cases")
    for case in cases:
        for field in ("input", "stdout", "stderr"):
            if not case.get(field) or not Path(case[field]).is_file():
                errors.append(f"{case['id']}: missing {field}")
        if case.get("format") == "html":
            if [v.get("width") for v in case.get("views", [])] != list(WIDTHS):
                errors.append(f"{case['id']}: missing viewport")
            for view in case.get("views", []):
                for field in ("raw", "network"):
                    if not view.get(field) or not Path(view[field]).is_file():
                        errors.append(f"{case['id']}: missing {field}")
                if not view.get("images") or any(not Path(i["path"]).is_file() for i in view.get("images", [])):
                    errors.append(f"{case['id']}: missing image artifacts")
    return errors


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout.decode("utf-8", errors="strict")


def provenance():
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    dirty = git("status", "--porcelain=v1", "--untracked-files=all", "--", "wordfreq", "tools", "tests", "pyproject.toml")
    return dict(head=git("rev-parse", "HEAD").strip(), status=status,
                product_status=dirty, product_diff=git("diff", "HEAD", "--", "wordfreq", "tools", "tests", "pyproject.toml"))


class Observer:
    """Native context events plus pre-page browser target and pre-open page CDP.

    No network blocking: any external target/attempt is a violation. No blanket
    browser-background filtering; unclassified events fail closed.
    """
    def __init__(self, browser, context):
        self.events = []
        self.start = now()
        self.context = context
        self.browser_cdp = browser.new_browser_cdp_session()
        self.browser_cdp.on("Target.targetCreated", lambda e: self.add("target-created", e))
        self.browser_cdp.on("Target.targetInfoChanged", lambda e: self.add("target-changed", e))
        self.browser_cdp.send("Target.setDiscoverTargets", {"discover": True})
        for event in ("request", "requestfailed", "requestfinished"):
            context.on(event, lambda req, kind=event: self.request(kind, req))
        context.on("response", lambda response: self.add("response", dict(url=response.url, status=response.status)))
        context.on("page", self.page)
        self.pages = []
        self.errors = []

    def add(self, kind, data):
        self.events.append(dict(at=now(), kind=kind, data=data))

    def request(self, kind, request):
        try:
            frame = dict(url=request.frame.url, name=request.frame.name)
        except Exception as exc:
            frame = dict(unavailable=str(exc))
        self.add(kind, dict(url=request.url, method=request.method,
                            resourceType=request.resource_type, navigation=request.is_navigation_request(),
                            frame=frame, redirectedFrom=request.redirected_from.url if request.redirected_from else None,
                            failure=request.failure))

    def page(self, page):
        self.pages.append(page)
        self.add("page", dict(url=page.url))
        page.on("framenavigated", lambda frame: self.add("frame-navigated", dict(url=frame.url, name=frame.name)))
        page.on("popup", lambda popup: self.add("popup", dict(url=popup.url)))

    def attach(self, page):
        cdp = self.context.new_cdp_session(page)
        for event in ("Network.requestWillBeSent", "Network.loadingFailed", "Network.loadingFinished", "Network.responseReceived", "Page.frameRequestedNavigation", "Page.frameNavigated", "Page.windowOpen"):
            cdp.on(event, lambda data, kind=event: self.add(kind, data))
        cdp.send("Network.enable")
        cdp.send("Page.enable")
        self.add("page-cdp-ready", {})
        return cdp

    def finish(self):
        self.end = now()
        return dict(start=self.start, end=self.end, interval="capture-only", events=self.events,
                    coverage=dict(context=True, browserTargets=True, mainCDP=True), errors=self.errors)


def network_errors(record, expected_url):
    errors = []
    if not record.get("start") or not record.get("end") or not record.get("events"):
        return ["missing observation interval/events"]
    if not all(record.get("coverage", {}).get(k) for k in ("context", "browserTargets", "mainCDP")):
        errors.append("missing observer coverage")
    local_seen = False
    pre_open = True
    background = {}
    for event in record["events"]:
        data = event["data"]
        if event["kind"] == "page-cdp-ready":
            pre_open = False
        target = data.get("targetInfo", {})
        if (pre_open and event["kind"] == "target-created" and target.get("type") == "browser_ui"
                and not target.get("openerId") and target.get("canAccessOpener") is False
                and target.get("url") in {"chrome://omnibox-popup.top-chrome/", "chrome://omnibox-popup.top-chrome/omnibox_popup_aim.html"}):
            background[target["targetId"]] = target["url"]
        if (target.get("targetId") in background and target.get("type") == "browser_ui"
                and target.get("url") == background[target["targetId"]] and not target.get("openerId")):
            continue  # Exact pre-document browser-ui identity, not generic filtering.
        urls = [data.get("url"), data.get("request", {}).get("url"),
                data.get("frame", {}).get("url"), data.get("targetInfo", {}).get("url")]
        for url in filter(None, urls):
            if url == expected_url:
                local_seen = True
            elif url != "about:blank":
                errors.append(f"external/unexpected attempt {event['kind']}: {url}")
    if not local_seen:
        errors.append("initial local document load missing")
    if record.get("errors"):
        errors.append("observer callback errors")
    return list(dict.fromkeys(errors))


def dom_errors(raw, case):
    errors = []
    dom = raw["dom"]
    expected_rows = [[str(i), w, str(n)] for i, (w, n) in enumerate(case["pairs"], 1)]
    if dom["basename"] != case["basename"] or dom["total"] != str(case["total"]) or dom["rows"] != expected_rows or dom["headers"] != ["順位", "単語", "回数"]:
        errors.append("browser DOM differs from independent case oracle")
    elements = raw["elements"]
    if len([e for e in elements if e["tag"] == "td"]) != 3 * len(case["pairs"]):
        errors.append("missing cell geometry")
    for cls in ("filename-value", "total-value"):
        matches = [e for e in elements if e["className"] == cls]
        if len(matches) != 1:
            errors.append(f"missing metadata geometry {cls}")
    for text in raw["texts"]:
        el = next(e for e in elements if e["id"] == text["owner"])
        if el["className"] in {"filename-value", "word"} and (el["style"]["whiteSpace"] != "break-spaces" or el["style"]["tabSize"] != "4"):
            errors.append("whitespace style differs")
        if case["id"].startswith("long"):
            # Numeric rows may not split digits in the required fixture.
            if el["className"] in {"rank", "count", "total-value"} and len({r["top"] for c in text["characters"] for r in c["rects"]}) != 1:
                errors.append("numeric fixture split")
            for letter, length in (("n", 176), ("w", 256)):
                start = text["text"].find(letter * length)
                if start >= 0:
                    tops = {r["top"] for c in text["characters"][start:start+length] for r in c["rects"]}
                    if len(tops) < 2:
                        errors.append(f"long {letter} run did not wrap")
    return errors


def collect_view(browser, case, width, output):
    folder = output / case["id"] / str(width)
    folder.mkdir(parents=True)
    context = browser.new_context(viewport=dict(width=width, height=900), device_scale_factor=1)
    observer = Observer(browser, context)
    page = context.new_page()
    cdp = observer.attach(page)
    errors = []
    view = dict(width=width, images=[], raw=str(folder / "raw.json"), network=str(folder / "network.json"),
                reviewed_images=[], verdict="pending-review")
    try:
        url = Path(case["stdout"]).as_uri()
        page.goto(url, wait_until="load", timeout=15000)
        page.evaluate("document.fonts.ready")
        raw = page.evaluate((ROOT / "tools/wordfreq_html_geometry.js").read_text(encoding="utf-8"))
        cdp.send("DOM.enable")
        cdp.send("CSS.enable")
        doc = cdp.send("DOM.getDocument")
        fonts = []
        for el in raw["elements"]:
            if not el["text"]:
                continue
            node = cdp.send("DOM.querySelector", dict(nodeId=doc["root"]["nodeId"], selector=el["id"]))
            used = cdp.send("CSS.getPlatformFontsForNode", dict(nodeId=node["nodeId"]))
            fonts.append(dict(element=el["id"], **used))
        raw["platformFonts"] = fonts
        save_json(folder / "raw.json", raw)
        errors += geometry_errors(raw) + dom_errors(raw, case)
        if not fonts or not any(f["fonts"] for f in fonts):
            errors.append("no actual platform font evidence")
        height = raw["document"]["scrollHeight"]
        full = folder / "full.png"
        page.screenshot(path=str(full), full_page=True)
        view["images"].append(dict(path=str(full), type="full", x=0, y=0, width=width, height=height))
        if height > 900:
            y = 0
            while y < height:
                tile_height = min(900, height-y)
                tile = folder / f"tile-{y}.png"
                page.screenshot(path=str(tile), clip=dict(x=0, y=y, width=width, height=tile_height))
                view["images"].append(dict(path=str(tile), type="tile", x=0, y=y, width=width, height=tile_height))
                y += 800
        view["browser"] = dict(version=browser.version, os=platform.platform(), viewport=raw["viewport"])
    finally:
        # Pump native event delivery through the end of capture, then persist.
        page.wait_for_timeout(100)
        net = observer.finish()
        save_json(folder / "network.json", net)
        observer.browser_cdp.detach()
        context.close()
    errors += network_errors(net, url)
    view["errors"] = errors
    save_json(folder / "derived.json", view)
    return view


def capture(args):
    from playwright.sync_api import sync_playwright

    output = args.output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError("output directory must be fresh")
    output.mkdir(parents=True, exist_ok=True)
    before = provenance()
    save_json(output / "provenance.json", before)
    if before["product_status"]:
        raise ValueError("dirty/untracked product/test/tool files; commit before attributable capture")
    manifest = dict(role=args.role, head=before["head"], verdict="unverified", cases=[], errors=[],
                    started=now(), mode="capture", reviewed_images=[], independent_acceptance=False)
    save_json(output / "manifest.json", manifest)
    try:
        manifest["cases"] = generate_cases(output)
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=args.browser, headless=True)
            manifest["browser"] = dict(executable=args.browser, version=browser.version, os=platform.platform())
            try:
                for case in manifest["cases"]:
                    if case["format"] == "html":
                        for width in WIDTHS:
                            view = collect_view(browser, case, width, output)
                            case["views"].append(view)
                            manifest["errors"] += [f"{case['id']}/{width}: {e}" for e in view["errors"]]
                            save_json(output / "manifest.json", manifest)
            finally:
                browser.close()
        manifest["errors"] += capture_errors(manifest, output)
        after = provenance()
        manifest["end_provenance"] = after
        if after["head"] != before["head"] or after["product_status"]:
            manifest["errors"].append("head/product changed during capture")
        manifest["verdict"] = "failed" if manifest["errors"] else "pending-review"
    except Exception as exc:
        manifest["errors"].append(f"execution/coverage unverified: {type(exc).__name__}: {exc}")
    manifest["ended"] = now()
    save_json(output / "manifest.json", manifest)
    print(json.dumps(dict(manifest=str(output / "manifest.json"), verdict=manifest["verdict"], errors=manifest["errors"]), ensure_ascii=False))
    return 1 if manifest["errors"] else 0


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--role", choices=("builder", "quality"), required=True)
    result.add_argument("--output-dir", type=Path, required=True)
    result.add_argument("--mode", choices=("capture", "review-session", "finalize"), default="capture")
    result.add_argument("--browser", default="/usr/bin/chromium-browser")
    return result


def main():
    args = parser().parse_args()
    if args.mode != "capture":
        raise SystemExit("review-session/finalize are not implemented in 03-03; no acceptance emitted")
    raise SystemExit(capture(args))


if __name__ == "__main__":
    main()
