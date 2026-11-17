"""Real-file CLI/browser evidence. Capture never claims visual acceptance.

Browser dependencies are imported only by explicit browser operations.
"""
import argparse
import base64
import copy
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
    pending = path.with_suffix(path.suffix + ".part")
    pending.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pending.replace(path)


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
        layout_width = min(viewport["width"], raw["document"]["clientWidth"])
        if raw["document"]["scrollWidth"] > layout_width:
            errors.append("document horizontal overflow")
        elements = {e["id"]: e for e in raw["elements"]}
        if not elements or not raw["texts"]:
            return errors + ["missing element/text measurements"]
        by_owner = {}
        for text in raw["texts"]:
            by_owner.setdefault(text["owner"], []).append(text)
        for element in elements.values():
            if element.get("tag") in {"td", "th", "h1", "caption"} or element.get("className") in {"filename-value", "total-value", "label", "empty-message"}:
                measured = by_owner.get(element["id"], [])
                if (not measured or not any(t["characters"] for t in measured)
                        or "".join(t["text"] for t in measured) != element["text"]):
                    errors.append(f"{element['id']}: text not fully measured")
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
                if not char.isspace() and not any(r["width"] > 0 and r["height"] > 0 for r in item["rects"]):
                    errors.append(f"{text['id']}[{i}]: no visible ink")
                for r in item["rects"]:
                    if r["width"] <= 0 or r["height"] <= 0:
                        continue  # Raw retains zero-area rectangles; no visible ink.
                    if r["left"] < 0 or r["right"] > layout_width:
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
    paths = ("wordfreq", "tools", "tests", "pyproject.toml",
             "conftest.py", "pytest.ini", "tox.ini", "setup.cfg")
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    dirty = git("status", "--porcelain=v1", "--untracked-files=all", "--", *paths)
    untracked = []
    for name in filter(None, git("ls-files", "--others", "--exclude-standard", "-z", "--", *paths).split("\0")):
        content = (ROOT / name).read_bytes()
        untracked.append(dict(path=name, sha256=hashlib.sha256(content).hexdigest(),
                              content_utf8=content.decode("utf-8", errors="backslashreplace")))
    return dict(head=git("rev-parse", "HEAD").strip(), status=status, untracked_product=untracked,
                product_status=dirty, product_diff=git("diff", "HEAD", "--", *paths))


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


def context_events(events, context_id, targets):
    """Exclude only proved other contexts; retain unknowns and explicit grounds."""
    kept, excluded = [], []
    by_id = {t.get("targetId"): t for t in targets.values()}
    for event in events:
        data = event["data"]
        target = data.get("targetInfo") or by_id.get(data.get("targetId"), {})
        other = target.get("browserContextId")
        if other and other != context_id:
            excluded.append(dict(event=event, target=target, reason="different browserContextId"))
        else:
            kept.append(event)
    return kept, excluded


class Observer:
    """Native context events plus pre-page browser target and pre-open page CDP.

    No network blocking: any external target/attempt is a violation. No blanket
    browser-background filtering; unclassified events fail closed.
    """
    def __init__(self, browser, context):
        self.events = []
        self.context_id = None
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
            excluded = []
            if getattr(self, "context_id", None):
                events, excluded = context_events(events, self.context_id, self.monitor.targets)
        return dict(start=self.start, end=self.end, interval="capture-only", events=events,
                    coverage=observer_coverage(events), errors=errors, excluded_other_contexts=excluded)


def observer_coverage(events, expected_url=None):
    """Infer readiness and same-document channel evidence, not declared flags."""
    kinds = [e["kind"] for e in events]
    browser_ready = kinds.index("browser-autoattach-ready") if "browser-autoattach-ready" in kinds else -1
    page_ready = kinds.index("page-cdp-ready") if "page-cdp-ready" in kinds else -1
    requests = [i for i, e in enumerate(events) if e["kind"] in {"request", "Network.requestWillBeSent"}]
    ordered = 0 <= browser_ready < page_ready and bool(requests) and page_ready < min(requests)
    if expected_url is None:
        expected_url = next((e["data"].get("url") for e in events if e["kind"] == "request"), None)
    attached = {e["data"]["targetInfo"].get("targetId") for e in events
                if e["kind"] == "target-attached" and e["data"].get("targetInfo", {}).get("type") == "page"
                and e["data"].get("waitingForDebugger") is True}
    root_requests = [e["data"] for e in events if e["kind"] == "Network.requestWillBeSent"
                     and e["data"].get("source") == "browser-autoattach"
                     and e["data"].get("request", {}).get("url") == expected_url
                     and all(e["data"].get(k) for k in ("requestId", "targetId", "frameId", "initiator"))]
    return dict(context=ordered and any(e["kind"] == "request" and e["data"].get("url") == expected_url for e in events),
                browserTargets=ordered and any(r["targetId"] in attached for r in root_requests),
                mainCDP=ordered and any(e["kind"] == "Network.requestWillBeSent" and
                    not e["data"].get("source") and e["data"].get("request", {}).get("url") == expected_url for e in events),
                flattenedAutoAttach=ordered and bool(root_requests))


