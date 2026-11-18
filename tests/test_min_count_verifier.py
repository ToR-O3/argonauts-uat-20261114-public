"""Phase 4 real-file tests; synthetic browser evidence is never acceptance."""
import importlib.util
import json
import os
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def driver():
    path = ROOT / "tools/verify_wordfreq_min_count.py"
    assert path.is_file(), "baseline driver implementation is missing"
    spec = importlib.util.spec_from_file_location("min_count_verifier", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_browser_free_real_cli_baseline_matrix(tmp_path):
    v = driver()
    records = v.generate_baseline_cases(tmp_path)
    assert len(records) == 12
    assert [r["format"] for r in records[:4]] == ["text", "text", "json", "html"]
    for record in records:
        assert record["exit"] == 0
        assert Path(record["stderr"]).read_bytes() == b""
        assert "--min-count" not in record["argv"]
        assert record["argv"][1:3] == ["-m", "wordfreq"]
        assert record["cwd"] == str(ROOT)
        assert Path(record["input"]).read_bytes() == record["body"].encode("utf-8")
        assert v.cli_errors(record) == []
    assert records[0]["argv"][-1] == records[0]["input"]
    assert Path(records[0]["stdout"]).read_bytes() == Path(records[1]["stdout"]).read_bytes()
    assert records[3]["pairs"] == [["hello", 3], ["zoo", 2], ["apple", 2], ["one", 2],
                                   ["two", 1], ["b", 1], ["c", 1], ["d", 1], ["e", 1], ["f", 1]]
    assert records[3]["total"] == 17


def test_browser_free_entrypoint_requires_real_capture_pipeline(tmp_path):
    v = driver()
    assert callable(getattr(v, "main", None)), "baseline entrypoint is not implemented"
    assert callable(getattr(v, "validate_baseline", None)), "read-only validator is missing"
    assert v.main(["--mode", "capture", "--role", "builder", "--output-dir", str(tmp_path),
                   "--baseline-dir", str(tmp_path)]) != 0
    assert not (tmp_path / "index.json").exists()


@pytest.fixture
def browser_free_repo(tmp_path, monkeypatch):
    import shutil
    import subprocess
    v = driver()
    repo = tmp_path / "repo"
    repo.mkdir()
    for name in ("wordfreq", "tools"):
        shutil.copytree(ROOT / name, repo / name, ignore=shutil.ignore_patterns("__pycache__"))
    (repo / "tests").mkdir()
    for name in ("test_cli.py", "test_html_verifier.py"):
        shutil.copy2(ROOT / "tests" / name, repo / "tests" / name)
    shutil.copy2(__file__, repo / "tests/test_min_count_verifier.py")
    shutil.copy2(ROOT / "pyproject.toml", repo / "pyproject.toml")
    def git(*args):
        return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True).stdout.decode().strip()
    git("init", "-q")
    git("config", "user.name", "Synthetic baseline fixture")
    git("config", "user.email", "fixture@example.invalid")
    git("add", ".")
    git("commit", "-qm", "feat(04-01): synthetic fixture formal task")
    monkeypatch.setattr(v, "ROOT", repo)
    monkeypatch.setattr(v, "BASE", git("rev-parse", "HEAD"))
    monkeypatch.setenv("HERMES_PROFILE", "argonauts-uat-builder")
    monkeypatch.setenv("HERMES_KANBAN_TASK", "synthetic-fixture-task")
    monkeypatch.setenv("HERMES_KANBAN_RUN_ID", "synthetic-fixture-run")
    return v, repo


