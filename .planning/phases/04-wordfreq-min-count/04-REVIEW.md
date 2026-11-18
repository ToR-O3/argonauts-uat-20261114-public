---
phase: 04-wordfreq-min-count
reviewed: 2026-11-18T03:16:50Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - README.md
  - docs/wordfreq-min-count-verification.md
  - openspec/changes/r-e476c11d-wordfreq-min-count/tasks.md
  - tests/test_cli.py
  - tests/test_min_count_verifier.py
  - tools/verify_wordfreq_min_count.py
  - wordfreq/__main__.py
findings:
  critical: 0
  warning: 2
  info: 4
  total: 6
  necessity: 0
status: issues_found
---

# Phase 4: Code Review Report

**Reviewed:** 2026-11-18T03:16:50Z
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

Scope: SUMMARY key-files (04-01, 04-04 block lists) cross-checked against `gsd_run check evaluation-scope --phase 04`
(status `degraded`, reason `no-task-commit-rows`, source `phase-range`, rangeBase `3e98720e2f6975f1a48f03f3176bd44121135be8`;
no outsideUnion / unreachable / missingOnDisk). The cross-check added `README.md`, `tests/test_cli.py` and
`wordfreq/__main__.py` (04-02/04-03 SUMMARYs use inline `[a, b]` lists the extractor does not parse). Planning artifacts excluded.
Depth `standard` from `workflow.code_review_depth`; no fallow pre-pass, no reviewer lanes. Reviewed at HEAD `afaa56fc022c895ee2243b8f67a239c7c0096086`.

**Product change (`wordfreq/__main__.py` +7/-1):** correct. `--min-count` uses the existing argparse `type=int`
path, rejects `< 1` with `parser.error` (exit 2) before `FileSource.read_text()`, keeps `total` from the unfiltered
`counts` (line 35), filters into a new `Counter` built by a dict comprehension that preserves first-occurrence insertion
order (lines 36-37), and then calls the unchanged `top_words` (line 38). It does not mutate `counts`. `top_words` (`wordfreq/aggregator.py:17`)
is a stable sort on `-count`, so tie order holds. Huge integers (`10**100`) and `+2`/`02` parse correctly. No security
issue: there is no new I/O, and HTML output still goes through the existing formatter. README wording matches the behavior.

**Verification code:** the large driver (`tools/verify_wordfreq_min_count.py`) fails closed. Validators catch exceptions
and turn them into errors, sealed markers use exclusive creation or a hash pair, and a publication failure revokes all
view/derived verdicts. No defect was found that would let a forged or partial capture validate. The two warnings confirm
the 04-04 per-PLAN findings independently. Both are test-strength gaps, not product defects. The info items cover brittleness and duplication.

Necessity (category 4) was assessed against `references/necessity-review.md`. No finding qualifies: the guards in the
driver sit on trust boundaries (saved files, env, git state), and the `Counter(...)` wrap in `__main__.py:36` keeps
`top_words`'s declared `Counter[str]` contract.

## Warnings

### WR-01: Runbook mutation test accepts any AssertionError/SystemExit, so it does not prove the targeted check fired

**File:** `tests/test_min_count_verifier.py:542`
**Issue:** `test_browser_free_runbook_rejects_mutations` applies one textual mutation and then expects only
`pytest.raises((AssertionError, SystemExit))` from the whole `assert_runbook_contract`. Any failing assertion satisfies
it, so the test does not show that the specific contract clause it targets catches the mutation. For example,
the `delivery` mutation (`PM原本読取りgate` → `添付だけ`) passes as long as *some* assertion trips, and the `root` mutation passes
whichever check fails first. If a future refactor removed the `final.review_ledger == review.output_dir / "reviews.json"`
assertion, the `root` case could still pass through an unrelated failure, or start failing for an unrelated reason that nobody
notices. The mutation suite therefore gives weaker evidence than its name suggests.
**Fix:** Match the expected failure per defect, for example by giving each assertion in `assert_runbook_contract` a stable
message and parametrizing the expected text:
```python
@pytest.mark.parametrize("defect,expected", [("mode", SystemExit), ("ac7", "AC/REQ table"),
                                             ("baseline", "baseline不変"), ("root", "ledger root"), ...])
...
with pytest.raises(AssertionError, match=expected): assert_runbook_contract(document)
```
(For `SystemExit` cases, assert `excinfo.value.code == 2`.)

