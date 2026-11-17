---
phase: 01-wordfreq-cli
plan: "03"
subsystem: cli
tags: [python, argparse, protocol, setuptools, pytest]
requires:
  - phase: 01-02
    provides: Aggregation, UTF-8 source boundary and pure formatters
provides:
  - Source-boundary composition tests with FileSource spy and FakeSource
  - Repository-local CLI with top and format options and exit codes 0/1/2
  - Minimal package metadata with no runtime dependencies
affects: [01-04]
tech-stack:
  added: []
  patterns: [argparse validation, boundary composition, subprocess CLI tests]
key-files:
  created: [tests/test_sources_boundary.py, wordfreq/__main__.py, tests/test_cli.py, pyproject.toml]
  modified: [openspec/changes/r-5a3b8a3f-wordfreq/tasks.md]
key-decisions: []
requirements-completed: [REQ-01, REQ-02, REQ-03, REQ-06, REQ-07, REQ-08]
coverage:
  - id: D1
    description: Pure aggregation avoids file acquisition and accepts equivalent fake and file source text
    requirement: REQ-06
    verification:
      - kind: unit
        ref: python -m pytest tests/test_sources_boundary.py -x
        status: pass
    human_judgment: false
  - id: D2
    description: Default top ten, top boundary and all-results behavior, text and JSON, and exit code contracts
    requirement: REQ-01
    verification:
      - kind: integration
        ref: python -m pytest tests/test_cli.py -x
        status: pass
    human_judgment: false
  - id: D3
    description: Setuptools package metadata with empty runtime dependencies and pytest only in development extras
    requirement: REQ-08
    verification:
      - kind: unit
        ref: tests/test_cli.py#test_package_declares_only_development_dependencies
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_readme_runs_as_json_from_repository_without_installation
        status: pass
    human_judgment: false
duration: 6min
completed: 2026-11-17
status: complete
---

# Phase 1 Plan 03: Source Composition and CLI Summary

**A repository-local stdlib CLI now composes UTF-8 input, normalized frequency counting, deterministic top-N selection, and text/JSON output with explicit exit codes.**

## Performance

- Started: 2026-11-17T03:29:26Z
- Product verification completed: 2026-11-17T03:35:06Z
- Duration: 6min (rounded)
- Tasks: 3
- Product/test/config files: 4; OpenSpec task file: 1

## Accomplishments

- Added three boundary tests: pure aggregation never invokes FileSource, a TextSource-compatible FakeSource provides equivalent text, and real-file composition crosses FileSource.read_text exactly once. This test-only task changes no production behavior and therefore has no claimed RED cycle.
- Added build_parser/main and 19 subprocess CLI scenarios, verifying exact default top-ten output, top 3/top 1/fewer-than-N, invalid zero/noninteger/negative top, JSON shape/order, invalid format, missing/decode-failing/unopenable input, file argument counts, empty text/JSON, explicit text, and unchanged input/git status. Only InputError is caught. Exit decisions stay in __main__.
- Added minimal setuptools metadata with explicit wordfreq package, dependencies=[], and pytest solely in development extras. Two additional tests parse TOML and execute README.md as JSON without installation. No package installation or egg-info generation was performed.
- Checked OpenSpec tasks 2.3, 3.1 and 3.2 in the corresponding task completion commits. Task 3.3 remains unchecked for PLAN 01-04.

## Task Commits

| Task / behavior | RED | GREEN / completion |
|---|---|---|
| 1: source boundary tests only | not applicable | 0226919 |
| 2: default text CLI | 1d67ffe | 816a736 |
| 2: top option | 1a1850e | 4d4e7e3 |
| 2: positive-top validation before input | 329e7c5 | aa31457 |
| 2: JSON option | 56b97e2 | 24880a9 |
| 2: concise InputError + regression scenarios | ee8d0af | ea5e166 |
| 3: minimal configuration + metadata regression tests | not applicable (configuration) | e4a33d9 |

## Verification and TDD

Each of the five named CLI RED runs executed its target and failed an assertion. The official `check tdd-red-evidence` returned `RED_EVIDENCE_OK` for each real, unchanged pytest JUnit report. The raw XML, console output, records, semantic assessments and capture script are in `.planning/argonauts/t_4b01f783/`.

Semantic assessment: default CLI RED proves a missing entry point via the subprocess exit-code assertion, not sorting discrimination. Top/JSON RED demonstrate absent option support via actual exit 2. Positive-top RED demonstrates that invalid N reaches input reading (exit 1 rather than required exit 2). InputError RED directly discriminates stderr behavior (19 traceback lines instead of one error line). GREEN executes the full output/ordering assertions. Additional edge scenarios are regression checks of the now-present paths, not separately claimed RED evidence. Refactor was unnecessary.

Fresh final results:
- `python -m pytest tests/test_sources_boundary.py -x`: **3 passed**.
- `python -m pytest tests/test_cli.py -x`: **21 passed** (19 CLI cases + metadata/readme checks).
- `python -m pytest -q`: **43 passed**.
- `PYTHONHASHSEED=42 python -m pytest -q`: **43 passed**.
- `python -m wordfreq README.md --format json`: exit **0**, real JSON array; also parsed by the README test.
- `git diff --check -- wordfreq tests pyproject.toml openspec`: exit **0**. Raw reporter evidence is intentionally not whitespace-normalized.
- Official `evaluation-scope --plan 01-03 --commits-only --raw`: resolved **12** task commits on this branch.

Readonly evidence is exactly the required unchanged input bytes/input directory and unchanged `git status --porcelain --untracked-files=all` assertion. It is not a claim of filesystem tracing, cold-import bytecode suppression, or independently exercised interruption/concurrent execution. Python's ordinary interpreter caches are not altered by application code.

## Decisions Made

None - followed the planned signatures, argparse settings and setuptools configuration. Dangerous path pyproject.toml was added as the single planned metadata file.

## Deviations from Plan

None in product scope. Planning-only RED evidence was added for the official gate. Execution is inline because the configured threshold is three tasks. Installed GSD files are under the active profile home; the official launcher must be sourced in each terminal command needing gsd_run because shell functions did not survive the next call. One invocation failed with command-not-found before mutation; sourcing again resolved it.

## Issues Encountered

None blocking this PLAN. Existing CI concern belongs to PLAN 01-04, which has not been executed. No workflow files changed, no CI success is claimed, and no phase completion was performed.

## User Setup Required

None for this PLAN.

## Next Phase Readiness

Ready for PLAN 01-04 after this card's quality review. Requirement IDs above copy the PLAN verbatim; they do not claim REQ-07 CI completion or whole-phase acceptance. Shared requirement completion remains subject to the official readiness gate.

## Self-Check: PASSED

All four planned artifacts exist; task commands and full suite pass. The official scope resolves this PLAN's commits. The SUMMARY was committed before state mutations. Official `state.advance-plan` returned previous_plan=3/current_plan=4/total_plans=4; saved Current Position agrees (Phase 1 EXECUTING, Plan 4, Ready to execute). `roadmap.update-plan-progress` and saved ROADMAP agree at 3/4, In Progress. `state.update-progress` returned completed=3,total=4 but percent=0, matching the pre-existing zero-percent display behavior; no manual percentage rewrite was applied. Official readiness marked REQ-01/02/03/06/08 complete and kept REQ-07 blocked by PLAN 01-04. STATE.md, ROADMAP.md, REQUIREMENTS.md and generated state.json are included in the follow-up metadata commit. PLAN 01-04 and phase.complete were not executed.
