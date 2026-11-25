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

Final IDs below match the three serial PLANs (same request branch). Planning ran only official GSD document validation, not product tests/browser. All execution/sign-off remains pending. Every automated tag in PLAN has an immediately following observable fails_when.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 08-01-01 | 08-01 | 1 | REQ-30, REQ-31 | T-08-01, T-08-02, T-08-03 | exclusive fresh pre-edit originals; actual browser and canary; legacy unchanged | regression + real browser | `env WORDFREQ_DISPLAY_CAPTURE=before PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_displayed_types_verifier.py::test_capture_before_real_browser -q -s` | new file/selector/input created and read in this task before execution; existing saved_baseline integrity command also required | pending |
| 08-01-02 | 08-01 | 1 | REQ-29, REQ-30, REQ-31 | T-08-03 | actual missing-display RED, not 0 collected/environment error | unit + CLI RED | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_formatters.py::test_html_displayed_types tests/test_cli.py::test_displayed_types_cli_matrix -q` | files existing; selectors/recording helper created in this task | pending RED; expected exit1/assertion |
| 08-02-01 | 08-02 | 2 | REQ-29, REQ-30 | T-08-04, T-08-05, T-08-06 | final pairs len, total leaf, strict HTML conversion/default legacy validator | unit + CLI + verifier | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_formatters.py tests/test_cli.py -q` | existing; prior RED plus same-task adapter, max/min verifier tests also required | pending |
| 08-02-02 | 08-02 | 2 | REQ-30, REQ-31 | T-08-04, T-08-06 | README1line, mutation/control discrimination, full suite no exclusions | full regression | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/ -q` | existing; recording helper/input created same/prior task | pending |
| 08-03-01 | 08-03 | 3 | REQ-29, REQ-30, REQ-31 | T-08-07, T-08-08, T-08-09 | current count geometry/network/head/actor and actual ledger fail closed | verifier regression | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_displayed_types_verifier.py -q` | created08-01-01, current tests/seam added same task | pending |
| 08-03-02 | 08-03 | 3 | REQ-30, REQ-31 | T-08-07, T-08-08, T-08-09 | actual Builder exercise not independent acceptance; fresh root | real browser + full regression | `env WORDFREQ_DISPLAY_CAPTURE=current WORDFREQ_DISPLAY_ROLE=builder WORDFREQ_DISPLAY_OUTPUT=.planning/argonauts/r-6ae2cbf2/builder PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_displayed_types_verifier.py::test_capture_current_real_browser -q -s` | file created08-01-01, real current selector/report writer created08-03-01 | pending |

OpenSpec mapping: 1.1→08-01-02; 1.2→08-02-01/02; 2.1→08-03 executable seam/exercise/handoff plus **separate quality-owned actual acceptance**. Builder never marks2.1 complete. New before/current pytest commands are not executed during planning. Full regression command is inherited verbatim; RED wave deliberately does not claim full GREEN. New report root is refused if it exists; partial failure is retained, browser inability blocks product edits at08-01-01 and remains gap/block later, never old Phase7 exemption. All normal full-suite contract paths collect tests without skip/xfail, and do not accidentally trigger a fresh real capture.

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
