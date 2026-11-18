"""Phase 4 evidence driver. Baseline capture is one-shot, never acceptance."""
import argparse
import importlib.util
import json
import os
import re
from pathlib import Path
import subprocess
import sys
from datetime import timedelta
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("wordfreq_html_parts", ROOT / "tools/verify_wordfreq_html.py")
assert _spec and _spec.loader
parts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(parts)
REQUEST = "r-e476c11d"
BASE = "9eb1e694aafc6cd29f0f7d2a29382764bc1627fb"
WIDTHS = (1280, 320)


def baseline_cases():
    cases = []

    def add(name, basename, body, pairs, total, fmt="html", top=None, explicit=True):
        cases.append(dict(id=name, basename=basename, body=body, pairs=[list(p) for p in pairs],
                          total=total, format=fmt, top=top, explicit_format=explicit))

    body = "Zoo APPLE apple zoo Hello hello HELLO one, two. one b c d e f g h"
    pairs = [("hello", 3), ("zoo", 2), ("apple", 2), ("one", 2),
             ("two", 1), ("b", 1), ("c", 1), ("d", 1), ("e", 1), ("f", 1)]
    add("default-text", "input.txt", body, pairs, 17, "text", explicit=False)
    for fmt in ("text", "json", "html"):
        add("baseline-" + fmt, "input.txt", body, pairs, 17, fmt)
    for name, body in (("empty", ""), ("whitespace", " \t\r\n  "), ("punctuation", "!?,.;: --")):
        add(name, name + ".txt", body, [], 0)
    pairs = [("w" * 256, 123)] + [(f"row{i:02}", 13-i) for i in range(1, 12)]
    body = " ".join(w for w, n in pairs for _ in range(n)) + "\n"
    basename = '集計  ' + 'n' * 176 + '\n続き\t終わり  &<>"\'.txt'
    for label, top in (("12", 12), ("default", None), ("99", 99)):
        add("long-" + label, basename, body, pairs[:10 if top is None else top], 200, top=top)
    add("injection", '検査  &<>"\'\n次\t終.txt', "Café CAFÉ Straße STRASSE 日本語",
        [("café", 2), ("strasse", 2), ("日本語", 1)], 5)
    add("cr-basename", 'a\rb\r\nc  \n\t.txt', body, pairs, 200, top=12)
    return cases


def cli_errors(case):
    errors = []
    if Path(case["input"]).read_bytes() != case["body"].encode("utf-8"):
        errors.append("input differs")
    if case["exit"] != 0 or Path(case["stderr"]).read_bytes():
        errors.append("CLI exit/stderr")
    raw = Path(case["stdout"]).read_bytes()
    text = raw.decode("utf-8", errors="strict")
    pairs = case["pairs"]
    if case["format"] == "text":
        if text != "".join(f"{n}\t{w}\n" for w, n in pairs):
            errors.append("text oracle")
    elif case["format"] == "json":
        if raw != (json.dumps([dict(word=w, count=n) for w, n in pairs], ensure_ascii=True) + "\n").encode():
            errors.append("JSON bytes oracle")
    else:
        doc = parts.Document(text)
        cells = [str(x) for i, (w, n) in enumerate(pairs, 1) for x in (i, w, n)]
        if doc.errors or doc.texts("td") != cells or doc.texts("th") != ["順位", "単語", "回数"]:
            errors.append("HTML static/rows oracle")
        if doc.texts("div", "filename-value") != [case["basename"]] or doc.texts("div", "total-value") != [str(case["total"])]:
            errors.append("HTML metadata oracle")
        empty = doc.texts("p", "empty-message")
        expected_empty = [] if pairs else ["集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。"]
        if empty != expected_empty:
            errors.append("HTML empty copy oracle")
        if Path(case["html"]).read_bytes() != raw:
            errors.append("HTML is not stdout bytes")
        from html import escape
        parent = str(Path(case["input"]).parent)
        if parent in text or escape(parent) in text or "private-source-directory" in text:
            errors.append("directory disclosure")
    return errors


def generate_baseline_cases(output):
    records = []
    for case in baseline_cases():
        folder = output / case["id"]
        source = folder / "private-source-directory" / case["basename"]
        source.parent.mkdir(parents=True, exist_ok=False)
        source.write_bytes(case["body"].encode("utf-8"))
        argv = [sys.executable, "-m", "wordfreq", str(source)]
        if case["explicit_format"]:
            argv += ["--format", case["format"]]
        if case["top"] is not None:
            argv += ["--top", str(case["top"])]
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=20)
        stdout, stderr = folder / "stdout.bin", folder / "stderr.bin"
        stdout.write_bytes(result.stdout)
        stderr.write_bytes(result.stderr)
        record = dict(case, input=str(source), input_sha256=parts.digest(source), argv=argv,
                      cwd=str(ROOT), executable=sys.executable, environment={k: env.get(k) for k in
                      ("PYTHONIOENCODING", "PYTHONUTF8", "PYTHONDONTWRITEBYTECODE", "PYTHONPATH", "LANG", "LC_ALL")},
                      exit=result.returncode, stdout=str(stdout), stderr=str(stderr), views=[])
        if case["format"] == "html":
            html = folder / "stdout.html"
            html.write_bytes(result.stdout)
            record["html"] = str(html)
        errors = cli_errors(record)
        if errors:
            raise ValueError(f"{case['id']}: {errors}")
        parts.save_json(folder / "cli.json", record)
        records.append(record)
    return records


TASK_FILES = ("tools/verify_wordfreq_min_count.py", "tests/test_min_count_verifier.py")
ANALOGS = ("wordfreq/__main__.py", "tests/test_cli.py", "tools/verify_wordfreq_html.py",
           "tools/wordfreq_html_geometry.js", "tests/test_html_verifier.py")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout.decode("utf-8")


def tree(ref):
    result = {}
    for entry in git("ls-tree", "-r", "-z", ref).split("\0"):
        if entry:
            meta, path = entry.split("\t", 1)
            mode, kind, oid = meta.split()
            if kind != "blob":
                raise ValueError("unsupported non-blob execution tree")
            result[path] = dict(mode=mode, blob=oid)
    return result


def execution_state():
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    dirty = git("status", "--porcelain=v1", "--untracked-files=all", "--", ".", ":(exclude).planning/**")
    return dict(head=git("rev-parse", "HEAD").strip(), status=status, execution_status=dirty,
                execution_diff=git("diff", "HEAD", "--", ".", ":(exclude).planning/**"))


