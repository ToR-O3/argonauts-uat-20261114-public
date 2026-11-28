---
phase: "08"
slug: "wordfreq-exclude"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-29"
---
# Phase 8 — Validation Strategy

## Test Infrastructure
| Property | Value |
|---|---|
| Framework | Existing pytest dev extra; runtime version not measured yet |
| Config file | pyproject.toml existing dev declaration, no new config required |
| Quick run command | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude` after feature cases authored |
| Full suite command | `uv run --extra dev python -m pytest -q` |
| Estimated runtime | Unmeasured; target quick <30s, full may exceed this |

## Sampling Rate
- Every task: write tests first, observe meaningful RED, implement, same verification GREEN; never count missing pytest/no selected tests as feature RED/GREEN.
- Every wave: accumulated exclusion cases plus affected existing boundaries.
- Before phase verification: full suite green; independent quality at target head and readable VERIFICATION.md/CLI evidence.
- Max feedback latency target: 30 seconds selective; measure at execution.

## Per-Task Verification Map
Final task IDs and unique threat references will be populated from checked PLANs; no feature execution yet.
| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| 08-01-* | 01 | 1 | REQ-28/29/30/32/33 | assign in PLAN | original validation then casefold, role-safe errors | CLI + unit | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude` | file yes / cases W0 | pending |
| later tasks | pending planner | sequential | REQ-28..33 | assign in PLAN | complete boundary/format/baseline coverage | CLI + regression | same selective command after cases created; full suite above | cases W0 | pending |

## Wave 0 Requirements
- [ ] Existing dev environment made usable; Python has no pytest currently, use existing dev extra without dependency/CI edits. Do not commit generated uv.lock.
- [ ] test_exclude_* written in existing tests/test_cli.py before production edits. New helper tests if used must be authored before command invocation.
- [ ] Actual missing/directory/decode failures plus deterministic PermissionError/generic OSError injection at read boundary; spies prove zero body reads and argument-first ordering.
- [ ] Exact baseline79d83ba binary comparison fixture from isolated historical package; same inputs/argv/interpreter/env, no candidate self-goldens, fail if baseline missing.
- [ ] Grammar matrix including all invalids/late invalid line4, valid Unicode/digits/underscore, normalization order, duplicate/order invariance.
- [ ] all text/json/html + min-count/top/ties/empty/no-op/all-excluded total, both files byte unchanged.
- [ ] help/README completeness and executable example tests.

## Manual-Only Verifications
| Behavior | Requirement | Why Manual | Instructions |
|---|---|---|---|
| scope/source ordering/pure boundaries | REQ-33 | independent source review | Quality reads complete diff, keeps no dependency/CI/HTML appearance changes |
| existing HTML appearance | REQ-33 | human-readable rendering | preserve formatter/CSS/source and baseline bytes; any browser images checked must have count/content/result documented in text; PM does not open images/archive |
| evidence provenance | REQ-32 | independent actor | exact target head, commands, exits, expected/actual, original AC/FR/EX mapping in VERIFICATION.md and text attachment |

## Validation Sign-Off
- [ ] All task IDs/threat references synchronized with final PLANs
- [ ] Every task has automated verification with observable fails_when and necessary files created first
- [ ] No three consecutive tasks without automated verification
- [ ] Wave0 covers missing feature cases
- [ ] No watch flags
- [ ] Actual feedback latency measured
- [ ] nyquist_compliant true only after evidence supports it

**Approval:** pending execution and independent quality; draft planning contract only.
