---
phase: "08"
slug: "wordfreq-html-displayed-types"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-26"
---

# Phase 08 — Validation Strategy

> Planning seed using official VALIDATION template; execution results/sign-off remain pending.

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | Existing pytest 9.0.3, CPython3.12.15 |
| Config file | pyproject.toml (no pytest configuration section) |
| Quick run command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_formatters.py -q` |
| Full suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest -q` |
| Estimated runtime | Unmeasured; Builder records actual runtime, no invented estimate |

## Sampling Rate

- After every task commit: quick formatter suite and affected focused pytest files.
- After every plan wave: full suite with no added exclusions/skip/xfail.
- Before phase verification: independent quality full suite green, fresh CLI and browser evidence.
- Max feedback latency: target 60 seconds for focused feedback, measure rather than assert. Full browser evidence is explicit longer gate, not substituted for quick feedback.

## Per-Task Verification Map

Planner must expand these rows to its final task IDs and unique threat refs before completion.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 08-preparation | preparation | 1 | REQ-30, REQ-31 | pending planner | sealed baseline unchanged, fresh comparison data | regression | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_max_count_verifier.py -q` | existing, current adapter W0 | pending |
| 08-display | display | next | REQ-29, REQ-30 | pending planner | count from final pairs; escapes/API preserved | unit + CLI | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_formatters.py tests/test_cli.py -q` | existing, N tests W0 | pending |
| 08-integration | evidence | final | REQ-30, REQ-31 | pending planner | strict byte/security checks, independent evidence | full regression | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest -q` | existing | pending |

## Wave 0 Requirements

- [ ] Add N/placement/literal pairs cases to existing tests/test_formatters.py and tests/test_cli.py first; capture new-feature assertion RED before production edits.
- [ ] Preserve sealed baseline; narrowly adapt current HTML expectations and current-CLI fixtures without relaxing text/json, security or legacy snapshot integrity gates.
- [ ] Create current browser/capture verification file before invoking its command; include negative tests and quality runbook. Reuse existing low-level browser collector, not old scope policy.
- [ ] Capture current pre-change CLI and both-width images in separate request root before formatter edits; record original head/checksums and actual image review ability. Do not overwrite old evidence.
- No framework, runtime dependency, CI or service installation required.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Adjacent count/readability and allowed visual delta | REQ-30 | Real rendering + image inspection cannot be replaced by DOM order | Quality independently generates CLI HTML, views 1280×900 and 320×900 DPR1, inspects every full/tile/comparison image and raw geometry; total left/N right above table, no clipping/overlap/overflow, long basename/words readable |
| No external attempts | REQ-30 | Browser observation distinct from static parser | Observe from before navigation through final flush including failed request/navigation/popup; record detector discrimination separately |
| Independent acceptance and PM-readable delivery | REQ-31 | Actor and actual inspection matter | Fresh quality head/profile/task/run, full suite and CLI evidence; VERIFICATION.md and CLI/CI text attachments with AC results/image count/content; pending CI is not success, PM never needs images/archive |

## Validation Sign-Off

- [ ] All final tasks have automated verify or earlier Wave0 dependency
- [ ] No three consecutive tasks without automated verify
- [ ] Wave0 covers every missing command/input
- [ ] No watch flags
- [ ] Focused feedback latency measured
- [ ] nyquist_compliant set only after actual validation

**Approval:** pending execution/official validation, not a product pass.
