---
phase: 03-wordfreq-html-output
plan: "04"
subsystem: testing
tags: [python, chromium, live-review, evidence-contract, independent-quality]
requires:
  - phase: 03-wordfreq-html-output
    provides: Reviewed03-03 collector at5cf6918 with attributed request and raw geometry checks
provides:
  - Finite live review-session, external image/raw ledger and fail-closed finalize handshake
  - Exact baseline/current-head scope, artifact hashes and independent actor/root controls
  - Executable independent quality runbook with full AC1 through AC6 evidence index
  - Mandatory pending independent-quality and all-image readability gate
affects: [phase-verification, independent-quality]
tech-stack:
  added: []
  patterns: [external attestations only, immutable artifact hashes, context-attributed live observation]
key-files:
  created: [.planning/argonauts/t_e549477c/03-04-live-index.json]
  modified: [tools/verify_wordfreq_html.py, tests/test_html_verifier.py, docs/wordfreq-html-verification.md, README.md, openspec/changes/r-50053edc-wordfreq-html/tasks.md]
key-decisions:
  - Readiness, capture and finalize-requested are not acceptance; only the live owner can flush and emit a final verdict
  - Quality requires the actual different Hermes profile and fresh quality root, not a role flag chosen by Builder
  - Every full image and tile needs a genuine external image/rawRange attestation; collector never invents viewing
requirements-completed: [REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14]
coverage:
  - id: D1
    description: Image/rawRange ledger completeness, role/root/session/head and AC discrimination
    verification:
      - kind: unit
        ref: tests/test_html_verifier.py#test_ledger_exact_image_and_ac_coverage_roundtrip
        status: pass
      - kind: integration
        ref: .planning/argonauts/t_e549477c/03-04-contract.json
        status: pass
    human_judgment: false
  - id: D2
    description: Actual live context observation and nonzero timeout without fabricated image review
    verification:
      - kind: e2e
        ref: .planning/argonauts/t_e549477c/03-04-live-index.json
        status: pass
    human_judgment: false
  - id: D3
    description: Guide/parser/schema/matrix agreement and scope protection
    verification:
      - kind: unit
        ref: tests/test_html_verifier.py#test_guide_commands_schema_cases_and_ac_match_real_parser
        status: pass
      - kind: integration
        ref: .planning/argonauts/t_e549477c/03-04-scope.json
        status: pass
    human_judgment: false
  - id: D4
    description: Independent final-target quality regeneration, genuine all-image review and accepted finalize path
    verification: []
    human_judgment: true
    rationale: Builder has not viewed the images or performed independent quality. Quality must regenerate at the pushed target head, inspect every full/tile/rawRange and complete all AC decisions while observation stays live. No accepted product evidence is supplied by Builder.
duration: 1159s
completed: 2026-11-17
status: complete
---

# Phase 3 Plan 04: Live evidence contract and independent quality handoff

**Live browser observers now stay open for an externally authored, image/hash/rawRange-bound review ledger; absent review remains unverified, and the exact quality workflow is documented and checked against the real CLI.**

## Performance and scope

- Started2026-11-17T15:17:27Z; delivery source verification ended15:36:46Z (1159s). Two specified tasks only; five source/test/docs/task-accounting paths modified, plus planning evidence.
- Existing local branch wt/t_e549477c aligned to origin/argonauts/r-50053edc at5cf6918. Fetch/origin matched the fixed repository. Base merge returned Already up to date. No local branch creation/rename/worktree move.
- Official init.execute-phase3 selected only03-04 as incomplete/runnable. Saved and official STATE position: phase3, Current Plan4, Total4, Ready to execute.03-03 already had SUMMARY and quality approval; no repeated begin-phase or position mutation.
- No product code change from the reviewed03-02 snapshot, no CI/dependency/tokenizer/source-boundary/new server/theme/timestamp/input change. HistoricalPhase1 and unrelatedPhase2 untouched.

## Task commits

