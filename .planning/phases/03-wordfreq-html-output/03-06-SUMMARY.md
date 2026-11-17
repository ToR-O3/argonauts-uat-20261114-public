---
phase: 03-wordfreq-html-output
plan: "06"
subsystem: testing
tags: [pytest, encoding, git, provenance, independent-review]
requires:
  - phase: 03-05
    provides: Final-view publication and fail-closed completion marker
provides:
  - Locale-independent real byte encoding regressions with separate native-host checks
  - Isolated git/shallow scope controls and structured missing-reference diagnostics
  - Pytest execution-surface provenance and saved-manifest actor regressions
  - Same-card independent-quality and Builder factual-record re-review protocol
affects: [phase-verification, independent-quality, openspec-records]
tech-stack:
  added: []
  patterns: [real-byte subprocess seam, fixture-owned git history, fail-closed exact refs]
key-files:
  created: [tests/fixtures/encoding_cli_probe.py]
  modified: [tests/test_cli.py, tests/test_html_verifier.py, tools/verify_wordfreq_html.py, docs/wordfreq-html-verification.md, openspec/changes/r-50053edc-wordfreq-html/tasks.md]
key-decisions:
  - Native ISO-locale checks remain mandatory where available; controlled seams do not claim native execution.
  - Fixture refs never replace actual scope baseline or approved snapshot.
  - H1 is only initial Builder delivery; H2/H3 each require fresh complete independent acceptance.
requirements-completed: [REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14]
coverage:
  - id: D1
    description: Host-independent encoding test preconditions with actual byte-file lookup
    verification:
      - kind: integration
        ref: tests/test_cli.py
        status: pass
    human_judgment: false
  - id: D2
    description: Isolated scope, depth1, execution-surface and actor regression controls
    verification:
      - kind: integration
        ref: tests/test_html_verifier.py
        status: pass
    human_judgment: false
  - id: D3
    description: Independent all-image/raw/network/CI acceptance and evidence-backed OpenSpec records
    verification: []
    human_judgment: true
    rationale: Initial Builder delivery only; independent quality and final-head record/re-review cycle have not run.
completed: 2026-11-17
status: implementation-delivered-review-pending
---

# Phase 3 Plan 06: CI prerequisites repaired; independent acceptance still pending

**Locale and history prerequisites are removed from unit tests without changing product code or weakening actual scope; initial delivery leaves all four independent acceptance tasks unchecked.**

## Accomplishments and task commits

1. `ca9cfbb` — Task 1: added real-file `probe()` launcher; `encoding_probe()` records filesystem display codec, stdout codec and raw path roundtrip before invoking unchanged real main/FileSource. `native_encoding_env()` verifies actual charmap and empty stderr. Both availability paths and native mismatch rejection covered. Raw caf/E9 path, café/rows/total/Japanese headers, strict UTF8 output identity and source bytes retained. Native filesystem/stdout and C/latin-1 actually executed on this host; absence is separately exercised under test control, not claimed as native execution.
2. `abacb9b` — Task 2: `scope_repo` fixture owns all historical refs. Actual file:// depth1 clone tests check missing base, approved ref, both and clean controls via copied verifier subprocesses. Scope preserves exact production constants, resolves commit objects before diff, reports ref_diagnostics/nonzero/unverified/null uncomputed paths rather than traceback or fake clean diff. Added owned encoding helper to exact allow-list (03-05 finalization test was already present). Shared provenance pathspecs cover tests outside tests/, both default collection patterns, nested conftest and root pytest.py; dirty/staged/deleted/untracked content/hash tested. Isolated collect-only/import subprocesses demonstrate execution influence. Wrong manifest actor creates no finalize request; omitted actor is saved as actual profile by review_session. Existing actor/role/root gates remain intact.
3. `1e45476` — Task 3 initial delivery: guide/parser contract and runbook now mandate H1 fresh quality, technical evidence with task-specific head/path/hash in request_changes, Builder-only actual task record H2 and re-request_review, then complete fresh-root H2/H3 independent rerun. OpenSpec 3.1/3.2/4.1/4.2 remain unchecked. Only actual Builder implementation/test facts were appended.

## TDD execution evidence

- RED: `test_encoding_obligations_run_without_native_locale` failed at required ISO-locale assertion under deterministic locale-absent control. GREEN: CLI100 passed.
- RED: missing baseline and missing approved ref raised CalledProcessError; owned encoding helper was rejected. GREEN: all five focused scope tests passed after structured report/allow-list fix.
- RED: root pytest.py untracked content absent from product_status. GREEN: all40 configuration/collection/provenance mutations pass with shared selection.
- RED: guide contract missing controlled-seam/native/ref/head-cycle terms. GREEN after runbook update.
- Existing actor gates were regression-tested without unnecessary implementation changes; they were already correct.

## Actual verification

All commands use existing `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3`, CPython3.12.15. No installs, dependencies, configuration, workflow or product changes.