def synthetic_collect(case, width, output):
    """Deliberately synthetic boundary; never a real browser/readability claim."""
    import struct
    import zlib
    folder = output / case["id"] / str(width)
    folder.mkdir(parents=True)
    raw = folder / "raw.json"
    raw.write_text(json.dumps(dict(synthetic=True, viewport=dict(width=width, height=900, dpr=1, scale=1),
                                  document=dict(clientWidth=width, scrollHeight=900))))
    network = folder / "network.json"
    network.write_text(json.dumps(dict(synthetic=True, interval="synthetic-only")))
    png = folder / "full.png"
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))
    png.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, 900, 8, 2, 0, 0, 0)) +
                    chunk(b"IDAT", zlib.compress((b"\0" + b"\xff" * (width*3)) * 900)) + chunk(b"IEND", b""))
    return dict(width=width, raw=str(raw), network=str(network), errors=[], reviewed_images=[],
                verdict="synthetic-only", images=[dict(path=str(png), type="full", x=0, y=0, width=width, height=900)],
                browser=dict(synthetic=True, viewport=dict(width=width, height=900, dpr=1, scale=1)))


def test_browser_free_entrypoint_real_files_to_readonly_validator(browser_free_repo, tmp_path):
    v, repo = browser_free_repo
    output = tmp_path / "baseline"
    argv = ["--mode", "baseline", "--role", "builder", "--output-dir", str(output)]
    assert callable(getattr(v, "validate_baseline", None)), "baseline validator missing"
    assert v.main(argv, collector=synthetic_collect) == 0
    before = {str(p): p.read_bytes() for p in output.rglob("*") if p.is_file()}
    assert v.validate_baseline(output, allow_synthetic=True) == []
    assert v.validate_baseline(output), "synthetic data must not validate as real evidence"
    index = json.loads((output / "index.json").read_text())
    assert index["synthetic"] and not index["independent_acceptance"]
    assert index["run"] == "synthetic-fixture-run"
    assert index["task"] == "synthetic-fixture-task"
    assert len(index["cases"]) == 12
    assert len([view for c in index["cases"] for view in c["views"]]) == 18
    assert set(index["ac_index"]) == {f"AC{i}" for i in range(1, 8)}
    assert all(a["verdict"] == "pending" for a in index["ac_index"].values())
    assert v.main(argv, collector=synthetic_collect) != 0
    assert before == {str(p): p.read_bytes() for p in output.rglob("*") if p.is_file()}


def test_browser_free_validator_rejects_forged_scope_and_argv(browser_free_repo, tmp_path):
    import copy
    v, repo = browser_free_repo
    output = tmp_path / "baseline"
    assert v.main(["--mode", "baseline", "--role", "builder", "--output-dir", str(output)],
                  collector=synthetic_collect) == 0
    index = json.loads((output / "index.json").read_text())
    assert v.baseline_errors(index, output, allow_synthetic=True) == []
    wrong = copy.deepcopy(index)
    wrong["cases"][0]["argv"] += ["--min-count", "1"]
    assert v.baseline_errors(wrong, output, allow_synthetic=True), "baseline argv must forbid min-count"
    wrong = copy.deepcopy(index)
    wrong["provenance"]["changed_paths"] = ["wordfreq/__main__.py"]
    assert v.baseline_errors(wrong, output, allow_synthetic=True), "scope must be derived, not trusted"


@pytest.fixture
def browser_free_saved(browser_free_repo, tmp_path):
    v, repo = browser_free_repo
    root = tmp_path / "baseline"
    assert v.main(["--mode", "baseline", "--role", "builder", "--output-dir", str(root)],
                  collector=synthetic_collect) == 0
    return v, root


@pytest.mark.parametrize("defect", ["format", "width", "input", "stdout", "html", "raw", "image",
                                   "sha", "request", "head", "root", "scope", "empty", "ac7",
                                   "timeline", "marker", "index-sha", "extra-file"])