def preflight(started):
    state = execution_state()
    if state["execution_status"]:
        raise ValueError("dirty execution surface; commit code/tests/config first")
    head = state["head"]
    git("cat-file", "-e", BASE + "^{commit}")
    git("merge-base", "--is-ancestor", BASE, head)
    base_tree, head_tree = tree(BASE), tree(head)
    allowed = set(TASK_FILES)
    changes = [p for p in base_tree.keys() | head_tree.keys() if base_tree.get(p) != head_tree.get(p)]
    forbidden = [p for p in changes if p not in allowed and not p.startswith(".planning/")]
    if forbidden:
        raise ValueError(f"baseline product/protected scope changed: {forbidden}")
    tracked = git("ls-files", "-z", "--", *ANALOGS).split("\0")
    if any(p not in tracked for p in ANALOGS):
        raise ValueError("untracked/missing analog")
    formal = git("log", "-1", "--format=%H", "--", *TASK_FILES).strip()
    if not git("show", "-s", "--format=%s", formal).startswith("feat(04-01):"):
        raise ValueError("formal 04-01 task commit missing")
    committed = tree(formal)
    import hashlib
    for path in TASK_FILES:
        if head_tree.get(path) != committed.get(path) or path not in committed:
            raise ValueError("formal driver/tests blob mismatch")
        blob = subprocess.run(["git", "show", f"{formal}:{path}"], cwd=ROOT, check=True, capture_output=True).stdout
        if hashlib.sha256(blob).hexdigest() != parts.digest(ROOT / path):
            raise ValueError("working driver/tests differ from formal commit")
    committed_at = int(git("show", "-s", "--format=%ct", formal))
    if committed_at > int(parts.datetime.fromisoformat(started).timestamp()):
        raise ValueError("formal commit is after baseline start")
    return dict(state=state, repo_root=str(ROOT), base=BASE, tree=head_tree, base_tree=base_tree,
                changed_paths=changes, formal_commit=formal, committed_at=committed_at,
                task_sha256={p: parts.digest(ROOT / p) for p in TASK_FILES}, analogs=list(ANALOGS))


def case_paths(case):
    paths = [case[k] for k in ("input", "stdout", "stderr")]
    paths.append(str(Path(case["stdout"]).parent / "cli.json"))
    if case["format"] == "html":
        paths.append(case["html"])
    for view in case["views"]:
        paths += [view["raw"], view["network"], str(Path(view["raw"]).parent / "derived.json")]
        paths += [image["path"] for image in view["images"]]
    return paths