def network_errors(record, expected_url):
    errors = []
    if not record.get("start") or not record.get("end") or not record.get("events"):
        return ["missing observation interval/events"]
    if not all(observer_coverage(record["events"], expected_url).values()) or not all(record.get("coverage", {}).get(k) for k in ("context", "browserTargets", "mainCDP", "flattenedAutoAttach")):
        errors.append("missing observer coverage")
    local_seen = False
    pre_open = True
    background = {}
    # IDs are channel-local: another CDP session/target is not proof of a start.
    def identity(data):
        return tuple(data.get(k) for k in ("source", "sessionId", "targetId", "requestId"))

    started = {identity(e["data"]) for e in record["events"]
               if e["kind"] == "Network.requestWillBeSent" and e["data"].get("requestId")}
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
        if event["kind"].startswith("Network.") and data.get("requestId") and identity(data) not in started:
            errors.append(f"unattributed request {event['kind']}: {identity(data)}")
        urls = [data.get("url"), data.get("request", {}).get("url"),
                data.get("response", {}).get("url"), data.get("redirectResponse", {}).get("url"),
                data.get("documentURL"), data.get("frame", {}).get("url"), data.get("targetInfo", {}).get("url")]
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


def collect_view(browser, case, width, output, live=None):
    folder = output / case["id"] / str(width)
    folder.mkdir(parents=True)
    context = browser.new_context(viewport=dict(width=width, height=900), device_scale_factor=1)
    observer = Observer(browser, context)
    page = context.new_page()
    cdp = observer.attach(page)
    if live is not None:
        observer.context_id = cdp.send("Target.getTargetInfo")["targetInfo"]["browserContextId"]
    errors = []
    view: dict = dict(width=width, images=[], raw=str(folder / "raw.json"), network=str(folder / "network.json"),
                reviewed_images=[], verdict="pending-review")
    url = Path(case["stdout"]).as_uri()
    try:
        # Enable inspection domains on about:blank, before the product exists.
        # CSS.enable on a loaded file causes a DevTools re-fetch without a
        # requestWillBeSent event in Chromium. Never whitelist that orphan.
        cdp.send("DOM.enable")
        cdp.send("CSS.enable")
        page.goto(url, wait_until="load", timeout=15000)
        page.evaluate("document.fonts.ready")
        raw = page.evaluate((ROOT / "tools/wordfreq_html_geometry.js").read_text(encoding="utf-8"))
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
        # CDP captures beyond the viewport without Playwright's temporary resize,
        # which can remove the scrollbar and reflow the measured document.
        full_clip = dict(x=0, y=0, width=raw["document"]["clientWidth"], height=height, scale=1)
        full.write_bytes(base64.b64decode(cdp.send("Page.captureScreenshot", dict(
            format="png", captureBeyondViewport=True, clip=full_clip))["data"], validate=True))
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
                tile.write_bytes(base64.b64decode(cdp.send("Page.captureScreenshot", dict(
                    format="png", captureBeyondViewport=True, clip=dict(clip, scale=1)))["data"], validate=True))
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
        if live is None:
            observer.browser_cdp.detach()
            context.close()
        else:
            net["interval"] = "live-review"
            save_json(folder / "network.json", net)
            live.append(dict(page=page, context=context, observer=observer, view=view, url=url))
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
        failed = [e for e in events if e["kind"] == "Network.loadingFailed"
                  and e["data"].get("requestId") in request_ids]
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


REVIEW_FIELDS = ("actor", "image", "sha256", "viewed_at", "scale", "extent",
                 "raw", "raw_sha256", "judgment", "notes")
