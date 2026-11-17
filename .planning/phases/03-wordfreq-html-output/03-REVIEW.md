---
phase: 03-wordfreq-html-output
reviewed: 2026-11-17T19:49:18Z
depth: standard
files_reviewed: 6
files_reviewed_list:
  - tools/verify_wordfreq_html.py
  - tests/test_html_finalization.py
  - tests/fixtures/encoding_cli_probe.py
  - tests/test_cli.py
  - tests/test_html_verifier.py
  - docs/wordfreq-html-verification.md
findings:
  critical: 0
  warning: 3
  info: 3
  total: 6
  necessity: 0
status: issues_found
---

# Phase 03: Code Review Report

**Reviewed:** 2026-11-17T19:49:18Z
**Depth:** standard
**Files Reviewed:** 6
**Status:** issues_found

## Summary

Reviewed HEAD `7c704f337df10a4bfd4bb18936266a16b606dd3c` against diff base `c26d9d963b5983e539b675b767fbd3d1c0572e7a`. The diff covers plans 03-05 (G1: final all-view/derived/ledger reconciliation and fail-closed publication) and 03-06 (G2: encoding seam, shallow/exact-ref scope, provenance outside `tests/`, actor recording). This report replaces the earlier review of HEAD `995011c`. That review's WR-01 (per-view pending after acceptance) and IN-02 (scope git failures escaping) are fixed in this diff. Its WR-02 (collection outside `tests/`) and WR-03 (missing locale) are partly addressed.

The G1 publication path holds up. `publish_final_reviews` runs in this order:
1. It writes an unverified checkpoint manifest.
2. It writes every `derived.json`.
3. It reconciles, and only then is the final manifest marker written.

Every exception, timeout, late network error and head/dirty change goes through `revoke_final_reviews`. That includes derived records found on disk that the manifest never listed. `final_review_errors` checks each view against the exact ledger path/sha256/viewed_at in canonical order and rejects `pending-review` at any depth. The exact-ref `scope_report` resolves both commits before diffing and returns `paths: null` plus `ref_diagnostics` rather than a clean list. Finalize rejects a manifest whose actor does not match, before it writes `finalize-request.json`.

The remaining defects are in the anti-tamper gates (scope and provenance), which can still miss real changes:
- the scope diff hides deletions of unauthorized files when git detects the change as a rename;
- the provenance selection follows git's ignore rules rather than pytest's discovery rules;
- import shadowing is detected only for a root-level `pytest.py`.

I reproduced the rename behaviour in a throwaway git repo under the scratch dir. With git's default `diff.renames=true`, `git diff --name-only` listed only `.planning/research/ci.yml` for `git mv .github/workflows/ci.yml .planning/research/ci.yml`. `--no-renames` listed both paths.

No necessity findings. I read the rubric. Every guard I reviewed sits on a trust boundary (files, git, environment, the external ledger) or is deliberate defense in depth.

## Warnings

### WR-01: Scope diff hides unauthorized deletions/moves via rename detection

**File:** `tools/verify_wordfreq_html.py:848-851`
**Issue:** `scope_report()` builds `paths` from `git diff --name-only -z SCOPE_BASE target`. With git's default rename detection, a rename lists **only the destination**. A file outside the allowed scope (for example `.github/workflows/ci.yml` or `pyproject.toml`) can be moved into an allowed prefix (`.planning/research/`, `.planning/argonauts/`, `.planning/intel/`). Its deletion then never appears, and `scope_path_errors()` passes it. Reproduced: the default output was `.planning/research/ci.yml` only, while `--no-renames` also listed `.github/workflows/ci.yml`. `test_scope_committed_diffs_are_discriminated` covers add/modify only, not renames.
**Fix:**
```python
paths = list(filter(None, git("diff", "--no-renames", "--name-only", "-z",
                              SCOPE_BASE, report["target"]).split("\0")))
unexpected_product = git("diff", "--no-renames", "--name-only",
                         APPROVED_PRODUCT, report["target"], "--", "wordfreq")
```
Add a `renamed-out-of-scope` case: `git mv .github/workflows/ci.yml .planning/research/ci.yml` must produce `unauthorized scope: .github/workflows/ci.yml`.

### WR-02: Provenance uses git ignore rules, not pytest discovery, so ignored-but-collected test code is invisible