def baseline(args, collector=None):
    import platform
    import time
    output = args.output_dir.resolve()
    if output.exists():
        raise ValueError("baseline root already exists; no overwrite, resume or recapture")
    actor = os.environ.get("HERMES_PROFILE")
    if (args.role != "builder" or actor != "argonauts-uat-builder" or
            not os.environ.get("HERMES_KANBAN_TASK") or not os.environ.get("HERMES_KANBAN_RUN_ID")):
        raise ValueError("baseline requires actual builder profile/run")
    started, timer = parts.now(), time.monotonic()
    provenance = preflight(started)
    output.mkdir(parents=True, exist_ok=False)
    parts.save_json(output / "provenance.json", provenance)
    index = dict(schema=1, request=REQUEST, mode="baseline", role=args.role, actor=actor,
                 task=os.environ["HERMES_KANBAN_TASK"], run=os.environ["HERMES_KANBAN_RUN_ID"],
                 root=str(output), head=provenance["state"]["head"],
                 started=started, synthetic=collector is not None, independent_acceptance=False,
                 reviews=[], verdict="baseline-sealed", cases=[], provenance=provenance,
                 environment=dict(executable=sys.executable, python=sys.version, os=platform.platform(),
                                  tmpdir=os.environ.get("TMPDIR")), errors=[])
    index["root_relative"] = str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else None
    records = generate_baseline_cases(output)
    index["cases"] = records

    def collect(browser):
        for case in records:
            if case["format"] != "html":
                continue
            # The reusable collector opens stdout as a file URL; give it the exact
            # stdout HTML copy, not an HTML template or a modified document.
            browser_case = dict(case, stdout=case["html"])
            for width in WIDTHS:
                view = collector(browser_case, width, output) if collector else parts.collect_view(browser, browser_case, width, output)
                if view["errors"]:
                    raise ValueError(f"browser capture {case['id']}/{width}: {view['errors']}")
                parts.save_json(Path(view["raw"]).parent / "derived.json", view)
                case["views"].append(view)
    if collector:
        index["browser"] = dict(synthetic=True)
        collect(None)
    else:
        from playwright.sync_api import sync_playwright
        executable = "/usr/bin/chromium-browser"
        with sync_playwright() as pw, parts.instrumented_browser(pw, executable) as browser:
            index["browser"] = dict(executable=executable, version=browser.version, os=platform.platform(),
                                    launch=browser.launch_record)
            collect(browser)
    after = execution_state()
    if after["head"] != index["head"] or after["execution_status"]:
        raise ValueError("head/execution surface changed during baseline")
    index["end_provenance"] = after
    index["ended"] = parts.now()
    index["duration_seconds"] = time.monotonic() - timer
    index["artifacts"] = {str(p): parts.digest(p) for p in output.rglob("*") if p.is_file()}
    refs = sorted(index["artifacts"])
    index["ac_index"] = {f"AC{i}": dict(requirement=f"REQ-{i+14}", verdict="pending", evidence=refs)
                         for i in range(1, 8)}
    errors = baseline_errors(index, output, allow_synthetic=collector is not None)
    if errors:
        raise ValueError(f"baseline unsealed: {errors}")
    # Last marker, exclusive creation: repeated verification never calls capture.
    with (output / "index.json").open("x", encoding="utf-8") as stream:
        json.dump(index, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    with (output / "index.sha256").open("x", encoding="ascii") as stream:
        stream.write(parts.digest(output / "index.json") + "\n")
    print(json.dumps(dict(index=str(output / "index.json"), verdict=index["verdict"],
                         synthetic=index["synthetic"], cli_cases=len(records),
                         views=sum(len(c["views"]) for c in records), exit=0)))
    return 0


def baseline_errors(index, output, allow_synthetic=False):
    errors = []
    try:
        # Same repository-relative baseline may be read in a successor worktree.
        # Preserve original bytes/root/cwd/head; translate artifact paths in memory
        # only. Arbitrary roots and changed declared capture roots still fail.
        original_root = index["root"]
        relative = index["root_relative"]
        if relative is not None:
            if (Path(relative).is_absolute() or ".." in Path(relative).parts or
                    original_root != str(Path(index["provenance"]["repo_root"]) / relative) or
                    output.resolve() != (ROOT / relative).resolve()):
                return ["capture root/repository-relative binding differs"]
        elif original_root != str(output.resolve()):
            return ["root mismatch"]
        def relocate(value):
            if isinstance(value, str) and (value == original_root or value.startswith(original_root + "/")):
                return str(output) + value[len(original_root):]
            if isinstance(value, dict):
                return {relocate(k): relocate(v) for k, v in value.items()}
            if isinstance(value, list):
                return [relocate(v) for v in value]
            return value
        index = relocate(index)
        if index["request"] != REQUEST or index["mode"] != "baseline" or index["root"] != str(output.resolve()):
            errors.append("request/mode/root mismatch")
        if index["synthetic"] and not allow_synthetic:
            errors.append("synthetic is not real baseline")
        if index["verdict"] != "baseline-sealed" or index["errors"] or index["independent_acceptance"] or index["reviews"]:
            errors.append("invalid baseline marker/review claim")
        provenance = index["provenance"]
        head = index["head"]
        if head != provenance["state"]["head"] or provenance["base"] != BASE or provenance["state"]["execution_status"]:
            errors.append("head/base/clean provenance mismatch")
        if tree(head) != provenance["tree"] or tree(BASE) != provenance["base_tree"]:
            errors.append("declared head/tree mismatch")
        actual_changes = sorted(p for p in provenance["tree"].keys() | provenance["base_tree"].keys()
                                if provenance["tree"].get(p) != provenance["base_tree"].get(p))
        if sorted(provenance["changed_paths"]) != actual_changes or any(
                p not in TASK_FILES and not p.startswith(".planning/") for p in actual_changes):
            errors.append("baseline product/protected scope mismatch")
        if provenance["analogs"] != list(ANALOGS) or any(p not in provenance["tree"] for p in ANALOGS):
            errors.append("analog tracked ownership mismatch")
        formal = provenance["formal_commit"]
        git("merge-base", "--is-ancestor", formal, head)
        if (not git("show", "-s", "--format=%s", formal).startswith("feat(04-01):") or
                provenance["committed_at"] != int(git("show", "-s", "--format=%ct", formal)) or
                provenance["committed_at"] > parts.datetime.fromisoformat(index["started"]).timestamp()):
            errors.append("formal commit-before-baseline timeline")
        for path in TASK_FILES:
            import hashlib
            blob = subprocess.run(["git", "show", f"{formal}:{path}"], cwd=ROOT, check=True, capture_output=True).stdout
            if (tree(formal).get(path) != provenance["tree"].get(path) or
                    hashlib.sha256(blob).hexdigest() != provenance["task_sha256"][path]):
                errors.append("formal task blob mismatch")
        if index["end_provenance"]["head"] != head or index["end_provenance"]["execution_status"]:
            errors.append("end head/clean mismatch")
        required = [str(output / "provenance.json")]
        cases = index["cases"]
        expected = baseline_cases()
        if [c["id"] for c in cases] != [c["id"] for c in expected]:
            errors.append("missing/reordered baseline cases")
        for case, oracle in zip(cases, expected):
            if any(case[k] != value for k, value in oracle.items()):
                errors.append("independent fixture differs")
            errors += cli_errors(case)
            expected_argv = [index["environment"]["executable"], "-m", "wordfreq", case["input"]]
            if oracle["explicit_format"]:
                expected_argv += ["--format", oracle["format"]]
            if oracle["top"] is not None:
                expected_argv += ["--top", str(oracle["top"])]
            sidecar = relocate(parts.load_json(Path(case["stdout"]).parent / "cli.json"))
            if (case["argv"] != expected_argv or case["cwd"] != provenance["repo_root"] or
                    case["executable"] != index["environment"]["executable"] or
                    sidecar != dict(case, views=[]) or case["input_sha256"] != parts.digest(case["input"])):
                errors.append("CLI argv/cwd/executable/input/sidecar mismatch")
            if case["format"] == "html" and [v["width"] for v in case["views"]] != list(WIDTHS):
                errors.append("missing viewport")
            required += case_paths(case)
            for view in case["views"]:
                raw = parts.load_json(view["raw"])
                if raw["viewport"] != dict(width=view["width"], height=900, dpr=1, scale=1):
                    errors.append("viewport/DPR/zoom mismatch")
                for image in view["images"]:
                    if parts.png_size(image["path"]) != (image["width"], image["height"]):
                        errors.append("PNG dimensions mismatch")
                errors += parts.image_coverage_errors(view, raw)
                if not index["synthetic"]:
                    if raw.get("synthetic") or view["browser"].get("synthetic"):
                        errors.append("synthetic browser boundary")
                    errors += parts.geometry_errors(raw) + parts.dom_errors(raw, case)
                    observed_html = Path(original_root) / Path(case["html"]).relative_to(output)
                    errors += parts.network_errors(parts.load_json(view["network"]), observed_html.as_uri())
                    if not raw["platformFonts"] or view["browser"]["viewport"] != raw["viewport"]:
                        errors.append("missing actual font/browser evidence")
                if view["errors"] or view["reviewed_images"]:
                    errors.append("baseline view errors/unearned review")
        actual_files = {str(p) for p in output.rglob("*") if p.is_file() and p.name not in {"index.json", "index.sha256"}}
        if actual_files != set(index["artifacts"]):
            errors.append("artifact inventory differs")
        if not required or not set(required) <= set(index["artifacts"]):
            errors.append("missing artifact identities")
        for path, value in index["artifacts"].items():
            if not Path(path).resolve().is_relative_to(output.resolve()) or parts.digest(path) != value:
                errors.append(f"artifact missing/changed/outside root: {path}")
        if parts.load_json(output / "provenance.json") != provenance:
            errors.append("provenance sidecar differs")
        refs = sorted(index["artifacts"])
        if index["ac_index"] != {f"AC{i}": dict(requirement=f"REQ-{i+14}", verdict="pending", evidence=refs) for i in range(1, 8)}:
            errors.append("AC/requirement pending mapping differs")
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        errors.append(f"baseline unavailable/malformed: {type(exc).__name__}: {exc}")
    return errors


def validate_baseline(output, allow_synthetic=False):
    """Read originals and historical git objects only; never execute CLI/browser."""
    output = Path(output).resolve()
    try:
        if (output / "index.sha256").read_text().strip() != parts.digest(output / "index.json"):
            return ["index SHA mismatch"]
        return baseline_errors(parts.load_json(output / "index.json"), output, allow_synthetic)
    except (OSError, ValueError, TypeError) as exc:
        return [f"baseline marker unavailable: {exc}"]


# Phase 4 owns cases, scope, AC mapping and lifecycle; only collectors are shared.
ACTORS = {"builder": "argonauts-uat-builder", "quality": "argonauts-uat-quality"}
ACS = tuple(f"AC{i}" for i in range(1, 8))
EXECUTABLE = "/usr/bin/chromium-browser"


def relocate(value: Any, old: str, new: Path) -> Any:
    if isinstance(value, str) and (value == old or value.startswith(old + "/")):
        return str(new) + value[len(old):]
    if isinstance(value, dict):
        return {relocate(k, old, new): relocate(v, old, new) for k, v in value.items()}
    if isinstance(value, list):
        return [relocate(v, old, new) for v in value]
    return value


def read_baseline(root, synthetic=False):
    errors = validate_baseline(root, allow_synthetic=synthetic)
    if errors:
        raise ValueError(f"baseline invalid: {errors}")
    index = parts.load_json(root / "index.json")
    return relocate(index, index["root"], root)


def capture_cases():
    cases = []
    for original in baseline_cases():
        for minimum in (None, 1):
            cases.append(dict(original, id=original["id"] + ("-omitted" if minimum is None else "-one"),
                              baseline_id=original["id"], minimum=minimum, reverse=False))
    matrix = [
        ("beta", "beta beta beta alpha gamma alpha delta", 2, None, [("beta", 3), ("alpha", 2)], 7),
        ("beta-top", "beta beta beta alpha gamma alpha delta", 2, 1, [("beta", 3)], 7),
        ("beta-none", "beta beta beta alpha gamma alpha delta", 4, None, [], 7),
        ("zoo", "Zoo apple APPLE zoo banana", 2, None, [("zoo", 2), ("apple", 2)], 5),
        ("zoo-top", "Zoo apple APPLE zoo banana", 2, 1, [("zoo", 2)], 5),
        ("zoo-reverse", "Zoo apple APPLE zoo banana", 2, 1, [("zoo", 2)], 5),
        ("zoo-none", "Zoo apple APPLE zoo banana", 3, None, [], 5),
        ("unicode", "Straße STRASSE", 2, None, [("strasse", 2)], 2),
        ("empty", "", 2, None, [], 0),
        ("whitespace", " \t\r\n  ", 2, None, [], 0),
        ("punctuation", "!?,.;: --", 2, None, [], 0)]
    for name, body, minimum, top, pairs, total in matrix:
        for fmt in ("text", "json", "html"):
            cases.append(dict(id=name + "-" + fmt, basename=name + ".txt", body=body,
                              pairs=[list(p) for p in pairs], total=total, format=fmt,
                              explicit_format=True, top=top, minimum=minimum, reverse=name == "zoo-reverse"))
    for original in baseline_cases()[7:]:
        # All inherited long/default/99/top12, injection and CR fixtures.
        cases.append(dict(original, id=original["id"] + "-threshold", minimum=2, reverse=False,
                          pairs=[p for p in original["pairs"] if p[1] >= 2]))
    return cases


def case_argv(case, executable):
    argv = [executable, "-m", "wordfreq", case["input"]]
    if case["explicit_format"]:
        argv += ["--format", case["format"]]
    threshold = [] if case["minimum"] is None else ["--min-count", str(case["minimum"])]
    top = [] if case["top"] is None else ["--top", str(case["top"])]
    return argv + (top + threshold if case["reverse"] else threshold + top)


def generate_capture_cases(output, baseline_index):
    records = []
    previous = {c["id"]: c for c in baseline_index["cases"]}
    for oracle in capture_cases():
        folder = output / oracle["id"]
        source = folder / "private-source-directory" / oracle["basename"]
        source.parent.mkdir(parents=True, exist_ok=False)
        source.write_bytes(oracle["body"].encode("utf-8"))
        env = dict(os.environ)
        if oracle.get("baseline_id"):
            recorded = previous[oracle["baseline_id"]]["environment"]
        else:
            recorded = dict(PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1",
                            PYTHONPATH=os.environ.get("PYTHONPATH"), LANG=os.environ.get("LANG"), LC_ALL=os.environ.get("LC_ALL"))
        for key, value in recorded.items():
            if value is None:
                env.pop(key, None)
            else:
                env[key] = value
        record = dict(oracle, input=str(source), input_sha256=parts.digest(source), executable=sys.executable,
                      environment=recorded, cwd=str(ROOT), stdout=str(folder / "stdout.bin"), stderr=str(folder / "stderr.bin"), views=[])
        record["argv"] = case_argv(record, sys.executable)
        result = subprocess.run(record["argv"], cwd=ROOT, env=env, capture_output=True, timeout=20)
        record["exit"] = result.returncode
        Path(record["stdout"]).write_bytes(result.stdout)
        Path(record["stderr"]).write_bytes(result.stderr)
        if oracle["format"] == "html":
            record["html"] = str(folder / "stdout.html")
            Path(record["html"]).write_bytes(result.stdout)
        errors = cli_errors(record)
        if errors:
            raise ValueError(f"{record['id']}: {errors}")
        parts.save_json(folder / "cli.json", record)
        records.append(record)
    return records


def allowed_capture_path(path):
    # Finalization moves this change and syncs its spec; both old and new tree
    # paths must remain verifiable. Do not allow unrelated OpenSpec changes.
    change_file = re.fullmatch(
        r"openspec/changes/(?:archive/[0-9]{4}-[0-9]{2}-[0-9]{2}-)?"
        r"r-e476c11d-wordfreq-min-count/"
        r"(?:\.openspec\.yaml|design\.md|proposal\.md|tasks\.md|specs/wordfreq-cli/spec\.md)", path)
    return (bool(change_file)
            or path in {*TASK_FILES, "wordfreq/__main__.py", "tests/test_cli.py", "README.md",
                        "docs/wordfreq-min-count-verification.md", "openspec/specs/wordfreq-cli/spec.md"}
            or path in {".planning/PROJECT.md", ".planning/STATE.md", ".planning/state.json",
                        ".planning/ROADMAP.md", ".planning/REQUIREMENTS.md"}
            or path.startswith((".planning/argonauts/", ".planning/phases/04-wordfreq-min-count/")))


def capture_scope(baseline_head, head):
    git("merge-base", "--is-ancestor", baseline_head, head)
    before, after = tree(baseline_head), tree(head)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    forbidden = [p for p in changed if not allowed_capture_path(p)]
    if forbidden:
        raise ValueError(f"forbidden current scope: {forbidden}")
    return dict(base=baseline_head, head=head, base_tree=before, tree=after, changed_paths=changed)


def actor_for(role, output):
    actor = os.environ.get("HERMES_PROFILE")
    if actor != ACTORS[role] or role not in output.parts or ({"builder", "quality"} - {role}).intersection(output.parts):
        raise ValueError("actual profile/role/root separation mismatch")
    if not os.environ.get("HERMES_KANBAN_TASK") or not os.environ.get("HERMES_KANBAN_RUN_ID"):
        raise ValueError("missing actual task/run")
    return actor


def run_capture_suite(output):
    import xml.etree.ElementTree as ET
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    for key in ("WORDFREQ_MIN_COUNT_BASELINE_ROOT", "WORDFREQ_MIN_COUNT_CAPTURE_ROOT"):
        env.pop(key, None)
    argv = [sys.executable, "-m", "pytest", "--junitxml", str(output / "suite.xml")]
    started = parts.now()
    result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=600)
    (output / "suite.stdout").write_bytes(result.stdout)
    (output / "suite.stderr").write_bytes(result.stderr)
    suites = list(ET.parse(output / "suite.xml").getroot().iter("testsuite"))
    return dict(argv=argv, cwd=str(ROOT), head=git("rev-parse", "HEAD").strip(), started=started,
                ended=parts.now(), exit=result.returncode, synthetic=False,
                collected=sum(int(s.get("tests", 0)) for s in suites), environment={k: env.get(k) for k in
                ("PYTHONPATH", "PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE", "LANG", "LC_ALL",
                 "WORDFREQ_MIN_COUNT_BASELINE_ROOT", "WORDFREQ_MIN_COUNT_CAPTURE_ROOT")})


