---
phase: 08-wordfreq-exclude
reviewed: 2026-11-28T18:36:23Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - README.md
  - openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md
  - tests/fixtures/README.md
  - tests/fixtures/exclude-baseline-git-objects.json
  - tests/test_cli.py
  - wordfreq/__main__.py
  - wordfreq/exclusions.py
findings:
  critical: 0
  warning: 0
  info: 2
  total: 2
  necessity: 0
status: issues_found
---

# Phase 8: Code Review Report

**Reviewed:** 2026-11-28T18:36:23Z
**Depth:** standard (from workflow.code_review_depth)
**Files Reviewed:** 7
**Status:** issues_found

## Summary

**Scope source.** Tier 2 (SUMMARY.md `key-files`) gave `wordfreq/exclusions.py`, `wordfreq/__main__.py`,
`tests/test_cli.py`, `README.md` and `openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md`; the
`.planning/` entries were filtered out. The Tier 3 cross-check against
`gsd_run check evaluation-scope --phase 08 --raw` added `tests/fixtures/README.md` and
`tests/fixtures/exclude-baseline-git-objects.json`. The resolver returned **`status: degraded`**
(`source: phase-range`, `reason: no-task-commit-rows`, `rangeBase: 17648fc2aa1fc9740faa3066a26daee2e8464a86`),
not `unresolvable`, so the explicit fallback list was not needed. The resolver's file set is the given
6-file product diff plus the OpenSpec `tasks.md`, which is a document and was checked only for
consistency. It reported no `outsideUnion`, `unreachable` or `missingOnDisk` entries. No prior REVIEW.md
commit exists, so this is a full review, not an incremental one. Fallow was disabled, no reviewer-lane
flags were given, and there is no `HERMES.md` or project skills directory.

**Assessment.** The production change is small and correct:
- `parse_exclusions` validates each original trimmed line with the tokenizer's own `\w+` grammar
  (`wordfreq/tokenizer.py:6`), then casefolds it. This keeps exclusion membership consistent with how
  body tokens are formed and normalized, including `İ` → `i̇` and `Straße`/`STRASSE`.
- Line numbers count ignored lines, and CRLF is handled by universal newlines plus `strip()`.
- `__main__` checks argv/numeric values first, then reads and fully validates the exclusion FILE, then
  reads the body.
- Every exclusion failure (`InputError` and `InvalidExclusion`) exits 2 with an empty stdout. Body
  failures still exit 1.
- `total` is still computed before exclusion and min-count, and exclusion is applied before
  min-count/top in one shared `selected_counts` that all three formatters use.

I traced edge cases and found no correctness or security defects: empty/comment-only/unmatched files,
BOM, a lone combining mark, NBSP and other Unicode whitespace, surrogate-escaped paths in diagnostics,
and duplicate rows.

README statements match the code. The fixture's object set matches tests/fixtures/README.md (commit,
root tree, `wordfreq` tree, 6 blobs), and so does the "64 comparisons" count (2 contents × 4 formats ×
8 option sets). The corruption controls behave as documented:
- missing-blob → `git show` CalledProcessError
- changed-blob → oid AssertionError
- rehashed-blob → the tree still points at the original oid → CalledProcessError

The two findings below are Info-level test-reliability notes. There are no Critical or Warning findings.
Necessity was assessed (rubric read) and nothing qualified. The exclusion FILE is a trust boundary, so
its validation is not an impossible-state guard.

## Info

### IN-01: Shallow-checkout test mixes working-tree fixtures with committed product code

**File:** `tests/test_cli.py:1356-1366`
**Issue:** The test clones only committed `HEAD` (`git clone --no-local --depth 1`). It then copies the
*working-tree* `tests/fixtures` over the clone (`copytree(..., dirs_exist_ok=True)`). Because `ROOT` is
monkeypatched to the clone, the candidate root copies the *committed* `wordfreq/`. So in a dirty local
tree the test can pass with a fixture that was never committed. It also checks committed code rather
than the edited `wordfreq/` it appears to cover. CI (clean checkout) is unaffected, and the comment at
line 1362 states this is intentional for the RED/GREEN loop.
**Fix:** Now that the fixture is committed, drop the copy (or copy only when `git status --porcelain tests/fixtures` is non-empty and fail with a clear "commit the fixture" message), so the shallow test proves the committed state end to end.

### IN-02: Subprocess calls in the shallow-checkout test have no timeout

**File:** `tests/test_cli.py:1356, 1374-1375`
**Issue:** `git clone` and the two `python -m wordfreq` runs in this test pass `check=True` but no
`timeout`. Every other CLI/baseline subprocess in the file uses `timeout=10` (`run_cli_bytes` at
line 422, and lines 1470-1471, 1523). A stuck child would hang the suite instead of failing this test.
**Fix:** Add `timeout=` to these three `subprocess.run` calls, for example `timeout=60` for the clone and `timeout=10` for the CLI runs, matching the rest of the file.

---

_Reviewed: 2026-11-28T18:36:23Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