SCOPE_BASE = "5a7659b949dc118b59cea5ef3eb40bcd94337d8d"
APPROVED_PRODUCT = "ed7e6cc9d608bc40a82da76e85ca6e57a0808b54"
ACTORS = {"builder": "argonauts-uat-builder", "quality": "argonauts-uat-quality"}
SCOPE_FILES = {"README.md", "CONCEPTS.md", "docs/wordfreq-html-verification.md",
    "wordfreq/__main__.py", "wordfreq/aggregator.py", "wordfreq/formatters.py",
    "tests/test_aggregator.py", "tests/test_cli.py", "tests/test_formatters.py",
    "tests/test_sources.py", "tests/test_html_verifier.py", "tests/test_html_finalization.py",
    "tools/verify_wordfreq_html.py", "tools/wordfreq_html_geometry.js",
    "openspec/changes/r-50053edc-wordfreq-html/tasks.md"}


def scope_path_errors(paths):
    allowed_planning = (".planning/argonauts/", ".planning/intel/", ".planning/research/",
                        ".planning/phases/03-wordfreq-html-output/")
    allowed_state = {".planning/STATE.md", ".planning/ROADMAP.md", ".planning/REQUIREMENTS.md",
                     ".planning/INGEST-CONFLICTS.md", ".planning/state.json"}
    return [f"unauthorized scope: {p}" for p in paths
            if p not in SCOPE_FILES | allowed_state and not p.startswith(allowed_planning)]


def scope_report():
    target = git("rev-parse", "HEAD").strip()
    working = provenance()
    paths = list(filter(None, git("diff", "--name-only", "-z", SCOPE_BASE, target).split("\0")))
    # Freeze the reviewed product snapshot:03-04 may only change verification/docs.
    unexpected_product = git("diff", "--name-only", APPROVED_PRODUCT, target, "--", "wordfreq")
    return dict(base=SCOPE_BASE, target=target, paths=paths,
                product_diff=git("diff", SCOPE_BASE, target, "--", "wordfreq"),
                product_status=working["product_status"], untracked_product=working["untracked_product"],
                intentional_change="approved lexical ties -> normalized first occurrence; HTML output",
                errors=scope_path_errors(paths) + (["product differs from approved03-02 snapshot"] if unexpected_product else [])
                + (["dirty/untracked product/test/tool code"] if working["product_status"] or working["untracked_product"] else []))


def session_actor(role, actor, output):
    if actor is None:
        actor = os.environ.get("HERMES_PROFILE")
    if actor != ACTORS.get(role) or os.environ.get("HERMES_PROFILE") != actor:
        raise ValueError("actor/role must match the actual Hermes profile; role flag is not independence")
    if role not in output.parts or ({"builder", "quality"} - {role}).intersection(output.parts):
        raise ValueError("output root must be separate and contain the actual role")
    return actor


def review_errors(entry, image, raw, raw_hash, actor, start, end):
    """Validate an external attestation, never invent one from image existence."""
    errors = []
    if any(field not in entry for field in REVIEW_FIELDS):
        return ["missing review fields"]
    if (entry["actor"] != actor or entry["image"] != image["path"]
            or entry["sha256"] != image["sha256"] or entry["raw"] != raw
            or entry["raw_sha256"] != raw_hash):
        errors.append("review identity/hash/raw mismatch")
    try:
        at, lower, upper = map(datetime.fromisoformat, (entry["viewed_at"], start, end))
        if not lower <= at <= upper:
            errors.append("review outside live interval")
        if type(entry["scale"]) not in (int, float) or entry["scale"] < 1:
            errors.append("review not at readable scale")
    except (TypeError, ValueError):
        errors.append("invalid review time/scale")
    if entry["extent"] != [0, 0, image["width"], image["height"]]:
        errors.append("review incomplete extent")
    if entry["judgment"] != "readable" or not isinstance(entry["notes"], str) or not entry["notes"].strip():
        errors.append("missing concrete readable judgment")
    return errors


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ledger_errors(manifest, ledger, end):
    errors = []
    try:
        for key in ("session", "head", "actor", "root"):
            if not manifest.get(key) or ledger.get(key) != manifest[key]:
                errors.append(f"ledger {key} mismatch")
        images = [(v, i) for c in manifest["cases"] for v in c["views"] for i in v["images"]]
        reviews = ledger["reviews"]
        expected = [i["path"] for _, i in images]
        actual = [r["image"] for r in reviews]
        if not expected or len(set(expected)) != len(expected) or sorted(actual) != sorted(expected):
            errors.append("missing/duplicate/unviewed image identity")
        for view, image in images:
            matching = [r for r in reviews if r["image"] == image["path"]]
            if len(matching) == 1:
                errors += review_errors(matching[0], image, view["raw"], view["raw_sha256"],
                                        manifest["actor"], manifest["ready_at"], end)
        acs = ledger["ac_reviews"]
        names = [f"AC{i}" for i in range(1, 7)]
        if sorted(a["ac"] for a in acs) != names or sorted(manifest["ac_index"]) != names:
            errors.append("missing/duplicate AC coverage")
        for ac in acs:
            if (ac["judgment"] != "accepted" or not isinstance(ac["notes"], str) or not ac["notes"].strip()
                    or not ac["evidence"] or ac["evidence"] != manifest["ac_index"][ac["ac"]]):
                errors.append(f"incomplete AC evidence/judgment: {ac['ac']}")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"missing/malformed ledger: {exc}")
    return errors