def suite_errors(root, synthetic=False, original=None):
    import xml.etree.ElementTree as ET
    suite = relocate(parts.load_json(root / "suite.json"), original or str(root), root)
    suites = list(ET.parse(root / "suite.xml").getroot().iter("testsuite"))
    count = sum(int(s.get("tests", 0)) for s in suites)
    errors = []
    if (suite["exit"] != 0 or count <= 0 or count != suite["collected"] or
            any(int(s.get(k, 0)) for s in suites for k in ("errors", "failures", "skipped"))):
        errors.append("full suite failed/empty/skipped")
    if suite["synthetic"] and not synthetic:
        errors.append("synthetic suite is not full regression")
    if not suite["synthetic"]:
        if (suite["argv"] != [sys.executable, "-m", "pytest", "--junitxml", str(root / "suite.xml")] or
                any(suite["environment"].get(k) for k in ("WORDFREQ_MIN_COUNT_BASELINE_ROOT", "WORDFREQ_MIN_COUNT_CAPTURE_ROOT"))):
            errors.append("suite command/opt-in recursion mismatch")
    return errors


def comparisons(manifest, baseline_index):
    previous = {c["id"]: c for c in baseline_index["cases"]}
    result = {}
    for case in manifest["cases"]:
        if not case.get("baseline_id"):
            continue
        old = previous[case["baseline_id"]]
        item = dict(bytes_equal=Path(case["stdout"]).read_bytes() == Path(old["stdout"]).read_bytes(),
                    environment_equal=case["environment"] == old["environment"], views=[])
        for view, before in zip(case["views"], old["views"]):
            raw, old_raw = parts.load_json(view["raw"]), parts.load_json(before["raw"])
            item["views"].append(dict(width=view["width"], raw_equal=raw == old_raw,
                browser_equal=view["browser"] == before["browser"],
                images_equal=[parts.digest(i["path"]) for i in view["images"]] == [parts.digest(i["path"]) for i in before["images"]],
                reviewed=False))
        result[case["id"]] = item
    return result