1. **Task1:** cbdba3412b10e9d23e3f1259d493f90337c57301 — review ledger, live browser contexts, finalize protocol, role/root/head/scope and artifact/AC gates; OpenSpec tooling-only checks in the same commit.
2. **Task2 / integrated hardening:** 80c162a (guide RED), faafe13 (dirty/provenance RED), b876983 (context/hash RED), 0c4d8c9 (exact guide/README and checks), 3f538c9 (finish-order RED), 4092e6a4548c447969091130c9e7b34ff6ad6aca (finish timestamp after actual checks and before final flush).

Official evaluation-scope --plan03-04 --commits-only resolved all seven above on this branch. Later SUMMARY/STATE/evidence transport commits do not relabel the browser execution head.

## Accomplishments

- `--mode review-session` reruns the full suite and real canaries, regenerates all fixed inputs/actual CLI outputs, retains all22 contexts/pages/listeners and publishes a session-bound initially empty reviews.json. Maximum local review window7200s, default3600s; no repo monitoring/service added.
- External records require actual actor, image identity/path/SHA, real viewing time, readable scale/full extent, corresponding rawRange path/SHA and concrete readability notes. All full images and tiles plus six AC reviews are mandatory; Boolean viewing claims cannot substitute. Actual Profile/root controls distinguish builder and quality under the documented trusted local-user model.
- `finalize` rechecks active process incarnation, role/root/head/status/scope, suite/canaries, immutable artifacts/raw/PNG hashes, case/width/order/geometry/tile coverage and exact AC links, then requests completion. The live owner repeats checks with freshly flushed events, timestamps the completed checks, flushes again and evaluates late events before its verdict. Ending capture cannot be retroactively accepted. Builder verdict is at most builder-reviewed, never independent quality acceptance.
- Network event separation uses proved browserContextId and retains excluded events plus target grounds; global browser-network.json rejects unobserved contexts or unknown global request attribution. Initial local file requests remain recorded. Nonzero failures and unknown attempts are never equated with no communication.
- Exact quality commands, runtime prerequisites, all fixture names, JSON field types, raw/whitespace/fonts review, observed interval/finalize semantics, head recheck and AC evidence are in docs/wordfreq-html-verification.md, linked from README. Ordinary pytest remains browser-free.

## Actual execution results

Every Python command used the existing `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3` prefix from repo root; browser processes additionally used TMPDIR=.browser-tmp, an uncommitted symlink into managed scratch. Nothing was installed.

| Operation | Actual result |
|---|---|
| pytest tests/test_html_verifier.py -x, final source |135 passed in2.69s, exit0 |
| pytest --junitxml=.planning/argonauts/t_e549477c/03-04-pytest.xml |261 passed in6.15s, zero skips/errors, exit0 |
| --check-evidence-contract |synthetic=true, product_acceptance=false; clean predicate accepted and17 invalid controls rejected, errors=[], exit0 |
| --check-scope at4092e6a |base5a7659b949dc118b59cea5ef3eb40bcd94337d8d, target4092e6a4548c447969091130c9e7b34ff6ad6aca, product_status empty, untracked_product=[], errors=[], exit0 |
| actual delivery review-session, builder / timeout1 |15 realCLI cases,22 views,32 images; real clean+four violating canaries passed discrimination; ready/pending-review then expected exit1/unverified because no genuine image review was supplied |
| earlier live probe atcbdba34 / timeout120 |ready/pending-review; finalize with empty ledger explicitly rejected missing/unviewed image identities and AC coverage; later timeout exit1 |
| ended-session finalize at0c4d8c9 |exit1; ended/stale session, not active review, unviewed images and missingAC rejected |
| zipfile -t delivery archive |Done testing, exit0 |
| static unsafe execution/secret-pattern scan and git diff --check |no matching unsafe patterns; diff check exit0 |

Delivery browser evidence execution head and end head are **4092e6a4548c447969091130c9e7b34ff6ad6aca**, end product status empty. ready_at15:35:48.655866Z, observation_end15:35:49.926070Z, ended15:35:51.280618Z. Every AC remains unverified, independent_acceptance=false; reviews=[]/ac_reviews=[] are genuine absence, not filled test claims. Browser capture being correct is not an all-image readability decision.

