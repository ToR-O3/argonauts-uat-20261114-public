---
status: testing
phase: 01-wordfreq-cli
source: [01-VERIFICATION.md]
started: 2026-11-17T05:20:00Z
updated: 2026-11-17T05:20:00Z
---

## Current Test

number: 1
name: 01-01 prohibition — token order does not depend on PYTHONHASHSEED or dict insertion order
expected: |
  No violation. Evidence: regex findall keeps input order, sorting uses an explicit key; PYTHONHASHSEED=1 and 777 give the same README.md output (sha256 6b8c60b8…).
awaiting: user response

## Tests

### 1. 01-01 prohibition — token order does not depend on PYTHONHASHSEED or dict insertion order
expected: No violation (regex findall input order, explicit sort key; PYTHONHASHSEED 1/777 give identical output sha256 6b8c60b8…)
result: [pending]

### 2. 01-02 prohibition — input reading and output formatting never create or modify files
expected: No violation (sources only `open(..., "r")`, formatters return strings; `git status` of wordfreq/ and tests/ empty after CLI runs)
result: [pending]

### 3. 01-03 prohibition — stdout carries only results (no progress, logs, warnings, traceback); JSON stays machine-readable
expected: No violation (errors go to stderr via `print(..., file=sys.stderr)` and argparse; bad/missing file runs leave stdout empty)
result: [pending]

### 4. 01-05 prohibition — human reports, local success or old-head CI are never presented as the latest-head independent quality pass
expected: No violation (CI-GAP / USER-SETUP / ci-handoff label human-reported, local and unverified items; this verification read push run 44021335880 for head 30d9c17 itself)
result: [pending]

### 5. 01-05 Task 1 human-check — CI-GAP and USER-SETUP keep historical absence, human-completed setup, human-reported runs and quality-unverified items apart
expected: Both documents keep the original absence record, record the 3.12 choice and human workflow addition, mark the two old runs as human-reported, and leave independent quality validation pending (recorded: Builder did it, quality PLAN review t_001775e5 re-checked and passed)
result: [pending]

### 6. 01-05 Task 2 human-check — ci-handoff.md covers latest-head resolution, quality ownership, single read, gaps kept on failure, attachment availability
expected: All referenced files exist; latest-head basis, separate local/remote gates, gaps_found on missing proof, no permission change, no polling are stated (recorded: Builder did it, quality PLAN review t_001775e5 re-checked and passed)
result: [pending]

## Summary

total: 6
passed: 0
issues: 0
pending: 6
skipped: 0
blocked: 0

## Gaps
