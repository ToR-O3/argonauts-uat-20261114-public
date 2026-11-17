"""Synthetic lifecycle controls, NOT product viewing or independent acceptance."""
import copy
from contextlib import nullcontext
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026-01-01T00:00:02+00:00"


@pytest.fixture
def lifecycle(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("finalization_verifier", ROOT / "tools/verify_wordfreq_html.py")
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)
    state = SimpleNamespace(v=v, output=tmp_path / "quality" / "synthetic", role="quality",
                            fault=None, immutable={}, ledger=None, writes=[])
    clean = dict(head="controlled-head", product_status="", untracked_product=[], status="")
    monkeypatch.setattr(v, "provenance", lambda: copy.deepcopy(clean))
    monkeypatch.setattr(v, "scope_report", lambda: dict(errors=[]))
    monkeypatch.setattr(v, "now", lambda: STAMP)
    monkeypatch.setattr(v, "run_suite", lambda output: None)
    monkeypatch.setattr(v, "self_test_network", lambda args: 0)
    # External capture/browser/environment boundaries only; finalization is real.
    monkeypatch.setattr(v, "generate_cases", lambda output: [dict(id=name, format="html", views=[]) for name in ("empty", "long")])
    monkeypatch.setattr(v, "capture_errors", lambda *args: [])
    browser = SimpleNamespace(version="controlled", launch_record={})
    monkeypatch.setattr(v, "instrumented_browser", lambda *args: nullcontext(browser))
    api = ModuleType("playwright.sync_api")
    api.sync_playwright = lambda: nullcontext(None)
    monkeypatch.setitem(sys.modules, "playwright.sync_api", api)
    monkeypatch.setitem(sys.modules, "playwright", ModuleType("playwright"))
    def collect(browser, case, width, output, live):
        folder = output / case["id"] / str(width)
        folder.mkdir(parents=True)
        raw = folder / "raw.json"
        raw.write_bytes(b'{"rawRange": [1.25, 2.75]}')
        images = []
        for kind in ("full", "tile"):
            image = folder / (kind + ".png")
            image.write_bytes((case["id"] + str(width) + kind).encode())
            images.append(dict(path=str(image), type=kind, width=width, height=900))
        view = dict(width=width, raw=str(raw), network=str(folder / "network.json"),
                    images=images, reviewed_images=[], verdict="pending-review", errors=[])
        v.save_json(folder / "derived.json", view)
        live.append(dict(view=view, page=SimpleNamespace(wait_for_timeout=lambda ms: None),
                         observer=SimpleNamespace(browser_cdp=SimpleNamespace(detach=lambda: None)),
                         context=SimpleNamespace(close=lambda: None)))
        return view
    monkeypatch.setattr(v, "collect_view", collect)
    flushes = []
    def snapshot(*args):
        flushes.append(1)
        return STAMP, (["late network error"] if state.fault == "late" and len(flushes) >= 5 else [])
    monkeypatch.setattr(v, "snapshot_live", snapshot)
    def evidence(manifest, ledger, output, end, **kwargs):
        return v.ledger_errors(manifest, ledger, end) + [e for c in manifest["cases"] for view in c["views"] for e in v.view_identity_errors(view)]
    monkeypatch.setattr(v, "evidence_errors", evidence)
    original_save = v.save_json
    def save(path, value):
        state.writes.append((path, copy.deepcopy(value)))
        original_save(path, value)
        if path.name == "manifest.json" and value["verdict"] == "pending-review" and state.ledger is None:
            ledger = {k: value[k] for k in ("session", "head", "actor", "root")}
            ledger["reviews"] = [dict(actor=value["actor"], image=i["path"], sha256=i["sha256"],
                viewed_at=STAMP, scale=1, extent=[0, 0, i["width"], i["height"]],
                raw=view["raw"], raw_sha256=view["raw_sha256"], judgment="readable", notes="SYNTHETIC control only")
                for c in value["cases"] for view in c["views"] for i in view["images"]]
            ledger["ac_reviews"] = [dict(ac=ac, judgment="accepted", notes="synthetic", evidence=refs)
                                     for ac, refs in value["ac_index"].items()]
            state.ledger = copy.deepcopy(ledger)
            original_save(state.output / "reviews.json", ledger)
            original_save(state.output / "finalize-request.json", dict(session=value["session"],
                          ledger_sha256=v.digest(state.output / "reviews.json"), at=STAMP))
            state.immutable = {str(p): p.read_bytes() for p in state.output.rglob("*") if p.name in {"raw.json", "full.png", "tile.png", "reviews.json"}}
    monkeypatch.setattr(v, "save_json", save)
    def run(role="quality"):
        state.role = role
        state.output = tmp_path / role / "synthetic"
        monkeypatch.setenv("HERMES_PROFILE", v.ACTORS[role])
        code = v.review_session(SimpleNamespace(role=role, actor=None, output_dir=state.output,
                               browser="controlled", session_timeout=1))
        return code, v.load_json(state.output / "manifest.json")
    state.run = run
    return state


@pytest.mark.parametrize("role,verdict", [("quality", "accepted"), ("builder", "builder-reviewed")])
def test_real_owner_projects_exact_ledger_into_every_persisted_view(lifecycle, role, verdict):
    s = lifecycle
    code, manifest = s.run(role)
    assert code == 0
    assert manifest["verdict"] == verdict
    assert manifest["independent_acceptance"] is (role == "quality")
    assert [c["id"] for c in manifest["cases"]] == ["empty", "long"]
    for case in manifest["cases"]:
        assert [view["width"] for view in case["views"]] == [1280, 320]
        for view in case["views"]:
            assert view["verdict"] == verdict
            assert view["reviewed_images"] == [dict(path=i["path"], sha256=i["sha256"], viewed_at=STAMP) for i in view["images"]]
            assert s.v.load_json(s.output / case["id"] / str(view["width"]) / "derived.json") == view
    assert "pending-review" not in str(manifest)
    assert all(Path(p).read_bytes() == data for p, data in s.immutable.items())
    assert s.writes[-1][0] == s.output / "manifest.json"
    assert s.v.final_review_errors(manifest, s.ledger, s.output) == []
