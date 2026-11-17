---
phase: 03-wordfreq-html-output
plan: "05"
subsystem: testing
tags: [python, evidence-ledger, fail-closed, finalization, synthetic-lifecycle]
requires:
  - phase: 03-wordfreq-html-output
    provides: Existing 03-04 live owner, immutable artifacts and review ledger
provides:
  - Exact validated image review projection to all manifest and derived views
  - Fail-closed final reconciliation and best-effort all-view rollback
  - Browser-free real-owner lifecycle regression and final-reader runbook
affects: [03-06, independent-quality, phase-verification]
tech-stack:
  added: []
  patterns: [validated-ledger projection, completion-marker-last publication, explicit persistence failures]
key-files:
  created: [tests/test_html_finalization.py]
  modified: [tools/verify_wordfreq_html.py, docs/wordfreq-html-verification.md]
key-decisions:
  - Synthetic lifecycle controls exercise real publication files but do not constitute genuine viewing or independent product acceptance
  - Partial readers must reject the unverified manifest completion marker regardless of any intermediate derived verdict
  - Storage failure cannot guarantee rollback; retain explicit nonzero persistence diagnostics instead of claiming complete saved evidence
requirements-completed: [REQ-12, REQ-14]
coverage:
  - id: G1-projection
    description: Both role outcomes project exact path/hash/viewed_at into every persisted full/tile view
    verification:
      - kind: integration
        ref: tests/test_html_finalization.py#test_real_owner_projects_exact_ledger_into_every_persisted_view
        status: pass
    human_judgment: false
  - id: G1-fail-closed
    description: Invalid identities, pending projections, partial saves, late network, timeout and final provenance failures revoke success
    verification:
      - kind: integration
        ref: tests/test_html_finalization.py#test_owner_failures_revoke_every_saved_view
        status: pass
      - kind: integration
        ref: tests/test_html_finalization.py#test_invalid_ledger_or_bytes_fail_closed_in_real_owner
        status: pass
      - kind: unit
        ref: tests/test_html_finalization.py#test_final_consistency_rejects_contradictory_persisted_records
        status: pass
    human_judgment: false
  - id: G1-runbook
    description: Final all-view ledger reconciliation, completion marker and pending G2/quality boundaries
    verification:
      - kind: unit
        ref: tests/test_html_finalization.py#test_runbook_requires_final_all_view_reconciliation
        status: pass
    human_judgment: false
  - id: product-independent-gate
    description: Fresh final-head genuine image/rawRange review and CI-compatible full-suite acceptance
    verification: []
    human_judgment: true
    rationale: G2 and the mandatory independent quality cycle belong to 03-06; no synthetic attestation proves actual viewing.
duration: 565s
completed: 2026-11-17
status: complete
---

# Phase 3 Plan 05: Validated ledger and final-view reconciliation

**The real live owner now projects exact ledger review identities into all views and derived files, reconciles persisted records before publishing its completion marker, and revokes success on finalization failures.**

## Performance and scope

- Card run began 2026-11-17T17:04:18Z (run epoch converted with date); official execution/position check at17:05:30Z; source verification completed17:13:43Z (565s from card start). Two tasks, three non-planning paths; no packages installed.
- Existing wt/t_0a35d736 aligned to origin/argonauts/r-50053edc at bd1faed0c150b3260ca3e343aa66103c833f2d67. Repository origin matches fixed input; fetch succeeded, base merge reported Already up to date.
- Official init.execute-phase3 selected 03-05 then03-06 incomplete; saved STATE and official state.get agree phase3, Current Plan5, Total Plans6, Ready to execute. Existing begin-phase record was retained; no new phase or next PLAN execution.
- Product, CI/workflow, configuration, dependencies, OpenSpec tasks, historical03-01..04, Phase1 and unrelatedPhase2 are unchanged. Explicit git diff --exit-code against bd1faed verified product/workflow/config/OpenSpec/historical scope preservation.

## Accomplishments and internal symbols

- `project_final_reviews(manifest, ledger, verdict)` validates the ledger and projects exactly `path`, `sha256`, `viewed_at`, in canonical image order, without mutating ledger/raw/image bytes. Both quality accepted and Builder builder-reviewed paths run through the actual review_session owner with real disk writes in synthetic controls.
- `final_review_errors(manifest, ledger, output)` rechecks canonical capture completeness, exact ledger/image cardinality, ledger file/hash identity, image/raw byte identities, per-view verdict/mapping, complete persisted derived equality and recursively absent pending-review values. Top-level success alone is rejected.
- `publish_final_reviews` is called only by review_session after final live flush/context close and final provenance checks. It projects reviews, persists an unverified manifest checkpoint, saves each derived view with existing atomic .part replacement, then reconciles every file. review_session writes the final manifest completion marker last.
- `revoke_final_reviews` is called by review_session on all final errors, and by publish_final_reviews for its unverified checkpoint (persist=False). It clears reviewed_images, independent acceptance and all AC verdicts, and attempts every existing view/derived write, including orphan derived records from interrupted capture. Storage errors are explicit nonzero diagnostics; an unavailable filesystem cannot promise complete rollback.
- Runbook explains owner exit versus finalize-requested acknowledgment, all full/tile image path/hash/time set equality, exact view/derived agreement, valid capture pending versus invalid final pending, partial-reader marker rules and fresh-root rerun rather than repairing historical evidence.

## Task commits and actual RED/GREEN

All commands used the authorized existing CPython3.12 environment prefix:
`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3`.