def test_browser_free_mutations(browser_free_saved, defect):
    import copy
    v, root = browser_free_saved
    index = json.loads((root / "index.json").read_text())
    assert v.validate_baseline(root, allow_synthetic=True) == []
    wrong = copy.deepcopy(index)
    html = wrong["cases"][3]
    if defect == "format":
        wrong["cases"].pop(2)
    elif defect == "width":
        html["views"].pop()
    elif defect in {"input", "stdout", "html", "raw", "image"}:
        path = html[defect] if defect in {"input", "stdout", "html"} else (
            html["views"][0]["raw"] if defect == "raw" else html["views"][0]["images"][0]["path"])
        Path(path).unlink()
    elif defect == "sha":
        Path(html["stdout"]).write_bytes(b"changed bytes")
    elif defect in {"request", "head", "root"}:
        wrong[defect] = "different"
    elif defect == "scope":
        wrong["provenance"]["tree"] = {}
    elif defect == "empty":
        wrong["cases"] = []
    elif defect == "ac7":
        del wrong["ac_index"]["AC7"]
    elif defect == "timeline":
        wrong["started"] = "2000-01-01T00:00:00+00:00"
    elif defect == "marker":
        (root / "index.json").unlink()
        assert v.validate_baseline(root, allow_synthetic=True)
        return
    elif defect == "index-sha":
        (root / "index.sha256").write_text("wrong\n")
        assert v.validate_baseline(root, allow_synthetic=True)
        return
    else:
        (root / "unindexed.bin").write_bytes(b"unindexed")
    assert v.baseline_errors(wrong, root, allow_synthetic=True), defect


@pytest.mark.parametrize("defect", ["dirty-product", "dirty-tests", "dirty-config", "untracked-shadow",
                                   "scope-unavailable", "partial-browser", "existing-empty-root", "wrong-profile"])
def test_browser_free_capture_refuses_unattributable_or_partial(browser_free_repo, tmp_path, monkeypatch, defect):
    v, repo = browser_free_repo
    output = tmp_path / "baseline"
    collector = synthetic_collect
    if defect.startswith("dirty-"):
        file = {"dirty-product": "wordfreq/__main__.py", "dirty-tests": "tests/test_cli.py",
                "dirty-config": "pyproject.toml"}[defect]
        with (repo / file).open("a") as stream:
            stream.write("\n# dirty control\n")
    elif defect == "untracked-shadow":
        (repo / "pytest.py").write_text("# shadow control\n")
    elif defect == "scope-unavailable":
        monkeypatch.setattr(v, "BASE", "1" * 40)
    elif defect == "partial-browser":
        def collector(*args):
            raise ValueError("synthetic boundary intentionally unavailable")
    elif defect == "existing-empty-root":
        output.mkdir()
    else:
        monkeypatch.setenv("HERMES_PROFILE", "argonauts-uat-quality")
    assert v.main(["--mode", "baseline", "--role", "builder", "--output-dir", str(output)], collector=collector) != 0
    assert not (output / "index.json").exists()


def test_browser_free_historical_baseline_reads_in_successor_worktree(browser_free_repo, tmp_path, monkeypatch):
    import shutil
    v, repo = browser_free_repo
    relative = Path(".planning/argonauts/r-e476c11d/baseline")
    output = repo / relative
    assert v.main(["--mode", "baseline", "--role", "builder", "--output-dir", str(output)],
                  collector=synthetic_collect) == 0
    successor = tmp_path / "successor"
    shutil.copytree(repo, successor)
    before = (successor / relative / "index.json").read_bytes()
    monkeypatch.setattr(v, "ROOT", successor)
    assert v.validate_baseline(successor / relative, allow_synthetic=True) == []
    assert (successor / relative / "index.json").read_bytes() == before
    assert v.validate_baseline(successor / relative.parent, allow_synthetic=True)


def synthetic_suite(output):
    """Explicit full-suite boundary, not a real regression result."""
    (output / "suite.xml").write_text('<testsuites><testsuite tests="1" failures="0" errors="0" skipped="0"/></testsuites>')
    (output / "suite.stdout").write_bytes(b"synthetic suite boundary\n")
    (output / "suite.stderr").write_bytes(b"")
    return dict(synthetic=True, exit=0, collected=1)


@pytest.fixture
def browser_free_capture(browser_free_saved, tmp_path):
    v, baseline = browser_free_saved
    root = tmp_path / "builder" / "capture"
    argv = ["--mode", "capture", "--role", "builder", "--output-dir", str(root),
            "--baseline-dir", str(baseline)]
    assert v.main(argv, collector=synthetic_collect, suite_runner=synthetic_suite) == 0
    return v, root, baseline


