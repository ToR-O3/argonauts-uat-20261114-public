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
| T-03-SC | Tampering | package installation | high | mitigate | no dependency/CI paths in scope diff; browser tooling pre-existing (Chromium 156.0.8078.73, Playwright/websockets from existing site-packages); nothing installed | closed |

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
