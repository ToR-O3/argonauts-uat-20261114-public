---
phase: 03-wordfreq-html-output
reviewed: 2026-11-17T16:15:42Z
depth: standard
files_reviewed: 10
files_reviewed_list:
  - wordfreq/__main__.py
  - wordfreq/aggregator.py
  - wordfreq/formatters.py
  - tools/verify_wordfreq_html.py
  - tools/wordfreq_html_geometry.js
  - tests/test_cli.py
  - tests/test_formatters.py
  - tests/test_aggregator.py
  - tests/test_sources.py
  - tests/test_html_verifier.py
findings:
  critical: 0
  warning: 3
  info: 5
  total: 8
  necessity: 0
status: issues_found
---

# Phase 03: Code Review Report

**Reviewed:** 2026-11-17T16:15:42Z
**Depth:** standard
**Files Reviewed:** 10
**Status:** issues_found

## Summary

Scope: `git diff 5a7659b949dc118b59cea5ef3eb40bcd94337d8d` at HEAD `995011cd3b77d4d87a6be3bdf5780bf5cbe3b95c` for the 10 listed files.

The product changes are small and correct for the cases checked:
- `format_html` escapes every value it interpolates (`html.escape(quote=True)`, and CR becomes `&#13;`). It contains no script, URL or external resource.
- `__main__` writes HTML as UTF-8 bytes whatever the locale. It decodes the basename with `errors="replace"`, so a filename that is not valid UTF-8 cannot raise.
- `top_words` uses a stable sort and does not mutate its input.

No security or data-loss defect was found in `wordfreq/`.

All three warnings are in the verification tool and its tests, not in the product code:
1. An accepted manifest still marks each view as pending.
2. The provenance check misses untracked test files that the suite will run.
3. Some tests fail on hosts that lack a specific locale, which includes the repository's own CI.

The necessity rubric (`gsd-core/references/necessity-review.md`) was applied. No finding qualified: the guards around the CLI and filenames sit at trust boundaries (argv, the filesystem, the locale).

## Warnings

### WR-01: Accepted final manifest keeps per-view `verdict: "pending-review"` and `reviewed_images: []`

**File:** `tools/verify_wordfreq_html.py:591-592` (set), `tools/verify_wordfreq_html.py:1151-1153` (final verdict)
**Issue:** `collect_view` creates each view with `reviewed_images=[]` and `verdict="pending-review"`. After a finalize that succeeds, `review_session` updates only the top-level fields `verdict`, `independent_acceptance` and `ac_verdicts` (lines 1151-1153). Nothing writes back to `cases[].views[]`. The saved `manifest.json` therefore says `verdict: "accepted"` at the top level, while every one of the 22 HTML views still says `verdict: "pending-review"` and `reviewed_images: []`. Each `derived.json` (line 657) is also frozen at the pending state. Quality's live run confirmed this. A downstream reader that checks per-view state will see the evidence as never reviewed. Worse, a reader that trusts the top level cannot tell which ledger entries approved which images. The evidence contradicts itself.
**Fix:** After a verdict without errors, project the ledger onto each view before the final `save_json`. For example, after line 1153:
```python
by_image = {r["image"]: r for r in ledger["reviews"]}
for case in manifest["cases"]:
    for view in case["views"]:
        view["reviewed_images"] = [dict(image=i["path"], sha256=i["sha256"],
            viewed_at=by_image[i["path"]]["viewed_at"]) for i in view["images"]]
        view["verdict"] = manifest["verdict"]
```
Then reset these fields to `unverified` in the `if manifest["errors"]` branch at lines 1168-1171. Alternatively, remove the per-view `verdict`/`reviewed_images` fields so the top level is the only authority. Add a test that asserts per-view state agrees with the final verdict.

### WR-02: Provenance and dirty checks do not cover test files that pytest collects outside `tests/`

**File:** `tools/verify_wordfreq_html.py:269-274`, `tools/verify_wordfreq_html.py:1063`
**Issue:** `provenance()` checks git status, and lists untracked files, only for `wordfreq`, `tools`, `tests` and the root `pyproject.toml`, `conftest.py`, `pytest.ini`, `tox.ini` and `setup.cfg`. `run_suite` runs plain `python -m pytest` from `ROOT`, and `pyproject.toml` sets no `testpaths`. Pytest therefore collects `test_*.py`, `*_test.py` and nested `conftest.py` files from every directory it does not skip, including `docs/`, `openspec/`, `_bmad/` and `_bmad-output/`. An untracked or modified `docs/test_x.py` or `_bmad/conftest.py` would change the suite. It could add tests, or monkeypatch and auto-pass tests through a conftest. Neither `product_status` nor `untracked_product` would report it, so the evidence in `suite.json`/`suite.xml` would be credited to a clean HEAD. The same gap means `scope_report()` (line 824) and the gates at lines 669, 938, 1097 and 1165 all pass.
**Fix:** Do one of the following:
- Pin collection by running `[sys.executable, "-m", "pytest", "tests", "-p", "no:cacheprovider", "--rootdir", str(ROOT)]`, and add `testpaths = ["tests"]` to `[tool.pytest.ini_options]` in `pyproject.toml`.
- Or make `provenance()` dirty-check the whole worktree except the allowed `.planning/` evidence paths. Record any untracked `test_*.py`, `*_test.py` or `conftest.py` anywhere as dirty.