def test_browser_free_capture_entrypoint_replays_baseline_and_thresholds(browser_free_saved, tmp_path):
    v, baseline = browser_free_saved
    root = tmp_path / "builder" / "capture"
    assert callable(getattr(v, "capture", None)), "capture pipeline is missing"
    assert v.main(["--mode", "capture", "--role", "builder", "--output-dir", str(root),
                   "--baseline-dir", str(baseline)], collector=synthetic_collect, suite_runner=synthetic_suite) == 0
    manifest = v.parts.load_json(root / "manifest.json")
    assert manifest["verdict"] == "pending-review"
    assert manifest["independent_acceptance"] is False
    assert manifest["synthetic"] is True
    assert len(manifest["cases"]) > 50
    assert manifest["baseline"]["index_sha256"] == v.parts.digest(baseline / "index.json")
    assert set(manifest["ac_index"]) == {f"AC{i}" for i in range(1, 8)}
    assert all(manifest["comparisons"][c["id"]]["bytes_equal"] for c in manifest["cases"] if c.get("baseline_id"))
    before = {str(p): v.parts.digest(p) for p in root.rglob("*") if p.is_file()}
    assert v.validate_capture(root, baseline, allow_synthetic=True) == []
    assert v.validate_capture(root, baseline), "synthetic boundary must not become real integration"
    assert before == {str(p): v.parts.digest(p) for p in root.rglob("*") if p.is_file()}


@pytest.mark.parametrize("wrong_argv", [False, True])
def test_browser_free_saved_capture_relocates_suite_argv(browser_free_saved, tmp_path, monkeypatch, wrong_argv):
    import shutil
    v, baseline = browser_free_saved
    repo = v.ROOT
    relative = Path(".planning/builder/capture")
    root = repo / relative

    def recorded_suite(output):
        result = synthetic_suite(output)
        # Exercise the real command predicate without running a recursive suite.
        return dict(result, synthetic=False,
                    argv=[sys.executable, "-m", "pytest", "--junitxml", str(output / "suite.xml")],
                    environment={"WORDFREQ_MIN_COUNT_BASELINE_ROOT": None,
                                 "WORDFREQ_MIN_COUNT_CAPTURE_ROOT": None})

    assert v.main(["--mode", "capture", "--role", "builder", "--output-dir", str(root),
                   "--baseline-dir", str(baseline)], collector=synthetic_collect,
                  suite_runner=recorded_suite) == 0
    successor = tmp_path / "successor"
    shutil.copytree(repo, successor)
    moved = successor / relative
    monkeypatch.setattr(v, "ROOT", successor)
    if wrong_argv:
        suite = v.parts.load_json(moved / "suite.json")
        suite["argv"][-1] = str(root / "wrong.xml")
        v.parts.save_json(moved / "suite.json", suite)
        manifest = v.parts.load_json(moved / "manifest.json")
        manifest["artifacts"][str(root / "suite.json")] = v.parts.digest(moved / "suite.json")
        v.seal_capture(manifest, moved)
    before = {str(p): v.parts.digest(p) for p in moved.rglob("*") if p.is_file()}
    errors = v.validate_capture(moved, baseline, allow_synthetic=True)
    assert errors == (["suite command/opt-in recursion mismatch"] if wrong_argv else [])
    assert before == {str(p): v.parts.digest(p) for p in moved.rglob("*") if p.is_file()}
    assert v.validate_capture(root, baseline, allow_synthetic=True) == ["capture root binding differs"]


