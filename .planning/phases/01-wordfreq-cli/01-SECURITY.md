---
phase: "1"
slug: "wordfreq-cli"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
block_on: high
register_authored_at_plan_time: true
created: "2026-11-17"
audited_target_sha: "30d9c175fd87a0d492ef6c1532271f55482c45b8"
---

# Phase 1 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Created by quality t_6545be27 via gsd-secure-phase 1 (State B, ASVS L1, block_on high). Register taken from the `<threat_model>` blocks of 01-01..01-05 PLAN; no SUMMARY has a `## Threat Flags` section. All threats classified CLOSED at L1 depth, so the auditor short-circuit applied (threats_open 0, plan-time register, ASVS 1).

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| CLI argument → filesystem | One user-chosen path opened read-only by `FileSource` | file bytes (user-provided, non-sensitive) |
| Program → stdout/stderr | Results on stdout only; errors on stderr | word counts / error text |
| PyPI → dev environment | pytest (dev extra only) installed after human legitimacy approval | third-party package |
| Human reports / Git files → acceptance records | Workflow presence and reported runs are not independent proof | CI provenance |
| Latest branch head → Actions run/job/logs → quality verdict | Evidence must bind to the reviewed target SHA | CI metadata / test logs |
| Bot documentation → privileged workflow control | Bots do not change workflows, permissions, dispatch | none (prohibited) |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-01-01 | Tampering | `pip install pytest` (dev dep) | high | mitigate | 01-01-SUMMARY L18/L55: human `default` approved PyPI pytest 9.2.0 and pytest-dev/pytest provenance before install | closed |
| T-01-02 | Denial of Service | `tokenizer.py` `\w+` regex | low | accept | single-repeat pattern, no catastrophic backtracking (AR-01) | closed |
| T-01-03 | Denial of Service | `FileSource.read_text()` whole-file read | medium | accept | design Non-Goal: no streaming; one user-chosen file (AR-02) | closed |
| T-01-04 | DoS / Repudiation | uncaught `UnicodeDecodeError` | high | mitigate | `sources.py:21-22` `except (OSError, UnicodeDecodeError)` → `InputError`; tests/test_sources.py + test_cli.py invalid-UTF-8 cases pass | closed |
| T-01-05 | Tampering | log/traceback on stdout | medium | mitigate | `__main__.py:26-27` errors via `print(..., file=sys.stderr)`; no other `print` in `wordfreq/`; json-loads CLI tests pass | closed |
| T-01-06 | Repudiation | exit code spoofed by broad except | medium | mitigate | only `except InputError` in `__main__.py`; no `BaseException`/`except Exception` in `wordfreq/`; returncode asserted in test_cli.py | closed |
| T-01-07 | Spoofing / Info Disclosure | file path handling | low | accept | single argparse path, no traversal/wildcards; OS permissions are the boundary (AR-03) | closed |
| T-01-08 | Repudiation | CI pytest job absence | high | transfer | transferred to human via 01-CI-GAP.md; human added `.github/workflows/pytest.yml` (5c9d8fa, CPython 3.12); quality independently read latest-head CI success (see `.planning/argonauts/t_6545be27/ci-evidence.md`) | closed |
| T-01-09 | Spoofing / Repudiation | CI provenance in records/handoff | high | mitigate | CI-GAP/USER-SETUP/ci-handoff label historical runs as human-reported; quality read run/job/log for exact target 30d9c17 itself | closed |
| T-01-10 | Tampering / EoP | workflow ownership boundary | high | mitigate | `git diff 5c9d8fa HEAD -- .github` empty; workflow `permissions: contents: read`; 01-05 diff is `.planning/` only; no dispatch/permission changes | closed |
| T-01-11 | Information Disclosure | evidence/log attachments | medium | mitigate | quality evidence contains run metadata and pytest excerpts only; Actions log masks token as `***`; no credentials recorded | closed |
| T-01-SC | Tampering | pip/uv installs | high | mitigate | `pyproject.toml` `dependencies = []`, pytest only in `dev` extra; no later PLAN installs anything | closed |

*Status: open · closed · open — below {block_on} threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-01 | T-01-02 | `\w+` is linear; no ReDoS surface | plan-time disposition (01-01 PLAN) | 2026-11-17 |
| AR-02 | T-01-03 | No streaming is a documented design Non-Goal; input is one explicitly chosen file | plan-time disposition (01-02 PLAN, design.md) | 2026-11-17 |
| AR-03 | T-01-07 | Single argparse path; OS permissions are the access-control boundary | plan-time disposition (01-03 PLAN) | 2026-11-17 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-17 | 12 | 12 | 0 | quality t_6545be27 (gsd-secure-phase 1, L1) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-17