def image_coverage_errors(view, raw):
    images = view["images"]
    full = [i for i in images if i["type"] == "full"]
    width, height = raw["document"]["clientWidth"], raw["document"]["scrollHeight"]
    if len(full) != 1 or (full[0]["x"], full[0]["y"], full[0]["width"], full[0]["height"]) != (0, 0, width, height):
        return ["missing/invalid full image coverage"]
    if height > 900:
        tiles = sorted((i for i in images if i["type"] == "tile"), key=lambda i: i["y"])
        end = 0
        for tile in tiles:
            if tile["x"] != 0 or tile["width"] != width or tile["y"] > end or tile["height"] > 900:
                return ["tile coverage hole/width/scale"]
            end = max(end, tile["y"] + tile["height"])
        if end != height:
            return ["tile coverage incomplete"]
    return []


def view_identity_errors(view):
    errors = []
    if digest(view["raw"]) != view["raw_sha256"]:
        errors.append("raw identity differs from bytes")
    for image in view["images"]:
        if digest(image["path"]) != image["sha256"]:
            errors.append("image identity differs from bytes")
    return errors


def evidence_errors(manifest, ledger, output, end, require_end=True):
    """Re-read immutable originals plus current live network snapshots fail closed."""
    errors = []
    try:
        if (manifest["mode"] != "review-session" or manifest.get("ended") or manifest.get("synthetic")
                or manifest["verdict"] != "pending-review" or manifest["errors"]):
            errors.append("not an active real review session")
        if manifest["root"] != str(output.resolve()):
            errors.append("wrong evidence root")
        session_actor(manifest["role"], manifest["actor"], output.resolve())
        current = provenance()
        if current["head"] != manifest["head"] or current["product_status"] or current["untracked_product"]:
            errors.append("head/product dirty or changed")
        scope = scope_report()
        errors += scope["errors"]
        if scope != manifest["scope"]:
            errors.append("scope/head changed")
        required = []
        for case in manifest["cases"]:
            required += [case[k] for k in ("input", "stdout", "stderr")]
            required.append(str(output / case["id"] / "cli.json"))
            for view in case["views"]:
                required.append(view["raw"])
                required += [i["path"] for i in view["images"]]
        required += [str(output / name) for name in ("provenance.json", "scope.json", "suite.json",
                     "suite.xml", "suite.stdout", "suite.stderr", "canaries/canaries.json")]
        if not required or not all(p in manifest["artifacts"] for p in required):
            errors.append("missing artifact identities")
        for path, hash_value in manifest["artifacts"].items():
            if not Path(path).resolve().is_relative_to(output.resolve()) or digest(path) != hash_value:
                errors.append(f"missing/stale/outside-root artifact: {path}")
        if manifest["ac_index"] != ac_index(manifest, output):
            errors.append("AC artifact mapping changed")
        suite = load_json(output / "suite.json")
        import xml.etree.ElementTree as ET
        suites = list(ET.parse(output / "suite.xml").getroot().iter("testsuite"))
        if (suite["exit"] != 0 or not suites or not any(int(s.get("tests", 0)) for s in suites)
                or any(int(s.get(k, 0)) for s in suites for k in ("errors", "failures", "skipped"))):
            errors.append("full suite missing/failed/skipped")
        canaries = load_json(output / "canaries/canaries.json")
        if canaries["provenance"]["head"] != manifest["head"] or canaries["role"] != manifest["role"]:
            errors.append("canaries wrong head/role")
        errors += canary_errors(canaries)
        errors += capture_errors(manifest, output)
        for case, expected in zip(manifest["cases"], fixed_cases()):
            if any(json.dumps(case[k], ensure_ascii=False) != json.dumps(value, ensure_ascii=False)
                   for k, value in expected.items()):
                errors.append(f"{case['id']}: stale case oracle")
            if Path(case["input"]).read_bytes() != expected["body"].encode("utf-8") or case["exit"] != 0 or Path(case["stderr"]).read_bytes():
                errors.append(f"{case['id']}: stale input/CLI failure")
            for view in case["views"]:
                raw = load_json(view["raw"])
                errors += view_identity_errors(view) + geometry_errors(raw) + dom_errors(raw, case) + image_coverage_errors(view, raw)
                if raw["viewport"] != view["browser"]["viewport"] or raw["viewport"]["width"] != view["width"] or not raw["platformFonts"]:
                    errors.append("missing/wrong browser environment")
                net = load_json(view["network"])
                errors += network_errors(net, Path(case["stdout"]).as_uri())
                if net["interval"] != "live-review" or (require_end and net["end"] < end) or net["start"] > manifest["ready_at"]:
                    errors.append("incomplete live observation interval")
                if view["errors"]:
                    errors += view["errors"]
        errors += ledger_errors(manifest, ledger, end)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        errors.append(f"evidence unverified: {type(exc).__name__}: {exc}")
    return list(dict.fromkeys(errors))


