---
phase: 01-wordfreq-cli
plan: "02"
subsystem: testing
tags: [python, counter, protocol, utf8, json, pytest]
requires:
  - phase: 01-01
    provides: Standalone package and tokenizer
provides:
  - Pure Counter aggregation and deterministic top-word ordering
  - UTF-8 FileSource behind TextSource with InputError normalization
  - Pure text and ASCII-safe single-line JSON formatters
affects: [01-03, 01-04]
tech-stack:
  added: []
  patterns: [pure functions, structural input protocol, exception chaining]
key-files:
  created: [wordfreq/aggregator.py, wordfreq/sources.py, wordfreq/formatters.py, tests/test_aggregator.py, tests/test_sources.py, tests/test_formatters.py]
  modified: [openspec/changes/r-5a3b8a3f-wordfreq/tasks.md]
key-decisions: []
requirements-completed: [REQ-01, REQ-03, REQ-04, REQ-05, REQ-06]
coverage:
  - id: D1
    description: Iterable counting and deterministic frequency/word sorting
    requirement: REQ-04
    verification:
      - kind: unit
        ref: python -m pytest tests/test_aggregator.py -x
        status: pass
    human_judgment: false
  - id: D2
    description: UTF-8 input, empty file, missing/unopenable path and decode-error normalization without input modification
    requirement: REQ-01
    verification:
      - kind: unit
        ref: python -m pytest tests/test_sources.py -x
        status: pass
    human_judgment: false
  - id: D3
    description: Count-first text and ordered ASCII-safe JSON with empty output and exact integer round-trip
    requirement: REQ-03
    verification:
      - kind: unit
        ref: python -m pytest tests/test_formatters.py -x
        status: pass
    human_judgment: false
duration: 4min
completed: 2026-11-17
status: complete
---

# Phase 1 Plan 02: Aggregation, Sources and Formatters Summary

**Three independently callable stdlib-only components now provide deterministic frequency sorting, UTF-8 input error normalization, and count-first text / ASCII-safe JSON output.**

## Performance

- Started: 2026-11-17T03:17:28Z
- Completed: 2026-11-17T03:22:13Z
- Duration: 4min
- Tasks: 3
- Product/test files: 6; OpenSpec task file: 1

## Accomplishments

- `count_words` accepts an iterable and returns `Counter`; `top_words` sorts by `(-count, word)` before slicing. Tests fix apple/zoo ties, empty input, exact/oversized/one-item limits, nonmutation and large integers.
- `TextSource` declares `read_text() -> str`; `FileSource` reads UTF-8 in a context manager. OSError and UnicodeDecodeError become chained `InputError`, with the path retained. Real-file tests cover normal/empty/invalid files, missing paths, and an unopenable directory, including unchanged input bytes and no extra input-directory files.
- Pure formatters return count-first tab-separated text and ordered JSON objects with `ensure_ascii=True`, no indentation, and exactly one final JSON newline. Tests include empty output, Unicode and special-character round-trip, order, nonmutation, and arbitrary-size integer precision.
- OpenSpec tasks 1.2, 2.1, 2.2 checked in their respective GREEN implementation commits. No CLI, packaging, CI, boundary-composition implementation, dependency installation, or later PLAN work was done.

## Task Commits

| Task | RED commits | GREEN commits |
|---|---|---|
| 1: aggregator | ecc4bcc, e78d86a | b2f44ab, 37b1d6b |
| 2: sources | 4fd653e, 3a54941 | c7d699b, f76557d |
| 3: formatters | e651d4f, 4b03d29 | aaa9fbd, 114954c |

## Verification and TDD

All six named RED runs executed one target and failed an assertion (no collection/fixture errors). The official `check tdd-red-evidence` returned `RED_EVIDENCE_OK` for each unchanged built-in pytest JUnit report. Records, reports, raw console output and capture helper are in `.planning/argonauts/t_61fb0c48/`.

Semantic assessment: initial count/source/text RED asserts the planned module is absent; top_words/JSON RED asserts the public callable is absent. These availability failures do not independently prove sorting/formatting discrimination. Their GREEN runs execute the actual behavior assertions. The normalization RED directly discriminates behavior: observed FileNotFoundError versus required InputError. No claim is made that module-presence RED alone proves every edge case. Refactor was unnecessary.

Final fresh results:
- `python -m pytest tests/test_aggregator.py -x`: **4 passed**.
- `python -m pytest tests/test_sources.py -x`: **5 passed**.
- `python -m pytest tests/test_formatters.py -x`: **4 passed**.
- `python -m pytest -q`: **19 passed**.
- `PYTHONHASHSEED=42 python -m pytest -q`: **19 passed**.
- `git diff --check c1bd5d3..HEAD -- wordfreq tests openspec`: exit 0. This is explicitly the product/test/spec range, not a claim about unmodified raw pytest console evidence (which contains reporter whitespace).
- Official evaluation-scope resolved all 12 plan commits on this branch.

## Files Created/Modified

- `wordfreq/aggregator.py`, `tests/test_aggregator.py`: pure counting/sorting.
- `wordfreq/sources.py`, `tests/test_sources.py`: input boundary and error mapping.
- `wordfreq/formatters.py`, `tests/test_formatters.py`: pure text/JSON serialization.
- `openspec/changes/r-5a3b8a3f-wordfreq/tasks.md`: only this PLAN's three task checks changed.
- Planning RED evidence and this SUMMARY.

## Decisions Made

None - followed the specified interfaces and implementation choices.

## Deviations from Plan

None - product scope follows the plan. Added planning-only evidence capture for the mandatory official RED gate. The installed workflow uses the profile home rather than shell HOME; the official launcher was sourced from that installed location. Configured inline threshold 3 permits this three-task plan to execute in the parent, sequentially.

## Issues Encountered

None blocking. Previous PLAN's CI concern remains assigned to 01-04, not this implementation. Raw reporter evidence is preserved without whitespace cleanup.

## User Setup Required

None for this PLAN.

## Next Phase Readiness

Ready for 01-03 after quality review. Shared requirement IDs above are copied verbatim from PLAN metadata, not a claim that CLI-level requirements or the entire phase are complete; global marking must use the official shared-ID readiness gate. No next PLAN or phase completion was executed.

## Self-Check: PASSED

All six planned product/test files exist, all task acceptance commands pass, and official evaluation-scope resolves 12 commits on this branch. Phase 1 is still in progress.
