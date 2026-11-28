---
phase: "08"
slug: "wordfreq-exclude"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_total: 8
threats_closed: 8
threats_open: 0
asvs_level: 1
block_on: high
register_authored_at_plan_time: true
audited_head: "f3747b7e6235775b3c21fa13201d7921be77306c"
created: "2026-11-29"
---

# Phase 08 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Source: `<threat_model>` blocks of 08-01/08-02/08-03-PLAN.md. SUMMARY files contain no `## Threat Flags` section (no unregistered flags).
> Path: the threat register was written at plan time, threats_open is 0, and ASVS is 1, so the workflow skipped the auditor (Step 3) and went straight to Step 6.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| argv→CLI | Untrusted paths/options; existing syntax/numeric validation before any acquisition | CLI args (untrusted) |
| exclusion bytes→pure interpretation→membership | Strict UTF-8 and original full-line validation, no permissive token extraction | Exclusion file text (untrusted) |
| membership/full counts→formatter | Selected pairs only; original total and safe basename retained | Word counts, basename |
| exclusion source failure→CLI | Preserve cause/path and role; stop before body acquisition | Error diagnostics (stderr) |
| body counts→shared pairs→HTML | Pure rendering, original total and escaped basename only | HTML output |
| historical Git bytes→test subprocess | Exact approved revision, isolated import root, same interpreter/inputs/argv/env | Test fixtures |
| Builder observations→independent acceptance | Independent actor re-executes exact head; no copied verdict | Evidence package |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation / Evidence | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-08-01 | Tampering | exclusions.py | high | mitigate | `wordfreq/exclusions.py:17-22`: strip, then `re.fullmatch(r"\w+", word)` before `casefold()`; invalid row → `InvalidExclusion(line_number)` (fail closed, original line numbering). `wordfreq/__main__.py:40-42` exit 2. Strict UTF-8: `wordfreq/sources.py:19-22`. Tests: `test_exclude_grammar_original_before_casefold`, `test_exclude_grammar_invalid_original_row`, `test_exclude_immutability_both_inputs[invalid-utf8]` | closed |
| T-08-02 | Tampering | __main__.py selection | medium | mitigate | `wordfreq/__main__.py:48-52`: full `counts`/`total` kept; separate `selected_counts` Counter filters out exclusions and applies min-count; `top_words(selected_counts)`. Test: `test_exclude_selection_preserves_full_counter_and_shared_pairs` (spies on count/top/formatter), `test_exclude_selection_matrix` | closed |
| T-08-03 | Repudiation | CLI error scopes | high | mitigate | `wordfreq/__main__.py:33-47`: exclusion read/parse happens before the body read; exclusion failures exit 2 with path and reason/line (`:38`, `:41`); body failures exit 1; nothing goes to stdout on failure. Error cause chained at `wordfreq/sources.py:22`. Tests: `test_exclude_failures_role_mapping`, `test_exclude_precedence_failed_exclusion_never_reads_body`, `test_exclude_precedence_argv_before_both_reads`, `test_exclude_precedence_success_order` | closed |
| T-08-04 | Information disclosure | HTML output | high | mitigate | `wordfreq/__main__.py:55-58`: only `os.path.basename(args.filename)` and the original total reach `format_html`; no exclusion metadata is passed. Escaping: `wordfreq/formatters.py:19` (`escape(..., quote=True)`), `:111`. Test: `test_exclude_ui_static_presentation` (asserts that the private parent path, exclusion path/name and excluded word are absent from the raw HTML, plus static-document checks) | closed |
| T-08-05 | Tampering | input files/full Counter | medium | mitigate | Read-only `open(..., "r")` at `wordfreq/sources.py:19`. Tests: `test_exclude_immutability_both_inputs` (both-role byte preservation for success/invalid/utf8), byte snapshots in `test_exclude_failures_role_mapping`, Counter spies in `test_exclude_selection_preserves_full_counter_and_shared_pairs` | closed |
| T-08-06 | Tampering | historical-byte fixture | high | mitigate | `tests/test_cli.py:1349` pinned `EXCLUDE_BASELINE`; `_exclude_baseline_roots` (`:1407-1447`) re-hashes every bundled object and asserts the oid (`:1426`), checks the commit (`:1427`), uses isolated historical/candidate roots, pops PYTHONPATH and sets PYTHONNOUSERSITE. Corrupted fixtures fail instead of being skipped: `test_exclude_baseline_corruption_is_not_skipped` (missing-file/missing-blob/changed-blob/rehashed-blob). Byte comparison: `test_exclude_baseline_exact_git_bytes`; shallow/offline: `test_exclude_baseline_available_in_offline_shallow_checkout` | closed |
| T-08-07 | Repudiation | evidence/quality | high | mitigate | Fail-closed handoff checker `.planning/argonauts/r-e0a2598f/check_quality_handoff.py` + `quality-handoff.json`; run at HEAD f3747b7, it exits 0 with `HANDOFF_READY_ONLY` and `quality_status: pending`, `openspec_3_2: pending` (no Builder verdict claimed as acceptance). Real negative controls are recorded in `real-package-controls.json` (missing original / stale target / missing obligation → exit 2). Independent re-execution of the exact head is a later quality card by design. | closed |
| T-08-SC | Tampering | package setup / test env | high | mitigate | `git diff --name-only 415b1bc~1..HEAD -- pyproject.toml uv.lock setup.cfg setup.py requirements*.txt .github` → 0 files. Only the existing `dev` extra (pytest) is used. `uv.lock` / `wordfreq.egg-info/` are untracked local artifacts of `uv run` and are not committed. | closed |

*Status: open · closed · open — below {block_on} threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

No accepted risks.

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-29 | 8 | 8 | 0 | gsd-secure-phase (argonauts-uat-quality, L1 grep-depth; auditor step skipped by short-circuit rule) |

Verification commands (HEAD f3747b7):
- `uv run --extra dev python -m pytest tests/test_cli.py -q -k exclude` → 457 passed, 358 deselected (21.85s)
- `python3 .planning/argonauts/r-e0a2598f/check_quality_handoff.py --repo-root . --handoff .planning/argonauts/r-e0a2598f/quality-handoff.json` → exit 0, `HANDOFF_READY_ONLY`, target_head 526b89c, quality pending

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log (none)
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-29
