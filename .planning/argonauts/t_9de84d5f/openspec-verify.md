# Verification Report: r-50053edc-wordfreq-html

Using change: r-50053edc-wordfreq-html (override: `openspec-verify-change <other>`).
Run by quality (argonauts-uat-quality, Kanban t_9de84d5f) at head 995011cd3b77d4d87a6be3bdf5780bf5cbe3b95c, 2026-11-18.
Inputs: `openspec status --change r-50053edc-wordfreq-html --json` (schema spec-driven, proposal/specs/design/tasks done), `openspec instructions apply --change r-50053edc-wordfreq-html --json` (taskTrackingConfigured true, progress 13/17, unavailableTrackingFiles null), `openspec validate r-50053edc-wordfreq-html --strict` → "Change 'r-50053edc-wordfreq-html' is valid".

## Summary

| Dimension    | Status |
|--------------|--------|
| Completeness | 13/17 tasks complete (3.1, 3.2, 4.1, 4.2 unchecked); 9 requirements (3 MODIFIED, 6 ADDED) all have implementation |
| Correctness  | 9/9 requirements implemented; 18/18 scenarios covered by tests and/or quality live evidence; 1 evidence-artifact divergence (HTML-6) and 1 CI divergence (HTML-6/4.2) |
| Coherence    | Design followed (stdlib html.escape, basename-only, stable sort, inline CSS, no script); code patterns consistent |

## Completeness

### Task Completion — 13/17
Incomplete tasks (from `progress.remaining` = 4):
- 3.1 明るい背景・連番・長文折返し (both widths). Quality evidence now exists: 22 views viewed at 1:1, light only, ranks 1..12 consecutive, long n/w runs wrap, no horizontal overflow (raw audit max right ≤ viewport and owner clip). Checkbox not ticked (quality does not edit openspec/).
- 3.2 ブラウザ検証手順と実測原本・画像. Tooling and quality raw/image evidence exist; checkbox not ticked.
- 4.1 品質の独立再実行. Executed by quality in this card (fresh root `.planning/argonauts/r-50053edc/quality`, session bf0a406b…, verdict accepted, AC1–AC6 accepted). Not fully closable: final manifest still shows per-view `pending-review` (see W-1).
- 4.2 全自動試験と差分の確認. Local full suite 284 passed and scope clean, but the repository's required CI `pytest` fails at this head (see C-1).

### Spec Coverage
MODIFIED: 実行方法とファイル読み込み（FR-1）, 出力形式オプション（FR-3）, 出力の順序決定論性（FR-4・D-2）. ADDED: HTML-1 … HTML-6. All found in `wordfreq/__main__.py`, `wordfreq/aggregator.py`, `wordfreq/formatters.py`, `tools/verify_wordfreq_html.py`, tests and docs. No REMOVED/RENAMED requirements.

## Correctness

### Requirement Implementation Mapping
| Requirement | Implementation | Evidence |
|---|---|---|
| FR-1 | `wordfreq/__main__.py` (unchanged error paths, html added) | quality CLI: missing file exit1, bad UTF-8 exit1, no argument exit2, empty file text '' / json '[]\n' / html 0 rows exit0 |
| FR-3 | `__main__.py` `--format` choices text/json/html; html written as UTF-8 bytes | `--format xml` exit2; tie text `2\tzoo\n2\tapple\n`, json `[{"word": "zoo", "count": 2}, …]` unchanged structure |
| FR-4 | `aggregator.py` `top_words` stable sort on `-count` then slice | tie-text/json/html 1 & 2 → zoo then apple; frequency beta 3, alpha 2 |
| HTML-1 | `formatters.py` `format_html` single document, meta charset utf-8, inline `<style>` | static audit passed; grep 0 for script/src/href/url()/@import/http; network.json only file:// doc |
| HTML-2 | `__main__.py` `os.path.basename`, `total = sum(counts.values())` before `top_words` | totals 6/6/6/7/0/200/200/200/5/5 in images; no `private-source-directory` or `/home/` in any stdout.html |
| HTML-3 | CSS `color-scheme: light`, `#FFFFFF`, `enumerate(pairs, 1)` | images: light only, no switch, ranks 1..n |
| HTML-4 | CSS `white-space: break-spaces; overflow-wrap: anywhere; table-layout: fixed` | 32 images readable at 1:1; jq audit of 22 raw.json: 0 owner/ancestor clip violations, 0 positive-area overlaps, contiguous UTF-16/codepoints |
| HTML-5 | `_html_text` = `html.escape(quote=True)` + CR → `&#13;` | injection stdout bytes `&amp;&lt;&gt;&quot;&#x27;`; image shows literal text; café/strasse casefold kept |
| HTML-6 | `tools/verify_wordfreq_html.py` review-session/finalize, runbook docs/wordfreq-html-verification.md | quality session exit 0, verdict accepted, independent_acceptance true, end head 995011c, product_status '' |

