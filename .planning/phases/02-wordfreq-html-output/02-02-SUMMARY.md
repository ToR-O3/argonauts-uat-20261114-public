---
phase: 02-wordfreq-html-output
plan: "02"
subsystem: testing
tags: [python, cli, html, regression, fidelity, safe-saving]
requires:
  - phase: 02-wordfreq-html-output/02-01
    provides: HTML formatter, CLI UTF-8 byte output and shared first-seen selection
provides:
  - All-format CLI/error/seed/concurrency and input-boundary regression coverage
  - Direct formatter exact-text, pure-selection and semantic document coverage
  - Executed safe UTF-8 distinct-output README example and compatibility guidance
affects: [02-03, phase-verification]
tech-stack:
  added: []
  patterns: [independent output oracles, completed-file parallel comparison, environment-aware permission failure]
key-files:
  created: []
  modified: [tests/test_cli.py, tests/test_sources_boundary.py, tests/test_html_output.py, README.md, CONCEPTS.md, openspec/changes/r-5c041156-wordfreq-html/tasks.md]
key-decisions:
  - "Keep shared OpenSpec 3.2 open until browser and independent quality evidence; check the completed 02-02 portion only."
  - "Static parser fidelity is not real-browser acceptance; retain all flagged-unverified signals."
requirements-completed: [REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14]
coverage:
  - id: D1
    description: All-format success/error, first-seen/seed, once-only composition, input/worktree immutability and distinct-output concurrency
    requirement: REQ-14
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_all_format_contract_matrix
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_all_format_error_matrix
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_all_format_first_seen_and_seed
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_cli_leaves_input_and_git_worktree_unchanged
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_cli_parallel_distinct_outputs
        status: pass
      - kind: unit
        ref: tests/test_sources_boundary.py#test_cli_composition_once_per_format
        status: pass
      - kind: unit
        ref: tests/test_sources_boundary.py#test_cli_read_permission_fault
        status: pass
    human_judgment: false
  - id: D2
    description: Static direct formatter exact text, explicit metadata, supplied row order, nonmutation and three-column document
    requirement: REQ-13
    verification:
      - kind: unit
        ref: tests/test_html_output.py#test_html_exact_text_matrix
        status: pass
      - kind: unit
        ref: tests/test_html_output.py#test_html_pure_selected_pairs
        status: pass
      - kind: unit
        ref: tests/test_html_output.py#test_html_document_contract
        status: pass
    human_judgment: false
  - id: D3
    description: Executed distinct-file UTF-8 save example, input bytes preserved and exposure/truncation/compatibility guidance
    requirement: REQ-14
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_readme_html_save_example
        status: pass
    human_judgment: true
    rationale: "Execution is automated; adequacy of sharing/truncation guidance and descriptor-less prohibitions requires independent review. Not a browser acceptance claim."
duration: 8min
completed: 2026-11-17
status: complete
---

# Phase 2 Plan 02: All-format regression and safe saving Summary

**All three output formats now have success/error/input-boundary regressions; direct HTML strings round-trip statically, and README's separate UTF-8 save command executes without changing the input. No production behavior was changed in this PLAN.**

## Performance
- Started: 2026-11-17T10:19:58Z; task verification completed: 2026-11-17T10:27:21Z.
- Tasks: 3/3, inline Pattern C (3 tasks within configured threshold3).
- Six test/doc/OpenSpec files modified; one PLAN inventory annotation. Sequential execution on the card worktree, not parallel; only02-02 executed.
- Start head: 565f42b0e4352a3e2d5c06e2cf4e604330bb02bf. Verified task head: 20341ad756ea0355c38fc4b75880da9e3f4cdf40. Later SUMMARY/state commits are reporting metadata.

## Accomplishments
- Full text/json/html success matrix: normal/empty/symbols/Unicode/casefold, default10 (12 distinct-word fixture proves truncation), top1/top3/overlarge. Error matrix checks exit2 for top0/negative/noninteger/xml/zero or multiple filenames and exit1 for missing/directory/invalid UTF-8; errors have empty stdout and nonempty stderr without traceback.
- CLI symbols actually referenced by main are wrapped with spies: read/tokenize/count/select/selected formatter once, other formatters never, top1 still receives full total5 and basename. Permission test probes a real chmod0 file; if permissions are ineffective, injects PermissionError at FileSource.open and asserts that call and main's exit1. No skip branch.
- Cold copy retains cache exclusion, .gitignore copying, git init/add-A baseline, removal of inherited PYTHONDONTWRITEBYTECODE and full untracked status comparison for every format. HTML is saved outside isolated input/repo. Two concurrent subprocesses use distinct output files; completed bytes equal serial output and input bytes/directory remain unchanged. No partial-write atomicity or same-output contention guarantee added.
- Direct formatter tests cover both quotes, ampersands/brackets, literal entities, closing tags/script/event/URL-looking strings, leading/trailing/repeated spaces, tabs, LF, CR and CRLF. Original strings are independent oracles; CR input-stream normalization is simulated before parsing only, never applied to decoded values. Payloads cannot alter the baseline tag/attribute inventory. Non-frequency order, duplicate words, large counts, explicit total123 and name are retained without reading or mutation. Empty/normal/tie/top1 document structure and rank sequence checked.
- README/CONCEPTS explain unchanged text/json structures, first-seen breaking change and top impact, pure formatter arguments, separate UTF-8 output, same-path pre-start truncation, sharing exposure/not anonymity, completed-file-only viewing and unsupported features. README example is executed through a fixed subprocess shell argument array with harmless data; output total6 and four ranked rows, input bytes unchanged.

## Task Commits
1. Task1: 5b90668 — CLI/error/seed/concurrent/cold/once-only/permission regression, helper inventory and scoped OpenSpec check.
2. Task2: 32c9d7b — static direct formatter fidelity/purity/document coverage and scoped OpenSpec check.
3. Task3: 8dc6f67 — failing README-example contract; 20341ad — safe usage/compatibility explanation plus OpenSpec2.1/2.2 completion and3.2 scoped check.

## Tests and Experiments
Existing interpreter (no install): `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python`.
- Task1 command `-m pytest tests/test_cli.py tests/test_sources_boundary.py tests/test_aggregator.py tests/test_sources.py tests/test_tokenizer.py -q`: 156 passed, exit0; tracer feedback re-execution after commit:156 passed in6.38s, exit0.
- Task2 command `-m pytest tests/test_html_output.py tests/test_formatters.py -q`:53 passed in1.37s, exit0.
- Task3 test-first: `-m pytest tests/test_cli.py::test_readme_html_save_example -q` before README changes:1 failed, exit1, intended missing fenced command assertion (not collection failure). After docs:1 passed in0.15s, exit0, including actual separate-file shell redirection.
- Full suite after Task3:210 passed in7.91s, exit0; fresh precommit rerun:210 passed in6.94s, exit0. No skips.
- Final task-head acceptance reruns: Task1 command157 passed in6.33s (now includes README test), Task2 command53 passed in1.36s, both exit0.
- `git diff --check`:exit0 on current changes; no workflow/dependency diff from start head. This PLAN changes only tests/docs/checklist/inventory. Preserved raw RED evidence from02-01 may still cause whole-request whitespace warnings; no whole-request clean claim.
- Official `check evaluation-scope --plan 02-02 --commits-only --raw`:status resolved, four reachable task commits above, no unreachable/outsideUnion entries.

## Requirement / scenario evidence
- REQ-09/10: output oracle checks single HTML document, metadata and empty/table rows; unchanged exact text shape and JSON word/count-only array. Existing02-01 top1 Zoo total5 and basename tests retained.
- REQ-11: static document/rank/three-header contracts only here; allcase×320/375/1280 real images/layout are NOT PERFORMED.
- REQ-12: first-seen, casefold collisions, priority and top1/top3 oracles plus byte equality for seeds1/777 in every format.
- REQ-13: direct static exact text/CR/entity/attribute checks; actual browser fidelity, nonexecution and network0 are NOT PERFORMED.
- REQ-14:210 full regressions, cold bytes/status, once-only composition, actual permission failure path, parallel distinct destinations and README execution. Independent browser evidence remains outstanding.
- `requirements-completed` copies PLAN IDs per official schema; it is not a full phase acceptance verdict. Shared requirements are not marked Complete before02-03 and independent verification.

## Deviations from Plan / TDD scope
- No production changes were needed: Task1/2 new tests protect existing02-01 behavior and passed immediately. These are regression expansion, NOT claimed new-feature RED→GREEN proof. No artificial failing oracle or fabricated RED was introduced. Task3 observed the intended documentation-contract failure before writing docs, committed it, then observed executable GREEN. PLAN type is execute, not tdd, and CLI tdd_mode=false.
- Added the named `assert_format_output` independent-oracle helper and recorded it in PLAN inventory before its creation. No new production helper/API.
- Shared OpenSpec3.2 includes real-browser acceptance: parent remains unchecked, completed02-02 portion checked in the docs commit.2.1/2.2 and their02-02 parts checked only after tests and docs executed;1.1 was already complete.

## Issues Encountered
- A nonexistent gsd-shell.sh launcher path failed before any state operation; resolved using the installed official gsd-tools.cjs launcher and gsd_run function. Identity verified as @opengsd/gsd-core1.21.0; init.execute-phase selected02-02 first and state Current Plan2/3 matched. No install or alternate implementation.
- Language-server pytest import warning reflects its environment; real cached-interpreter execution above is the test evidence.

## User Setup Required
None for this PLAN. Existing cached pytest used; no CI, dependency or configuration edits.

## Next Phase Readiness / flagged-unverified handoff
After same-card quality review, ready for02-03. No next PLAN execution, browser harness/evidence generation or phase.complete here.
- **A-E10, A-E13, A-E14**: official edge unclassified3 remain unresolved/flagged-unverified. Known behavior tests do not dismiss official classification signals.
- **P-02-01, P-02-02**: descriptor-less prohibitions2 remain unresolved/flagged-unverified (do not call shared HTML anonymous; do not call partial stdout or absent browser evidence complete/accepted). README guards these risks; independent human/quality review still required. No invented descriptors or automatic green.
-02-03 and quality must run all cases×320/375/1280, inspect actual images independently, exact DOM original strings, no injected execution, all-target monitoring with positive main-file evidence, zero external/unexpected-local requests, version/head attribution. Native-CDP end-to-end/font adequacy remain unverified. Static parser passes do not discharge these gates.

## Self-Check: PASSED
Scoped to this PLAN's runnable automated regressions, documentation example and committed artifacts. Not browser/phase acceptance and not a claim of test-first production changes.
