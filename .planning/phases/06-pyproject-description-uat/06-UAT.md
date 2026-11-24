---
status: testing
phase: 06-pyproject-description-uat
source: [06-VERIFICATION.md]
started: 2026-11-24T15:35:00Z
updated: 2026-11-24T15:35:00Z
---

## Current Test

number: 1
name: A-06-02 transparency prohibition (unverified-prohibition — human review recommended)
expected: |
  No artifact calls `argonauts-uat public` an observed/old description; every failed or unavailable run is reported with its real exit; Builder records are labelled as Builder and quality results come from actor argonauts-uat-quality. The prospective claims in 06-VALIDATION.md (last row) and 06-SECURITY.md (T-06-08 closed) are backed by the attachment readback recorded on card t_81c896f6. PM decides the PLAN prohibition status.
awaiting: user response

## Tests

### 1. A-06-02 transparency prohibition (unverified-prohibition — human review recommended): judge whether 「指定連結元を観測済み旧descriptionと偽ってはならず、実行不能やBuilder自己検証を独立品質合格として表示してはならない。」 holds (read inputs.json, product-target.json, builder-cli.md, quality-runbook.md, quality-cli.md, 06-VALIDATION.md, 06-SECURITY.md, 06-VERIFICATION.md)
expected: No artifact calls `argonauts-uat public` an observed/old description; every failed or unavailable run is reported with its real exit; Builder records are labelled as Builder and quality results come from actor argonauts-uat-quality. The prospective claims in 06-VALIDATION.md (last row) and 06-SECURITY.md (T-06-08 closed) are backed by the attachment readback recorded on card t_81c896f6. PM decides the PLAN prohibition status.
result: [pending]

### 2. A-06-01: classify the REQ-23 edge (category=unclassified, status=unresolved, probe 'unclassified — review manually')
expected: Human records a category/resolution, considering that the self-tests (18 OK) reject missing value, doubled suffix, different value, non-string, other-key/other-table change, malformed TOML, duplicate key, whitespace/CRLF/trailing-newline changes and every Git scope mutation.
result: [pending]

### 3. Residual process-path boundary: decide how the quality-gate originals 06-SECURITY.md, 06-UAT.md, .planning/argonauts/t_81c896f6/openspec-verify.md (committed in the quality report commit) and 06-REVIEW.md (attached only, not committed) are handled, since they are not in the hash-fixed registry c78c12ef…
expected: Either PM explicitly accepts them as known quality process paths (product conditions all PASS; the post-report repository gate fails only on these unregistered `.planning/` paths), or PM sends a gap to Builder to register them (which rebinds process_paths_sha256 in product-target.json) followed by re-verification.
result: [pending]

### 4. PM original-text read and acceptance of quality-cli.md and 06-VERIFICATION.md (attachments on card t_81c896f6, SHA-256 readback recorded there)
expected: Attachment readback hashes match; PM reads them with read_file and accepts REQ-23. Only after that may finalization run OpenSpec sync/archive.
result: [pending]

## Summary

total: 4
passed: 0
issues: 0
pending: 4
skipped: 0
blocked: 0

## Gaps
