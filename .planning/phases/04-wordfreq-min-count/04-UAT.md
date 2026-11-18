---
status: testing
phase: 04-wordfreq-min-count
source: [04-01-SUMMARY.md, 04-02-SUMMARY.md, 04-03-SUMMARY.md, 04-04-SUMMARY.md, 04-VERIFICATION.md]
started: 2026-11-18T03:40:00Z
updated: 2026-11-18T03:40:00Z
---

## Current Test

number: 1
name: PM reads the delivered quality originals
expected: |
  PM opens .planning/argonauts/t_419e62f7/delivery/quality-final-01.tar.gz (and the same files under
  .planning/argonauts/r-e476c11d/quality/final-01/ at the pushed report commit), checks them against
  final-01-sha256sums.txt (618 lines), follows docs/wordfreq-min-count-verification.md §5.3, and records
  per AC1–AC7 which originals it read with matching SHA-256. Then the finalization Builder may check OpenSpec 2.2.
awaiting: user response

## Tests

### 1. PM reads the delivered quality originals (REQ-20, SC4, PLAN F3, OpenSpec 2.2 PM part)
expected: PM records that it read the originals itself (path + SHA-256 matching the index) for each of AC1–AC7. Quality-technical part already done at afaa56f (final-01 accepted, independent_acceptance true, AC1–AC7 accepted, errors []).
result: [pending]

### 2. REQ-17 / P6 concurrency and interruption scope
expected: PM/requester confirms no guarantee beyond the existing single-shot CLI is required (no stdout atomicity / parallel-run guarantee), or provides a spec for it.
result: [pending]

### 3. 04-04 independent quality gate (harvested human-check)
expected: Human confirms the independent quality gate result recorded at afaa56f (quality final-01 manifest verdict accepted, 142 image reviews by argonauts-uat-quality, source order lines 34/35/36/37/38/44) is accepted as the quality acceptance; OpenSpec 2.2 completion still depends on test 1.
result: [pending]

## Summary

total: 3
passed: 0
issues: 0
pending: 3
skipped: 0
blocked: 0

## Gaps

