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
import tempfile
import threading
import time
from contextlib import contextmanager

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
                    own = dict(id=owner["id"], overflowX=owner["style"].get("overflowX", "visible"),
                               overflowY=owner["style"].get("overflowY", "visible"),
                               clip=owner.get("clip", owner["rect"]))
                    for ancestor in [own, *owner["ancestors"]]:
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


def png_size(path):
    """Read actual PNG IHDR pixel dimensions without browser/image dependencies."""
    with Path(path).open("rb") as stream:
        header = stream.read(24)
    if len(header) != 24 or header[:16] != b"\x89PNG\r\n\x1a\n\0\0\0\rIHDR":
        raise ValueError("missing PNG IHDR")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if not width or not height:
        raise ValueError("empty PNG dimensions")
    return width, height


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
                for image in view.get("images", []):
                    try:
                        actual = png_size(image["path"])
                        if actual != (image["width"], image["height"]):
                            errors.append(f"{case['id']}: image dimensions {actual} differ from record {image}")
                    except (OSError, ValueError, KeyError, TypeError) as exc:
                        errors.append(f"{case['id']}: image dimensions unverified: {exc}")
    return errors


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout.decode("utf-8", errors="strict")


def provenance():
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    dirty = git("status", "--porcelain=v1", "--untracked-files=all", "--", "wordfreq", "tools", "tests", "pyproject.toml")
    untracked = []
    for name in filter(None, git("ls-files", "--others", "--exclude-standard", "-z", "--", "wordfreq", "tools", "tests", "pyproject.toml").split("\0")):
        content = (ROOT / name).read_bytes()
        untracked.append(dict(path=name, sha256=hashlib.sha256(content).hexdigest(),
                              content_utf8=content.decode("utf-8", errors="backslashreplace")))
    return dict(head=git("rev-parse", "HEAD").strip(), status=status, untracked_product=untracked,
                product_status=dirty, product_diff=git("diff", "HEAD", "--", "wordfreq", "tools", "tests", "pyproject.toml"))


class ProtocolMonitor:
    """Public flattened CDP transport, independent of Playwright's pipe session.

    Subscribe before pages exist. Pause new targets, enable Network/Page, then
    resume; the first popup request has requestId/initiator/frame/target metadata.
    """
    def __init__(self, endpoint):
        from websockets.sync.client import connect

        self.socket = connect(endpoint, proxy=None, max_size=None)
        self.events, self.errors, self.targets = [], [], {}
        self.ids, self.pending = 0, {}
        self.lock = threading.RLock()
        self.running = True
        self.thread = threading.Thread(target=self.receive, daemon=True)
        self.thread.start()
        for method, params in (("Target.setDiscoverTargets", dict(discover=True)),
                               ("Target.setAutoAttach", dict(autoAttach=True, waitForDebuggerOnStart=True, flatten=True))):
            ack = threading.Event()
            mid = self.send(method, params, ack=ack)
            if not ack.wait(5) or self.errors:
                raise RuntimeError(f"CDP setup unverified {method}/{mid}: {self.errors}")

    def send(self, method, params=None, session=None, ack=None):
        with self.lock:
            self.ids += 1
            mid = self.ids
            message = dict(id=mid, method=method, params=params or {})
            if session:
                message["sessionId"] = session
            if ack:
                self.pending[mid] = ack
            self.socket.send(json.dumps(message))
            return mid

    def receive(self):
        try:
            while self.running:
                message = json.loads(self.socket.recv())
                with self.lock:
                    if message.get("error"):
                        self.errors.append(message)
                    if message.get("id") in self.pending:
                        self.pending.pop(message["id"]).set()
                    method = message.get("method", "")
                    data = message.get("params", {})
                    sid = message.get("sessionId")
                    if method in {"Target.targetCreated", "Target.targetInfoChanged"}:
                        target = data["targetInfo"]
                        self.targets[target["targetId"]] = target
                    if method == "Target.attachedToTarget":
                        self.targets[data["sessionId"]] = data["targetInfo"]
                        self.events.append(dict(at=now(), kind="target-attached", data=data))
                        child = data["sessionId"]
                        if data["targetInfo"]["type"] in {"page", "iframe"}:
                            self.send("Network.enable", session=child)
                            self.send("Page.enable", session=child)
                        self.send("Runtime.runIfWaitingForDebugger", session=child)
                    elif method.startswith(("Network.", "Page.")):
                        target = self.targets.get(sid, {})
                        self.events.append(dict(at=now(), kind=method, data=dict(data, sessionId=sid,
                            targetId=target.get("targetId"), source="browser-autoattach")))
        except Exception as exc:
            if self.running:
                self.errors.append(f"CDP receive stopped: {exc}")

    def close(self):
        self.running = False
        self.socket.close()
        self.thread.join(timeout=5)