def artifact_hashes(output, mutable=False):
    excluded = {"manifest.json", "manifest.sha256"}
    if mutable:
        excluded |= {"network.json", "browser-network.json", "derived.json", "reviews.json", "finalize-request.json"}
    return {str(p): parts.digest(p) for p in output.rglob("*") if p.is_file() and p.name not in excluded}


def ac_mapping(artifacts):
    return {ac: dict(requirement=f"REQ-{15+i}", evidence=sorted(artifacts), verdict="pending") for i, ac in enumerate(ACS)}


def capture_errors(m, output, baseline_dir, allow_synthetic=False, live=False):
    errors = []
    try:
        b = read_baseline(baseline_dir, allow_synthetic)
        original = m["root"]
        relative = m["root_relative"]
        if relative is not None:
            if (Path(relative).is_absolute() or ".." in Path(relative).parts or
                    original != str(Path(m["repo_root"]) / relative) or (ROOT / relative).resolve() != output.resolve()):
                return ["capture root binding differs"]
        elif original != str(output.resolve()):
            return ["capture root differs"]
        m = relocate(m, original, output)
        if (m["request"] != REQUEST or m["mode"] not in {"capture", "review-session"} or
                m["actor"] != ACTORS[m["role"]] or m["role"] not in output.parts or
                not m["task"] or not m["run"] or m["errors"]):
            errors.append("request/mode/actor/root/errors mismatch")
        if m["synthetic"] and not allow_synthetic:
            errors.append("synthetic is not integration")
        if not live and (m["verdict"] != "pending-review" or m["independent_acceptance"] or m["reviews"] or m["ac_reviews"]):
            errors.append("unearned acceptance/review")
        if m["baseline"] != dict(head=b["head"], index_sha256=parts.digest(baseline_dir / "index.json")):
            errors.append("baseline identity differs")
        if (m["head"] != m["provenance"]["head"] or m["provenance"]["execution_status"] or
                m["end_provenance"]["head"] != m["head"] or m["end_provenance"]["execution_status"]):
            errors.append("head/dirty start/end mismatch")
        if capture_scope(b["head"], m["head"]) != m["scope"]:
            errors.append("scope/tree mismatch")
        if parts.load_json(output / "scope.json") != m["scope"] or parts.load_json(output / "provenance.json") != m["provenance"]:
            errors.append("scope/provenance sidecar mismatch")
        if m["environment"]["executable"] != m["cases"][0]["executable"]:
            errors.append("executable environment mismatch")
        if not m["synthetic"]:
            if any(m["environment"][k] != b["environment"][k] for k in ("executable", "python", "os")):
                errors.append("baseline runtime environment differs")
            if any(m["browser"][k] != b["browser"][k] for k in ("executable", "version", "os")):
                errors.append("baseline browser environment differs")
        expected = capture_cases()
        if [c["id"] for c in m["cases"]] != [c["id"] for c in expected]:
            errors.append("missing/reordered cases")
        required = [str(output / n) for n in ("suite.json", "suite.xml", "suite.stdout", "suite.stderr", "scope.json", "provenance.json")]
        for case, oracle in zip(m["cases"], expected):
            if any(case[k] != val for k, val in oracle.items()):
                errors.append("literal oracle differs")
            errors += cli_errors(case)
            sidecar = relocate(parts.load_json(Path(case["stdout"]).parent / "cli.json"), original, output)
            if (sidecar != dict(case, views=[]) or case["argv"] != case_argv(case, m["environment"]["executable"]) or
                    case["cwd"] != m["repo_root"] or case["input_sha256"] != parts.digest(case["input"])):
                errors.append("CLI sidecar/argv/cwd/input differs")
            if case["format"] == "html" and [v["width"] for v in case["views"]] != list(WIDTHS):
                errors.append("missing viewport")
            required += case_paths(case)
            for view in case["views"]:
                raw = parts.load_json(view["raw"])
                errors += parts.view_identity_errors(view) + parts.image_coverage_errors(view, raw)
                if raw["viewport"] != dict(width=view["width"], height=900, dpr=1, scale=1):
                    errors.append("viewport differs")
                for image in view["images"]:
                    if parts.png_size(image["path"]) != (image["width"], image["height"]):
                        errors.append("image dimensions differ")
                if not m["synthetic"]:
                    errors += parts.geometry_errors(raw) + parts.dom_errors(raw, case)
                    url = (Path(original) / Path(case["html"]).relative_to(output)).as_uri()
                    errors += parts.network_errors(parts.load_json(view["network"]), url)
                    if not raw["platformFonts"] or view["browser"]["viewport"] != raw["viewport"]:
                        errors.append("missing font/browser environment")
                derived = relocate(parts.load_json(Path(view["raw"]).parent / "derived.json"), original, output)
                if derived != view or view["errors"]:
                    errors.append("view/derived/errors differ")
        errors += suite_errors(output, allow_synthetic, original)
        actual = artifact_hashes(output, mutable=live)
        if actual != m["artifacts"]:
            errors.append("artifact set/hash differs")
        if not live and not set(required) <= set(m["artifacts"]):
            errors.append("missing required artifacts")
        if m["ac_index"] != ac_mapping(m["artifacts"]):
            errors.append("AC1-7 mapping differs")
        comparison = comparisons(m, b)
        if m["comparisons"] != comparison or any(not c["bytes_equal"] or not c["environment_equal"] or
                any(not v["raw_equal"] or not v["browser_equal"] or not v["images_equal"] for v in c["views"]) for c in comparison.values()):
            errors.append("baseline bytes/raw/environment/images comparison differs")
    except Exception as exc:
        errors.append(f"capture unavailable/malformed: {type(exc).__name__}: {exc}")
    return list(dict.fromkeys(errors))