@pytest.mark.parametrize("defect", ["case", "width", "total", "ac7", "head", "root", "actor", "scope", "suite-zero", "sha", "png", "raw", "baseline", "environment"])
def test_browser_free_saved_capture_mutations(browser_free_capture, defect):
    import copy
    v, root, baseline = browser_free_capture
    assert v.validate_capture(root, baseline, allow_synthetic=True) == []
    m = copy.deepcopy(v.parts.load_json(root / "manifest.json"))
    html = next(c for c in m["cases"] if c["format"] == "html")
    if defect == "case":
        m["cases"].pop()
    elif defect == "width":
        html["views"].pop()
    elif defect == "total":
        html["total"] += 1
    elif defect == "ac7":
        del m["ac_index"]["AC7"]
    elif defect in {"head", "root", "actor"}:
        m[defect] = "different"
    elif defect == "scope":
        m["scope"]["tree"] = {}
    elif defect == "suite-zero":
        (root / "suite.xml").write_text('<testsuites><testsuite tests="0"/></testsuites>')
    elif defect == "sha":
        Path(html["stdout"]).write_bytes(b"changed")
    elif defect in {"png", "raw"}:
        path = html["views"][0]["images"][0]["path"] if defect == "png" else html["views"][0]["raw"]
        Path(path).write_bytes(b"changed")
    elif defect == "baseline":
        m["baseline"]["index_sha256"] = "0" * 64
    else:
        m["environment"]["executable"] = "other-python"
    assert v.capture_errors(m, root, baseline, allow_synthetic=True), defect


def synthetic_ledger(v, m, baseline):
    """Synthetic attestations exercise publication, never actual image viewing."""
    views = [view for c in m["cases"] for view in c["views"]] + v.baseline_review_views(baseline, synthetic=True)
    ledger = {k: m[k] for k in ("request", "session", "head", "actor", "root", "run", "task")}
    ledger["reviews"] = [dict(actor=m["actor"], image=i["path"], sha256=v.parts.digest(i["path"]),
        raw=view["raw"], raw_sha256=v.parts.digest(view["raw"]), viewed_at=v.parts.now(), scale=1,
        extent=[0, 0, i["width"], i["height"]], judgment="readable", notes="SYNTHETIC extent/identity control only")
        for view in views for i in view["images"]]
    ledger["ac_reviews"] = [dict(ac=ac, judgment="accepted", notes="SYNTHETIC acceptance control only",
                                      evidence=m["ac_index"][ac]["evidence"]) for ac in v.ACS]
    ledger["source_order"] = dict(head=m["head"], path="wordfreq/__main__.py",
        sha256=v.parts.digest(v.ROOT / "wordfreq/__main__.py"), lines=[34, 35, 36, 37, 38, 44],
        judgment="filter-before-top-original-total", notes="SYNTHETIC source-order control only")
    return ledger


def test_browser_free_live_owner_normal_publication(browser_free_saved, tmp_path):
    v, baseline = browser_free_saved
    root = tmp_path / "builder" / "review"
    assert callable(getattr(v, "review_session", None)), "live owner pipeline missing"
    def hook(m):
        ledger = synthetic_ledger(v, m, baseline)
        v.parts.save_json(root / "reviews.json", ledger)
        assert v.main(["--mode", "finalize", "--role", "builder", "--output-dir", str(root),
                       "--baseline-dir", str(baseline), "--review-ledger", str(root / "reviews.json")],
                      collector=synthetic_collect) == 0
        assert v.parts.load_json(root / "manifest.json")["verdict"] == "pending-review"
        assert v.parts.load_json(root / "finalize-request.json")["session"] == m["session"]
    assert v.main(["--mode", "review-session", "--role", "builder", "--output-dir", str(root),
                   "--baseline-dir", str(baseline)], collector=synthetic_collect,
                  suite_runner=synthetic_suite, owner_hook=hook) == 0
    m = v.parts.load_json(root / "manifest.json")
    assert m["verdict"] == "builder-reviewed" and not m["independent_acceptance"]
    assert m["synthetic"] and set(m["ac_verdicts"]) == set(v.ACS)
    assert all(view["verdict"] == "builder-reviewed" for c in m["cases"] for view in c["views"])
    assert v.final_publication_errors(m, v.parts.load_json(root / "reviews.json"), root, baseline, synthetic=True) == []
    assert v.main(["--mode", "finalize", "--role", "builder", "--output-dir", str(root),
                   "--baseline-dir", str(baseline), "--review-ledger", str(root / "reviews.json")],
                  collector=synthetic_collect) != 0


