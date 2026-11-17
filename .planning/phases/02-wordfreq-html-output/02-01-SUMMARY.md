---
phase: 02-wordfreq-html-output
plan: "01"
subsystem: ui
tags: [python, html, escaping, counter, first-seen, cli]
requires:
  - phase: 01-wordfreq-cli
    provides: stdlib CLI and input/tokenizer/aggregation/formatter boundaries
provides:
  - Safe standalone HTML from CLI stdout with basename and pre-top total
  - Shared stable frequency-first selection with normalized first-seen ties
  - Static HTML and all-format ordering regression tests
affects: [02-02, 02-03, phase-verification]
tech-stack:
  added: []
  patterns: [single text-node escape boundary, stable Counter ordering, pure HTML formatter]
key-files:
  created: [tests/test_html_output.py]
  modified: [wordfreq/formatters.py, wordfreq/__main__.py, wordfreq/aggregator.py, tests/test_aggregator.py, tests/test_cli.py, CONCEPTS.md, openspec/changes/r-5c041156-wordfreq-html/tasks.md]
key-decisions:
  - "Preserve Counter insertion order through frequency-only stable sort, then top."
  - "Keep shared OpenSpec tasks 2.1/2.2 unchecked until 02-02; record checked 02-01 sub-deliverables instead."
requirements-completed: [REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14]
coverage:
  - id: D1
    description: CLI-generated UTF-8 standalone HTML with basename, full total, scoped ranked table and empty/single cases
    requirement: REQ-09
    verification:
      - kind: integration
        ref: tests/test_html_output.py#test_cli_html_saved_document
        status: pass
      - kind: integration
        ref: tests/test_html_output.py#test_html_empty_and_single
        status: pass
      - kind: integration
        ref: tests/test_html_output.py#test_html_metadata_top1
        status: pass
    human_judgment: false
  - id: D2
    description: First-seen ties after casefold, frequency precedence, top boundary and seed reproducibility across all formats
    requirement: REQ-12
    verification:
      - kind: unit
        ref: tests/test_aggregator.py#test_first_seen_after_casefold
        status: pass
      - kind: integration
        ref: tests/test_html_output.py#test_html_first_seen_cases
        status: pass
      - kind: integration
        ref: tests/test_html_output.py#test_all_format_seed_bytes
        status: pass
    human_judgment: false
  - id: D3
    description: Static escape/CR preservation and approved responsive CSS, pending actual browser acceptance
    requirement: REQ-13
    verification:
      - kind: unit
        ref: tests/test_html_output.py#test_html_safe_text
        status: pass
    human_judgment: true
    rationale: "Static parser cannot prove browser text/layout, font availability, injection nonexecution or zero external requests. 02-03 and independent quality evidence required."
duration: 5min
completed: 2026-11-17
status: complete
---

# Phase 2 Plan 01: Safe HTML and first-seen selection Summary

**CLI stdout now produces an escaped, self-contained three-column HTML report; all formats select equal-frequency words by normalized first encounter.**

## Performance
- Started: 2026-11-17T09:49:38Z
- Product verification completed: 2026-11-17T09:54:09Z
- Tasks: 2/2
- Product/test/glossary/OpenSpec files: 8; additional RED evidence files: 3.
- Execution: inline Pattern C, 2 tasks within configured threshold3; sequential execution despite linked worktree. Only 02-01 executed.

## Accomplishments
- HTML choices and pure `format_html(pairs, *, filename, total_count)` connect the existing input boundary to a separately saved UTF-8 file. Metadata precedes table; basename only, full Counter total, 1-based selected-row ranks. Empty keeps three headers and zero data rows.
- Text-node `html.escape(quote=True)` once, followed by CR numerical references; static tests retain entity-like strings, quotes, whitespace and CR/CRLF without adding input-derived elements. Inline CSS implements the approved UI-SPEC; no product JS/assets/URL added.
- Stable frequency-only sort preserves Counter first encounter, then slices top. Existing text/json byte structures remain unchanged; old tie oracles and glossary deliberately replaced. Unicode/casefold, frequency precedence, large integer and input-boundary regressions retained.

## Task Commits
1. Task1: `be4baf6` — production HTML tracer and its static tests; OpenSpec 2.1/2.2 scoped checkmarks in the same commit.
2. Task2 RED: `56cdba9` — first-seen oracles and real RED evidence.
3. Task2 GREEN: `621a640` — stable sort, glossary and OpenSpec1.1 checked together.