@contextmanager
def instrumented_browser(pw, executable):
    # Chromium's Unix socket path limit needs a short TMPDIR spelling. An operator
    # may provide a relative symlink into managed scratch; never substitute /tmp.
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"), prefix="wf-") as profile:
        logs = Path(profile) / "chromium.log"
        with logs.open("wb") as log:
            command = [executable, "--headless", "--no-sandbox", "--disable-dev-shm-usage",
                       "--disable-background-networking", "--disable-component-update", "--disable-extensions",
                       "--disable-component-extensions-with-background-pages", "--disable-default-apps", "--no-first-run",
                       "--no-default-browser-check", "--disable-popup-blocking", "--no-startup-window",
                       "--remote-debugging-port=0", "--remote-debugging-address=127.0.0.1",
                       f"--user-data-dir={profile}"]
            process = subprocess.Popen(command, stdout=log, stderr=log)
            monitor = None
            try:
                port_file = Path(profile) / "DevToolsActivePort"
                deadline = time.monotonic() + 10
                while not port_file.is_file() and process.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.05)  # Bounded browser startup, not an external workflow poll.
                if not port_file.is_file():
                    raise RuntimeError(f"Chromium debugger unavailable: {logs.read_text(errors='replace')}")
                port, path = port_file.read_text().splitlines()[:2]
                endpoint = f"ws://127.0.0.1:{port}{path}"
                monitor = ProtocolMonitor(endpoint)
                browser = pw.chromium.connect_over_cdp(endpoint)
                browser.protocol_monitor = monitor
                browser.launch_record = dict(argv=command, tmpdir=os.environ.get("TMPDIR"),
                                             transport="loopback flattened CDP", websocket_package="websockets")
                try:
                    yield browser
                finally:
                    browser.close()
            finally:
                if monitor:
                    monitor.close()
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)


class Observer:
    """Native context events plus pre-page browser target and pre-open page CDP.

    No network blocking: any external target/attempt is a violation. No blanket
    browser-background filtering; unclassified events fail closed.
    """
    def __init__(self, browser, context):
        self.events = []
        self.start = now()
        self.context = context
        self.pages, self.errors = [], []
        self.monitor = browser.protocol_monitor
        with self.monitor.lock:
            self.monitor_start = len(self.monitor.events)
        self.browser_cdp = browser.new_browser_cdp_session()
        self.browser_cdp.on("Target.targetCreated", lambda e: self.add("target-created", e))
        self.browser_cdp.on("Target.targetInfoChanged", lambda e: self.add("target-changed", e))
        self.browser_cdp.send("Target.setDiscoverTargets", {"discover": True})
        for event in ("request", "requestfailed", "requestfinished"):
            context.on(event, lambda req, kind=event: self.request(kind, req))
        context.on("response", lambda response: self.add("response", dict(url=response.url, status=response.status)))
        context.on("page", self.page)
        self.add("browser-autoattach-ready", {})

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
        with self.monitor.lock:
            events = sorted(self.events + self.monitor.events[self.monitor_start:], key=lambda e: e["at"])
            errors = self.errors + list(self.monitor.errors)
        return dict(start=self.start, end=self.end, interval="capture-only", events=events,
                    coverage=dict(context=True, browserTargets=True, mainCDP=True, flattenedAutoAttach=True), errors=errors)