@pytest.mark.parametrize("defect", ["unviewed", "extra", "duplicate", "ac7", "scope", "head", "actor", "root",
    "late-network", "write-failure", "derived", "zero-suite", "ended", "png", "raw", "baseline-unviewed", "source-order"])
def test_browser_free_owner_rejects_mutations(browser_free_saved, tmp_path, monkeypatch, defect):
    v, baseline = browser_free_saved
    root = tmp_path / "builder" / "review"
    assert callable(getattr(v, "review_session", None)), "live owner pipeline missing"
    def hook(m):
        ledger = synthetic_ledger(v, m, baseline)
        if defect == "unviewed":
            ledger["reviews"].pop(0)
        elif defect == "baseline-unviewed":
            ledger["reviews"].pop()
        elif defect == "extra":
            ledger["reviews"].append(dict(ledger["reviews"][0], image="/extra.png"))
        elif defect == "duplicate":
            ledger["reviews"].append(ledger["reviews"][0])
        elif defect == "ac7":
            ledger["ac_reviews"].pop()
        elif defect in {"head", "actor", "root"}:
            ledger[defect] = "different"
        elif defect == "source-order":
            ledger.pop("source_order")
        elif defect == "scope":
            m["scope"]["base"] = "old-scope"
        elif defect == "ended":
            m["ended"] = v.parts.now()
        elif defect in {"png", "raw"}:
            view = next(c for c in m["cases"] if c["format"] == "html")["views"][0]
            Path(view["raw"] if defect == "raw" else view["images"][0]["path"]).write_bytes(b"mutated")
        elif defect == "zero-suite":
            (root / "suite.xml").write_text('<testsuites><testsuite tests="0"/></testsuites>')
        v.parts.save_json(root / "reviews.json", ledger)
        v.parts.save_json(root / "finalize-request.json", dict(session=m["session"], ledger_sha256=v.parts.digest(root / "reviews.json"), at=v.parts.now()))
        if defect == "late-network":
            monkeypatch.setattr(v, "finish_observation", lambda *a: (v.parts.now(), ["late external attempt"]))
        elif defect in {"write-failure", "derived"}:
            original = v.parts.save_json
            fired = False
            def save(path, value):
                nonlocal fired
                if Path(path).name == "derived.json" and value.get("verdict") == "builder-reviewed" and not fired:
                    fired = True
                    if defect == "write-failure":
                        raise OSError("synthetic mid-publication storage error")
                    value = dict(value, verdict="pending-review")
                original(path, value)
            monkeypatch.setattr(v.parts, "save_json", save)
    assert v.main(["--mode", "review-session", "--role", "builder", "--output-dir", str(root),
                   "--baseline-dir", str(baseline)], collector=synthetic_collect,
                  suite_runner=synthetic_suite, owner_hook=hook) != 0
    m = v.parts.load_json(root / "manifest.json")
    assert m["verdict"] == "unverified" and m["errors"] and not m["independent_acceptance"]
    assert set(m["ac_verdicts"].values()) == {"unverified"}
    for c in m["cases"]:
        for view in c["views"]:
            assert view["verdict"] == "unverified"
            assert v.parts.load_json(Path(view["raw"]).parent / "derived.json")["verdict"] == "unverified"


