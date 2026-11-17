---
phase: "1"
slug: "wordfreq-cli"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-11-17"
audited: "2026-11-17"
audited_by: "quality t_6545be27 (gsd-validate-phase 1, State A)"
audited_target_sha: "30d9c175fd87a0d492ef6c1532271f55482c45b8"
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest; earlier local evidence reports 9.2.0, current version recorded by executor |
| **Config file** | `pyproject.toml` (development dependency declaration; no new pytest config needed) |
| **Quick run command** | `python -m pytest` |
| **Full suite command** | `python -m pytest` |
| **Estimated runtime** | Earlier 43-case local runs were about 1 second; not a current measurement or guaranteed deadline |

---

## Sampling Rate

- **After each 01-05 task endpoint:** Run `python -m pytest` against that endpoint, before task completion is reported.
- **After the plan wave:** Run `python -m pytest`; the final endpoint run can also serve this wave gate if the reviewed tree has not changed.
- **Before phase re-verification:** Quality independently runs the same full suite and separately reads latest-target-head CI evidence.
- **Failure direction:** Nonzero exit, zero collected, collection/import errors, failed/error cases, or missing/skipped existing cases fail local verification. Expected unchanged baseline is 43 cases; never synthesize a result.
- **Feedback policy:** No watch mode, CI polling loops, or invented verification scripts. Remote reads are bounded as specified by 01-05-PLAN. Actual timing is recorded at execution, not asserted by this plan.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | REQ-07 | — | pytest legitimacy approval (human/doc gate) | manual (approval record) | — | 01-01-SUMMARY | ✅ green (manual, recorded) |
| 01-01-02 | 01 | 1 | REQ-07 | — | pytest available, no runtime dep | smoke | `python -m pytest --version` | yes | ✅ green (pytest 9.2.0) |
| 01-01-03 | 01 | 1 | REQ-05 | — | tokenizer unit | unit | `python -m pytest tests/test_tokenizer.py -x` | yes | ✅ green (6 passed) |
| 01-02-01 | 02 | 2 | REQ-04, REQ-05 | — | aggregator sort/ties | unit | `python -m pytest tests/test_aggregator.py -x` | yes | ✅ green (4 passed) |
| 01-02-02 | 02 | 2 | REQ-01, REQ-06 | — | FileSource read-only / InputError | unit | `python -m pytest tests/test_sources.py -x` | yes | ✅ green (5 passed) |
| 01-02-03 | 02 | 2 | REQ-03 | — | text/json formatters | unit | `python -m pytest tests/test_formatters.py -x` | yes | ✅ green (4 passed) |
| 01-03-01 | 03 | 3 | REQ-06 | — | boundary-crossing tests | integration | `python -m pytest tests/test_sources_boundary.py -x` | yes | ✅ green (3 passed) |
| 01-03-02 | 03 | 3 | REQ-01, REQ-02, REQ-03, REQ-07 | — | CLI exit codes / stdout-only results | e2e (subprocess) | `python -m pytest tests/test_cli.py -x` | yes | ✅ green (21 passed) |
| 01-03-03 | 03 | 3 | REQ-08 | — | minimal pyproject, stdlib-only | smoke | `python -m wordfreq README.md --format json` | yes | ✅ green (exit 0) |
| 01-04-01 | 04 | 4 | REQ-07 | — | CI absence inspection (historical) | whole-suite regression | `python -m pytest` | yes | ✅ green (43 passed) |
| 01-05-01 | 05 | 5 | REQ-07 | T-01-09 / T-01-10 / T-01-SC | Preserve report provenance and human workflow ownership | existing whole-suite regression, local only | `python -m pytest` | Existing six `tests/test_*.py` files from 01-01..03 | ✅ green (43 passed) |
| 01-05-02 | 05 | 5 | REQ-07 | T-01-09 / T-01-10 / T-01-11 | Handoff requires independent latest-target evidence and safe attachments | existing whole-suite regression, local only | `python -m pytest` | Same existing suite; Task 1 documents precede Task 2 handoff | ✅ green (43 passed) |

Audit 2026-11-17 (quality t_6545be27, target `30d9c175fd87a0d492ef6c1532271f55482c45b8`): every command above was run locally by quality (Python 3.14.9, pytest 9.2.0) and is green; whole suite 43 collected / 43 passed / exit 0. REQ-01..REQ-08 each map to at least one automated command. Local runs are local evidence only; the remote CI part of REQ-07 is the manual-only row below and was independently read (see `.planning/argonauts/t_6545be27/ci-evidence.md`).

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

No new Wave 0 work is assigned for 01-05: prior summaries record an approved, installed pytest environment and six existing test files. Builder checks availability and returns a blocker if unavailable; no installs or test stubs are authorized by this gap plan. Original `wave_0_complete: false` is retained pending an actual phase-wide audit, not inferred from a document update.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Source-labelled reconciliation of CI-GAP and USER-SETUP | REQ-07 | Existing tests do not assert planning prose | Builder reads human fix-1, Git workflow and document diff; retain historical absence, mark 3.12/workflow supplied by human, two old run successes human-reported only, independent CI checkbox still pending |
| Latest-target CI job success and phase verdict | REQ-07 | Remote evidence is separate from local pytest; quality-owned read/review, not a new automated test | Quality resolves latest request head, independently reads matching run/job/event/setup-Python 3.12/full pytest logs with existing Actions read authority, and records target SHA, URLs, collected/passed/failed/exit evidence; pending/auth failure/mismatch/skipped/absent logs retain gaps_found. No polling. See 01-05 independent quality protocol |
| Handoff completeness and attachment availability | REQ-07 | Local tests cannot validate evidence provenance or hook policy | Quality confirms same-branch prior PLAN artifacts plus handoff, distinguishes historic/current heads and human/independent evidence, states attachment success or exact refusal reason; never bypasses hooks |

---

## Validation Sign-Off

- [x] Phase-wide task/automated verification mapping audited (01-01..05, 12 tasks; all commands run)
- [x] Sampling continuity audited over all phase plans (every task has an automated command or a recorded manual gate; no 3 consecutive tasks without automated verify)
- [x] Wave 0 availability independently audited (pytest 9.2.0 present; six test files exist)
- [x] No watch-mode flags independently audited (commands contain no watch/poll flags)
- [x] Actual local feedback latency recorded (whole suite ~1.05s; per-file ≤1s)
- [x] Remote latest-target CI and manual-only gates independently validated by quality (push run 44021335880 / job 133831272938 at 30d9c17: CPython 3.12.16, 43 collected/passed, step success; PR run 44021344458 / job 133831300907 on merge 150576c = main 792e9c4 + 30d9c17)
- [x] Nyquist compliance decision made from actual audit, not template completion

**Approval:** approved 2026-11-17 by quality t_6545be27 — nyquist_compliant: true. Gaps found 0, resolved 0, escalated 0; no new tests generated.

## Validation Audit 2026-11-17

| Metric | Count |
|---|---|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |
