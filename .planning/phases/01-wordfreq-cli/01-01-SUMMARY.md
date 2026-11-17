---
phase: 01-wordfreq-cli
plan: "01"
subsystem: testing
tags: [python, unicode, tokenizer, pytest]
requires: []
provides:
  - Unicode word extraction with casefold normalization and tokenizer injection
  - pytest 9.2.0 validation environment
affects: []
tech-stack:
  added: [pytest 9.2.0 (development environment only)]
  patterns: [pure tokenizer, callable injection]
key-files:
  created: [wordfreq/__init__.py, wordfreq/tokenizer.py, tests/test_tokenizer.py]
  modified: [openspec/changes/r-5a3b8a3f-wordfreq/tasks.md]
key-decisions:
  - Human default explicitly approved pytest 9.2.0 installation on this card.
requirements-completed: [REQ-05, REQ-07]
coverage:
  - id: D1
    description: Unicode word extraction, casefold, and callable injection
    requirement: REQ-05
    verification:
      - kind: unit
        ref: python -m pytest tests/test_tokenizer.py -x
        status: pass
    human_judgment: false
  - id: D2
    description: Development pytest environment is usable
    requirement: REQ-07
    verification:
      - kind: other
        ref: python -m pytest --version
        status: pass
    human_judgment: false
duration: 4min
completed: 2026-11-17
status: complete
---

# Phase 1 Plan 01: Tokenizer Summary

**Unicode `\w+` extraction and casefold normalization are independently callable, with an injected tokenizer and six passing unit tests.**

## Performance

- Started: 2026-11-17T02:53:03Z
- Completed: 2026-11-17T02:56:16Z
- Tasks: 3 (one approved checkpoint, environment setup, tokenizer)
- Product/test files: 3

## Accomplishments

- Task 1: Human `default` approved PyPI pytest 9.2.0 and pytest-dev/pytest provenance in this card's comment at 2026-11-17 11:51 JST. No automatic approval was used.
- Task 2: `uv pip install pytest` installed pytest 9.2.0 for Python/Python3 3.14.9. `python -m pytest --version` returned `pytest 9.2.0`. No runtime dependency or repository package configuration was added.
- Task 3: `_WORD_RE = re.compile(r"\w+", re.UNICODE)`, `default_tokenizer`, and `iter_tokens` implement the planned interface. Unit tests cover casefold (including Straße/STRASSE), punctuation/symbol boundaries, underscores/digits, maximal Japanese word sequences with repeatability, empty input, and injected tokenizer input/output.
- OpenSpec task 1.1 checked in the same commit as final tokenizer implementation.

## Task Commits

- `868f888`: RED — package/casefold contract test and captured evidence.
- `6cd634f`: GREEN — minimal split/casefold iterator and injection.
- `15da486`: RED — punctuation/Unicode extraction contract and evidence.
- `f073ca3`: GREEN — Unicode regex extraction, remaining edge tests, OpenSpec 1.1 check.
- Tasks 1 and 2 changed approval/environment only and have no separate repository code commit.

## Verification and TDD

- First RED: named test executed and failed at the package-availability assertion because the planned standalone package was absent, not a collection/import/fixture error. The token normalization assertion then passed after package implementation. This initial RED does not independently discriminate casefold from lower; the final Straße assertion does.
- Second RED: default tokenizer returned `one,` rather than `one`; the named punctuation assertion failed for missing extraction behavior. Japanese splitting also failed before regex implementation.
- Official `check tdd-red-evidence` classified both unchanged JUnit reports as `RED_EVIDENCE_OK`, one target failure, zero errors. Raw pytest console format was initially rejected as unsupported; rerunning with pytest's built-in JUnit reporter resolved that without altering reports.
- RED evidence JSON, original JUnit XML, and console logs are under `.planning/argonauts/t_1d238d2e/`.
- `python -m pytest tests/test_tokenizer.py -x`: **6 passed**.
- `python -m pytest -q`: **6 passed** (current full suite).
- `PYTHONHASHSEED=1 python -m pytest tests/test_tokenizer.py -q`: **6 passed**.
- `PYTHONHASHSEED=987 python -m pytest tests/test_tokenizer.py -q`: **6 passed**.
- `git diff --check`: exit 0.
- Official evaluation-scope resolved four plan commits on this branch.
- Refactor: not needed.

## Deviations from Plan

- [Rule 3 - Blocker] STATE.md had `Plan: none yet (Plans: TBD)`, which the official advance-plan diagnostic could not parse. Used its suggested `Current Plan: 1` / `Total Plans in Phase: 4`, checked the official four-plan list, and called `state.begin-phase --phase 1` before execution. This repairs bookkeeping only; scope is unchanged.
- JUnit evidence capture helper added under planning artifacts for the official RED gate; no product dependency or scope change.

## Issues Encountered

Official CLI launch functions do not persist between terminal calls in this environment; each invocation sources the installed official launcher. The initial raw pytest report was not an accepted RED evidence format; built-in JUnit was accepted.

## Files Created/Modified

- `wordfreq/__init__.py`: package marker.
- `wordfreq/tokenizer.py`: pure extraction and normalization with callable injection.
- `tests/test_tokenizer.py`: six standalone tests, no file/CLI dependencies.
- `openspec/changes/r-5a3b8a3f-wordfreq/tasks.md`: only 1.1 checked.
- Planning RED evidence and state/roadmap close-out records.

## User Setup Required

None for this plan. CI pytest job verification belongs to PLAN 01-04; CI success is not claimed here.

## Next Phase Readiness

Ready for 01-02 after this card's quality review. No later PLAN executed. REQ-05 and REQ-07 above are copied verbatim from PLAN frontmatter as required by the SUMMARY schema; they describe this plan's contribution, not completion of the entire shared requirements. Their global completion remains gated by sibling PLAN summaries and phase verification.

## Self-Check: PASSED

All three product/test files exist, official scope resolved four local plan commits, the six current tests pass, and the approved checkpoint is recorded. Phase 1 remains incomplete.