### Scenario Coverage
All 18 scenarios have tests in tests/test_cli.py, tests/test_formatters.py, tests/test_aggregator.py, tests/test_html_verifier.py (284 passed locally, twice) and, for the HTML-1/2/3/4/5/6 scenarios, quality live browser evidence. The legacy scenario name 「同回数ワードは単語の昇順」 is kept as identifier with the new first-occurrence expectation, as the spec states (approved intentional change).

## Coherence

### Design Adherence
Followed: stdlib-only escaping, caller-supplied basename/total, pure formatter, single stable sort, HTML bytes independent of locale, no dependency/CI change (`--check-scope` errors []).

### Code Pattern Consistency
Consistent with existing package layout. Suggestion S-1: `wordfreq/__main__.py:33-47` checks `args.format == "html"` twice (from 03-REVIEW IN-01).

## Issues by Priority

### CRITICAL
- C-1 Required CI `pytest` fails at head 995011c (GitHub Actions runs 44119531438 pull_request and 44119518087 push, job "pytest" conclusion failure; job log: "5 failed, 279 passed"). Failures: `tests/test_cli.py::test_html_preserves_basename_in_filesystem_encoding` and `test_html_bytes_are_utf8_independent_of_stdout_encoding[en_GB.iso885915-None]` (locale en_GB.iso885915 not installed on ubuntu runner); `tests/test_html_verifier.py::test_scope_has_exact_baseline_target_and_approved_product_snapshot`, `test_builtin_contract_and_scope_commands_need_no_browser_or_role`, `test_scope_rejects_dirty_and_untracked_code` (`git diff 5a7659b… <merge sha>` exit 128 — baseline commit not present in the CI checkout). Locally all pass. CI changes are out of scope, so tests must be made to work in the existing CI. Recommendation: Builder makes these tests independent of host locale availability and of full git history without weakening their assertions where the environment provides them (task 4.2).
- C-2 Tasks 3.1, 3.2, 4.1, 4.2 are unchecked. Recommendation: after C-1 and W-1 are fixed and quality re-verifies at the new head, mark them done.

### WARNING
- W-1 HTML-6 evidence artifact divergence: final `manifest.json` keeps `cases[].views[].verdict: "pending-review"` and `reviewed_images: []` for all 22 views (and every `derived.json`) after an accepted finalize; only top-level `verdict`/`ac_verdicts` are updated (`tools/verify_wordfreq_html.py` ~1146-1172). 03-04 PLAN verification requires "no pending fields". Recommendation: propagate the validated ledger into each view (verdict + reviewed_images), fail closed if any pending field remains, add a test.
- W-2 Provenance dirty check covers only wordfreq/, tools/, tests/ and root config, but pytest has no `testpaths`; untracked `test_*.py`/`conftest.py` elsewhere change the suite unnoticed (`tools/verify_wordfreq_html.py:269-274,1063`).

### SUGGESTION
- S-1 Duplicate `args.format == "html"` branch in `wordfreq/__main__.py:33-47`.
- S-2 Hard-coded SCOPE_BASE/APPROVED_PRODUCT/ACTORS make the verifier single-phase (`tools/verify_wordfreq_html.py:793-801`).

## Final Assessment
2 critical issue(s) found. Fix before archiving.