def ac_index(manifest, output):
    # Conservative full chain for every AC: all cases, not sampled evidence.
    refs = sorted(manifest["artifacts"]) + sorted(v["network"] for c in manifest["cases"] for v in c["views"])
    return {f"AC{i}": refs for i in range(1, 7)}


def process_start(pid):
    # Linux process incarnation, not PID alone (PID reuse must not revive capture).
    return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]


def live_session_errors(manifest):
    try:
        if (manifest["mode"] != "review-session" or manifest["verdict"] != "pending-review"
                or manifest.get("ended") or not manifest["session"]
                or process_start(manifest["pid"]) != manifest["process_start"]):
            return ["live session absent/ended/stale"]
        os.kill(manifest["pid"], 0)
    except (KeyError, TypeError, ValueError, OSError):
        return ["live session unavailable"]
    return []


def global_context_errors(events, targets, context_ids):
    errors = []
    by_id = {t.get("targetId"): t for t in targets.values()}
    for event in events:
        data = event["data"]
        target = data.get("targetInfo") or by_id.get(data.get("targetId"), {})
        if target.get("browserContextId") and target["browserContextId"] not in context_ids:
            errors.append(f"unobserved browser context: {target}")
        if event["kind"].startswith(("Network.", "Page.")) and not target.get("browserContextId"):
            errors.append(f"unknown global target attribution: {event}")
    return list(dict.fromkeys(errors))


def snapshot_live(live, browser, output):
    # Pump all native listeners, then take complete CDP snapshots. No page closes.
    for item in live:
        item["page"].wait_for_timeout(10)
    boundary = now()
    errors = []
    for item in live:
        net = item["observer"].finish()
        net["interval"] = "live-review"
        save_json(Path(item["view"]["network"]), net)
        errors += network_errors(net, item["url"])
    monitor = browser.protocol_monitor
    with monitor.lock:
        save_json(output / "browser-network.json", dict(events=list(monitor.events),
            targets=dict(monitor.targets), errors=list(monitor.errors), snapshot_at=now()))
        errors += list(map(str, monitor.errors))
        errors += global_context_errors(monitor.events, monitor.targets,
            {item["observer"].context_id for item in live})
    return boundary, errors


def validate_live_finish(manifest, ledger, live, browser, output):
    boundary, errors = snapshot_live(live, browser, output)
    errors += evidence_errors(manifest, ledger, output, boundary)
    # Native events queued during validation are delivered before a second check.
    boundary, late = snapshot_live(live, browser, output)
    errors += late + evidence_errors(manifest, ledger, output, boundary)
    finished = now()  # actual completion, not the start of the last check
    _, late = snapshot_live(live, browser, output)
    return errors + late, finished


def project_final_reviews(manifest, ledger, verdict):
    """Project validated attestations in canonical image order, never invent viewing."""
    errors = ledger_errors(manifest, ledger, manifest["verification_finished"])
    if errors:
        raise ValueError(f"invalid final ledger: {errors}")
    reviews = {r["image"]: r for r in ledger["reviews"]}
    for case in manifest["cases"]:
        for view in case["views"]:
            view["verdict"] = verdict
            view["reviewed_images"] = [dict(path=i["path"], sha256=reviews[i["path"]]["sha256"],
                viewed_at=reviews[i["path"]]["viewed_at"]) for i in view["images"]]