if os.environ.get("WORDFREQ_MIN_COUNT_CAPTURE_ROOT") and os.environ.get("WORDFREQ_MIN_COUNT_BASELINE_ROOT"):
    def test_saved_capture_originals_readonly():
        v = driver()
        root = Path(os.environ["WORDFREQ_MIN_COUNT_CAPTURE_ROOT"]).resolve()
        baseline = Path(os.environ["WORDFREQ_MIN_COUNT_BASELINE_ROOT"]).resolve()
        before = {str(p): v.parts.digest(p) for p in root.rglob("*") if p.is_file()}
        assert before
        assert v.validate_capture(root, baseline) == []
        assert before == {str(p): v.parts.digest(p) for p in root.rglob("*") if p.is_file()}

    @pytest.mark.parametrize("defect", ["case", "width", "head", "actor", "ac7", "total", "scope", "empty", "acceptance", "hash"])
    def test_saved_capture_manifest_controls(defect):
        import copy
        v = driver()
        root = Path(os.environ["WORDFREQ_MIN_COUNT_CAPTURE_ROOT"]).resolve()
        baseline = Path(os.environ["WORDFREQ_MIN_COUNT_BASELINE_ROOT"]).resolve()
        assert v.validate_capture(root, baseline) == []
        m = copy.deepcopy(v.parts.load_json(root / "manifest.json"))
        if defect == "case":
            m["cases"].pop()
        elif defect == "width":
            next(c for c in m["cases"] if c["format"] == "html")["views"].pop()
        elif defect in {"head", "actor"}:
            m[defect] = "other"
        elif defect == "ac7":
            del m["ac_index"]["AC7"]
        elif defect == "total":
            m["cases"][0]["total"] += 1
        elif defect == "scope":
            m["scope"]["tree"] = {}
        elif defect == "empty":
            m["cases"] = []
        elif defect == "acceptance":
            m["independent_acceptance"] = True
        else:
            key = next(iter(m["artifacts"]))
            m["artifacts"][key] = "0" * 64
        assert v.capture_errors(m, root, baseline)


def assert_runbook_contract(document):
    """Check executable examples against the actual parser, not a mock CLI."""
    import re
    import shlex
    v = driver()
    commands = re.findall(r"^env .* tools/verify_wordfreq_min_count\.py (.+)$", document, re.M)
    assert len(commands) == 4, "four public mode examples required"
    modes = {}
    for command in commands:
        args = v.parser().parse_args(shlex.split(command))
        assert args.mode not in modes
        modes[args.mode] = args
        assert str(args.output_dir).startswith(f".planning/argonauts/{v.REQUEST}/{args.role}/")
        if args.mode != "baseline":
            assert args.baseline_dir == Path(f".planning/argonauts/{v.REQUEST}/baseline")
    assert set(modes) == {a for a in v.parser()._actions if a.dest == "mode" for a in a.choices}
    assert modes["baseline"].role == modes["capture"].role == "builder"
    review, final = modes["review-session"], modes["finalize"]
    assert review.role == final.role == "quality"
    assert final.output_dir == review.output_dir
    assert final.review_ledger == review.output_dir / "reviews.json"
    assert re.findall(r"^\| (AC\d+) \| REQ-(\d+) \|", document, re.M) == [
        (ac, str(15+i)) for i, ac in enumerate(v.ACS)]
    for required in ("fresh root", "baseline不変", "保存gate", "標準添付gate", "PM原本読取りgate",
                     "argonauts-uat-quality", "Builder自己承認不可", "owner実終了", "全view/全derived",
                     "headが変わったら", "CI未報告は成功でない", "independent_acceptance=true"):
        assert required in document, required
    for i in range(1, 15):
        assert f"| UI{i:02d} |" in document
    assert v.BASE in document
    assert "openspec verify " not in document
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    example = "python -m wordfreq input.txt --min-count 2 --top 1 --format json"
    assert example in readme and example in document