1. Task1 RED `9fd2a49`: real review_session returned accepted with a pending-review view. Target `test_real_owner_projects_exact_ledger_into_every_persisted_view[quality-accepted]` executed and failed at the planned view verdict assertion, not setup/import/collection. Original JUnit + JSON are under `.planning/argonauts/t_0a35d736/task1-red.*`; official tdd-red-evidence returned RED_EVIDENCE_OK before GREEN. Task1 GREEN `aba7f11`:2 passed in0.17s, both role outcomes. Tracer gate cleared before task2 expansion.
2. Task2 RED `1200dab`: partial-publication reader assertion saw pending-review instead of an unverified completion marker. Target executed the real owner publication path; no fixture setup failure. Original task2-red XML/JSON preserved; official classifier RED_EVIDENCE_OK. GREEN `24ad633`:27 passed in1.85s, including missing/extra/duplicate/empty/wrong path/hash/time, changed bytes, timeout, late network, final head/dirty mismatch, derived pending, partial save, final marker save failure, persistent storage diagnostics and runbook assertions.
3. Integrated final-gate RED `4a5b5a0`: case reordering incorrectly produced no final errors; the newly owned regression path was rejected by the existing scope allow-list.2 assertion failures, no setup errors. Original reconcile-red XML/JSON preserved, classifier RED_EVIDENCE_OK. GREEN `7bd982e`:29 passed in1.85s; final gate reuses capture completeness and scope permits exactly the added owned test path.

Official evaluation-scope --plan03-05 --commits-only resolved all six commits on this branch (status resolved, no unreachable commit).

## Final verification results

| Command | Real result |
|---|---|
| pytest tests/test_html_finalization.py -x |29 passed,1.85s,exit0 |
| pytest tests/test_html_verifier.py -x |158 passed,4.09s,exit0 |
| pytest tests/test_cli.py -x |97 passed,3.35s,exit0 |
| pytest --junitxml=.planning/argonauts/t_0a35d736/local-suite.xml |313 passed,9.43s,zero skips/errors/failures,exit0 |
| tools/verify_wordfreq_html.py --check-scope at7bd982e |exact base5a7659b949dc118b59cea5ef3eb40bcd94337d8d;target7bd982eff89c7492418c6668ef287efa76323a51;product_status empty;untracked_product=[];errors=[];exit0 |
| tools/verify_wordfreq_html.py --check-evidence-contract |synthetic=true,product_acceptance=false;17 invalid controls rejected;errors=[];exit0 |
| git diff --check / protected-scope diff |exit0 |

Local full-suite success is **not G2 closure**: this host has full history and the native locale. Existing CI shallow/locale compatibility fixes and remote exact-head success remain03-06 obligations. No new product browser run, actual image viewing, accepted independent product evidence or CI success is claimed by this Builder run. Synthetic quality-role test data are temporary test controls only, never genuine quality records.

## Deviations from Plan

- [Rule1 — integration correction] Final reconciliation also reuses existing capture completeness for canonical case order; the exact new test file was added to the existing scope allow-list. Both were justified by actual failing assertions and stay within tools/tests scope; no generic scope relaxation or product change.
- The profile-local GSD workflow was resolved at the active builder profile path after the initially requested home-relative workflow location was absent. Official installed launcher and gsd_run were used. Terminal shell functions do not persist between calls, so each official command explicitly sources the installed launcher; no custom GSD implementation was substituted.

## Mandatory pending handoff

- G1 implementation/isolated regression only. G2 CI-compatible full suite, fresh independent final-head quality, genuine all full/tile/rawRange review, all AC evidence and exact-head CI remain pending for03-06.
- OpenSpec3.1/3.2/4.1/4.2 remain unchecked and unchanged. Required requirements-completed frontmatter copies PLAN IDs as the official template requires; it does not assert independent REQ-12/14 acceptance or authorize requirements.mark-complete.
- Child t_13f258db is the next implementation, not this card's review. This Builder run requests same-card review by argonauts-uat-quality, no quality status mark, PR ready/merge, phase.complete or automatic03-06 execution.
- Full final-head review/record/re-review loop is explicitly owned by03-06. Historical quality evidence is unchanged and must not be hand-patched or reused as fresh evidence.
- Reusable evidence-publication lessons submitted to this profile's skill approval queue, pending a8b0fc52; not reported as already saved.

## Official sequential close-out

After SUMMARY commit da8dc07, state.advance-plan returned advanced=true,previous_plan5,current_plan6,total6. state.update-progress returned updated=true,completed10,total11,percent50 (official percentage retained). roadmap.update-plan-progress3 returned updated=true,summary_count5,plan_count6,In Progress,complete=false. Official state.get and saved STATE body/frontmatter agree phase3,Current Plan6 of6,Ready to execute. Metric/session recorded, next03-06 remains unexecuted and same-card03-05 review pending. requirements.ready-ids returned ready=[] and blocked=[REQ-12,REQ-14]; no requirements.mark-complete or phase.complete was called.

Initial verify-summary advisory misclassified a prose reference to an absent home-relative workflow path as a created project file, and the phrase about negative controls in this final self-check as a failed outcome. The prose was clarified without changing evidence or product. The actual on-disk deliverables and real test results remain authoritative.

## Self-Check: PASSED

Created tests/test_html_finalization.py and modified tools/verify_wordfreq_html.py plus docs/wordfreq-html-verification.md exist. Both task criteria have positive real lifecycle counts and negative controls. All local313 tests passed. This is tooling-delivery self-check only, not product acceptance. Next PLAN is not executed.