## Tests and Experiments
Interpreter (existing, no install): `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python` (pytest9.2.0).
- Task1 initial RED: `-m pytest tests/test_html_output.py -q`: 1 failed, exit1, `test_cli_html_saved_document` asserted success but actual CLI exit2: html invalid choice. Target executed; planned missing CLI capability, not collection/fixture error.
- Task1 initial GREEN: HTML/CLI/formatter suite: 26 passed; after empty/safety assertions: 31 passed, exit0.
- Task2 RED: `-m pytest tests/test_aggregator.py::test_first_seen_after_casefold --junitxml=.planning/argonauts/t_c5efdec5/task2-red.xml -q`: 1 failed, exit1, apple appeared before zoo. Original XML/log and JSON record retained. Official `check tdd-red-evidence ... --raw`: RED_EVIDENCE_OK. Semantic inspection confirms the target's ordered-pairs assertion failed for old lexical tie behavior.
- Task2 GREEN full suite: 72 passed, exit0.
- Final acceptance reruns at product head621a640: `-m pytest tests/test_html_output.py tests/test_cli.py tests/test_formatters.py -q`: **53 passed**; `-m pytest -q`: **72 passed**, exit0. `git diff --check`: exit0.
- Binary subprocess seed1/777 checks cover each format separately; top1 Zoo case has total5 and only 1/zoo/2. Real CLI stdout bytes are saved to a different tmp_path report and UTF-8 decoded; input bytes are compared unchanged.
- Official `check evaluation-scope --plan 02-01 --commits-only --raw`: resolved three reachable plan-subject commits.

## TDD Gate Compliance / Deviations from Plan
- Task1's initial CLI failing assertion was observed before implementation, but a separate RED commit and machine-classified saved record were not made before GREEN. Empty and direct safety tests were added after that implementation and passed immediately; they are regression coverage, not test-first proof. This is a process deviation, not claimed full TDD compliance. Task2 did record/classify RED and commit before implementation. No fabricated RED evidence or retroactive history rewriting.
- `ReportParser.handle_decl` was added to inspect actual doctype declarations in addition to the named parser methods in the inventory; no production API deviation. Inventory update before that helper was missed.
- Shared OpenSpec2.1/2.2 contain 02-02 work, so their parent checkboxes remain open. Explicit checked 02-01 subitems record the delivered parts instead of falsely claiming full completion. OpenSpec1.1 is complete.
- No architecture, dependency, CI, input acquisition, tokenizer or scope changes.

## Issues Encountered
- Active-profile language-server import diagnostics cannot resolve cached pytest; real tests executed with the existing cached interpreter pass. No toolchain installs or settings changes.
- `requirements-completed` copies the PLAN's IDs as required by the official summary schema; it does **not** certify full phase acceptance. Shared requirement IDs remain Pending until remaining PLANs and phase verification establish them.

## User Setup Required
None for this PLAN. Safe usage documentation and its execution belong to 02-02, not done here.

## Next Phase Readiness
Ready for 02-02 after same-card quality review. No next PLAN or phase.complete executed.
- Real-browser acceptance is **NOT PERFORMED**: 320/375/1280px layout, actual DOM text fidelity, image/font reading, injection nonexecution, and external requests0 remain for02-03 and independent quality. No image/network log was manufactured.
- Planning flags remain flagged-unverified: edge unclassified3, descriptor-less prohibition2, native-CDP end-to-end/font/all-target monitoring. Do not dismiss from static passes.
- Preserve sharing exposure (words/basename remain), shell same-path redirect pre-start truncation risk and separate UTF-8 output guidance in02-02.

## Official Sequential Close-out
- `state.advance-plan`: advanced=true, previous_plan1 → current_plan2, total_plans3.
- `state.update-progress`: updated=true, completed6/total8; official percentage remains50. No independent percentage substituted.
- `roadmap.update-plan-progress 2`: updated=true, summary_count1/plan_count3, In Progress, complete=false; saved ROADMAP has02-01 checked,02-02/03 unchecked.
- Saved Current Position: Phase2 EXECUTING, Current Plan2, Total Plans3, Status Ready to execute. No last_plan branch and no phase.complete.
- `requirements.ready-ids`: ready=[], blocked=REQ-09 throughREQ-14, so none marked complete.

## Self-Check: PASSED
Product artifacts exist; task and plan automated verification passed; official evaluation scope resolved commits on this branch. This self-check is scoped to02-01 automated deliverables, not browser/phase acceptance or flawless TDD process.