def test_browser_free_runbook_matches_real_driver():
    path = ROOT / "docs/wordfreq-min-count-verification.md"
    assert path.is_file(), "quality runbook is missing"
    assert_runbook_contract(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("defect", ["mode", "flag", "ac7", "baseline", "delivery", "root", "owner", "empty"])
def test_browser_free_runbook_rejects_mutations(defect):
    document = (ROOT / "docs/wordfreq-min-count-verification.md").read_text(encoding="utf-8")
    assert_runbook_contract(document)  # The same original must pass first.
    if defect == "mode":
        document = document.replace("--mode review-session", "--mode imaginary")
    elif defect == "flag":
        document = document.replace("--review-ledger", "--actor")
    elif defect == "ac7":
        document = document.replace("| AC7 | REQ-21 |", "| omitted | REQ-21 |")
    elif defect == "baseline":
        document = document.replace("baseline不変", "baseline可変")
    elif defect == "delivery":
        document = document.replace("PM原本読取りgate", "添付だけ")
    elif defect == "root":
        document = document.replace("final-01/reviews.json", "other-root/reviews.json")
    elif defect == "owner":
        document = document.replace("owner実終了", "finalize受付だけ")
    else:
        document = "# empty control\n"
    with pytest.raises((AssertionError, SystemExit)):
        assert_runbook_contract(document)


# Ordinary suite does not collect saved-original tests without the opt-in root.
# Explicit -k saved_baseline with no root therefore collects zero and exits 5.
if os.environ.get("WORDFREQ_MIN_COUNT_BASELINE_ROOT"):
    def test_saved_baseline_originals_readonly():
        v = driver()
        root = Path(os.environ["WORDFREQ_MIN_COUNT_BASELINE_ROOT"]).resolve()
        before = {str(p): v.parts.digest(p) for p in root.rglob("*") if p.is_file()}
        assert before, "saved baseline root is absent or empty"
        assert v.validate_baseline(root) == []
        after = {str(p): v.parts.digest(p) for p in root.rglob("*") if p.is_file()}
        assert before == after

    @pytest.mark.parametrize("field", ["input", "stdout", "html", "raw", "network", "image", "sha"])
    def test_saved_baseline_file_copy_controls(tmp_path, monkeypatch, field):
        import shutil
        v = driver()
        original = Path(os.environ["WORDFREQ_MIN_COUNT_BASELINE_ROOT"]).resolve()
        assert v.validate_baseline(original) == []
        original_hashes = {str(p): v.parts.digest(p) for p in original.rglob("*") if p.is_file()}
        # Read the same historical object store, but damage only managed-scratch
        # copies of evidence. No checkout/commit/CLI/browser or index re-save.
        repo = tmp_path / "readonly-copy-repo"
        repo.mkdir()
        (repo / ".git").symlink_to(ROOT / ".git")
        relative = Path(v.parts.load_json(original / "index.json")["root_relative"])
        root = repo / relative
        shutil.copytree(original, root)
        monkeypatch.setattr(v, "ROOT", repo)
        assert v.validate_baseline(root) == []
        case = v.parts.load_json(root / "index.json")["cases"][3]
        if field in {"input", "stdout", "html"}:
            path = case[field]
        elif field in {"raw", "network"}:
            path = case["views"][0][field]
        elif field == "image":
            path = case["views"][0]["images"][0]["path"]
        else:
            path = case["stdout"]
        # Paths in the immutable index belong to the capture worktree, not
        # necessarily this successor worktree's opt-in root.
        capture_root = Path(v.parts.load_json(root / "index.json")["root"])
        path = root / Path(path).relative_to(capture_root)
        if field == "sha":
            path.write_bytes(b"modified-copy-only")
        else:
            path.unlink()
        assert v.validate_baseline(root), field
        assert original_hashes == {str(p): v.parts.digest(p) for p in original.rglob("*") if p.is_file()}

    @pytest.mark.parametrize("defect", ["format", "width", "empty", "request", "head", "root", "timeline", "artifact"])
    def test_saved_baseline_manifest_controls(defect):
        import copy
        v = driver()
        root = Path(os.environ["WORDFREQ_MIN_COUNT_BASELINE_ROOT"]).resolve()
        assert v.validate_baseline(root) == []
        index = copy.deepcopy(v.parts.load_json(root / "index.json"))
        if defect == "format":
            index["cases"].pop(2)
        elif defect == "width":
            index["cases"][3]["views"].pop()
        elif defect == "empty":
            index["cases"] = []
        elif defect in {"request", "head", "root"}:
            index[defect] = "different"
        elif defect == "timeline":
            index["started"] = "2000-01-01T00:00:00+00:00"
        else:
            del index["artifacts"][index["cases"][0]["input"]]
        assert v.baseline_errors(index, root)