def final_review_errors(manifest, ledger, output):
    """Reconcile final on-disk views against exact ledger identities and bytes."""
    def pending(value):
        if isinstance(value, dict):
            return any(pending(v) for v in value.values())
        if isinstance(value, list):
            return any(pending(v) for v in value)
        return value == "pending-review"

    errors = []
    try:
        verdict = "accepted" if manifest["role"] == "quality" else "builder-reviewed"
        if (manifest["verdict"] != verdict or manifest["errors"]
                or manifest["independent_acceptance"] != (manifest["role"] == "quality")
                or manifest["ac_verdicts"] != {f"AC{i}": "accepted" for i in range(1, 7)}):
            errors.append("inconsistent final verdict")
        if not manifest["cases"] or pending(manifest):
            errors.append("empty/pending final manifest")
        errors += capture_errors(manifest, output)
        errors += ledger_errors(manifest, ledger, manifest["verification_finished"])
        if (load_json(output / "reviews.json") != ledger
                or digest(output / "reviews.json") != manifest["ledger_sha256"]):
            errors.append("final ledger changed")
        for case in manifest["cases"]:
            if case["format"] == "html" and [v["width"] for v in case["views"]] != list(WIDTHS):
                errors.append("missing/reordered final views")
            for view in case["views"]:
                errors += view_identity_errors(view)
                expected = []
                for image in view["images"]:
                    matches = [r for r in ledger["reviews"] if r["image"] == image["path"]]
                    if len(matches) != 1:
                        errors.append("final review cardinality mismatch")
                        continue
                    expected.append(dict(path=image["path"], sha256=matches[0]["sha256"],
                                         viewed_at=matches[0]["viewed_at"]))
                derived = load_json(output / case["id"] / str(view["width"]) / "derived.json")
                if (view["verdict"] != verdict or not expected or view["reviewed_images"] != expected
                        or derived != view or pending(derived)):
                    errors.append("final manifest/derived/ledger mismatch")
    except (KeyError, TypeError, ValueError, OSError) as exc:
        errors.append(f"final review unverified: {type(exc).__name__}: {exc}")
    return list(dict.fromkeys(errors))


def revoke_final_reviews(manifest, output, persist=True):
    """Revoke all projections; best-effort writes never hide persistence failures."""
    manifest["verdict"] = "unverified"
    manifest["independent_acceptance"] = False
    manifest["ac_verdicts"] = {f"AC{i}": "unverified" for i in range(1, 7)}
    records = {}
    for case in manifest.get("cases", []):
        for view in case.get("views", []):
            view.update(verdict="unverified", reviewed_images=[])
            records[output / case["id"] / str(view["width"]) / "derived.json"] = view
    if not persist:
        return
    # Include a derived record left behind by an interrupted capture, even if its
    # view was not yet appended to the manifest. Immutable raw/images stay intact.
    for path in output.glob("*/*/derived.json"):
        if path not in records:
            try:
                record = load_json(path)
                record.update(verdict="unverified", reviewed_images=[])
                records[path] = record
            except Exception as exc:
                manifest["errors"].append(f"persistence rollback read {path}: {exc}")
    for path, record in records.items():
        try:
            save_json(path, record)
        except Exception as exc:
            manifest["errors"].append(f"persistence rollback {path}: {exc}")


def publish_final_reviews(manifest, ledger, output):
    """Write the completion marker last; partial readers must reject the marker."""
    verdict = manifest["verdict"]
    project_final_reviews(manifest, ledger, verdict)
    checkpoint = copy.deepcopy(manifest)
    revoke_final_reviews(checkpoint, output, persist=False)
    save_json(output / "manifest.json", checkpoint)
    for case in manifest["cases"]:
        for view in case["views"]:
            save_json(output / case["id"] / str(view["width"]) / "derived.json", view)
    errors = final_review_errors(manifest, ledger, output)
    if errors:
        raise ValueError(f"final reconciliation: {errors}")


def run_suite(output):
    argv = [sys.executable, "-m", "pytest", "--junitxml", str(output / "suite.xml")]
    start = now()
    result = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=180,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    (output / "suite.stdout").write_bytes(result.stdout)
    (output / "suite.stderr").write_bytes(result.stderr)
    save_json(output / "suite.json", dict(argv=argv, cwd=str(ROOT), started=start,
        ended=now(), exit=result.returncode, environment=dict(PYTHONPATH=os.environ.get("PYTHONPATH"),
        PYTHONHASHSEED=os.environ.get("PYTHONHASHSEED")), head=git("rev-parse", "HEAD").strip()))
    if result.returncode:
        raise ValueError("full suite failed; see suite.stdout/stderr")


