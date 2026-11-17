## Verification Report: r-50053edc-wordfreq-html

Using change: r-50053edc-wordfreq-html (override: `openspec-verify-change <other>`).
Run by quality argonauts-uat-quality, Kanban t_c9dd351a (phase 3 verification, final phase), against checked head `7c704f337df10a4bfd4bb18936266a16b606dd3c` (= origin/argonauts/r-50053edc = ToR-O3/argonauts-uat-20261114-public#5 headRefOid). Official workflow: `openspec status --change … --json` (schema spec-driven, isComplete true, proposal/specs/design/tasks done), `openspec instructions apply --change … --json` (state all_done, taskTrackingConfigured true, unavailableTrackingFiles null), `openspec validate r-50053edc-wordfreq-html --strict --json` (1/1 passed). Raw outputs: os-status.json, os-apply.json, os-validate.json in this directory.

### Summary
| Dimension    | Status |
|--------------|--------|
| Completeness | 17/17 tasks complete (remaining 0); 9 requirements (3 MODIFIED, 6 ADDED), all mapped |
| Correctness  | 9/9 reqs covered; 21/21 scenarios covered by tests and/or fresh independent quality evidence |
| Coherence    | Design decisions 1–6 followed; no significant pattern deviations |

### Completeness
- Task completion: `progress` total 17, complete 17, remaining 0. 3.1/3.2/4.1/4.2 were checked by the Builder only after independent quality evidence (card t_13f258db H1→H4 cycle); this run re-established that evidence independently at the same head 7c704f3 in fresh root `quality/gap1-final-05` (see below), so the checked boxes are backed by current-head facts.
- Spec coverage (delta `specs/wordfreq-cli/spec.md`):
  - MODIFIED FR-1 実行方法とファイル読み込み — `wordfreq/__main__.py`, `wordfreq/sources.py` (unchanged since main); tests/test_cli.py (100 passed) cover missing/undecodable/empty/arg-count and html error paths.
  - MODIFIED FR-3 出力形式オプション — `--format` choices text/json/html (`wordfreq/__main__.py:16`); fresh CLI tie-text/tie-json/tie-html runs give identical words/counts/order; html-only metadata.
  - MODIFIED FR-4 出力の順序決定論性 — `wordfreq/aggregator.py:11-17` stable sort on `-count` over Counter insertion (first-occurrence) order; tests/test_aggregator.py 5 passed; fresh CLI tie top1 `zoo 2`, top2 `zoo 2, apple 2` in all three formats.
  - ADDED HTML-1..HTML-6 — `wordfreq/formatters.py:17-…` (`format_html`, `_html_text` = html.escape(quote=True) + CR→`&#13;`, single inline `<style>`, UTF-8 meta, no script/external refs), `wordfreq/__main__.py:31-38` (total = sum(counts) before top, basename only), verification tooling `tools/verify_wordfreq_html.py` + `tools/wordfreq_html_geometry.js`.

### Correctness — requirement → evidence
| Requirement | Implementation | Evidence at 7c704f3 |
|---|---|---|
| FR-1 | __main__/sources | test_cli 100 passed; per-file runs green |
| FR-3 | __main__ `--format` | tie-text/json/html CLI stdout consistent; test_cli/test_formatters |
| FR-4 | aggregator.top_words | test_aggregator 5 passed; tie/normal/frequency CLI order |
| HTML-1 (AC1) | formatters.format_html | 11 HTML stdouts strict UTF-8, 1 `<style>`, 0 `<script>`, 0 external refs; 22 view network.json errors 0, only file/about/chrome schemes; canaries passed (session + gap1-network-07) |
| HTML-2 (AC2) | __main__ total/basename | totals 6/6/6/7/0/200/200/200/5/5/5; basename only, no worktree path in any stdout |
| HTML-3 (AC4) | formatters CSS | light background only, no toggle, ranks 1..n consecutive (images) |
| HTML-4 (AC4) | formatters CSS (break-spaces, overflow-wrap:anywhere) | 32 images viewed 1:1 readable; rawaudit 22/22 zero problems (no right overflow, no clip escape, no positive-area overlap); own-element vertical containment not required |
| HTML-5 (AC5) | `_html_text` | injection basename rendered as text; café/strasse/日本語 casefold kept |
| HTML-6 (AC6) | verifier tool | fresh quality regeneration, owner exit 0, manifest accepted, independent_acceptance true, AC1–6 accepted, 22/22 views+derived accepted, ledger/manifest/derived image sets identical, 0 pending; full suite 361 passed; scope passed; CI same head success (361 passed); no CI/dependency change |

Scenario coverage: all 21 scenarios have a covering test and/or fresh CLI/browser observation (FR-1 ×6, FR-3 ×3, FR-4 ×2, HTML-1 ×1, HTML-2 ×3, HTML-3 ×1, HTML-4 ×2, HTML-5 ×1, HTML-6 ×2).

### Coherence
- Design 1 (Counter insertion order + stable sort) — followed (`aggregator.py:17`).
- Design 2 (total from pre-top Counter, basename only) — followed (`__main__.py:31-38`).
- Design 3 (pure HTML formatter, standard escape, fixed tags/CSS) — followed.
- Design 4 (static light responsive table, wrap, no truncation) — followed; confirmed visually.
- Design 5 (geometry + images, no own-vertical requirement) — followed by tooling; quality audit used raw floats without correction.
- Design 6 (independent reproduction and evidence) — followed in this run.
- Code pattern consistency: product files follow existing module boundaries; no new dependencies; tokenizer/sources unchanged vs main.

### Issues by Priority
1. **CRITICAL**: none.
2. **WARNING**:
   - W-1: Scenario title `同回数ワードは単語の昇順` (spec.md:50) keeps the old identifier although its body now requires first-occurrence order. Intentional and explained in the scenario text; recommend renaming at archive/sync time to avoid misreading (spec.md:50-52).
   - W-2: tasks.md history paragraph pointer `次節` points the wrong way (carried from PLAN 03-06 review WR-02). Recommendation: reword when tasks.md is next edited (openspec/changes/r-50053edc-wordfreq-html/tasks.md:105).
3. **SUGGESTION**:
   - S-1: Phase code review (03-REVIEW.md) WR-01..03 harden the verifier's scope/provenance checks (`--no-renames`, ignored collected tests, other root import shadows). Not requirement gaps at this head; consider a follow-up.

### Final Assessment
No critical issues. 2 warning(s) to consider, 1 suggestion. Ready for archive (with noted improvements).