Add a regression test with an untracked `docs/test_extra.py`.

### WR-03: Locale-dependent CLI tests fail instead of skipping on hosts without ISO-8859-15 locales (including the repo CI)

**File:** `tests/test_cli.py:296`, `tests/test_cli.py:320-332`
**Issue:** `test_html_preserves_basename_in_filesystem_encoding` asserts that `en_GB.iso885915` is in `locale -a`. `test_html_bytes_are_utf8_independent_of_stdout_encoding[en_GB.iso885915-None]` asserts that `locale charmap` is `ISO-8859-15`. The repository's own workflow, `.github/workflows/pytest.yml`, runs `python -m pytest` on `ubuntu-latest` and installs no locales. Stock runners and containers usually ship only `C.UTF-8` and `en_US.UTF-8`, so both tests fail there with assertion errors rather than being reported as skipped. They pass only on this WSL host, where the locale happens to be installed. A failure caused by the environment makes the suite unreliable, and `run_suite` will refuse any review session on such a host.
**Fix:** Skip when the locale is missing instead of failing, for example:
```python
if locale_name not in available:
    pytest.skip(f"{locale_name} not installed")
```
Apply the same skip to the parametrized case, after a `locale -a` probe. Or install the locale in CI (`sudo locale-gen en_GB.ISO-8859-15`) and document the requirement.

## Info

### IN-01: Duplicated `args.format == "html"` dispatch in `main`

**File:** `wordfreq/__main__.py:33-47`
**Issue:** The format is tested twice: once to build `output`, and again to choose between writing bytes and writing text. This is harmless, but the two branches can drift apart.
**Fix:** Write the HTML bytes inside the first `html` branch, or keep the dispatch in a single `if/elif/else` that produces `(output, writer)`.

### IN-02: `scope_report()` git failures escape the CLI error handling and the manifest

**File:** `tools/verify_wordfreq_html.py:265`, `tools/verify_wordfreq_html.py:818`, `tools/verify_wordfreq_html.py:1087`, `tools/verify_wordfreq_html.py:1250`
**Issue:** `git()` uses `check=True`, which raises `subprocess.CalledProcessError`. That happens, for example, when the hard-coded `APPROVED_PRODUCT`/`SCOPE_BASE` commits are missing from a shallow clone. `review_session` calls `scope_report()` at line 1087, before its `try`, and `main` catches only `ValueError, OSError, KeyError, TypeError`. The run ends in a raw traceback, and `manifest.json` is never written. The tool still fails closed (exit is non-zero), but it leaves no failure provenance.
**Fix:** Add `subprocess.SubprocessError` to the `except` tuple at line 1250. Move the `provenance()`/`scope_report()` calls into the guarded block, or wrap the git errors into `ValueError`.

### IN-03: Hard-coded commit and profile constants make the verifier single-use

**File:** `tools/verify_wordfreq_html.py:793-801`
**Issue:** `SCOPE_BASE`, `APPROVED_PRODUCT`, `ACTORS` (specific `argonauts-uat-*` profile names) and `SCOPE_FILES` (including an `openspec/changes/r-50053edc-...` path) are literals. The tool can only verify this one phase in this one environment.
**Fix:** Accept the base, the approved snapshot and the actor mapping as CLI options or a config file. Keep the current values as defaults.

### IN-04: Scope-gate tests are tautological against the live worktree state

**File:** `tests/test_html_verifier.py:511`, `tests/test_html_verifier.py:680-683`
**Issue:** The test asserts `bool(report["errors"]) == bool(v.provenance()["product_status"])`. That passes whether the worktree is clean or dirty, so it never proves the scope gate rejects anything on the real repo. Separately, `test_plan_quality_commands_resolve_actual_actor_without_actor_option` (line 537) reads `.planning/.../03-04-PLAN.md`, which couples the product suite to planning artifacts.
**Fix:** Run the real-repo assertion against a temporary git repo whose state is known, as `test_root_test_configuration_is_dirty_evidence` already does. Move the PLAN-command parsing check out of the product test suite.

### IN-05: Permission-failure matrix fails when run as root

**File:** `tests/test_cli.py:446-449`
**Issue:** `pytest.raises(PermissionError)` on `path.read_bytes()` after `chmod(0)` fails under UID 0, where read access is not denied, as in many Docker CI images. The test checks its precondition correctly but should skip rather than fail.
**Fix:** `if os.geteuid() == 0: pytest.skip("root bypasses file permissions")` for `failure == "permission"`.

---

_Reviewed: 2026-11-17T16:15:42Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