def validate_capture(output, baseline_dir, allow_synthetic=False):
    """Read-only saved-original check; declared head is never retagged to HEAD."""
    output, baseline_dir = Path(output).resolve(), Path(baseline_dir).resolve()
    try:
        if (output / "manifest.sha256").read_text().strip() != parts.digest(output / "manifest.json"):
            return ["manifest SHA mismatch"]
        return capture_errors(parts.load_json(output / "manifest.json"), output, baseline_dir, allow_synthetic)
    except Exception as exc:
        return [f"capture marker unavailable: {exc}"]


def seal_capture(m, output):
    parts.save_json(output / "manifest.json", m)
    (output / "manifest.sha256").write_text(parts.digest(output / "manifest.json") + "\n", encoding="ascii")


def baseline_review_views(baseline_dir, synthetic=False):
    b = read_baseline(baseline_dir, synthetic)
    return [v for c in b["cases"] for v in c["views"]]


def ledger_errors(m, ledger, baseline_dir, end, synthetic=False):
    errors = []
    try:
        for key in ("request", "session", "head", "actor", "root", "run", "task"):
            if not m[key] or ledger[key] != m[key]:
                errors.append(f"ledger {key} differs")
        views = [v for c in m["cases"] for v in c["views"]] + baseline_review_views(baseline_dir, synthetic)
        images = [(v, i) for v in views for i in v["images"]]
        expected = [i["path"] for _, i in images]
        actual = [r["image"] for r in ledger["reviews"]]
        if not expected or len(set(expected)) != len(expected) or sorted(expected) != sorted(actual):
            errors.append("missing/extra/duplicate/unviewed current or baseline image")
        for view, image in images:
            image = dict(image, sha256=parts.digest(image["path"]))
            matches = [r for r in ledger["reviews"] if r["image"] == image["path"]]
            if len(matches) == 1:
                errors += parts.review_errors(matches[0], image, view["raw"], parts.digest(view["raw"]), m["actor"], m["ready_at"], end)
        if sorted(a["ac"] for a in ledger["ac_reviews"]) != list(ACS):
            errors.append("missing/duplicate AC1-7")
        for a in ledger["ac_reviews"]:
            if a["judgment"] != "accepted" or not a["notes"].strip() or a["evidence"] != m["ac_index"][a["ac"]]["evidence"]:
                errors.append("AC evidence/judgment differs")
        source = ledger["source_order"]
        if (source["head"] != m["head"] or source["path"] != "wordfreq/__main__.py" or
                source["sha256"] != parts.digest(ROOT / source["path"]) or
                source["lines"] != [34, 35, 36, 37, 38, 44] or
                source["judgment"] != "filter-before-top-original-total" or not source["notes"].strip()):
            errors.append("missing current-head source-order/diff attestation")
    except Exception as exc:
        errors.append(f"ledger malformed/unavailable: {exc}")
    return errors


def finish_observation(live, browser, output):
    if browser is None:
        return parts.now(), []  # Explicit synthetic boundary only.
    return parts.snapshot_live(live, browser, output)


def live_errors(m, output, baseline_dir, ledger, end, synthetic=False, require_end=True):
    errors = capture_errors(m, output, baseline_dir, synthetic, live=True)
    if (m["mode"] != "review-session" or m["verdict"] != "pending-review" or m.get("ended") or
            m["actor"] != actor_for(m["role"], output) or parts.live_session_errors(m)):
        errors.append("live session absent/ended/actor differs")
    state = execution_state()
    if state["head"] != m["head"] or state["execution_status"]:
        errors.append("current head/execution surface changed")
    if capture_scope(m["baseline"]["head"], state["head"]) != m["scope"]:
        errors.append("current scope changed")
    if parts.datetime.fromisoformat(end) > parts.datetime.fromisoformat(m["expires_at"]):
        errors.append("session expired")
    if not synthetic:
        canaries = parts.load_json(output / "canaries/canaries.json")
        errors += parts.canary_errors(canaries)
        if canaries["role"] != m["role"] or canaries["provenance"]["head"] != m["head"]:
            errors.append("canary head/role differs")
        for case in m["cases"]:
            for view in case["views"]:
                net = parts.load_json(view["network"])
                if net["interval"] != "live-review" or net["start"] > m["ready_at"] or (require_end and net["end"] < end):
                    errors.append("incomplete live observation interval")
    return errors + ledger_errors(m, ledger, baseline_dir, end, synthetic)