def network_errors(record, expected_url):
    errors = []
    if not record.get("start") or not record.get("end") or not record.get("events"):
        return ["missing observation interval/events"]
    if not all(record.get("coverage", {}).get(k) for k in ("context", "browserTargets", "mainCDP", "flattenedAutoAttach")):
        errors.append("missing observer coverage")
    local_seen = False
    pre_open = True
    background = {}
    for event in record["events"]:
        data = event["data"]
        if event["kind"] == "page-cdp-ready":
            pre_open = False
        target = data.get("targetInfo", {})
        if (pre_open and event["kind"] in {"target-created", "target-attached"} and target.get("type") == "browser_ui"
                and not target.get("openerId") and target.get("canAccessOpener") is False
                and target.get("url") in {"chrome://omnibox-popup.top-chrome/", "chrome://omnibox-popup.top-chrome/omnibox_popup_aim.html"}):
            background[target["targetId"]] = target["url"]
        if (target.get("targetId") in background and target.get("type") == "browser_ui"
                and target.get("url") == background[target["targetId"]] and not target.get("openerId")):
            continue  # Exact pre-document browser-ui identity, not generic filtering.
        if not (event["kind"].startswith(("Network.", "Page.")) or event["kind"] in {"browser-autoattach-ready", "page-cdp-ready", "target-created", "target-changed", "target-attached", "request", "requestfailed", "requestfinished", "response", "page", "frame-navigated", "popup"}):
            errors.append(f"unknown attribution/event {event['kind']}")
        if event["kind"] in {"request", "requestfailed", "requestfinished", "response", "frame-navigated"} and not data.get("url"):
            errors.append(f"missing URL attribution {event['kind']}")
        if event["kind"] == "request" and pre_open:
            errors.append("request before page observer ready")
        urls = [data.get("url"), data.get("request", {}).get("url"),
                data.get("frame", {}).get("url"), data.get("targetInfo", {}).get("url")]
        for url in filter(None, urls):
            if url == expected_url:
                local_seen = True
            elif url != "about:blank":
                errors.append(f"external/unexpected attempt {event['kind']}: {url}")
    if not local_seen or not any(e["kind"] == "request" and e["data"].get("url") == expected_url for e in record["events"]):
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
        image_width, image_height = png_size(full)
        view["images"].append(dict(path=str(full), type="full", x=0, y=0,
                                   width=image_width, height=image_height))
        if (image_width, image_height) != (raw["document"]["clientWidth"], height):
            errors.append("full image dimensions differ from document capture bounds")
        if height > 900:
            y = 0
            while y < height:
                tile_height = min(900, height-y)
                tile = folder / f"tile-{y}.png"
                clip = dict(x=0, y=y, width=image_width, height=tile_height)
                page.screenshot(path=str(tile), full_page=True, clip=clip)
                tile_width, actual_height = png_size(tile)
                view["images"].append(dict(path=str(tile), type="tile", x=0, y=y,
                                           width=tile_width, height=actual_height, requested_clip=clip))
                if (tile_width, actual_height) != (image_width, tile_height):
                    errors.append(f"tile {y}: image dimensions differ from requested clip")
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
        from playwright.sync_api import sync_playwright

        manifest["cases"] = generate_cases(output)
        with sync_playwright() as pw, instrumented_browser(pw, args.browser) as browser:
            manifest["browser"] = dict(executable=args.browser, version=browser.version, os=platform.platform(), launch=browser.launch_record)
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


CANARIES = ("clean", "failed-resource", "document-navigation", "early-popup", "redirect")
CANARY_URL = "http://wordfreq-canary.invalid:9/attempt"


