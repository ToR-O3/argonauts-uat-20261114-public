---
phase: 03
review: 03-REVIEW.md
titles: json
findings:
  - id: WR-01
    severity: warning
    disposition: open
    title: "Scope diff hides unauthorized deletions/moves via rename detection"
  - id: WR-02
    severity: warning
    disposition: open
    title: "Provenance uses git ignore rules, not pytest discovery, so ignored-but-collected test code is invisible"
  - id: WR-03
    severity: warning
    disposition: open
    title: "Import-shadow coverage is limited to root `pytest.py`; other root modules still alter the suite"
  - id: IN-01
    severity: info
    disposition: open
    title: "`roundtrip_path_hex` duplicates `raw_path_hex` by construction"
  - id: IN-02
    severity: info
    disposition: open
    title: "`test_native_encoding_availability_and_charmap_mismatch[False]` asserts only its own mock"
  - id: IN-03
    severity: info
    disposition: open
    title: "Final ledger identity is not bound to the finalize request's hash"
open: 6
total: 6
recorded: 2026-11-17T19:58:00Z
---

# Phase 03: Code Review Disposition

| Finding | Severity | Disposition | Source |
|---------|----------|-------------|--------|
| WR-01 | warning | open | - |
| WR-02 | warning | open | - |
| WR-03 | warning | open | - |
| IN-01 | info | open | - |
| IN-02 | info | open | - |
| IN-03 | info | open | - |

Dispositions: `open` (recorded, not yet triaged), `fixed`, `skipped`, `deferred`.
Set `deferred` by hand and put the reason in the Source cell; both are preserved. A `|` in the reason is kept as prose and escaped on the next run.
Re-running the gate keeps every row it can. A row the current review no longer reports is kept and its Source cell flagged, so a finding does not leave this record silently. ONE exception: when a finding id is REUSED by a different finding, the earlier decision cannot keep a row — the id is taken — and it is dropped. A RECORDED decision (anything but `open`) is named on the console when that happens; a row still at `open` is replaced silently, because `open` records no decision to lose.

Quality note (t_c9dd351a, head 7c704f3): the code-review gate is advisory. All six findings concern verifier tooling/test robustness, not product behaviour. At this head the real diff contains no rename that would hide a forbidden path (only 5 `.planning/` internal renames), no ignored collected test files exist, and no root import-shadow module exists, so none of the findings changes this phase's verdict. Triage is left to the PM/Builder; quality does not edit tools/tests.
