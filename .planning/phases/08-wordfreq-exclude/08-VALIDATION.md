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
- Before Builder PLAN completion: full suite green plus fail-closed real-package handoff checks; no independent-quality result is a Builder prerequisite.
- After Builder PLAN completion: separate independent quality phase-verification card re-executes at exact target head, creates readable08-VERIFICATION.md/CLI/quality originals, runs official GSD/OpenSpec verify and standard-delivers them. OpenSpec3.2 is quality-owned and stays pending until then; Builder never checks it.
- Max feedback latency target: 30 seconds selective; measure at execution.

## Per-Task Verification Map
Final task map synchronized with 08-01/02/03-PLAN.md (two tasks each; sequential waves on argonauts/r-e0a2598f). No feature execution yet. Every named new group/fixture is authored in its own task before invocation; commands below are execution assignments, not planning results. Each PLAN contains every automated command's observable fails_when, including nonzero/zero-selected rejection.
| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| 08-01-01 | 01 | 1 | REQ-28..33 | T-08-01/02/SC | real read-only exclusion tracer, role-safe missing-file handling and docs | real CLI + docs | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_tracer`; `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_help_readme_tracer` | file yes / cases authored here | pending |
| 08-01-02 | 01 | 1 | REQ-28..33 | T-08-01 | original whole-line Unicode validation then casefold, original row diagnostics | pure + CLI | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_grammar or exclude_tracer or exclude_help_readme_tracer'` | file yes / grammar fixtures authored here | pending |
| 08-02-01 | 02 | 2 | REQ-28..33 | T-08-03/05/SC | all exclusion failures exit2, argv first, late-invalid line4/body-unread, body exit1 | source + role trace + CLI | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_failures or exclude_precedence'`; `uv run --extra dev python -m pytest tests/test_sources.py tests/test_sources_boundary.py -q -x` | files yes / new failure fixtures authored here | pending |
| 08-02-02 | 02 | 2 | REQ-28..33 | T-08-02/04/05 | full Counter/pairs nonmutation, original total, static/basename safety and fourteen UI states | CLI + pure regression | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_selection or exclude_empty or exclude_ui'`; `uv run --extra dev python -m pytest tests/test_tokenizer.py tests/test_aggregator.py tests/test_formatters.py -q -x`; `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude` | files yes / new groups authored here | pending |
| 08-03-01 | 03 | 3 | REQ-28..33 | T-08-06/07/SC | exact historical Git binary comparison, both inputs immutable, complete executable docs/Builder originals | baseline + docs + full regression | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_baseline or exclude_immutability or exclude_docs'`; `uv run --extra dev python -m pytest -q` | test file yes / live isolated historical fixture authored here | pending |
| 08-03-02 | 03 | 3 | REQ-28..33 | T-08-04/07 | Builder actual-head/original/obligation handoff, no independent verdict or3.2 checkoff | Builder CLI/full regression + stdlib positive/negative handoff controls + actual-package check | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude`; `uv run --extra dev python -m pytest -q`; `python3 -m unittest discover -s .planning/argonauts/r-e0a2598f -p test_quality_handoff.py -v`; `python3 .planning/argonauts/r-e0a2598f/check_quality_handoff.py --repo-root . --handoff .planning/argonauts/r-e0a2598f/quality-handoff.json` | preceding feature tests; quality-handoff.md/json and check_quality_handoff.py/test_quality_handoff.py authored in this task before invocation; no future quality file required | pending Builder handoff |

Fallback no-silent-drop: 26 raw applicable/unclassified0 edges = 21 explicit truth strings + 5 flat backstop truths across PLANs; raw classification is not product acceptance. Two kept prohibitions are official-projectProhibitions-projected descriptor-less unresolved objects, flagged-unverified; never auto-dismiss/auto-green. Fourteen UI states are individually lifted in 08-02 must_haves.08-03-02 validates the full identity inventories and pending obligations; actual independent dispositions for all26 edges/14 UI/2 prohibitions belong to the later quality card, not Builder task completion. Unconfirmed backstop yields human_needed/insufficient_spec, not a newly invented interruption/parallel guarantee. Nyquist and Wave0 completion flags remain false until execution evidence supports changing them.

### Handoff failure observability and later-quality boundary
08-03-02 retains both original pytest commands; they cannot detect missing handoff materials alone. Its added stdlib unittest command must fail if malformed/missing/stale-head/incomplete real materials are accepted (including scratch copies of the actual package), and its actual-package checker command fails on absent/empty/unreadable originals, wrong digests/target content, missing commands/results/AC links, missing/duplicate inventory identities, missing procedure/delivery obligations or premature3.2/quality completion. Every command has an adjacent fails_when in PLAN03; no new command target is assumed to exist before task02 authors it. Checker success means Builder handoff readiness only.

The later independent quality phase-verification card is outside this Builder task map. It must independently rerun the two retained pytest commands and real six-AC CLI cases at freshly checked exact head, perform official GSD and OpenSpec verification and complete source/scope/immutability review. It owns08-VERIFICATION.md, quality-evidence.md, readable command/input/argv/environment/exit/stdout/stderr/expected-vs-actual originals, all coverage/flag dispositions, honest image count/content/result (zero if none), and standard parent text delivery for PM read_file review. Full obligations are enumerated in PLAN03's mandatory later quality section and copied into the checked handoff, not omitted or Builder self-certified. Missing independent actor/results blocks that quality card/phase acceptance, not completion of the Builder handoff task.

## Wave 0 Requirements
- [ ] Existing dev environment made usable; Python has no pytest currently, use existing dev extra without dependency/CI edits. Do not commit generated uv.lock.
- [ ] test_exclude_* written in existing tests/test_cli.py before production edits. New helper tests if used must be authored before command invocation.
- [ ] Actual missing/directory/decode failures plus deterministic PermissionError/generic OSError injection at read boundary; spies prove zero body reads and argument-first ordering.
- [ ] Exact baseline79d83ba binary comparison fixture from isolated historical package; same inputs/argv/interpreter/env, no candidate self-goldens, fail if baseline missing.
- [ ] Grammar matrix including all invalids/late invalid line4, valid Unicode/digits/underscore, normalization order, duplicate/order invariance.
- [ ] all text/json/html + min-count/top/ties/empty/no-op/all-excluded total, both files byte unchanged.
- [ ] help/README completeness and executable example tests.
- [ ] In08-03-02 author process-only stdlib handoff tests before checker implementation; create real handoff.md/json, then exercise unittest controls and actual-package checker. No product/dependency/CI change for these process checks; no quality report/checkoff prerequisite.

## Manual-Only Verifications
| Behavior | Requirement | Why Manual | Instructions |
|---|---|---|---|
| scope/source ordering/pure boundaries | REQ-33 | independent source review | Quality reads complete diff, keeps no dependency/CI/HTML appearance changes |
| existing HTML appearance | REQ-33 | human-readable rendering | preserve formatter/CSS/source and baseline bytes; any browser images checked must have count/content/result documented in text; PM does not open images/archive |
| Builder handoff readiness | REQ-32 | automated materials check plus readable provenance review, not independent acceptance |08-03-02 real-package checker validates exact initial head/bytes/originals and all mandatory pending quality obligations; no future report needed |
| evidence provenance | REQ-32 | later independent quality actor | after Builder completion, quality independently records exact head, commands/exits/expected/actual and original AC/FR/EX mapping in08-VERIFICATION.md and standard text attachment; runs official GSD/OpenSpec verify; Builder never checks3.2 |

## Validation Sign-Off
- [ ] All task IDs/threat references synchronized with final PLANs
- [ ] Every task has automated verification with observable fails_when and necessary files created first
- [ ] No three consecutive tasks without automated verification
- [ ] Wave0 covers missing feature cases
- [ ] No watch flags
- [ ] Actual feedback latency measured
- [ ] nyquist_compliant true only after evidence supports it

**Approval:** pending execution and independent quality; draft planning contract only.