def review_session(args):
    import uuid
    from types import SimpleNamespace

    output = args.output_dir.resolve()
    actor = session_actor(args.role, args.actor, output)
    if not 0 < args.session_timeout <= 7200:
        raise ValueError("session timeout must be >0 and <=7200 seconds")
    if output.exists():
        raise ValueError("review output root must be new, never reused")
    output.mkdir(parents=True)
    before, scope = provenance(), scope_report()
    save_json(output / "provenance.json", before)
    save_json(output / "scope.json", scope)
    manifest: dict = dict(mode="review-session", root=str(output), role=args.role, actor=actor,
        session=uuid.uuid4().hex, pid=os.getpid(), process_start=process_start(os.getpid()),
        head=before["head"], started=now(), scope=scope, verdict="unverified", cases=[], errors=[],
        independent_acceptance=False)
    save_json(output / "manifest.json", manifest)
    live = []
    ledger = {}
    try:
        if before["product_status"] or before["untracked_product"] or scope["errors"]:
            raise ValueError("dirty/untracked or unauthorized scope; commit code first")
        run_suite(output)
        if self_test_network(SimpleNamespace(output_dir=output / "canaries", role=args.role, browser=args.browser)):
            raise ValueError("real canary discrimination failed")
        manifest["cases"] = generate_cases(output)
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw, instrumented_browser(pw, args.browser) as browser:
            try:
                manifest["browser"] = dict(executable=args.browser, version=browser.version,
                    os=platform.platform(), launch=browser.launch_record)
                for case in manifest["cases"]:
                    if case["format"] == "html":
                        for width in WIDTHS:
                            view = collect_view(browser, case, width, output, live=live)
                            case["views"].append(view)
                            manifest["errors"] += view["errors"]
                            view["raw_sha256"] = digest(view["raw"])
                            for image in view["images"]:
                                image["sha256"] = digest(image["path"])
                manifest["errors"] += capture_errors(manifest, output)
                _, net_errors = snapshot_live(live, browser, output)
                manifest["errors"] += net_errors
                if manifest["errors"]:
                    raise ValueError("initial live evidence failed")
                # Immutable inputs/CLI/raw/images/canaries/suite; network is live.
                manifest["artifacts"] = {str(p): digest(p) for p in output.rglob("*")
                    if p.is_file() and p.name not in {"manifest.json", "network.json", "browser-network.json", "derived.json"}}
                manifest["ac_index"] = ac_index(manifest, output)
                manifest["ready_at"] = now()
                manifest["verdict"] = "pending-review"
                save_json(output / "reviews.json", dict(session=manifest["session"], head=manifest["head"],
                    root=str(output), actor=actor, reviews=[], ac_reviews=[]))
                save_json(output / "manifest.json", manifest)
                print(json.dumps(dict(ready=True, manifest=str(output / "manifest.json"),
                    session=manifest["session"], verdict="pending-review")), flush=True)
                deadline = time.monotonic() + args.session_timeout
                request_path = output / "finalize-request.json"
                while not request_path.exists() and time.monotonic() < deadline:
                    live[0]["page"].wait_for_timeout(100)  # finite local review protocol, not repo surveillance
                if not request_path.exists():
                    raise ValueError("review timeout: images/rawRange unverified; no completion request")
                request = load_json(request_path)
                ledger_path = output / "reviews.json"
                if request["session"] != manifest["session"] or request["ledger_sha256"] != digest(ledger_path):
                    raise ValueError("finalize request/ledger identity changed")
                manifest["finalize_requested_at"] = request["at"]
                ledger = load_json(ledger_path)
                errors, finished = validate_live_finish(manifest, ledger, live, browser, output)
                manifest["verification_finished"] = finished
                manifest["errors"] += errors
                manifest["ledger_sha256"] = digest(ledger_path)
                manifest["end_provenance"] = provenance()
                manifest["verdict"] = "failed" if errors else ("accepted" if args.role == "quality" else "builder-reviewed")
                manifest["independent_acceptance"] = not errors and args.role == "quality"
                manifest["ac_verdicts"] = {f"AC{i}": "accepted" if not errors else "unverified" for i in range(1, 7)}
            finally:
                if live:
                    end, errors = snapshot_live(live, browser, output)
                    manifest["observation_end"] = end
                    manifest["errors"] += errors
                for item in live:
                    item["observer"].browser_cdp.detach()
                    item["context"].close()
    except Exception as exc:
        manifest["errors"].append(f"unverified: {type(exc).__name__}: {exc}")
    try:
        manifest["end_provenance"] = provenance()
        if (manifest["end_provenance"]["head"] != manifest["head"]
                or manifest["end_provenance"]["product_status"]
                or manifest["end_provenance"]["untracked_product"]):
            manifest["errors"].append("head/product changed before final verdict")
        if not manifest["errors"]:
            publish_final_reviews(manifest, ledger, output)
        manifest["ended"] = now()
        if manifest["errors"]:
            revoke_final_reviews(manifest, output)
        save_json(output / "manifest.json", manifest)
    except Exception as exc:
        manifest["errors"].append(f"final publication/persistence unverified: {type(exc).__name__}: {exc}")
        manifest["ended"] = now()
        revoke_final_reviews(manifest, output)
        try:
            save_json(output / "manifest.json", manifest)
        except Exception as save_exc:
            manifest["errors"].append(f"persistence manifest unavailable: {save_exc}")
    print(json.dumps(dict(manifest=str(output / "manifest.json"), verdict=manifest["verdict"], errors=manifest["errors"])), flush=True)
    return 0 if manifest["verdict"] in {"accepted", "builder-reviewed"} else 1