Concise tracked outputs:03-04-live-index.json,03-04-scope.json,03-04-contract.json,03-04-pytest.xml under `.planning/argonauts/t_e549477c/`.

Original raw/CLI/PNG/network/suite/canary bundle provided as review artifact: `.planning/argonauts/t_e549477c/03-04-live-evidence.zip`, SHA-256 **4c28bd0859a440cb5e0478403a6df531796a73be2cc60b7446092cc76a1f5d69**. Original absolute paths intentionally preserve execution provenance; archive originals must not be rewritten or called fresh quality data.

## TDD observations and gate compliance

- Task1 tests were written before implementation and genuinely exposed absent ledger/scope/role/lifecycle APIs and CLI options in terminal output, then became green. **Process deviation:** initial task1 RED results were not persisted/classified with the official gate, and no test commit preceded cbdba34. Do not claim full official TDD gate compliance for task1; those early failures are terminal evidence only.
- Task2 guide test executed and failed at the intended assertion: onlycapture documented versus capture/review-session/finalize required. Its original JUnit+JSON returned official RED_EVIDENCE_OK before documentation changes;80c162a records RED.
- Follow-up assertions exposed dirty scope incorrectly accepted, rejected sessions missing end provenance, absent global-context/hash gates, and missing ordered verification-finish operation. Original JUnit+JSON files (`closeout-red`, `identities-red`, `interval-red`) are preserved. Official tdd-red-evidence returned RED_EVIDENCE_OK, followed by semantic inspection and RED commits before fixes. The closeout record's command text was corrected to its exact actual invocation without altering the original XML.
- Synthetic predicates exercise wrong actor/root/head/session, missing/duplicate/unviewed images/ACs, missing review fields/hash/raw/interval, stale byte identities, tile holes and ended/absent processes. Existing geometry regressions preserve valid own-height overhang, touching edges semantics and raw coordinates. Synthetic controls are not product evidence.

## Deviations from Plan

- [Rule1 — verifier correction] Task2 integrated inspection found dirty scope reporting and failure end-provenance gaps. Added failing tests then corrected diagnostics, context/hash checks and completion timestamp ordering. Only specified verifier/tests/docs/accounting changed; no product expansion.
- Initial task1 official TDD mechanical gate omission is disclosed above, not retrospectively fabricated.

## Issues Encountered / mandatory pending quality gate

No image-viewing capability was used by this Builder run. No image was claimed viewed. The real timeout/rejection paths were exercised rather than prefilled passing reviews. **The genuine all-image review and successful accepted/finalize path have not been exercised against product data by Builder.** Independent quality must execute that path at the final pushed target, not accept these timeout records as acceptance.

Quality must use its own run and fresh quality root, run all tests/canaries, regenerate actualCLI HTML, inspect every full image and tile at readable size plus rawRange/ancestors/whitespace/codepoints/numeric cells, supply actual reviews/AC1–AC6 records while observers stay alive, finalize, wait for session exit and read final manifest/network/end-head/scope. Missing image/environment capability remains explicitly unverified; no install/skip-to-pass. Head changes require fresh generation.

OpenSpec3.2/4.1/4.2 tooling-only subchecks accompany code; original3.1/3.2/4.1/4.2 full acceptance checkboxes remain pending. Required frontmatter requirements-completed copies PLAN IDs as the template demands, **not** a claim that independent REQ09–14 acceptance is complete. Do not mark requirements or phase accepted from this SUMMARY. REQ-09/10 unclassified2 flagged assumptions remain unchanged in the source probe; concrete AC tests and independent gate handle them without automatic resolution.

## Next Phase Readiness

Same-card quality review is required first. Child t_9de84d5f is phase-wide verification, not this implementation's review. Builder requests review and does not complete the card, mark phase.complete, ready/merge the PR or execute another PLAN. After same-card approval, the phase verifier performs the mandatory independent gate.

## Self-Check: PASSED

Specified source/test/docs deliverables exist,261 tests pass with no skips, contract/scope pass, real live observation and expected missing-review rejection/timeout are recorded with matching execution/end head. This is tooling-delivery self-check only; independent acceptance remains pending.