def canary_errors(report):
    errors = []
    if [c.get("id") for c in report.get("cases", [])] != list(CANARIES):
        return ["missing canary coverage"]
    for case in report["cases"]:
        net = case.get("observation", {})
        failures = network_errors(net, case["url"])
        if case["id"] == "clean":
            if failures:
                errors.append(f"clean control failed: {failures}")
            continue
        structural = [error for error in failures if not error.startswith("external/unexpected attempt ")]
        if structural:
            errors.append(f"{case['id']}: coverage/attribution unverified: {structural}")
        events = net.get("events", [])
        external_requests = [e for e in events if e["kind"] == "Network.requestWillBeSent"
                             and e["data"].get("request", {}).get("url", "").startswith(CANARY_URL)
                             and e["data"].get("source") == "browser-autoattach"
                             and e["data"].get("requestId") and e["data"].get("initiator")
                             and e["data"].get("targetId") and e["data"].get("frameId")]
        request_ids = {e["data"]["requestId"] for e in external_requests}
        failed = [e for e in events if (e["kind"] == "Network.loadingFailed" and e["data"].get("requestId") in request_ids)
                  or (e["kind"] == "requestfailed" and e["data"].get("url", "").startswith(CANARY_URL))]
        if not failures or not external_requests or not failed:
            errors.append(f"{case['id']}: real attributed request/failure not observed and rejected")
        if case["id"] == "early-popup":
            targets = [e["data"]["targetInfo"]["targetId"] for e in events if e["kind"] == "target-attached" and e["data"]["targetInfo"].get("openerId") and e["data"].get("waitingForDebugger") is True]
            if not any(e["data"]["targetId"] in targets for e in external_requests):
                errors.append("early-popup: paused new-target request evidence missing")
        if case["id"] in {"redirect", "document-navigation"} and not any(e["kind"] == "Page.frameRequestedNavigation" and e["data"].get("url", "").startswith(CANARY_URL) for e in events):
            errors.append(f"{case['id']}: attempted navigation absent")
    return errors


def self_test_network(args):
    from playwright.sync_api import sync_playwright

    output = args.output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError("canary output directory must be fresh")
    output.mkdir(parents=True, exist_ok=True)
    pages = {
        "clean": "<!doctype html><title>clean control</title><p>local only</p>",
        "failed-resource": f'<!doctype html><img src="{CANARY_URL}?resource">',
        "document-navigation": f'<!doctype html><script>location.href="{CANARY_URL}?navigation"</script>',
        "early-popup": f'<!doctype html><script>window.open("{CANARY_URL}?popup")</script>',
        "redirect": f'<!doctype html><meta http-equiv="refresh" content="0;url={CANARY_URL}?redirect">',
    }
    report = dict(role=args.role, started=now(), provenance=provenance(), cases=[], errors=[], verdict="unverified")
    try:
        with sync_playwright() as pw, instrumented_browser(pw, args.browser) as browser:
            report["browser"] = dict(executable=args.browser, version=browser.version, os=platform.platform(), tmpdir=os.environ.get("TMPDIR"), launch=browser.launch_record)
            try:
                for name in CANARIES:
                    source = output / f"{name}.html"
                    source.write_text(pages[name], encoding="utf-8")
                    context = browser.new_context()
                    observer = Observer(browser, context)
                    page = context.new_page()
                    observer.attach(page)
                    case = dict(id=name, url=source.as_uri(), command_error=None)
                    try:
                        page.goto(case["url"], wait_until="load", timeout=5000)
                    except Exception as exc:
                        case["command_error"] = str(exc)  # NOT evidence that the canary worked.
                    page.wait_for_timeout(700)
                    case["observation"] = observer.finish()
                    case["detected"] = network_errors(case["observation"], case["url"])
                    save_json(output / f"{name}.json", case)
                    report["cases"].append(case)
                    observer.browser_cdp.detach()
                    context.close()
            finally:
                browser.close()
        report["errors"] = canary_errors(report)
        report["verdict"] = "passed" if not report["errors"] else "unverified"
    except Exception as exc:
        report["errors"].append(f"observer environment/coverage: {exc}")
    report["ended"] = now()
    save_json(output / "canaries.json", report)
    print(json.dumps(dict(report=str(output / "canaries.json"), verdict=report["verdict"], errors=report["errors"]), ensure_ascii=False))
    return 1 if report["errors"] else 0


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--role", choices=("builder", "quality"), required=True)
    result.add_argument("--output-dir", type=Path, required=True)
    result.add_argument("--mode", choices=("capture", "review-session", "finalize"), default="capture")
    result.add_argument("--browser", default="/usr/bin/chromium-browser")
    result.add_argument("--self-test-network", action="store_true")
    return result


def main():
    args = parser().parse_args()
    if args.self_test_network:
        raise SystemExit(self_test_network(args))
    if args.mode != "capture":
        raise SystemExit("review-session/finalize are not implemented in 03-03; no acceptance emitted")
    raise SystemExit(capture(args))


if __name__ == "__main__":
    main()