### WR-02: Runbook contract validates only the four `env … verify_wordfreq_min_count.py` lines

**File:** `tests/test_min_count_verifier.py:485-486`
**Issue:** `assert_runbook_contract` extracts executable examples with
`^env .* tools/verify_wordfreq_min_count\.py (.+)$` and requires exactly 4 of them. The runbook's other executable
instructions are not checked against reality:
- the two pytest commands at `docs/wordfreq-min-count-verification.md:18-19` (`-k saved_baseline` / `-k browser_free`, env var name `WORDFREQ_MIN_COUNT_BASELINE_ROOT`);
- the launcher substitution at `docs/wordfreq-min-count-verification.md:42-43` (`.planning/argonauts/t_e22f75a9/run154/authorized_capture_retry.py`).

If either drifts (a renamed `-k` selector that collects 0 tests, a renamed env var, or a missing launcher), the contract test still
passes, even though the runbook says "0 collected" counts as a failure. The contract claims to check "executable examples against the actual parser",
and it does so for only part of the document.
**Fix:** Also extract the `-m pytest tests/test_min_count_verifier.py …` lines and assert that every `-k` selector matches at
least one test name defined in the module, and that every env var referenced is one the module reads (`WORDFREQ_MIN_COUNT_BASELINE_ROOT`,
`WORDFREQ_MIN_COUNT_CAPTURE_ROOT`). Assert that the launcher path named in the runbook exists (`(ROOT / path).is_file()`), or
narrow the docstring to state that only the driver command lines are contract-checked.

## Info

### IN-01: Source-order attestation hard-codes line numbers of `wordfreq/__main__.py`

**File:** `tools/verify_wordfreq_min_count.py:713`
**Issue:** `ledger_errors` requires `source["lines"] == [34, 35, 36, 37, 38, 44]`, mirrored in
`tests/test_min_count_verifier.py:351` and `docs/wordfreq-min-count-verification.md:86,91`. The check already binds the
file's SHA-256 at the reviewed head. With fixed line numbers on top of that, any harmless edit to `__main__.py` (an import or a
comment) breaks the driver, the synthetic tests and the runbook together, even when the filter→top order is unchanged.
**Fix:** Derive the expected lines from the source (for example, locate `total = sum(`, `selected_counts`, `top_words(`, `format_html(`
with `ast`/text search) or keep only the SHA binding and the judgment token.

### IN-02: `datetime` reached through the helper module's namespace (`parts.datetime`)

**File:** `tools/verify_wordfreq_min_count.py:172`
**Issue:** Lines 172, 310, 737 and 841 call `parts.datetime.fromisoformat(...)`, relying on `tools/verify_wordfreq_html.py:8`
happening to do `from datetime import datetime`. If that helper changes its import style, the driver breaks with an `AttributeError`.
Validators would turn this into "malformed" errors, which fails closed but is misleading.
**Fix:** `from datetime import datetime, timedelta` at the top of the driver and use `datetime.fromisoformat` directly.

### IN-03: Duplicate path-relocation implementation

**File:** `tools/verify_wordfreq_min_count.py:278-285`
**Issue:** `baseline_errors` defines a nested `relocate` closure that duplicates the module-level `relocate(value, old, new)`
at lines 395-402 (same prefix logic). Two copies of path-rebinding logic can drift; this logic decides whether a successor worktree's evidence is accepted.
**Fix:** Move the module-level `relocate` above `baseline_errors` and call `relocate(index, original_root, output)`.

### IN-04: Shadowed comprehension variable over a private argparse attribute

**File:** `tests/test_min_count_verifier.py:495`
**Issue:** `{a for a in v.parser()._actions if a.dest == "mode" for a in a.choices}` reuses `a` for both the action and
the choice, and reads the private `_actions`. It is correct today but hard to read and depends on argparse internals.
**Fix:** `mode_action = next(x for x in v.parser()._actions if x.dest == "mode"); assert set(modes) == set(mode_action.choices)`
or keep the expected tuple literal next to the driver's `choices=`.

---

_Reviewed: 2026-11-18T03:16:50Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
