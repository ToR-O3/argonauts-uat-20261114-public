---
phase: "1"
slug: "wordfreq-cli"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-17"
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
| 01-05-01 | 05 | 5 | REQ-07 | T-01-09 / T-01-10 / T-01-SC | Preserve report provenance and human workflow ownership | existing whole-suite regression, local only | `python -m pytest` | Existing six `tests/test_*.py` files from 01-01..03 | ⬜ pending |
| 01-05-02 | 05 | 5 | REQ-07 | T-01-09 / T-01-10 / T-01-11 | Handoff requires independent latest-target evidence and safe attachments | existing whole-suite regression, local only | `python -m pytest` | Same existing suite; Task 1 documents precede Task 2 handoff | ⬜ pending |

This map adds the REQ-07 gap sampling contract only. Earlier 01-01..04 PLAN verify fields and original phase evidence remain the authoritative historical task map; no claim of a full Nyquist audit is made. Local pytest does not validate these prose records or remote CI; separate read/review gates below are mandatory.

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

- [ ] Phase-wide task/automated verification mapping audited (01-05 mapping authored; not yet executed)
- [ ] Sampling continuity audited over all phase plans
- [ ] Wave 0 availability independently audited
- [ ] No watch-mode flags independently audited
- [ ] Actual local feedback latency recorded
- [ ] Remote latest-target CI and manual-only gates independently validated by quality
- [ ] Nyquist compliance decision made from actual audit, not template completion

**Approval:** Pending. `status: draft`, `nyquist_compliant: false`, and `wave_0_complete: false` deliberately remain unchanged. Updating this planning contract is not a test run, remote CI verification, or REQ-07 acceptance.