- `-m pytest tests/test_cli.py -x`: 100 passed.
- `-m pytest tests/test_html_verifier.py -x`: 200 passed.
- `-m pytest`: 358 passed, no skips/errors/failures (14.75s final task verification).
- Focused encoding `-s -q`: 6 passed,94 deselected. Output distinguishes native unavailable control, native ISO filesystem/stdout execution, and native C stdout execution.
- Extra actual local depth1 clone of committed initial-delivery code: `rev-parse --is-shallow-repository` true; full suite358 passed, no skips/errors/failures (14.57s). This is not hosted CI and still has host native locale; unconditional absent-native controls run within the suite.
- Real exact-ref `--check-scope` at 1e45476a5774f67317bfefb8596cd186d06f5ee3: exit0/passed/errors[], empty product_status. Both requested refs resolved exactly: base5a7659b949dc118b59cea5ef3eb40bcd94337d8d and approved_producted7e6cc9d608bc40a82da76e85ca6e57a0808b54. Raw report `.planning/argonauts/t_13f258db-scope.json`. This actual result is separate from fixture-scope success.
- `git diff --check`: exit0.

## Issues Encountered and deviations

- Installed execute-plan path is under active Builder profile, not $HOME/gsd-core. Attempted nonexistent gsd-init.sh was not used; loaded the installed official `_runtime-launcher.snippet.sh`, then gsd_run query init.execute-phase3 and state.get verified phase3/plan6/6 and sole incomplete03-06. No state-position repair required.
- Artifact03-05 already allowed tests/test_html_finalization.py; retained rather than duplicate it.
- Task3's independent action is intentionally a same-card quality/rework cycle, not performed or certified by Builder. Initial implementation delivery is not complete task/phase acceptance. No product architectural deviation.

## Independent review / record / final-head states

- **H1 initial repair delivery:** code/runbook delivered, Builder self-check green. Final push SHA belongs in review handoff (SUMMARY/state commits change head after code checks).
- **Independent quality H1:** pending. Must execute independent_quality_gate in03-06-PLAN in full on pushed head, including all raw/all images/live communications/final owner exit and final manifest/derived/ledger matching, actual scope, full suite and exact-head hosted CI. No synthetic or old evidence substitution.
- **OpenSpec original3.1/3.2/4.1/4.2:** unchecked. Await independent task-specific immutable evidence and no unmet condition, then Builder alone records supported facts and pushes H2.
- **H2/H3 final independent quality:** pending, requires new roots and all gates again even for document-only changes. No H1 carry-forward.
- **Hosted CI:** not yet read for the not-yet-pushed final H1 metadata commit. Local/shallow358 pass is not hosted CI success. Quality must read final-head runs/jobs/logs once; queued/unreported is not success.
- **OpenSpec final critical0 / phase acceptance:** pending, not claimed. requirements-completed frontmatter copies PLAN IDs per template only; it does not certify these acceptance obligations. No requirements completion mutation or phase.complete performed.

## Self-Check: PASSED (initial Builder implementation only)

New helper exists; three task commits are on current branch; targeted/full suites and real scope executed above. Initial delivery records all unresolved gates rather than falsely completing acceptance. Next action is same-card independent quality review, not next phase execution.

## Review rework: H1 evidence-backed OpenSpec record (H2)

This section supersedes only the pending H1 statements above; the original delivery history remains intact.

- Quality run114 independently checked H1 `fe5d67863ad7d8927b17eb33cbdfdd560a82951f`: all technical gates passed; returned request_changes solely for the four unchecked original OpenSpec records. Report is comment52 and quality's `evidence/t_13f258db/quality-report-H1.md` (SHA-256 `d2957a215593cb1c8d3607dddedb3574ca4d73d93feaf55e9e8bfd94c8baa62b`). Standard attachments71–103 contain code review and all32 viewed images. The unattachable originals archive is preserved in quality's evidence directory; it is not falsely described as attached.
- Builder read the complete independent report and originals, verified manifest/ledger/canary/scope/suite/CI hashes and all131 manifest artifact hashes (0 mismatches), checked accepted AC1–6, empty errors, independent_acceptance true and32 readable scale1 ledger reviews. No H1 technical obligation remains unsatisfied; non-blocking warnings stay with PM/phase verification rather than unrelated code changes.
- Updated only original tasks3.1/3.2/4.1/4.2 and their factual task-specific H1 path/hash basis in `openspec/changes/r-50053edc-wordfreq-html/tasks.md`. The checks certify H1 execution facts, not acceptance of this H2 record head. Product/tests/tools/config/CI/dependencies unchanged. No new behavior requires a new RED/GREEN cycle for this documentation-only rework.
- Fresh Builder rework verification: full CPython3.12 pytest358 passed, no skips (14.36s); official `openspec validate r-50053edc-wordfreq-html --type change --strict --json` valid true/issues[], exit0; `git diff --check` exit0. Strict validation is not the official final implementation verify workflow and is not claimed as OpenSpec critical0 acceptance.
- Official GSD `init.execute-phase 3` reports six plans/six summaries/incomplete0; `state.get` matches saved phase3/plan6/6/verifying. This is review rework of completed implementation: do not repeat state.advance-plan/progress mutations or call phase.complete.
- **H2 independent acceptance remains pending:** push this record and re-request_review on the same card. Quality must execute the complete independent_quality_gate again at this new head, with new roots (gap1-final-02 / gap1-network-03 onward), full image/raw/network/canary/owner/manifest/ledger/derived reconciliation, exact-ref scope/full suite, exact-head CI and official OpenSpec verify critical0. H1's accepted manifest and CI cannot be reused as H2 acceptance. Verify standard originals attachments at that review; failures or missing evidence must not receive approval. Phase verification remains separate and has not run.
