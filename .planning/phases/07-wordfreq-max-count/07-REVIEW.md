---
phase: 07-wordfreq-max-count
reviewed: 2026-11-25T14:03:45Z
depth: standard
files_reviewed: 6
files_reviewed_list:
  - wordfreq/__main__.py
  - README.md
  - tests/test_cli.py
  - tests/test_max_count_verifier.py
  - tools/verify_wordfreq_max_count.py
  - docs/wordfreq-max-count-verification.md
findings:
  critical: 0
  warning: 2
  info: 4
  total: 6
  necessity: 0
status: issues_found
---

# Phase 7: Code Review Report

**Reviewed:** 2026-11-25T14:03:45Z
**Depth:** standard (from workflow.code_review_depth)
**Files Reviewed:** 6
**Status:** issues_found

## Summary

Scope is the phase 7 source diff `origin/v112-b...HEAD` at HEAD `b4e9037892f01582554a96df2389c9e0458d7c35`, excluding `.planning/`, `openspec/`, `_bmad-output/`, `.compound-engineering/` and `docs/solutions/`. The scope was passed in explicitly, so the SUMMARY/git tiers were not used. `init.code-review 7` found the phase, and `workflow.code_review` is `true`. No fallow pre-pass ran (`fallow_enabled: false`), and no reviewer lanes were requested. This run was unattended in a subagent that could not dispatch further agents, so the orchestrator ran the gsd-code-reviewer role inline, following that agent's own instructions. COMMIT_DOCS was forced to false for this run, so the report is not committed.

Product change (`wordfreq/__main__.py:18,37-39`): `--max-count` is an `int` defaulting to `None`. The upper bound is joined with AND to the existing `min-count` filter, after the original Counter and total are computed and before `top_words`. The original `counts` Counter is not mutated, and the HTML total stays the pre-filter total. Zero, negative and inverted ranges produce a normal empty result. Non-integer or missing values make argparse exit 2 before any input is read. No product defect was found. The README example and its claims match the implementation. The current hashes of `wordfreq/__main__.py` and `README.md` match the `approved` pins in `validate_scope`. Every changed path since START is either in the allowed exact set or under an allowed prefix.

The findings are in the evidence tool and in the tests' reliability: the environment recorded for the full suite differs from the one it actually runs in, and one input-failure test cannot pass when run as root. The rest are Info-level robustness or maintainability notes. Necessity was assessed using `references/necessity-review.md`. There were no necessity findings: the guards are on trust boundaries (argv, env, files, git) or are deliberate defence in depth.

## Narrative Findings (AI reviewer)

## Warnings

### WR-01: Full-suite subprocess runs with the full inherited environment, but `suite-command.json` records the pinned environment

**File:** `tools/verify_wordfreq_max_count.py:513-518`
**Issue:** `capture()` runs `pytest tests/` with `env = dict(os.environ, WORDFREQ_MAX_ACTIVE_ROOT=...)`. That is the caller's entire environment: every inherited variable, any tokens, and whatever `PYTHONHASHSEED`, `PYTHONIOENCODING` or `PYTHONUTF8` the caller has. But `suite-command.json` (line 515) stores `environment=environment()`, the filtered and pinned set (`PYTHONHASHSEED='0'`, UTF-8 forced). So the sealed evidence claims a reproducible, pinned environment that the suite did not actually run under. CLI case capture (lines 363, 387) does use `environment()`, so the suite step is inconsistent with the rest of the tool. A suite result that depends on hash seed or locale could therefore be sealed under a false provenance record. The full environment, including any secrets, is also passed to every test subprocess. That contradicts the stated intent at line 63 to use an "explicit, non-secret execution environment".
**Fix:** Run the suite under the same environment that is recorded:
```python
suite_env = dict(environment(), WORDFREQ_MAX_ACTIVE_ROOT=str(output))
save_json(output/'suite-command.json', dict(argv=argv, cwd=str(ROOT), environment=suite_env))
run = subprocess.run(argv, cwd=ROOT, env=suite_env, capture_output=True, timeout=...)
```
If `HERMES_*` variables are needed, add an explicit allow-list. If the inherited environment is intentional, record it accurately instead.

### WR-02: Permission-failure test fails deterministically when run as root

**File:** `tests/test_cli.py:952-957`
**Issue:** `test_max_count_input_failure[...-permission]` does `path.chmod(0)` and then asserts `pytest.raises(PermissionError)` on `path.read_bytes()`. Under uid 0, which is common in container CI, the read succeeds. The assertion then fails for 12 parametrizations (3 formats × 3 options) for a reason unrelated to the product. The evidence tool's `suite_counts` rejects any failure, so `capture`/`review-session` cannot complete in such an environment. The precondition check is a good guard against a false pass, but it should skip rather than fail.
**Fix:**
```python
if failure == "permission" and hasattr(os, "geteuid") and os.geteuid() == 0:
    pytest.skip("chmod 0 is not enforced for root")
```
If skips must stay at zero for the suite gate, choose the parametrization at collection time instead. For example, drop `"permission"` from the parameter list when running as root, and record that decision in the evidence.

## Info

### IN-01: Scope prefix lacks a trailing slash and also admits sibling directories

**File:** `tools/verify_wordfreq_max_count.py:477`
**Issue:** `'.planning/argonauts/r-d4bcda40'` has no trailing `/`, so `str.startswith` also accepts paths such as `.planning/argonauts/r-d4bcda40-other/...` or `.planning/argonauts/r-d4bcda40x`. The other two prefixes end with `/`.
**Fix:** Use `'.planning/argonauts/r-d4bcda40/'`.

### IN-02: Runbook commands hard-code a user-specific interpreter path and an output root that already exists

**File:** `docs/wordfreq-max-count-verification.md:39-40,70,88`
**Issue:** The commands pin `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3` and `--output-dir .../quality/final-01`. The current worktree already contains untracked files under `quality/final-01`, so pasting the command as written stops with `FileExistsError`. That is safe, but line 34 tells the reader to pick `final-02` while the commands still say `final-01`. The interpreter path only works on one machine.
**Fix:** Use placeholders such as `<python>` and `<fresh-root>`, or state explicitly that `final-01` must be replaced by the next unused number.

### IN-03: Hard-coded baseline case count in a parametrized test

**File:** `tests/test_cli.py:1017`
**Issue:** `range(39)` duplicates the case count from `build_baseline_cases()` (13 × 3). If the baseline definition changes, the test will either miss cases silently or raise `IndexError` instead of reporting a mismatch.
**Fix:** Derive the parameters from the sealed index, or add `assert len(index["cases"]) == 39` with a message, so a count drift fails with a clear reason.

### IN-04: The role/profile gate is environment-only and can be spoofed

**File:** `tools/verify_wordfreq_max_count.py:338-343`
**Issue:** `actor()` only compares `HERMES_PROFILE` and the basename of `HERMES_HOME`. The test fixture spoofs both (`tests/test_max_count_verifier.py:104-105`), which shows that any process can satisfy the check. The runbook (line 23) already says this is provenance, not authentication. Flagged only so that no downstream consumer treats `provenance.role == 'quality'` as proof of identity.
**Fix:** No code change required. Keep the documentation caveat, and have downstream gates (such as PM readback) rely on card or attachment identity rather than this field.

---

_Reviewed: 2026-11-25T14:03:45Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
