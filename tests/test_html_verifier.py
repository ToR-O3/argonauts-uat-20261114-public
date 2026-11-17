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


def test_geometry_accepts_raw_own_vertical_overhang_and_empty_ranges():
    v = verifier()
    raw = raw_record()
    original = copy.deepcopy(raw)
    assert v.geometry_errors(raw) == []
    assert raw == original
    assert json.loads(json.dumps(raw)) == raw


@pytest.mark.parametrize("defect", ["overflow", "column", "clip", "overlap", "missing-char", "missing-empty", "offset", "missing-elements", "missing-texts"])
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
    else:
        raw["texts"] = []
    assert v.geometry_errors(raw), defect


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


def test_browser_files_and_capture_entrypoint_exist():
    v = verifier()
    assert (ROOT / "tools/wordfreq_html_geometry.js").is_file()
    assert callable(getattr(v, "capture", None)), "actual browser capture entrypoint required"


def local_network():
    return dict(start="2026-01-01T00:00:00+00:00", end="2026-01-01T00:00:01+00:00",
                coverage=dict(context=True, browserTargets=True, mainCDP=True), errors=[],
                events=[dict(kind="page-cdp-ready", data={}),
                        dict(kind="request", data=dict(url="file:///control.html"))])


def test_browser_ui_exclusion_requires_pre_open_target_identity():
    v = verifier()
    net = local_network()
    event = dict(kind="target-created", data=dict(targetInfo=dict(targetId="ui1", type="browser_ui",
                url="chrome://omnibox-popup.top-chrome/", canAccessOpener=False)))
    net["events"].insert(0, event)
    assert v.network_errors(net, "file:///control.html") == []
    bad = copy.deepcopy(net)
    bad["events"][0]["data"]["targetInfo"]["type"] = "page"
    assert v.network_errors(bad, "file:///control.html")
    late = local_network()
    late["events"].append(event)
    assert v.network_errors(late, "file:///control.html")


def test_unimplemented_review_mode_cannot_succeed(tmp_path):
    result = subprocess.run([sys.executable, str(ROOT / "tools/verify_wordfreq_html.py"),
                             "--role", "builder", "--output-dir", str(tmp_path),
                             "--mode", "review-session"], capture_output=True)
    assert result.returncode != 0