**File:** `tools/verify_wordfreq_html.py:276-279`
**Issue:** `git status --porcelain=v1` and `git ls-files --others --exclude-standard` skip every path matched by `.gitignore`, `.git/info/exclude` or the user's `core.excludesFile`. pytest ignores those rules. It still collects any `test_*.py` / `*_test.py` and loads any `conftest.py` outside `norecursedirs` (`.*`, `build`, `dist`, `venv`, …) and `__pycache__`. An ignored `conftest.py` can deselect, skip or force-pass the whole suite, yet it would not show up in `product_status` or `untracked_product`. `run_suite()`/`suite.json` would then record a green suite that hidden code influenced. 03-06-PLAN requires the selection to be derived "from the repository's actual discovery contract" (T-03-16). `test_planning_evidence_and_ignored_cache_do_not_become_execution_code` tests only `__pycache__` and `.planning`, which pytest skips anyway. It never tests an ignored path that pytest would collect.
**Fix:** Also list ignored files under the same pathspecs. Record them as dirty unless they sit in directories pytest never recurses into:
```python
ignored = git("ls-files", "--others", "--ignored", "--exclude-standard", "-z", "--", *paths)
for name in filter(None, ignored.split("\0")):
    parts = Path(name).parts
    if "__pycache__" in parts or any(p.startswith(".") for p in parts[:-1]):
        continue
    # record path/sha256/content like untracked, and mark dirty
```
Add a fixture that puts `nested/conftest.py` in `.git/info/exclude` and asserts that `provenance()`/`scope_report()` block on it.

### WR-03: Import-shadow coverage is limited to root `pytest.py`; other root modules still alter the suite

**File:** `tools/verify_wordfreq_html.py:272-275`
**Issue:** `run_suite()` runs `python -m pytest` with `cwd=ROOT`, and `-m` puts the cwd first on `sys.path`. Any untracked or modified root-level module or package named like a pytest dependency or stdlib module therefore replaces the real one for the entire run. Examples: `_pytest/`, `pluggy/`, `iniconfig.py`, `packaging/`, `json.py`, `xml/`. The selection includes only `pytest.py`, `conftest.py` and the test-name globs, so an untracked root `pluggy.py` leaves `product_status` empty. `test_isolated_collection_and_module_shadow_are_execution_influence` covers only `pytest.py`.
**Fix:** Track every importable top-level entry rather than a single name, e.g. add `":(glob)*.py"`, `":(glob)*/__init__.py"` and `":(glob)*.pth"` to `paths`. Alternatively, dirty-check the whole worktree minus an explicit list of non-code paths (`.planning/**`, `docs/**`, `*.md`). Add a fixture with an untracked root `pluggy.py` (or `_pytest/__init__.py`) that must block.

## Info

### IN-01: `roundtrip_path_hex` duplicates `raw_path_hex` by construction

**File:** `tests/fixtures/encoding_cli_probe.py:18,26-27` (asserted at `tests/test_cli.py:301-302`)
**Issue:** Both fields evaluate `os.fsencode(argv[0])`. `os.fsencode` binds the startup codec when `os` is imported, so the patched `sys.getfilesystemencoding` cannot change it, and the two values are always equal. The real argv-byte check is the parent comparing `raw_path_hex` with its own `os.fsencode(path)`. The doc presents the round-trip as a separate verified obligation (G2 bullet 1).
**Fix:** Drop the redundant field. Or make it independent, e.g. compare `Path(os.fsdecode(raw_path)).read_bytes()` against the input bytes, or `os.stat` identity against the parent's file.

### IN-02: `test_native_encoding_availability_and_charmap_mismatch[False]` asserts only its own mock

**File:** `tests/test_cli.py:318-335`
**Issue:** In the unavailable case, the test calls the patched `subprocess.run(["locale","-a"])` and asserts `names == [b"C"]`, which is exactly the mocked return value. No test or product branch logic runs, so the case can never fail. The real unavailable path is exercised by `test_encoding_obligations_run_without_native_locale`, so no coverage is lost, but this case overstates the doc's claim that "availabilityの両分岐は決定論的回帰" ("both availability branches are deterministic regression tests").
**Fix:** Remove the `False` parameter, or have it call `test_html_preserves_basename_in_filesystem_encoding(tmp_path)` and assert the controlled-only message via `capsys`.

### IN-03: Final ledger identity is not bound to the finalize request's hash

**File:** `tools/verify_wordfreq_html.py:1281-1290`
**Issue:** The request hash is compared with `digest(ledger_path)` at line 1283. The ledger is then parsed in a separate read at line 1286, and `manifest["ledger_sha256"]` is recomputed after validation at line 1290. If `reviews.json` is replaced between those reads, the session validates and records a ledger the reviewer never attested. `ledger_errors` still validates every field, and `final_review_errors` compares the content, so this is a provenance-binding gap, not an acceptance bypass.
**Fix:** Read the bytes once, check them against the request hash, and parse those same bytes:
```python
data = ledger_path.read_bytes()
if request["ledger_sha256"] != hashlib.sha256(data).hexdigest():
    raise ValueError("finalize request/ledger identity changed")
ledger = json.loads(data.decode("utf-8"))
...
manifest["ledger_sha256"] = request["ledger_sha256"]
```

---

_Reviewed: 2026-11-17T19:49:18Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
