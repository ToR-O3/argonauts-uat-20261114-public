"""Deterministic evidence discrimination; importing this suite needs no browser."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def verifier():
    path = ROOT / "tools/verify_wordfreq_html.py"
    assert path.is_file(), "real-file collector is required"
    spec = importlib.util.spec_from_file_location("html_verifier", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_independent_fixture_matrix():
    v = verifier()
    cases = v.fixed_cases()
    assert len(cases) == 15
    assert len({c["id"] for c in cases}) == 15
    long = next(c for c in cases if c["id"] == "long-12")
    assert long["basename"] == '集計  ' + 'n' * 176 + '\n続き\t終わり  &<>"\'.txt'
    expected = [("w" * 256, 123)] + [(f"row{i:02}", 13-i) for i in range(1, 12)]
    assert long["pairs"] == expected
    assert long["body"] == ' '.join(word for word, count in expected for _ in range(count)) + '\n'
    assert long["total"] == 200
    assert next(c for c in cases if c["id"] == "long-default")["pairs"] == expected[:10]
    assert next(c for c in cases if c["id"] == "long-99")["pairs"] == expected
    for fmt in ("text", "json", "html"):
        for top in (1, 2):
            case = next(c for c in cases if c["id"] == f"tie-{fmt}-{top}")
            assert case["pairs"] == [("zoo", 2), ("apple", 2)][:top]
            assert case["total"] == 5
    injection = next(c for c in cases if c["id"] == "injection")
    assert injection["basename"] == '検査  &<>"\'\n次\t終.txt'
    assert injection["pairs"] == [("café", 2), ("strasse", 2), ("日本語", 1)]
    assert json.loads(json.dumps(cases, ensure_ascii=False))[0]["id"] == "empty"


def rect(left=20.25, top=10.5, right=30.75, bottom=28.5):
    return dict(x=left, y=top, left=left, top=top, right=right, bottom=bottom,
                width=right-left, height=bottom-top)


def raw_record():
    return dict(viewport=dict(width=320, height=900, dpr=1, scale=1),
                document=dict(scrollWidth=320, clientWidth=320),
                elements=[dict(id="cell", rect=rect(top=14, bottom=25, right=60), rects=[],
                               style={}, ancestors=[])],
                texts=[dict(id="text0", owner="cell", text="A\n😀", fullRects=[rect()],
                            characters=[dict(index=0, utf16Start=0, utf16End=1,
                                             codepoint=65, char="A", rects=[rect()]),
                                        dict(index=1, utf16Start=1, utf16End=2,
                                             codepoint=10, char="\n", rects=[]),
                                        dict(index=2, utf16Start=2, utf16End=4,
                                             codepoint=128512, char="😀", rects=[rect(31, 10.5, 48, 28.5)])])])


@pytest.mark.parametrize("bounds", [rect(20, 10, 20, 28), rect(20, 10, 30, 10), rect(20, 10, 20, 10)])
def test_geometry_rejects_zero_area_visible_glyph(bounds):
    raw = raw_record()
    raw["texts"][0]["characters"][0]["rects"] = [bounds]
    original = copy.deepcopy(raw)
    assert any("no visible ink" in e for e in verifier().geometry_errors(raw))
    assert raw == original


def test_geometry_accepts_positive_ink_with_raw_zero_rect():
    raw = raw_record()
    raw["texts"][0]["characters"][0]["rects"].append(rect(20, 10, 20, 10))
    assert verifier().geometry_errors(raw) == []


def test_geometry_accepts_raw_own_vertical_overhang_and_empty_ranges():
    v = verifier()
    raw = raw_record()
    original = copy.deepcopy(raw)
    assert v.geometry_errors(raw) == []
    assert raw == original
    assert json.loads(json.dumps(raw)) == raw


@pytest.mark.parametrize("defect", ["overflow", "column", "clip", "overlap", "missing-char", "missing-empty", "offset", "missing-elements", "missing-texts", "own-clip"])
def test_geometry_rejects_each_invalid_record(defect):
    v = verifier()
    raw = raw_record()
    if defect == "overflow":
        raw["document"]["scrollWidth"] = 321
    elif defect == "column":
        raw["texts"][0]["characters"][0]["rects"][0]["right"] = 322.125
    elif defect == "clip":
        raw["elements"][0]["ancestors"] = [dict(id="clipper", overflowX="visible", overflowY="hidden", clip=rect(bottom=20))]
    elif defect == "overlap":
        second = copy.deepcopy(raw["texts"][0])
        second["id"] = "adjacent-row"
        raw["texts"].append(second)
    elif defect in ("missing-char", "missing-empty"):
        raw["texts"][0]["characters"].pop(0 if defect == "missing-char" else 1)
    elif defect == "offset":
        raw["texts"][0]["characters"][2]["utf16End"] = 3
    elif defect == "missing-elements":
        raw["elements"] = []
    elif defect == "own-clip":
        raw["elements"][0]["style"]["overflowY"] = "hidden"
        raw["elements"][0]["clip"] = rect(top=14, bottom=25, right=60)
    else:
        raw["texts"] = []
    assert v.geometry_errors(raw), defect


@pytest.mark.parametrize("defect", ["scroll-width", "glyph"])
def test_geometry_rejects_content_under_scrollbar(defect):
    raw = raw_record()
    raw["document"]["clientWidth"] = 305
    raw["document"]["scrollWidth"] = 305
    if defect == "scroll-width":
        raw["document"]["scrollWidth"] = 310
    else:
        raw["elements"][0]["rect"]["right"] = 320
        raw["texts"][0]["characters"][0]["rects"] = [rect(304, 10, 310, 28)]
    original = copy.deepcopy(raw)
    assert verifier().geometry_errors(raw)
    assert raw == original


@pytest.mark.parametrize("kind", ["td", "filename-value", "total-value"])
@pytest.mark.parametrize("defect", ["missing", "empty", "partial", "no-characters"])
def test_geometry_requires_complete_text_for_each_cell_and_metadata(kind, defect):
    raw = raw_record()
    owner = copy.deepcopy(raw["elements"][0])
    owner.update(id="unmeasured", tag="td" if kind == "td" else "div",
                 className="word" if kind == "td" else kind, text="A\n😀")
    raw["elements"].append(owner)
    text = copy.deepcopy(raw["texts"][0])
    text.update(id="required-text", owner=owner["id"])
    # Move new owner/glyphs out of the first owner's ink to isolate coverage.
    for item in text["characters"]:
        for r in item["rects"]:
            r.update(top=r["top"]+100, bottom=r["bottom"]+100, y=r["y"]+100)
    raw["texts"].append(text)
    assert verifier().geometry_errors(raw) == []
    if defect == "missing":
        raw["texts"].pop()
    elif defect == "empty":
        text.update(text="", characters=[], fullRects=[])
    elif defect == "partial":
        text["text"] = "A"
        text["characters"] = text["characters"][:1]
    else:
        text["characters"] = []
    original = copy.deepcopy(raw)
    assert verifier().geometry_errors(raw)
    assert raw == original


def test_real_generation_bytes_oracles_privacy_and_lazy_browser(tmp_path):
    v = verifier()
    cases = v.generate_cases(tmp_path)
    assert len(cases) == 15
    for case in cases:
        assert case["exit"] == 0
        assert Path(case["stdout"]).is_file()
        assert Path(case["stderr"]).read_bytes() == b""
        assert case["argv"][1:3] == ["-m", "wordfreq"]
        assert Path(case["stdout"]).read_bytes().decode("utf-8", errors="strict")
    result = subprocess.run([sys.executable, "-S", str(ROOT / "tools/verify_wordfreq_html.py"), "--help"], capture_output=True)
    assert result.returncode == 0, result.stderr
    assert b"--mode" in result.stdout


def test_capture_completeness_rejects_empty_or_missing_artifacts(tmp_path):
    v = verifier()
    assert v.capture_errors({"cases": []}, tmp_path)
    manifest = {"cases": [{"id": "empty", "format": "html", "views": []}]}
    assert v.capture_errors(manifest, tmp_path)


@pytest.mark.parametrize("kind", ["tile", "full"])
def test_capture_rejects_png_dimensions_different_from_record(tmp_path, kind):
    import struct
    import zlib

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))

    png = tmp_path / "actual.png"
    png.write_bytes(b"\x89PNG\r\n\x1a\n" +
                    chunk(b"IHDR", struct.pack(">IIBBBBB", 320, 100, 8, 2, 0, 0, 0)) +
                    chunk(b"IDAT", zlib.compress((b"\0" + b"\xff" * 960) * 100)) +
                    chunk(b"IEND", b""))
    artifact = tmp_path / "artifact"
    artifact.touch()
    v = verifier()
    cases = []
    for case in v.fixed_cases():
        record = dict(case, input=str(artifact), stdout=str(artifact), stderr=str(artifact), views=[])
        if case["format"] == "html":
            record["views"] = [dict(width=width, raw=str(artifact), network=str(artifact),
                images=[dict(path=str(png), type=kind, x=0, y=800, width=320, height=100)])
                for width in v.WIDTHS]
        cases.append(record)
    manifest = dict(cases=cases)
    assert v.capture_errors(manifest, tmp_path) == []
    cases[0]["views"][0]["images"][0]["height"] = 759
    assert any("image dimensions" in e for e in v.capture_errors(manifest, tmp_path))


def test_browser_files_and_capture_entrypoint_exist():
    v = verifier()
    assert (ROOT / "tools/wordfreq_html_geometry.js").is_file()
    assert callable(getattr(v, "capture", None)), "actual browser capture entrypoint required"


def local_network():
    return dict(start="2026-01-01T00:00:00+00:00", end="2026-01-01T00:00:01+00:00",
                coverage=dict(context=True, browserTargets=True, mainCDP=True, flattenedAutoAttach=True), errors=[],
                events=[dict(kind="browser-autoattach-ready", data={}),
                        dict(kind="target-attached", data=dict(waitingForDebugger=True,
                            targetInfo=dict(type="page", targetId="main"))),
                        dict(kind="page-cdp-ready", data={}),
                        dict(kind="request", data=dict(url="file:///control.html")),
                        dict(kind="Network.requestWillBeSent", data=dict(requestId="local",
                            request=dict(url="file:///control.html"))),
                        dict(kind="Network.requestWillBeSent", data=dict(requestId="local-root",
                            request=dict(url="file:///control.html"), source="browser-autoattach",
                            targetId="main", frameId="main-frame", initiator=dict(type="other")))])


@pytest.mark.parametrize("kind", ["Network.responseReceived", "Network.dataReceived", "Network.loadingFinished", "Network.loadingFailed", "Network.responseReceivedExtraInfo"])
@pytest.mark.parametrize("channel", ["missing", "other-source", "other-session", "other-target"])
def test_network_rejects_orphan_request_ids_per_channel(kind, channel):
    net = local_network()
    data = dict(requestId="orphan")
    if channel != "missing":
        start = dict(requestId="orphan", request=dict(url="file:///control.html"),
                     source="browser-autoattach", sessionId="session-a", targetId="main")
        net["events"].append(dict(kind="Network.requestWillBeSent", data=start))
        data.update(source="browser-autoattach", sessionId="session-a", targetId="main")
        data[{"other-source": "source", "other-session": "sessionId", "other-target": "targetId"}[channel]] = "different"
    net["events"].append(dict(kind=kind, data=data))
    assert any("unattributed request" in e for e in verifier().network_errors(net, "file:///control.html"))


@pytest.mark.parametrize("field", ["response", "redirectResponse", "documentURL"])
def test_network_checks_all_url_bearing_fields(field):
    net = local_network()
    data = dict(requestId="local")
    data[field] = "https://unexpected.invalid/" if field == "documentURL" else dict(url="https://unexpected.invalid/")
    net["events"].append(dict(kind="Network.responseReceived", data=data))
    assert any("external/unexpected" in e for e in verifier().network_errors(net, "file:///control.html"))


def test_network_rejects_external_orphan_response():
    net = local_network()
    net["events"].append(dict(kind="Network.responseReceived", data=dict(
        requestId="orphan", response=dict(url="https://unexpected.invalid/"))))
    errors = verifier().network_errors(net, "file:///control.html")
    assert any("unattributed request" in e for e in errors)
    assert any("external/unexpected" in e for e in errors)


def test_network_accepts_same_channel_lifecycle():
    net = local_network()
    for kind in ("Network.responseReceived", "Network.dataReceived", "Network.loadingFinished"):
        net["events"].append(dict(kind=kind, data=dict(requestId="local", response=dict(url="file:///control.html"))))
    assert verifier().network_errors(net, "file:///control.html") == []


def test_browser_ui_exclusion_requires_pre_open_target_identity():
    v = verifier()
    net = local_network()
    event = dict(kind="target-created", data=dict(targetInfo=dict(targetId="ui1", type="browser_ui",
                url="chrome://omnibox-popup.top-chrome/", canAccessOpener=False)))
    net["events"].insert(0, event)
    net["events"].insert(0, dict(kind="target-attached", data=copy.deepcopy(event["data"])))
    assert v.network_errors(net, "file:///control.html") == []
    bad = copy.deepcopy(net)
    bad["events"][0]["data"]["targetInfo"]["type"] = "page"
    assert v.network_errors(bad, "file:///control.html")
    late = local_network()
    late["events"].append(event)
    assert v.network_errors(late, "file:///control.html")


@pytest.mark.parametrize("kind,data", [
    ("requestfailed", dict(url="http://failed.invalid/resource", failure="net::ERR_NAME_NOT_RESOLVED")),
    ("Page.frameRequestedNavigation", dict(url="https://navigate.invalid/")),
    ("Page.windowOpen", dict(url="https://popup.invalid/", userGesture=False)),
    ("Network.requestWillBeSent", dict(requestId="early", request=dict(url="https://popup.invalid/"), initiator=dict(type="script"), targetId="popup")),
    ("unknown-event", {}),
    ("request", dict(frame=dict(unavailable="unknown origin"))),
])
def test_failed_navigation_popup_unknown_never_clean(kind, data):
    v = verifier()
    net = local_network()
    net["events"].append(dict(kind=kind, data=data))
    assert v.network_errors(net, "file:///control.html")


def test_missing_pre_open_or_empty_observation_cannot_pass():
    v = verifier()
    net = local_network()
    net["events"].pop(0)
    assert v.network_errors(net, "file:///control.html")
    net = local_network()
    net["events"] = [e for e in net["events"] if e["kind"] != "request"]
    net["events"].append(dict(kind="target-changed", data=dict(targetInfo=dict(url="file:///control.html"))))
    assert v.network_errors(net, "file:///control.html")
    net["events"] = []
    assert v.network_errors(net, "file:///control.html")


@pytest.mark.parametrize("missing", ["browser-autoattach-ready", "page-cdp-ready"])
def test_network_requires_ready_evidence_even_with_true_flags(missing):
    net = local_network()
    assert verifier().network_errors(net, "file:///control.html") == []
    net["events"] = [e for e in net["events"] if e["kind"] != missing]
    assert verifier().network_errors(net, "file:///control.html")


@pytest.mark.parametrize("defect", ["target-missing", "main-missing", "auto-missing", "wrong-url", "wrong-target", "ready-late"])
def test_coverage_requires_same_document_all_channels(defect):
    net = local_network()
    assert all(verifier().observer_coverage(net["events"]).values())
    if defect.endswith("missing"):
        index = {"target-missing": 1, "main-missing": 4, "auto-missing": 5}[defect]
        net["events"].pop(index)
    elif defect == "wrong-url":
        net["events"][5]["data"]["request"]["url"] = "about:blank"
    elif defect == "wrong-target":
        net["events"][5]["data"]["targetId"] = "unrelated"
    else:
        net["events"].append(net["events"].pop(0))
    assert not all(verifier().observer_coverage(net["events"]).values())
    assert verifier().network_errors(net, "file:///control.html")


def test_canary_results_require_actual_all_path_rejection():
    v = verifier()
    assert callable(getattr(v, "canary_errors", None)), "genuine observer canary validation required"
    assert v.canary_errors({"cases": []})


def synthetic_canaries(v):
    cases = []
    for name in v.CANARIES:
        net = local_network()
        if name != "clean":
            net["events"] += [dict(kind="Network.requestWillBeSent", data=dict(
                request=dict(url=v.CANARY_URL), source="browser-autoattach", requestId="req1",
                initiator=dict(type="script"), targetId="popup", frameId="frame1")),
                dict(kind="Network.loadingFailed", data=dict(requestId="req1", source="browser-autoattach", targetId="popup")),
                dict(kind="Page.frameRequestedNavigation", data=dict(url=v.CANARY_URL))]
        if name == "early-popup":
            net["events"].append(dict(kind="target-attached", data=dict(waitingForDebugger=True,
                targetInfo=dict(targetId="popup", openerId="main"))))
        cases.append(dict(id=name, url="file:///control.html", observation=net))
    return dict(cases=cases)


@pytest.mark.parametrize("defect", ["none", "wrong-failure", "missing-protocol", "unknown", "unpaused-popup", "missing-local"])
def test_canary_validator_requires_correlated_real_path_evidence(defect):
    v = verifier()
    report = synthetic_canaries(v)
    if defect == "wrong-failure":
        report["cases"][1]["observation"]["events"][7]["data"]["requestId"] = "unrelated"
    elif defect == "missing-protocol":
        report["cases"][0]["observation"]["coverage"]["flattenedAutoAttach"] = False
    elif defect == "unknown":
        report["cases"][1]["observation"]["events"].append(dict(kind="unknown-event", data={}))
    elif defect == "unpaused-popup":
        report["cases"][3]["observation"]["events"][-1]["data"]["waitingForDebugger"] = False
    elif defect == "missing-local":
        report["cases"][2]["observation"]["events"].pop(3)
    assert bool(v.canary_errors(report)) == (defect != "none")


def test_canary_url_only_failure_cannot_replace_correlated_request_id():
    v = verifier()
    report = synthetic_canaries(v)
    events = report["cases"][1]["observation"]["events"]
    events[7]["data"]["requestId"] = "unrelated"
    events.append(dict(kind="requestfailed", data=dict(url=v.CANARY_URL, failure="failed")))
    assert v.canary_errors(report)


def test_untracked_product_content_is_recorded(monkeypatch, tmp_path):
    v = verifier()
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools/untracked.py").write_bytes(b"# actual untracked content\n")
    monkeypatch.setattr(v, "ROOT", tmp_path)
    def git(*args):
        if args[0] == "ls-files":
            return "tools/untracked.py\0"
        if args[0] == "rev-parse":
            return "target-head\n"
        return "?? tools/untracked.py\n" if args[0] == "status" else ""
    monkeypatch.setattr(v, "git", git)
    result = v.provenance()
    assert result["untracked_product"][0]["path"] == "tools/untracked.py"
    assert result["untracked_product"][0]["content_utf8"] == "# actual untracked content\n"
    assert result["product_status"]


def test_dirty_product_blocks_capture_after_diagnostics(tmp_path, monkeypatch):
    v = verifier()
    from types import SimpleNamespace
    monkeypatch.setattr(v, "provenance", lambda: dict(head="h", product_status=" M wordfreq/formatters.py", product_diff="actual diff", status="dirty"))
    with pytest.raises(ValueError, match="dirty/untracked"):
        v.capture(SimpleNamespace(output_dir=tmp_path, role="builder", browser="unused"))
    assert json.loads((tmp_path / "provenance.json").read_text())["product_diff"] == "actual diff"
    assert not (tmp_path / "manifest.json").exists()


def test_review_without_actor_cannot_succeed(tmp_path):
    result = subprocess.run([sys.executable, str(ROOT / "tools/verify_wordfreq_html.py"),
                             "--role", "builder", "--output-dir", str(tmp_path),
                             "--mode", "review-session"], capture_output=True)
    assert result.returncode != 0


def test_review_ledger_requires_real_identity_time_hash_and_raw_reference():
    v = verifier()
    image = dict(path="/quality/full.png", sha256="a" * 64, width=320, height=900)
    entry = dict(actor="argonauts-uat-quality", image=image["path"], sha256=image["sha256"],
                 viewed_at="2026-01-01T00:00:02+00:00", scale=1,
                 extent=[0, 0, 320, 900], raw="/quality/raw.json", raw_sha256="b" * 64,
                 judgment="readable", notes="All words, whitespace and numeric cells inspected")
    original = copy.deepcopy(entry)
    assert v.review_errors(entry, image, "/quality/raw.json", "b" * 64,
                           "argonauts-uat-quality", "2026-01-01T00:00:01+00:00",
                           "2026-01-01T00:00:03+00:00") == []
    assert entry == original
    for field in entry:
        bad = dict(entry)
        del bad[field]
        assert v.review_errors(bad, image, "/quality/raw.json", "b" * 64,
                               "argonauts-uat-quality", "2026-01-01T00:00:01+00:00",
                               "2026-01-01T00:00:03+00:00"), field


@pytest.mark.parametrize("field,value", [
    ("actor", "argonauts-uat-builder"), ("viewed_at", "2025-01-01T00:00:00+00:00"),
    ("viewed_at", "2027-01-01T00:00:00+00:00"), ("scale", 0.2),
    ("extent", [0, 0, 320, 800]), ("sha256", "wrong"), ("raw_sha256", "wrong"),
    ("raw", "/builder/raw.json"), ("judgment", True), ("notes", ""),
])
def test_review_invalid_attestation_rejected(field, value):
    v = verifier()
    image = dict(path="/quality/full.png", sha256="a" * 64, width=320, height=900)
    entry = dict(actor="argonauts-uat-quality", image=image["path"], sha256=image["sha256"],
                 viewed_at="2026-01-01T00:00:02+00:00", scale=1, extent=[0, 0, 320, 900],
                 raw="/quality/raw.json", raw_sha256="b" * 64, judgment="readable", notes="inspected")
    entry[field] = value
    assert v.review_errors(entry, image, "/quality/raw.json", "b" * 64,
                           "argonauts-uat-quality", "2026-01-01T00:00:01+00:00",
                           "2026-01-01T00:00:03+00:00")


def test_scope_has_exact_baseline_target_and_approved_product_snapshot():
    v = verifier()
    report = v.scope_report()
    assert report["base"] == "5a7659b949dc118b59cea5ef3eb40bcd94337d8d"
    assert report["target"] == v.git("rev-parse", "HEAD").strip()
    assert report["product_diff"]
    assert bool(report["errors"]) == bool(v.provenance()["product_status"])


@pytest.mark.parametrize("path", [".github/workflows/new.yml", "pyproject.toml",
    "wordfreq/tokenizer.py", "wordfreq/sources.py", "new_server.py",
    ".planning/phases/01-wordfreq-cli/01-01-SUMMARY.md",
    ".planning/phases/02-other/02-01-PLAN.md"])
def test_scope_rejects_out_of_plan_paths(path):
    assert verifier().scope_path_errors([path])


def test_scope_accepts_exact_owned_files_and_preserves_approved_tie_replacement():
    v = verifier()
    assert v.scope_path_errors(["wordfreq/aggregator.py", "tools/verify_wordfreq_html.py",
        "tests/test_html_verifier.py", "README.md", "docs/wordfreq-html-verification.md",
        "openspec/changes/r-50053edc-wordfreq-html/tasks.md",
        ".planning/phases/03-wordfreq-html-output/03-04-SUMMARY.md"]) == []


def test_session_identity_cannot_be_selected_by_role_flag(monkeypatch, tmp_path):
    v = verifier()
    monkeypatch.setenv("HERMES_PROFILE", "argonauts-uat-builder")
    with pytest.raises(ValueError, match="actor/role"):
        v.session_actor("quality", "argonauts-uat-quality", tmp_path / "quality")
    assert v.session_actor("builder", "argonauts-uat-builder", tmp_path / "builder") == "argonauts-uat-builder"
    with pytest.raises(ValueError, match="root"):
        v.session_actor("builder", "argonauts-uat-builder", tmp_path / "quality")


def ledger_control():
    image = dict(path="/quality/full.png", sha256="a" * 64, width=320, height=900)
    manifest = dict(session="synthetic-only", actor="argonauts-uat-quality", role="quality",
        head="h", root="/quality", ready_at="2026-01-01T00:00:01+00:00",
        cases=[dict(views=[dict(raw="/quality/raw.json", raw_sha256="b" * 64, images=[image])])])
    review = dict(actor=manifest["actor"], image=image["path"], sha256=image["sha256"],
        viewed_at="2026-01-01T00:00:02+00:00", scale=1, extent=[0, 0, 320, 900],
        raw="/quality/raw.json", raw_sha256="b" * 64, judgment="readable", notes="synthetic predicate only")
    ledger = dict(session=manifest["session"], head="h", actor=manifest["actor"], root="/quality",
        reviews=[review], ac_reviews=[dict(ac=f"AC{i}", judgment="accepted", notes="synthetic only",
            evidence=["/quality/full.png", "/quality/raw.json"]) for i in range(1, 7)])
    manifest["ac_index"] = {f"AC{i}": ["/quality/full.png", "/quality/raw.json"] for i in range(1, 7)}
    return manifest, ledger


@pytest.mark.parametrize("defect", ["none", "empty", "duplicate", "unviewed", "session",
    "head", "actor", "root", "ac-missing", "ac-duplicate", "ac-evidence", "ac-boolean"])
def test_ledger_exact_image_and_ac_coverage_roundtrip(defect):
    v = verifier()
    manifest, ledger = ledger_control()
    if defect == "empty":
        ledger = {}
    elif defect == "duplicate":
        ledger["reviews"] *= 2
    elif defect == "unviewed":
        ledger["reviews"] = []
    elif defect in {"session", "head", "actor", "root"}:
        ledger[defect] = "wrong"
    elif defect == "ac-missing":
        ledger["ac_reviews"].pop()
    elif defect == "ac-duplicate":
        ledger["ac_reviews"][-1] = ledger["ac_reviews"][0]
    elif defect == "ac-evidence":
        ledger["ac_reviews"][0]["evidence"] = []
    elif defect == "ac-boolean":
        ledger["ac_reviews"][0]["judgment"] = True
    assert bool(v.ledger_errors(manifest, ledger, "2026-01-01T00:00:03+00:00")) == (defect != "none")
    assert json.loads(json.dumps(ledger)) == ledger


def test_ended_or_empty_evidence_cannot_be_finalized(tmp_path):
    v = verifier()
    assert v.evidence_errors({}, {}, tmp_path, "2026-01-01T00:00:03+00:00")
    manifest, ledger = ledger_control()
    manifest.update(mode="capture", ended="2026-01-01T00:00:03+00:00")
    assert v.evidence_errors(manifest, ledger, tmp_path, "2026-01-01T00:00:03+00:00")


def test_live_options_and_finalize_require_actual_process(tmp_path):
    v = verifier()
    args = v.parser().parse_args(["--role", "builder", "--output-dir", str(tmp_path / "builder"),
        "--actor", "argonauts-uat-builder", "--mode", "review-session", "--session-timeout", "1"])
    assert args.session_timeout == 1
    assert args.actor == "argonauts-uat-builder"
    assert v.live_session_errors({})
    import os
    manifest = dict(pid=os.getpid(), process_start=v.process_start(os.getpid()),
                    mode="review-session", verdict="pending-review", session="s")
    assert v.live_session_errors(manifest) == []
    manifest["process_start"] = "wrong"
    assert v.live_session_errors(manifest)
    manifest["ended"] = "done"
    assert v.live_session_errors(manifest)


def test_multicontext_observation_never_drops_unknown_targets():
    v = verifier()
    targets = {"one": dict(targetId="one", browserContextId="a"),
               "two": dict(targetId="two", browserContextId="b")}
    events = [dict(kind="Network.requestWillBeSent", data=dict(targetId=t)) for t in ("one", "two", "unknown")]
    kept, excluded = v.context_events(events, "a", targets)
    assert [e["data"]["targetId"] for e in kept] == ["one", "unknown"]
    assert excluded == [dict(event=events[1], target=targets["two"], reason="different browserContextId")]


@pytest.mark.parametrize("defect", ["none", "full", "hole", "end", "width"])
def test_tile_extent_coverage_is_not_image_existence(defect):
    v = verifier()
    view = dict(images=[dict(type="full", x=0, y=0, width=305, height=1559),
                        dict(type="tile", x=0, y=0, width=305, height=900),
                        dict(type="tile", x=0, y=800, width=305, height=759)])
    if defect == "full":
        view["images"].pop(0)
    elif defect == "hole":
        view["images"][-1]["y"] = 901
    elif defect == "end":
        view["images"][-1]["height"] = 700
    elif defect == "width":
        view["images"][-1]["width"] = 300
    assert bool(v.image_coverage_errors(view, dict(document=dict(clientWidth=305, scrollHeight=1559)))) == (defect != "none")


def test_builtin_contract_and_scope_commands_need_no_browser_or_role():
    for flag in ("--check-evidence-contract", "--check-scope"):
        result = subprocess.run([sys.executable, "-S", str(ROOT / "tools/verify_wordfreq_html.py"), flag], capture_output=True)
        expected_dirty = flag == "--check-scope" and bool(verifier().provenance()["product_status"])
        assert result.returncode == int(expected_dirty), result.stderr + result.stdout
        report = json.loads(result.stdout)
        assert bool(report["errors"]) == expected_dirty
        if flag == "--check-evidence-contract":
            assert report["synthetic"] is True
            assert report["product_acceptance"] is False
            assert report["clean"] == "accepted-predicate-only"
            assert len(report["rejected"]) >= 15


def test_guide_commands_schema_cases_and_ac_match_real_parser():
    import re
    import shlex
    v = verifier()
    guide = (ROOT / "docs/wordfreq-html-verification.md").read_text()
    commands = [line for line in guide.splitlines() if line.startswith("env PYTHONPATH=")
                and "tools/verify_wordfreq_html.py" in line]
    parsed = [v.parser().parse_args(shlex.split(line)[4:]) for line in commands]
    assert {p.mode for p in parsed} >= {"capture", "review-session", "finalize"}
    assert any(p.check_evidence_contract for p in parsed)
    assert any(p.check_scope for p in parsed)
    for p in parsed:
        if p.mode in {"review-session", "finalize"}:
            assert p.role == "quality"
            assert p.actor == "argonauts-uat-quality"
            assert "quality" in p.output_dir.parts
        if p.mode == "finalize":
            assert p.review_ledger == p.output_dir / "reviews.json"
    assert all(f"`{field}`" in guide for field in v.REVIEW_FIELDS)
    assert all(f"`{case['id']}`" in guide for case in v.fixed_cases())
    assert all(f"AC{i}" in guide for i in range(1, 7))
    examples = re.findall(r"```json\n(.*?)\n```", guide, re.S)
    assert len(examples) == 1
    example = json.loads(examples[0])
    assert set(example["reviews"][0]) == set(v.REVIEW_FIELDS)
    assert example["reviews"][0]["judgment"] == "unverified"
    assert v.ledger_errors({}, example, v.now())
    for term in ("tracked background", "rawRange", "browser-network.json", "finalize-requested",
                 "observation_end", "verification_finished", "REQ-09", "REQ-10"):
        assert term in guide
    assert "[ブラウザ検証手順](docs/wordfreq-html-verification.md)" in (ROOT / "README.md").read_text()


def test_dirty_review_session_always_saves_end_provenance(tmp_path, monkeypatch):
    from types import SimpleNamespace
    v = verifier()
    monkeypatch.setenv("HERMES_PROFILE", "argonauts-uat-builder")
    state = dict(head="h", status="dirty", product_status=" M tools/new.py", untracked_product=[], product_diff="diff")
    monkeypatch.setattr(v, "provenance", lambda: state)
    monkeypatch.setattr(v, "scope_report", lambda: dict(base=v.SCOPE_BASE, target="h", errors=[]))
    output = tmp_path / "builder" / "fresh"
    assert v.review_session(SimpleNamespace(role="builder", actor="argonauts-uat-builder",
        output_dir=output, session_timeout=1)) == 1
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["end_provenance"] == state
    assert manifest["independent_acceptance"] is False


def test_scope_rejects_dirty_and_untracked_code(monkeypatch):
    v = verifier()
    monkeypatch.setattr(v, "provenance", lambda: dict(product_status="?? tools/new.py",
        untracked_product=[dict(path="tools/new.py", sha256="hash", content_utf8="actual")]))
    assert any("dirty" in e for e in v.scope_report()["errors"])