def revoke_reviews(m, output):
    m.update(verdict="unverified", independent_acceptance=False, ac_verdicts={a: "unverified" for a in ACS})
    for case in m.get("cases", []):
        for view in case.get("views", []):
            view.update(verdict="unverified", reviewed_images=[])
            try:
                parts.save_json(Path(view["raw"]).parent / "derived.json", view)
            except Exception as exc:
                m["errors"].append(f"rollback persistence failed: {exc}")


def final_publication_errors(m, ledger, output, baseline_dir, synthetic=False):
    errors = ledger_errors(m, ledger, baseline_dir, m["verification_finished"], synthetic)
    verdict = "accepted" if m["role"] == "quality" and not synthetic else "builder-reviewed"
    if (m["verdict"] != verdict or m["errors"] or m["independent_acceptance"] != (verdict == "accepted") or
            m["ac_verdicts"] != {a: "accepted" for a in ACS} or not m.get("observation_end") or
            m["end_provenance"]["head"] != m["head"] or m["end_provenance"]["execution_status"]):
        errors.append("inconsistent final verdict/end provenance")
    if parts.load_json(output / "reviews.json") != ledger or parts.digest(output / "reviews.json") != m["ledger_sha256"]:
        errors.append("final ledger changed")
    for case in m["cases"]:
        for view in case["views"]:
            reviews = [r for i in view["images"] for r in ledger["reviews"] if r["image"] == i["path"]]
            projected = [dict(path=r["image"], sha256=r["sha256"], viewed_at=r["viewed_at"]) for r in reviews]
            errors += parts.view_identity_errors(view)
            if (not projected or view["verdict"] != verdict or view["reviewed_images"] != projected or
                    parts.load_json(Path(view["raw"]).parent / "derived.json") != view):
                errors.append("all-view/derived/ledger final identity differs")
    return errors


def publish_owner(m, output, baseline_dir, live, browser, synthetic=False):
    """The owner, never the requester, flushes and publishes the last marker."""
    try:
        request = parts.load_json(output / "finalize-request.json")
        ledger = parts.load_json(output / "reviews.json")
        if request["session"] != m["session"] or request["ledger_sha256"] != parts.digest(output / "reviews.json"):
            raise ValueError("finalize request identity changed")
        for _ in range(2):
            boundary, errors = finish_observation(live, browser, output)
            m["errors"] += errors + live_errors(m, output, baseline_dir, ledger, boundary, synthetic)
        m["verification_finished"] = parts.now()
        m["observation_end"], late = finish_observation(live, browser, output)
        m["errors"] += late
        m["end_provenance"] = execution_state()
        if m["end_provenance"]["head"] != m["head"] or m["end_provenance"]["execution_status"]:
            m["errors"].append("head changed at publication")
        if m["errors"]:
            raise ValueError("owner revalidation failed")
        m["ledger_sha256"] = parts.digest(output / "reviews.json")
        m["verdict"] = "accepted" if m["role"] == "quality" and not synthetic else "builder-reviewed"
        m["independent_acceptance"] = m["verdict"] == "accepted"
        m["ac_verdicts"] = {a: "accepted" for a in ACS}
        # Invalidate the old marker before any projection can be partly written.
        import copy
        checkpoint = copy.deepcopy(m)
        checkpoint.update(verdict="unverified", independent_acceptance=False)
        seal_capture(checkpoint, output)
        for case in m["cases"]:
            for view in case["views"]:
                view["verdict"] = m["verdict"]
                view["reviewed_images"] = [dict(path=i["path"], sha256=r["sha256"], viewed_at=r["viewed_at"])
                    for i in view["images"] for r in ledger["reviews"] if r["image"] == i["path"]]
                parts.save_json(Path(view["raw"]).parent / "derived.json", view)
        errors = final_publication_errors(m, ledger, output, baseline_dir, synthetic)
        if errors:
            raise ValueError(f"final reconciliation: {errors}")
    except Exception as exc:
        m["errors"].append(f"owner publication unverified: {type(exc).__name__}: {exc}")
        revoke_reviews(m, output)
    m["ended"] = parts.now()
    try:
        seal_capture(m, output)
    except Exception as exc:
        m["errors"].append(f"completion marker persistence failed: {exc}")
        revoke_reviews(m, output)
        try:
            seal_capture(m, output)
        except Exception as final_exc:
            print(json.dumps(dict(verdict="unverified", persistence_error=str(final_exc))), flush=True)
    return 0 if not m["errors"] and m["verdict"] in {"accepted", "builder-reviewed"} else 1


def serve_review(m, output, baseline_dir, live, browser, owner_hook=None):
    import uuid
    import time
    synthetic = m["synthetic"]
    m.update(session=uuid.uuid4().hex, pid=os.getpid(), process_start=parts.process_start(os.getpid()),
             ready_at=parts.now(), verdict="pending-review")
    m["expires_at"] = (parts.datetime.fromisoformat(m["ready_at"]) + timedelta(seconds=7200)).isoformat()
    m["artifacts"] = artifact_hashes(output, mutable=True)
    m["ac_index"] = ac_mapping(m["artifacts"])
    parts.save_json(output / "reviews.json", {**{k: m[k] for k in ("request", "session", "head", "root", "actor", "run", "task")},
                                              "reviews": [], "ac_reviews": []})
    seal_capture(m, output)
    print(json.dumps(dict(ready=True, manifest=str(output / "manifest.json"), verdict="pending-review", expires_at=m["expires_at"])), flush=True)
    try:
        if owner_hook:
            if not synthetic:
                raise ValueError("owner hook only permitted at explicit synthetic boundary")
            owner_hook(m)
        else:
            deadline = time.monotonic() + 7200
            while not (output / "finalize-request.json").exists() and time.monotonic() < deadline:
                live[0]["page"].wait_for_timeout(100)
        if not (output / "finalize-request.json").exists():
            raise ValueError("session expired/interrupted without finalize request")
        return publish_owner(m, output, baseline_dir, live, browser, synthetic)
    except Exception as exc:
        m["errors"].append(f"live owner unverified: {exc}")
        revoke_reviews(m, output)
        m["ended"] = parts.now()
        seal_capture(m, output)
        return 1


