---
phase: "03"
slug: "wordfreq-html-output"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-11-18"
---

# Phase 03 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Audited by quality (argonauts-uat-quality, Kanban t_9de84d5f) at head 995011cd3b77d4d87a6be3bdf5780bf5cbe3b95c.
> Register authored at plan time (03-01..03-04 `<threat_model>`), ASVS L1, block_on high → L1 evidence check, auditor not required (secure-phase short-circuit).
> Re-audited by quality (argonauts-uat-quality, Kanban t_c9dd351a) at head 7c704f337df10a4bfd4bb18936266a16b606dd3c: register extended with 03-05 (T-03-13, T-03-14) and 03-06 (T-03-15..T-03-17) plan-time threat models; T-03-SC re-checked. No SUMMARY `## Threat Flags`. ASVS L1, block_on high, threats_open 0 → short-circuit to L1 evidence (no auditor spawn).

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| input file → HTML document | Untrusted file text and filename are rendered into a static HTML page | words, basename (may contain markup, LF/TAB/spaces) |
| CLI argv path → HTML | Full path given on the command line; only the basename may appear | local directory names (private) |
| generated HTML → browser | Opened from file:// in a browser | must not trigger any network request |
| Builder vs quality evidence | Verdict files vs actual independent review | actor/root/head attribution |
| git target vs executed code | Head and working tree used to produce evidence | product diff, untracked files |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-03-01 | Tampering | format_html data slots | high | mitigate | `wordfreq/formatters.py` `_html_text` = `html.escape(quote=True)` + CR→`&#13;` for every slot; injection case stdout bytes show `&amp;&lt;&gt;&quot;&#x27;`; images show markup as literal text; tests/test_formatters.py 9 passed | closed |
| T-03-02 | Information disclosure | main basename/total seam | high | mitigate | `wordfreq/__main__.py` passes `os.path.basename(args.filename)` only; all 11 quality stdout.html contain no `private-source-directory` or `/home/` (grep 0); tests/test_cli.py 97 passed | closed |
| T-03-03 | Tampering | top_words | medium | mitigate | single stable sort on `-count` before slicing (`wordfreq/aggregator.py`); tie text/json/html all zoo→apple in quality session; tests/test_aggregator.py 5 passed | closed |
| T-03-04 | Information disclosure | HTML entire document | high | mitigate | same evidence as T-03-02 over every HTML surface (title fixed, basename only) | closed |
| T-03-05 | Tampering | source/CLI failure path | medium | mitigate | quality CLI reruns: malformed UTF-8 exit1, missing file exit1, no argument / --top 0 / -1 / --format xml exit2, empty file exit0; tests/test_sources.py 6 passed | closed |
| T-03-06 | Denial of service | responsive presentation | medium | mitigate | 32 images viewed 1:1; jq audit of 22 raw.json: max right within viewport and owner clip, 0 ancestor clip violations, 0 positive-area overlaps; long n/w runs wrap | closed |
| T-03-07 | Information disclosure | generated HTML/browser network | high | mitigate | static audit passed (no script/src/href/url()/@import/http in any stdout.html); per-view network.json only about:blank, case file:// and omnibox chrome:// UI; session canaries and standalone `--self-test-network` passed (4 violation kinds observed and rejected) | closed |
| T-03-08 | Repudiation | raw geometry and image capture | high | mitigate | raw.json keeps float rects, empty/zero-width whitespace records (LF width 0 retained), codepoints, UTF-16 offsets (quality jq audit: contiguous, concatenation equals text) | closed |
| T-03-09 | Spoofing | CLI evidence provenance | high | mitigate | provenance.json/scope.json at session start and end_provenance at end: head 995011c, product_status empty; untracked product code checked. Residual (non-blocking, reviewer WR-01 r2): untracked test_*.py outside tests/ not dirty-checked | closed |
| T-03-10 | Repudiation | final evidence verdict | high | mitigate | finalize accepted only for actor argonauts-uat-quality with ledger sha d2d5f2a7 matching; Builder profile rejected (parent review). Note: final manifest still carries per-view `verdict: pending-review` / empty `reviewed_images` (reported as gap in VERIFICATION, not a security bypass) | closed |
| T-03-11 | Information disclosure | review-session observation interval | high | mitigate | ready_at 16:00:55Z → all reviews 16:01:52–16:06:21Z → verification_finished 16:09:55Z → observation_end 16:09:56Z → ended 16:09:57Z; process exit 0; errors empty | closed |
| T-03-12 | Tampering | scope/head attribution | high | mitigate | `--check-scope` errors empty; base 5a7659b vs target 995011c; no .github/, pyproject.toml, lockfile, tokenizer or sources change in product diff | closed |
| T-03-SC | Tampering | package installation | high | mitigate | no dependency/CI paths in scope diff; browser tooling pre-existing (Chromium 156.0.8078.73, Playwright/websockets from existing site-packages); nothing installed. Re-checked at 7c704f3: `git diff origin/main...HEAD -- .github pyproject.toml` empty, `--check-scope` passed errors [] | closed |
| T-03-13 | Repudiation | manifest/derived/ledger projection | high | mitigate | tests/test_html_finalization.py (test_real_owner_projects_exact_ledger_into_every_persisted_view, test_ledger_order_does_not_change_canonical_projection, test_final_consistency_rejects_contradictory_persisted_records) 29 passed at 7c704f3. Live quality root gap1-final-05: owner exit0, 22/22 views and derived accepted and identical as canonical (key-sorted) JSON, [image,sha256,viewed_at] set (32) identical across ledger/manifest/derived, 0 pending-review, ledger_sha256 = sha256(reviews.json) cb83d72d… | closed |
| T-03-14 | Tampering | interrupted final publication | high | mitigate | test_owner_failures_revoke_every_saved_view, test_invalid_ledger_or_bytes_fail_closed_in_real_owner, test_persistent_storage_failure_is_explicit_and_nonzero green; `tools/verify_wordfreq_html.py` re-snapshots live listeners after checks (`snapshot_live` late events added to errors, lines ~1093-1097) and starts every manifest as `unverified` (line ~683) | closed |
| T-03-15 | Tampering | encoding regression preconditions | medium | mitigate | tests/fixtures/encoding_cli_probe.py controlled byte seam; test_encoding_obligations_run_without_native_locale, test_native_encoding_availability_and_charmap_mismatch, test_html_bytes_are_utf8_independent_of_stdout_encoding in tests/test_cli.py 100 passed; host has en_US.iso885915 so the native branch actually ran; 0 skipped | closed |
| T-03-16 | Spoofing | shallow scope/execution provenance | high | mitigate | test_depth_one_scope_command_keeps_exact_missing_refs and test_isolated_collection_and_module_shadow_are_execution_influence green (tests/test_html_verifier.py 203 passed); real `--check-scope` resolved exact base 5a7659b / approved ed7e6cc, target 7c704f3, errors [], product_status empty, untracked_product [] | closed |
| T-03-17 | Repudiation | actor/record/head/CI handoff | high | mitigate | test_finalize_implicit_actor_matches_manifest_actor and test_plan_quality_commands_resolve_actual_actor_without_actor_option green; live session with `--actor` omitted recorded actor argonauts-uat-quality; same-card quality→Builder record→re-review cycle completed on t_13f258db (H1→H4); same-head CI read once (runs 44154730435/44154716225 success, 361 passed) | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

No accepted risks.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-18 | 13 | 13 | 0 | argonauts-uat-quality (t_9de84d5f, gsd-secure-phase L1) |
| 2026-11-18 | 18 | 18 | 0 | argonauts-uat-quality (t_c9dd351a, gsd-secure-phase L1, head 7c704f3) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-18

## Security Audit 2026-11-17

| Metric | Count |
|---|---|
| Threats found | 13 |
| Closed | 13 |
| Open | 0 |

## Security Audit 2026-11-17

| Metric | Count |
|---|---|
| Threats found | 18 |
| Closed | 18 |
| Open | 0 |
