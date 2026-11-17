"""Phase 4 evidence driver. Baseline capture is one-shot, never acceptance."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

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


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--mode", choices=("baseline", "capture", "review-session", "finalize"), required=True)
    result.add_argument("--role", choices=("builder", "quality"), required=True)
    result.add_argument("--output-dir", type=Path, required=True)
    result.add_argument("--baseline-dir", type=Path)
    result.add_argument("--review-ledger", type=Path)
    return result


def main(argv=None, collector=None):
    p = parser()
    args = p.parse_args(argv)
    if args.mode != "baseline" and args.baseline_dir is None:
        p.error("--baseline-dir is required for this mode")
    if args.mode == "finalize" and args.review_ledger is None:
        p.error("--review-ledger is required for finalize")
    try:
        if args.mode != "baseline":
            raise ValueError(f"unsupported mode until PLAN 04-03: {args.mode}")
        return baseline(args, collector=collector)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(json.dumps(dict(verdict="unverified", errors=[str(exc)], exit=1)))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