def review_session(args, collector=None, suite_runner=None, owner_hook=None):
    return capture(args, collector, suite_runner, owner_hook)


def finalize(args, synthetic=False):
    output, baseline_dir = args.output_dir.resolve(), args.baseline_dir.resolve()
    actor = actor_for(args.role, output)
    if args.review_ledger.resolve() != output / "reviews.json":
        raise ValueError("ledger must be the live root reviews.json")
    m = parts.load_json(output / "manifest.json")
    if m["role"] != args.role or m["actor"] != actor or (m["synthetic"] and not synthetic):
        raise ValueError("finalize actor/role/synthetic differs")
    ledger = parts.load_json(args.review_ledger)
    # Request-side validation is conservative. Only the live owner may accept.
    errors = live_errors(m, output, baseline_dir, ledger, parts.now(), synthetic, require_end=False)
    if errors:
        raise ValueError(f"finalize unverified: {errors}")
    path = output / "finalize-request.json"
    with path.open("x", encoding="utf-8") as stream:
        json.dump(dict(session=m["session"], ledger_sha256=parts.digest(args.review_ledger), at=parts.now()), stream)
    print(json.dumps(dict(verdict="finalize-requested", independent_acceptance=False)), flush=True)
    return 0


def capture(args, collector=None, suite_runner=None, owner_hook=None):
    import platform
    import time
    output, baseline_dir = args.output_dir.resolve(), args.baseline_dir.resolve()
    if output.exists():
        raise ValueError("capture root already exists; never overwrite or recapture")
    actor = actor_for(args.role, output)
    synthetic = collector is not None or suite_runner is not None
    b = read_baseline(baseline_dir, synthetic)
    start = execution_state()
    if start["execution_status"]:
        raise ValueError("dirty execution surface; commit first")
    scope = capture_scope(b["head"], start["head"])
    output.mkdir(parents=True)
    started, timer = parts.now(), time.monotonic()
    m = dict(schema=2, request=REQUEST, mode=args.mode, role=args.role, actor=actor,
        task=os.environ["HERMES_KANBAN_TASK"], run=os.environ["HERMES_KANBAN_RUN_ID"], root=str(output),
        root_relative=str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else None, repo_root=str(ROOT),
        head=start["head"], provenance=start, scope=scope, baseline=dict(head=b["head"], index_sha256=parts.digest(baseline_dir / "index.json")),
        environment=dict(executable=sys.executable, python=sys.version, os=platform.platform(), tmpdir=os.environ.get("TMPDIR")),
        started=started, synthetic=synthetic, errors=[], reviews=[], ac_reviews=[], independent_acceptance=False,
        verdict="unverified", cases=[])
    try:
        parts.save_json(output / "provenance.json", start)
        parts.save_json(output / "scope.json", scope)
        suite = (suite_runner or run_capture_suite)(output)
        parts.save_json(output / "suite.json", suite)
        if suite_errors(output, synthetic):
            raise ValueError("full suite failed/empty/skipped")
        live = []
        if args.mode == "review-session" and not synthetic:
            from types import SimpleNamespace
            if parts.self_test_network(SimpleNamespace(output_dir=output / "canaries", role=args.role, browser=EXECUTABLE)):
                raise ValueError("real canary discrimination failed")
        m["cases"] = generate_capture_cases(output, b)
        def collect(browser):
            for case in m["cases"]:
                if case["format"] != "html":
                    continue
                for width in WIDTHS:
                    view = collector(case, width, output) if collector else parts.collect_view(
                        browser, dict(case, stdout=case["html"]), width, output,
                        live=live if args.mode == "review-session" else None)
                    view["raw_sha256"] = parts.digest(view["raw"])
                    for image in view["images"]:
                        image["sha256"] = parts.digest(image["path"])
                    parts.save_json(Path(view["raw"]).parent / "derived.json", view)
                    case["views"].append(view)
        def review(browser):
            m["end_provenance"] = execution_state()
            m["comparisons"] = comparisons(m, b)
            return serve_review(m, output, baseline_dir, live, browser, owner_hook)
        if collector:
            m["browser"] = dict(synthetic=True)
            collect(None)
            if args.mode == "review-session":
                return review(None)
        else:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as pw, parts.instrumented_browser(pw, EXECUTABLE) as browser:
                try:
                    m["browser"] = dict(executable=EXECUTABLE, version=browser.version, os=platform.platform(), launch=browser.launch_record)
                    collect(browser)
                    if args.mode == "review-session":
                        return review(browser)
                finally:
                    for item in live:
                        item["observer"].browser_cdp.detach()
                        item["context"].close()
        m["end_provenance"] = execution_state()
        m["comparisons"] = comparisons(m, b)
        m["artifacts"] = artifact_hashes(output)
        m["ac_index"] = ac_mapping(m["artifacts"])
        m["verdict"] = "pending-review"
        m["errors"] += capture_errors(m, output, baseline_dir, synthetic)
        if m["errors"]:
            m["verdict"] = "unverified"
    except Exception as exc:
        m["errors"].append(f"capture unverified: {type(exc).__name__}: {exc}")
        m["verdict"] = "unverified"
    m["ended"], m["duration_seconds"] = parts.now(), time.monotonic() - timer
    seal_capture(m, output)
    print(json.dumps(dict(manifest=str(output / "manifest.json"), head=m["head"], verdict=m["verdict"],
        cases=len(m["cases"]), views=sum(len(c["views"]) for c in m["cases"]), errors=m["errors"], synthetic=synthetic)))
    return 1 if m["errors"] else 0


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--mode", choices=("baseline", "capture", "review-session", "finalize"), required=True)
    result.add_argument("--role", choices=("builder", "quality"), required=True)
    result.add_argument("--output-dir", type=Path, required=True)
    result.add_argument("--baseline-dir", type=Path)
    result.add_argument("--review-ledger", type=Path)
    return result


def main(argv=None, collector=None, suite_runner=None, owner_hook=None):
    p = parser()
    args = p.parse_args(argv)
    if args.mode != "baseline" and args.baseline_dir is None:
        p.error("--baseline-dir is required for this mode")
    if args.mode == "finalize" and args.review_ledger is None:
        p.error("--review-ledger is required for finalize")
    try:
        if args.mode == "capture":
            return capture(args, collector, suite_runner)
        if args.mode == "review-session":
            return review_session(args, collector, suite_runner, owner_hook)
        if args.mode == "finalize":
            return finalize(args, synthetic=collector is not None)
        return baseline(args, collector=collector)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(json.dumps(dict(verdict="unverified", errors=[str(exc)], exit=1)))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
