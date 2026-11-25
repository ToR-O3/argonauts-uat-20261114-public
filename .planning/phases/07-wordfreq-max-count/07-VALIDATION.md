---
phase: "07"
slug: "wordfreq-max-count"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-25"
---

# Phase 7 — Validation Strategy

## Test Infrastructure

| Property | Value |
|---|---|
| Framework | existing pytest 9.0.3 / CPython3.12.15 (research version probe only) |
| Config file | pyproject.toml; no dependency/CI update |
| Quick run command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -q -x` |
| Full suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/ -q` |
| Estimated runtime | not measured; measure at first Builder run, focused feedback target <60s; full browser checks are separate finite phase gates |

## Sampling Rate
- After each task commit run focused tests relevant to that task, then full suite after each PLAN/wave.
- Before phase verify/UAT: full suite must be green.
- Every task has automated assertions; no three-task manual-only gap. Browser/visual verification supplements, never replaces pytest.
- Commands run from repo root; no outer cd/grep, watch, polling, or fabricated result.

## Per-Task Verification Map

Initial mapping; planner must refine exact task IDs and paths in this same strategy when PLANs are saved.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| 07-baseline | TBD | first | REQ-26,REQ-27 | T-07-01 | immutable pre-change bytes/argv/exit/stderr | regression | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -q -x` | file yes / new baseline assertions W0 | pending |
| 07-option-selection | TBD | after baseline | REQ-23,REQ-24,REQ-25,REQ-26 | T-07-02 | parser-before-I/O, no Counter mutation, safe HTML | CLI+spy | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -q -x` | file yes / max assertions W0 | pending |
| 07-readme-regression | TBD | after feature | REQ-27,REQ-28 | T-07-03 | exact example and no unrelated changes | CLI+full | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/ -q` | files yes / example assertion W0 | pending |

## Wave 0 Requirements
- [ ] Before production edits, inspect existing saved output and freeze any missing omission oracle/input/argv/cwd/env/exit/stderr. Never regenerate expected values from new implementation.
- [ ] Add max-count regression/spy/README tests to actual test files before commands are used for those behaviors. Confirm targeted assertion RED, not environment error or zero collection; then minimal implementation GREEN.
- [ ] If new baseline fixture or verifier/test driver is needed, PLAN explicitly creates it in same/earlier task, with nonzero failure assertions and standard Python/pytest execution. No no-op or synthetic evidence.
- [ ] Existing CPython3.12 pytest environment suffices; do not add dependencies/CI. PATH Python3.14 has no pytest; use recorded explicit environment.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|---|---|---|---|
| Actual HTML readability and image inspection | REQ-26,REQ-27 | DOM/pytest cannot substitute actual visual review | Quality independently generates HTML from target head; 1280x900 and 320x900 CSS px DPR1; compare same-condition pre-change states; inspect all images/tiles, raw Range, clipping, overlap, whitespace and injection candidates; track all document-caused request/failed-request/navigation/popup attempts. |
| Ownership/head and delivery | REQ-27 | evidence attribution not inferred from file presence | Quality records fresh head, source, actor, argv/input/exit/stdout/stderr, HTML/raw/image/network files; attaches VERIFICATION.md plus CLI/CI text proof and states viewed image count/content/result per AC. PM reads text only; no archive/image requirement. OpenSpec2.2 execution belongs to phase verification. |

## Validation Sign-Off
- [ ] All final task IDs/commands mapped after planner
- [ ] No missing command inputs at task completion
- [ ] Sampling continuity and no watch flags
- [ ] RED/GREEN and all existing suite results measured, not inferred
- [ ] Quality independent CLI/browser/image/network evidence and text attachment complete
- [ ] nyquist_compliant true only after official validate-phase verifies actual implementation

**Approval:** planning seed only; implementation and validation pending.