def finalize(args):
    output = args.output_dir.resolve()
    actor = session_actor(args.role, args.actor, output)
    manifest = load_json(output / "manifest.json")
    if args.review_ledger is None or args.review_ledger.resolve() != output / "reviews.json":
        raise ValueError("review ledger must be the live root reviews.json")
    ledger = load_json(args.review_ledger)
    errors = live_session_errors(manifest)
    if manifest.get("role") != args.role or manifest.get("actor") != actor:
        errors.append("finalize role/actor mismatch")
    errors += evidence_errors(manifest, ledger, output, now(), require_end=False)
    if errors:
        print(json.dumps(dict(verdict="unverified", errors=errors)))
        return 1
    # The live owner repeats ALL checks with freshly flushed events before verdict.
    save_json(output / "finalize-request.json", dict(session=manifest["session"],
        ledger_sha256=digest(args.review_ledger), at=now()))
    print(json.dumps(dict(verdict="finalize-requested", final_acceptance=False)))
    return 0


def check_evidence_contract():
    """Synthetic review predicates only. Never emit a product acceptance."""
    image = dict(path="/synthetic/full.png", sha256="a" * 64, width=320, height=900)
    entry = dict(actor="synthetic-reviewer", image=image["path"], sha256=image["sha256"],
        viewed_at="2026-01-01T00:00:02+00:00", scale=1, extent=[0, 0, 320, 900],
        raw="/synthetic/raw.json", raw_sha256="b" * 64, judgment="readable", notes="synthetic control only")
    def check(value):
        return review_errors(value, image, entry["raw"], entry["raw_sha256"], entry["actor"],
            "2026-01-01T00:00:01+00:00", "2026-01-01T00:00:03+00:00")
    errors, rejected = check(entry), []
    invalid: dict = {f"missing-{k}": {key: value for key, value in entry.items() if key != k} for k in entry}
    for key, value in (("actor", "other"), ("sha256", "other"), ("raw", "/other/raw"),
                       ("judgment", True), ("scale", 0.5), ("extent", [0, 0, 320, 1]),
                       ("viewed_at", "2025-01-01T00:00:00+00:00")):
        invalid[f"wrong-{key}"] = dict(entry, **{key: value})
    for name, record in invalid.items():
        if check(record):
            rejected.append(name)
        else:
            errors.append(f"invalid accepted: {name}")
    return dict(synthetic=True, product_acceptance=False, clean="accepted-predicate-only",
                rejected=rejected, errors=errors)


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--role", choices=("builder", "quality"))
    result.add_argument("--output-dir", type=Path)
    result.add_argument("--mode", choices=("capture", "review-session", "finalize"), default="capture")
    result.add_argument("--browser", default="/usr/bin/chromium-browser")
    result.add_argument("--self-test-network", action="store_true")
    result.add_argument("--actor")
    result.add_argument("--session-timeout", type=float, default=3600)
    result.add_argument("--review-ledger", type=Path)
    result.add_argument("--check-evidence-contract", action="store_true")
    result.add_argument("--check-scope", action="store_true")
    return result


def main():
    args = parser().parse_args()
    if args.check_evidence_contract or args.check_scope:
        report = check_evidence_contract() if args.check_evidence_contract else scope_report()
        print(json.dumps(report, ensure_ascii=False))
        raise SystemExit(1 if report["errors"] else 0)
    if args.role is None or args.output_dir is None:
        parser().error("--role and --output-dir are required for browser operations")
    if args.self_test_network:
        raise SystemExit(self_test_network(args))
    try:
        operation = {"capture": capture, "review-session": review_session, "finalize": finalize}[args.mode]
        raise SystemExit(operation(args))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps(dict(verdict="unverified", errors=[str(exc)])))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
