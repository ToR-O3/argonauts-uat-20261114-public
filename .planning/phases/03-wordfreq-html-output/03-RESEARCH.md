# Phase 3: wordfreq HTML output — Research

**Researched:** 2026-11-17 (JST)
**Domain:** Python CLI / pure HTML formatting / local Chromium evidence
**Confidence:** Local code findings verified by reads; documentation cited; browser execution remains unverified. Research is sufficient for planning, not a product acceptance result.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

## Locked approved decisions
- D-01: --format html outputs one self-contained static UTF-8 HTML document to stdout. Inline CSS only; no script/external resources or communication attempts.
- D-02: Three columns: rank, word, count. Above table show basename only and total occurrences before top. No directory information anywhere in title/attributes/body.
- D-03: Frequency descending, ties by first normalized occurrence, then top. This intentionally supersedes Phase 1 REQ-04 / PROJECT D-2 / CONTEXT D-10 lexical ties for text/json/html. Approval explicitly covers the compatibility change. Do not restore lexical ties or mutate historical completion evidence.
- D-04: Keep tokenizer, Unicode extraction, casefold, input boundary, top default10 and positive integer/error contracts, text/json structure and empty forms except new tie order.
- D-05: Light background only, no toggle, rank 1-based displayed row sequence (not competition rank).
- D-06: Normal and 320 CSS px widths must show full long words and valid long basename including repeated spaces/newlines/tabs. UI-SPEC fixes actual browser, normal width and wrapping fixture.
- D-07: Preserve raw element/character Range line fragments/clipping ancestor geometry; judge horizontal containment, clipping-ancestor containment, adjacent nonoverlap and actual full screenshot readability. Strict own-element vertical containment is not mandatory; never adjust raw geometry to force pass.
- D-08: Quality independently regenerates actual CLI HTML at target head for empty/normal/top/long/injection; records input originals, exact command, exit/stdout/stderr, expectation, HTML, browser/version/viewport, raw geometry, all image viewing and network attempts including failed attempts/document navigation. Observe from before opening until end; distinguish browser background traffic with grounds. Builder images or blocked network alone do not suffice.
- D-09: No CI change, dependency addition, timestamp, theme switch, interactive UI, server or input source extension.
- D-10: Automated commands run unattended from repo root against real test files available by that task completion; no inline code or outer cd/grep. Each task has concrete fails_when observable with existing/new tests, never a command whose no-op can pass a defect.
- D-11: PLANs stack sequentially on same request branch in numeric order; task verification runs at task completion, phase verification includes all earlier PLANs. Independent PLAN tests must not depend on absent later artifacts. Max 3 tasks per PLAN. Security/nyquist/plan_check/pattern_mapper settings stay enabled.
- D-12: Exact required acceptance examples from PRD: `Zoo apple APPLE zoo banana` top1=>zoo2, top2=>zoo2/apple2; `zoo apple zoo banana apple cherry` top1/2/10 => total6, 1/2/4 rows; `beta beta beta alpha gamma alpha delta` top2=>beta3/alpha2 total7. Later repeated tokens never update first position. Unequal counts remain descending. Empty HTML has basename/total0/headers and zero data rows; text empty stdout, JSON [] plus newline. Formatter tests inject `& < > " '` and tag/event-looking tokens directly; CLI uses valid hostile basename without weakening tokenizer. Read errors including permission/decode=>exit1, invalid top0/negative/noninteger or format/arity=>exit2, stderr and empty stdout. Encoding must match actual saved UTF8. Browser contract adds whitespace, multi-digit rank/count fixtures and both widths, retaining exact raw Range coordinates.

### Claude's Discretion
Local implementation names and test decomposition only, constrained by existing package boundaries and approved design. UI choices fixed by 03-UI-SPEC.md. No additional product decision remains open.

### Deferred Ideas (OUT OF SCOPE)
CI edits, dependency changes, new input sources, theme controls, generation timestamps, servers. Implementation and product browser acceptance are not part of this planning card.
</user_constraints>

## Summary

Use the approved existing pipeline, not a new architecture: read once through FileSource, normalize in iter_tokens, count in Counter, calculate total before top, stable-sort by count alone, then format. HTML receives already-ordered pairs plus basename and total; it does not reopen input, infer totals from visible rows, or sort separately. The approved design explicitly selects Counter insertion order and stable sort. [VERIFIED: openspec/changes/r-50053edc-wordfreq-html/design.md:10-16; wordfreq/aggregator.py:6-13; wordfreq/__main__.py:24-31]

The main planning risk is evidence infrastructure, not rendering complexity. Existing tests have lexical-order expectations; there are no HTML assertions in the read formatter/CLI files. Bare `python -m pytest --version`, `pytest --version`, and `playwright --version` fail in this session because the active interpreter/HOME does not expose the installed packages. A read-only alternative succeeds with `/usr/bin/python3` and explicit existing Python 3.12 site-packages. Chromium resolves and reports a version, but no browser was launched and no product tests were run. Do not equate CLI discovery with runnable browser acceptance. [VERIFIED: tests/test_aggregator.py:17-33; tests/test_cli.py:22-60; tests/test_formatters.py:1-46; environment probe outputs this session]

**Primary recommendation:** Plan sequential, independently verifiable increments: shared order contract → complete HTML CLI tracer with final UI structure/CSS → strengthened cross-format/error/security coverage → real-file browser collector and independent quality evidence. Each PLAN has at most three tasks, verifies only artifacts present by its completion, and includes earlier coverage in the final phase gate. This is a decomposition recommendation, not an additional product decision. [VERIFIED: 03-CONTEXT.md:24-29; approved tasks.md:3-19]

## Architectural Responsibility Map

| Capability | Primary owner | Secondary owner | Boundary |
|---|---|---|---|
| Input acquisition and UTF-8 read errors | Existing source boundary | CLI exit mapping | Do not add input types |
| Extraction and casefold | Existing tokenizer | — | Preserve input order and current token rules |
| Counts and first-occurrence tie order | Aggregator | CLI passes ordered normalized tokens | Single ordering path for all formats |
| Pre-top total and basename selection | CLI composition | — | Calculate once before top; never send full input path to formatter |
| Safe HTML document and CSS | Pure formatter | — | Fixed markup/style, escaped data text only |
| Layout and text fragments | Browser/static document | Local evidence collector | No product JavaScript |
| Acceptance and evidence attribution | Independent quality | Builder supplies reproducible real-file tools | Quality regenerates its own CLI outputs |

Source for responsibility boundaries: [VERIFIED: wordfreq/sources.py:1-22; wordfreq/tokenizer.py:6-18; wordfreq/formatters.py:1-13; openspec/changes/r-50053edc-wordfreq-html/design.md:10-16].

<phase_requirements>
## Phase Requirements

Source descriptions below follow the six Phase 3 requirements; use REQUIREMENTS.md as the full acceptance text. [VERIFIED: .planning/REQUIREMENTS.md:32-50]

| ID | Description / acceptance area | Research support |
|---|---|---|
| REQ-09 | AC1: single self-contained UTF-8 HTML, rank/word/count, inline CSS, no execution/resources/communication attempts | Pure formatter; structural allow-list and CSS audit; strict stdout byte decoding; pre-navigation network collector |
| REQ-10 | AC2: basename only above table; pre-top total; top/default/oversized/empty | CLI metadata seam and fixtures with totals 6, 7, 0, 200; raw/escaped parent-path absence; DOM order and visible geometry |
| REQ-11 | AC3: descending frequency, normalized first-occurrence ties, then top in every format | Counter insertion-order precondition; count-only stable sort; update lexical assertions and current glossary/help; preserve Phase 1 history |
| REQ-12 | AC4: fixed light responsive three-column table, sequential ranks, complete text and raw geometry/readability | Exact approved UI-SPEC and both viewport dimensions; character/line Ranges, all ancestors, nonoverlap, full image viewing |
| REQ-13 | AC5: escaped words/basename; tokenizer/source/error/default/text-json regressions | Direct formatter hostile tokens; real valid hostile basename; all-format subprocess tests; existing tokenizer/source suites; permission-error gap |
| REQ-14 | AC6: automated plus independent quality regeneration/browser evidence at target head; full AC evidence and scope guard | Collector with explicit failure states, AC manifest, separate Builder/quality output roots and image-review record; no CI/dependency edits |
</phase_requirements>

## Project Constraints (from HERMES.md / discovery)

No root HERMES.md was found by filename search; `.hermes` and `.agents` project paths were absent. Therefore no project HERMES directives are invented. Official `query agent-skills gsd-phase-researcher --skills-only` returned no configured additions. Official `query init.phase-op 3` resolved `"phase_number": "03"`, `"phase_slug": "wordfreq-html-output"`, `"has_context": true`, `"has_research": false`, `"has_plans": false` before this write. `graphify status` reported disabled; it was not enabled. [VERIFIED: discovery and official CLI outputs this session]

Keep the read config settings `"nyquist_validation": true`, `"plan_check": true`, `"pattern_mapper": true`, `"security_enforcement": true`, `"security_asvs_level": 1`, `"security_block_on": "high"`. The task's no-commit/no-push instruction overrides `"commit_docs": true` for this research. STATE's older Phase 1 position is not permission to research/reuse residual Phase 2; Phase 3 and its explicit approved replacement are authoritative here. Context-drift skip `no-upstream-artifacts` and inactive Teams status were supplied by the parent, not reinterpreted as product validation. [VERIFIED: .planning/config.json:21-53,79-81; .planning/STATE.md:3-16,79-81; 03-CONTEXT.md:5-7; parent task context]

## Standard Stack

| Tool/library | Verified existing version or contract | Purpose / disposition |
|---|---|---|
| CPython standard library | Existing CI declares `python-version: "3.12"`; local `/usr/bin/python3 --version` reports 3.12.15; active `python --version` reports 3.14.9 | Target current CI major/minor, not new version-crossing compatibility code |
| collections.Counter, sorted | Already imported/used; documented insertion order and sort stability | Keep API; remove lexical secondary key only |
| html.escape | Standard library, `quote=True` documented in Python 3.12 | Escape each dynamic text value once |
| os.path.basename | Standard library uses host pathname convention | Use at CLI seam; no manual split or full-path interpolation |
| pytest | Existing dev declaration `dev = ["pytest"]`; environment-scoped probe reports 9.0.3 | Keep ordinary real-file pytest commands; no dependency/config change |
| Playwright Python | Existing external METADATA `Name: playwright`, `Version: 1.60.0`; scoped module CLI reports 1.60.0 | Local verification only, outside runtime/project dependencies |
| Chromium | `/usr/bin/chromium-browser --version` reports 156.0.8078.73 | Required browser; launch and protocol compatibility still untested |

[VERIFIED: .github/workflows/pytest.yml:13-18; pyproject.toml:5-14, including `dependencies = []`; wordfreq/aggregator.py:2-13; /home/Yuki/.local/lib/python3.12/site-packages/playwright-1.60.0.dist-info/METADATA:1-23; environment outputs]. [CITED: https://docs.python.org/3.12/library/html.html; https://docs.python.org/3.12/library/os.path.html#os.path.basename; https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts; https://docs.python.org/3/library/collections.html#collections.Counter]

**Installation / Package Legitimacy Audit:** No package installation is recommended or performed. No pyproject, lockfile, CI or project dependency additions. Environment discovery does not justify adding browser packages to `dev`. Existing Node Playwright is a possible environment fallback, not a project stack alternative; prefer the working Python 3.12 module discovery. [VERIFIED: 03-CONTEXT.md:23; pyproject.toml:8-14; environment probe outputs]

## Architecture Patterns

### System architecture / data flow

```text
argv → existing parser → valid top/format?
                        ├─ no → stderr + exit 2, stdout empty
                        └─ yes → FileSource → readable UTF-8?
                                             ├─ no → stderr + exit 1, stdout empty
                                             └─ yes → extraction → casefold → Counter
                                                       ├─ full-count total
                                                       └─ stable frequency sort → top pairs
argv filename → host basename only ──────────────────────────────┐
top pairs + (HTML-only total and basename) → chosen pure formatter│
                            text / json / HTML ←────────────────┘
                            → stdout → exit 0
saved real CLI HTML → local Chromium file navigation
                    → raw ranges + network attempts + screenshots
                    → independent quality's full-image review + AC verdict
```

This is the approved data-flow recommendation, not an implementation. Existing error mapping remains in CLI. [VERIFIED: wordfreq/__main__.py:19-32; openspec/changes/r-50053edc-wordfreq-html/design.md:10-16]

### Concrete file targets and nearest analogues

Existing targets below were opened this session. Paths listed as **proposed NEW** do not exist as verified artifacts and must be created before their commands are run.

| Target | Planned responsibility | Existing source/analogue |
|---|---|---|
| `wordfreq/aggregator.py` | Change `top_words` sorting and docstring; preserve Counter insertion order as precondition | Current `return sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))[:n]` at :11-13 |
| `wordfreq/formatters.py` | Add pure HTML formatter with pairs/basename/total; final approved semantic HTML/CSS | `format_text` and `format_json` at :5-13, no I/O/exit |
| `wordfreq/__main__.py` | Add HTML choice/dispatch; hold counts; calculate total before top; basename extraction | Current `choices=["text", "json"]` at :15, composition at :24-31 |
| `tests/test_aggregator.py` | Replace lexical expectations; assert first-occurrence, repeat stability, top and nonmutation | Current lexical test `test_top_words_sorts_frequency_then_word` at :17-23 and limits at :26-33 |
| `tests/test_formatters.py` | Retain exact text/json assertions; add HTML parser/escape/empty/static/document tests | :7-46 |
| `tests/test_cli.py` | Revise lexical expected results; all-format order, metadata, byte encoding, error and no-write regressions | `run_cli` at :15-19, legacy expectations :22-60, existing errors :63-149, cold repo test :152-180 |
| `tests/test_sources.py` | Add deterministic PermissionError boundary coverage if needed; retain UTF-8/error behavior | :21-52, source exception mapping :17-22 |
| `tests/test_tokenizer.py`, `tests/test_sources_boundary.py` | Regression execution, preferably unchanged | Current tokenizer :6-60, source boundary :7-42 |
| `README.md` | CLI HTML/save usage, deliberate tie compatibility change, local browser verification instructions | Current README is only title/description at :1-3 |
| `CONCEPTS.md` | Update current glossary entry, explicitly superseded initial tie contract | `## 決定論的順位` at :45-47 currently says codepoint ascending |
| **proposed NEW** `tools/verify_wordfreq_html.py` | Real-file subprocess generation, fixture construction, static audit, Chromium capture, evidence manifest and failure exit | CLI's `run_cli` is subprocess pattern; no existing browser collector was read/found in repository file discovery |
| **proposed NEW** `tools/wordfreq_html_geometry.js` | Read-only DOM/Range collector loaded by verifier from disk; no inserted product script | UI-SPEC :165-183 and official Range API |
| **proposed NEW** `tests/test_html_verifier.py` | Test collector manifest/completeness and deterministic failure predicates with supplied records | Existing pytest modules; do not require browser import at collection |
| **proposed NEW** `docs/wordfreq-html-verification.md` | Exact invocation, independence, image-viewing ledger, AC evidence schema, failure/unverified semantics | Approved tasks 3.2/4.1/4.2 |

Do not edit archived Phase 1 plans/evidence, another request's Phase 2, approved source decisions, `.github/workflows/pytest.yml`, or dependency declarations. Current approved delta is sufficient to supersede old lexical text; do not turn historical evidence into a new acceptance assertion. [VERIFIED: 03-CONTEXT.md:7,17,23-26; approved design.md:27-28]

### Shared ranking contract

Counter is built directly from normalized tokens in current `count_words`. Python documents remembered insertion order since 3.7 and stable sorts. Use a count-only key, leaving ties in original counts iteration order, then slice. State in the public component docstring that insertion order in supplied counts must represent normalized first occurrence. Arbitrarily reordered mappings cannot reconstruct input history; do not introduce sets/reinsertions or HTML-only sorts. Counter equality alone does not assert order: tests must examine ordered pairs/keys as well as counts. [VERIFIED: wordfreq/aggregator.py:6-13; approved design.md:11; tests/test_aggregator.py:11-14]. [CITED: https://docs.python.org/3/library/collections.html#collections.Counter; https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts]

Updating order will intentionally change these existing CLI assertions: default mixed input at test_cli.py:22-28, top-three input at :31-36, JSON normalized ties at :48-58. Derive each expected sequence from normalized first positions; do not merely rename tests. Empty text/json representations and count-first tab/newline structure remain exact. [VERIFIED: tests/test_cli.py:22-60,137-149; wordfreq/formatters.py:5-13]

### HTML metadata and safe rendering

Retain counts as one CLI value; calculate `sum(counts.values())` before calling `top_words`. Pass basename, not args.filename, into HTML formatter. Use fixed title and dynamic values in dedicated text-only nodes, including basename without template-added whitespace within its value node. All user data must pass html.escape once. Fixed tags/CSS do not need data interpolation; never put basename/words into selectors, attributes, URL, comments or style. [VERIFIED: approved design.md:12-14; 03-UI-SPEC.md:43-53]. [CITED: https://docs.python.org/3.12/library/html.html; https://docs.python.org/3.12/library/os.path.html#os.path.basename]

Do not change text/json formatter signatures. Add no HTML-specific data there. A string formatter returning a completed document preserves existing separation; no template engine, filesystem access, stdout writes or exit calls belong in formatter. Escape tests must parse displayed text and compare to the original, as well as reject extra nodes/attributes; presence of `&lt;` alone is not a safety proof. [VERIFIED: wordfreq/formatters.py:1-13; approved design.md:13; 03-UI-SPEC.md:152-153,181]

### UI implementation boundary

Use the approved UI-SPEC, not a new design exercise: document `lang="ja"`, early charset/viewport, fixed Japanese title/h1, separate labels/values above semantic table/caption, three `th scope="col"`, empty message outside zero-row tbody. Its exact values include `max-width: 960px`, normal/compact main padding `32px`/`16px`, compact breakpoint `480px`, rank/count columns `56px`/`64px`, table `table-layout: fixed`, cell padding `8px`, white background, system font and fixed light color scheme. Basename/word `white-space: break-spaces; overflow-wrap: anywhere; word-break: normal; tab-size: 4`; numeric columns may wrap without shrinking. These are locked values, not empirical results. [VERIFIED: 03-UI-SPEC.md:26-54,58-104]

The required normal browser size is **1280 × 900**, not an arbitrary desktop width; narrow is **320 × 900 CSS px**, DPR 1/100% zoom, fresh headless Chromium context each case. Exact long fixture: L = 256 ASCII `w`; B = `集計  ` + 176 ASCII `n` + actual LF + `続き` + actual TAB + `終わり  &<>"'.txt`. Body multiplicities are L123, row01:12, row02:11, row03:10, row04:9, row05:8, row06:7, row07:6, row08:5, row09:4, row10:3, row11:2, spaces between tokens and one trailing LF, top12. Expected 12 rows / total200 / counts123 through2; top omitted10 rows / top99 all12. Preserve actual control characters, not backslash escapes in the real filename. Both long nonspace runs must measurably wrap at both sizes. Injection basename is `検査  &<>"'` + LF + `次` + TAB + `終.txt`, body `Café CAFÉ Straße STRASSE 日本語`, expected café2/strasse2/日本語1 total5. [VERIFIED: 03-UI-SPEC.md:134-163]

## Don't Hand-Roll

| Problem | Do not build | Use instead |
|---|---|---|
| HTML escaping | Replacement chain, JS/URL escaping, tokenizer relaxation | Standard html.escape with quote=True; text-node placement |
| Basename extraction | Slash splitting or cross-platform normalization inventions | Host os.path.basename at CLI seam |
| First-position storage | Parallel positional model or reconstruction from top rows | Approved Counter insertion-order + stable frequency-only sort |
| Geometry | Estimated font widths or modified DOM pretending to fit | Browser Element/Range raw getClientRects and screenshots |
| Network safety | Offline success, blocked requests, successful-response-only count | Static audit + request/failed/navigation/initiator observation |
| Evidence completion | Auto-fill image review as passed | Explicit independent image viewing with reviewer decisions |

[VERIFIED: approved design.md:10-20; 03-UI-SPEC.md:165-183]. [CITED: Python HTML/path/sorting documentation; https://developer.mozilla.org/en-US/docs/Web/API/Range/getClientRects]

## Common Pitfalls / fails_when Design

Each row is a concrete failure condition the PLAN can attach to a task, not an implemented test result.

| Defect | Required observable failure / assertion location |
|---|---|
| Lexical ties survive; top taken before ranking; later token moves first position | Aggregator ordered-pair assertion and all-format `Zoo apple APPLE zoo banana` top1/top2 give wrong first row/order |
| Total = kinds or sum(top rows) | CLI parsed total differs from 6 at top1/2/10 or 7 at frequency top2; empty differs from0 |
| Full path leaks anywhere | Raw HTML contains unique parent marker/full path, or escaped variants, including title/attrs/comments; fail with location |
| Escaping absent or double | Parsed text differs from exact original hostile value, or extra tag/event/resource attribute appears |
| No HTML support / empty fake row | CLI format html exits2; or empty tbody data-row count not0; missing three headers/basename/total |
| CSS clips or changes data to fit | Raw characters leave viewport/column, clip ancestor, or overlap adjacent text; screenshot is unreadable; whitespace/codepoints differ |
| Invalid numeric/rank behavior | Ranks are not sequential1..12, rank10..12 or count123 is split in required fixture, count lost |
| False geometry rejection | Synthetic raw record extending own vertical box but not clipped/overlapping incorrectly fails; retain record and do not add own-height criterion |
| False no-network pass | Failed external attempt/navigation detected even when success responses are0; event logged and nonzero collector result |
| No-op collector / missing cases | Manifest misses expected case-width records, output files, character indices, observation endpoints, or screenshot coverage; must fail, never empty-loop success |
| Missing tool or failed browser launch | Explicit environment failure, exit nonzero, evidence status unverified; no skip-to-pass |
| Old Builder evidence presented as quality | Head/actor/output-root/provenance or independent CLI output absent; incomplete AC14 evidence |

Tests for failure discrimination should use deterministic records and, when needed, isolated scratch copies/controlled verification pages. Never inject deliberate defects into the working product tree. Existing cold-copy status test must retain tracked baseline and independent cache handling when extended to HTML. The learning's old lexical sort is superseded, not reusable. [VERIFIED: tests/test_cli.py:152-180; docs/solutions/best-practices/git-state-test-discrimination-and-staged-baseline.md:35-44; docs/solutions/best-practices/input-boundary-verification-and-deterministic-ordering.md:30-36; 03-CONTEXT.md:17,24-26]

## Code Examples (planning patterns, not implementation artifacts)

The following recommended seam follows approved design exactly; it is not a file written or command executed in this research:

```python
counts = count_words(iter_tokens(text))
total = sum(counts.values())
pairs = top_words(counts, args.top)
# HTML gets only pairs, basename, total; text/json keep existing inputs.
```

For aggregation, approved replacement pattern is `sorted(counts.items(), key=lambda wc: -wc[1])[:n]`. Its precondition is documented ordered counts; no extra tie key. For dynamic text, use `html.escape(value, quote=True)`. These are recommendations based on [VERIFIED: approved design.md:11-13; wordfreq/__main__.py:24-31] and [CITED: Python sorting HOWTO and html.escape documentation above], not assertions of an existing HTML function/signature.

## Environment Availability

Read-only probes returned:

```text
python --version: Python 3.14.9
python -m pytest --version: No module named pytest
pytest --version: ModuleNotFoundError: No module named 'pytest'
playwright --version: ModuleNotFoundError: No module named 'playwright'
/usr/bin/python3 --version: Python 3.12.15
/usr/bin/python3 -m pytest --version: No module named pytest
/usr/bin/python3 -m playwright --version: No module named playwright
/usr/bin/chromium-browser --version:
Chromium 156.0.8078.73 Built from source for Red Hat Enterprise Linux release 10.2 (Coughlan)
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest --version:
pytest 9.0.3
env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m playwright --version:
Version 1.60.0
node /home/Yuki/.local/share/note-post-mcp/node_modules/playwright/cli.js --version:
Version 1.56.0
```

[VERIFIED: actual probe stdout/stderr this session; launcher shebang `#!/usr/bin/python3` in /home/Yuki/.local/bin/pytest:1-8 and /home/Yuki/.local/bin/playwright:1-8]. Existing Node package declares `"name": "playwright"`, `"version": "1.56.0"` in /home/Yuki/.local/share/note-post-mcp/node_modules/playwright/package.json:1-3; do not assume it is globally importable or prefer it over the discovered Python module.

**Planning consequence:** The canonical pytest commands below are real-file standards, not proven runnable in the current default shell. Builder/quality must record interpreter resolution and select a working existing environment before running them. The verified alternative is an explicit external site-package path with **Python3.12 only**; do not point Python3.14 at Python3.12 binary extensions. An equivalent real-file fallback for each canonical command is, for example, `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_aggregator.py -x`. This changes no project files/declarations and installs nothing. Preserve the canonical command in VALIDATION.md together with exact actual interpreter invocation. Browser launch/protocol/fonts/image-tool readiness still must be exercised by the implemented real-file verifier. There is no claim that versions alone establish compatibility. [VERIFIED: probe outputs; .github/workflows/pytest.yml:16-18; 03-UI-SPEC.md:136-140,183]

No product/browser tests or nonexistent verifier commands were run during research. No server was started. Research is not blocked by deferred browser execution, but execution acceptance must stop unverified if the environment cannot run it. [VERIFIED: this session tool activity and task boundary]

## Validation Architecture

### Test Framework

| Property | Value |
|---|---|
| Framework | Existing pytest; scoped version discovery 9.0.3, actual test runtime not exercised here |
| Config | `pyproject.toml` contains package/dev configuration, no pytest table in that read file; use existing pytest discovery, no new config/dependency requirement |
| Quick commands (prior_verify_commands preserved) | `python -m pytest tests/test_aggregator.py -x`; `python -m pytest tests/test_formatters.py -x`; `python -m pytest tests/test_cli.py -x`; `python -m pytest tests/test_tokenizer.py -x`; `python -m pytest tests/test_sources_boundary.py -x` |
| Supplementary source regression | `python -m pytest tests/test_sources.py -x` |
| Full suite | `python -m pytest` — existing CI command; no browser dependency at normal pytest collection |
| Browser run | **Proposed, not executed:** `python tools/verify_wordfreq_html.py --role builder --output-dir .planning/argonauts/r-50053edc/builder` and independently `python tools/verify_wordfreq_html.py --role quality --output-dir .planning/argonauts/r-50053edc/quality`; CLI/options are local design recommendations, require real file first |
| Collector predicate tests | **Proposed, not executed:** `python -m pytest tests/test_html_verifier.py -x`; create before use |

[VERIFIED: tests/test_aggregator.py, tests/test_formatters.py, tests/test_cli.py, tests/test_tokenizer.py, tests/test_sources_boundary.py, tests/test_sources.py read this session; .github/workflows/pytest.yml:18; pyproject.toml:1-14; parent prior_verify_commands]. No durations/pass counts are invented; measure at execution. Do not promise sub-30-second runtime without a real run.

### Phase Requirements → Test Map

| Req ID | Behavior | Type | Command / evidence | File exists now? |
|---|---|---|---|---|
| REQ-09 | Single document, semantic3columns, no executable/communication markup, UTF-8 actual bytes | Formatter unit + CLI subprocess + browser observation | `python -m pytest tests/test_formatters.py -x`; `python -m pytest tests/test_cli.py -x`; subsequent collector + independent review | Existing pytest files YES; HTML cases NEW; collector NO |
| REQ-10 | Basename-only/privacy, pre-top total6/7/0/200, above-table position, top limits | CLI subprocess + browser geometry | `python -m pytest tests/test_cli.py -x`; collector metadata geometry | File YES; assertions NEW; collector NO |
| REQ-11 | First normalized occurrence, repeated tokens, unequal frequencies, slicing, same order all formats | Unit + CLI integration | `python -m pytest tests/test_aggregator.py -x`; `python -m pytest tests/test_cli.py -x` | YES; lexical expectations require replacement |
| REQ-12 | UI exact fixtures, both widths, full wrapping/whitespace, ranks, raw Range and clipping/nonoverlap/readability | Browser + predicate unit + independent image review | Proposed collector real-file commands; `python -m pytest tests/test_html_verifier.py -x` after creation | NO; no screenshot/HTML acceptance claimed |
| REQ-13 | Escaping, valid hostile basename, Unicode/casefold/boundary, errors/empty/text-json unchanged | Formatter unit + CLI subprocess + source/tokenizer regression | All five preserved quick commands, plus `python -m pytest tests/test_sources.py -x` | YES; HTML/PermissionError coverage NEW |
| REQ-14 | Independently regenerated head-specific evidence, failed attempts, all images viewed, AC index, unchanged scope | Real-file collector + manifest tests + quality review | Full pytest; independent quality collector; actual full-image viewing and AC verdict record | Collector/manifest tests NEW; independent execution NOT DONE |

REQ-12/14 cannot be fully discharged by pytest alone. Screenshot readability/all-image viewing is an explicit reviewer step; keep it pending in the evidence index until actual viewing is recorded. Do not silently replace it with screenshot existence, OCR, textContent, or automated geometry. [VERIFIED: 03-UI-SPEC.md:140,165-183]

### Existing test gaps and real-file sequencing

1. Existing aggregator and CLI tests assert lexical order; update those expectations alongside the shared aggregator change and new order tests. Earlier PLAN coverage must not invoke later HTML-only tests/collector before they exist. [VERIFIED: tests/test_aggregator.py:17-33; tests/test_cli.py:22-60; 03-CONTEXT.md:25]
2. Extend existing formatter tests with a standard-library HTMLParser-based document model. Assert exact header/caption/metadata/row shapes; expected dynamic text roundtrip; empty tbody0; no data-derived attributes. Prefer a fixed allowed-tag/attribute set plus style checks rejecting url/@import/events/meta-refresh/resource/navigation elements. This is test-tool design, not a replacement renderer/parser dependency. [CITED: https://docs.python.org/3.12/library/html.html; VERIFIED: approved tasks.md:7-9; 03-UI-SPEC.md:181]
3. Extend subprocess helper for HTML **raw bytes** rather than relying only on existing `text=True`: save stdout byte-for-byte, strict UTF-8 decode, parse and compare normalized output/metadata; assert stderr/exit separately. Preserve existing text/json newline tests. Include repeated seed runs inside real pytest/verification files with explicit PYTHONHASHSEED values and byte comparisons, not shell inline code. [VERIFIED: tests/test_cli.py:15-19,54-60,137-149; 03-UI-SPEC.md:163,178]
4. Permission errors are not explicitly covered by current tests: unopenable path is a directory, not EACCES. Add deterministic FileSource PermissionError unit test using monkeypatch and an in-process CLI exception-to-exit assertion, plus real subprocess filesystem permission denial on a user/environment where denial is effective. Restore mode in test cleanup. Privileged/root execution must not skip-to-pass or claim chmod denial occurred; report unverified real permission case or run under an available unprivileged user. Missing/decode/directory errors remain subprocess-tested for HTML. [VERIFIED: tests/test_sources.py:21-52; tests/test_cli.py:63-134; wordfreq/sources.py:17-22; 03-CONTEXT.md:26]
5. Create collector, geometry JS, verifier predicate tests and verification guide in the same or preceding task as their verification commands. Normal pytest must not import Playwright globally or require browser install; environment-only browser verification is a separate command with fail-fast prerequisites. Do not modify CI to run it. [VERIFIED: .github/workflows/pytest.yml:17-18; 03-CONTEXT.md:23-25; 03-UI-SPEC.md:132,183]

### Browser collector design (required responsibilities)

**Regeneration / provenance:** Record starting HEAD, git status and product diff (including untracked product files), executable/cwd, argv as an array, input original bytes/path with escaped control-character representation, expected values, actual exit/stderr, stdout raw bytes saved as HTML. Use UTF-8 for child stdout generation in the verification environment and record that environment; strict decoding must still check real saved bytes. Reject dirty product code as evidence of a committed target HEAD. Planning-only changes can be listed separately, not falsely described as a clean tree. Use separate fresh Builder/quality roots and regenerate from source inputs each run. Re-resolve HEAD before final verdict. [VERIFIED: 03-UI-SPEC.md:176-183; docs/solutions/workflow-issues/ci-dependent-requirement-evidence-types-and-head-recheck.md:31-37]

**Observation before navigation:** Launch system Chromium explicitly, establish new context, subscribe context request/response/requestfailed/requestfinished before opening target, attach Chromium CDP Network/Page observation before file navigation. Preserve requestWillBeSent initiator/documentURL/frame/request IDs, loading failures and outcome; track frame navigation, popups/new targets and redirect chains, including attempted navigation before commitment. Context-wide handlers cover other pages; do not rely only on the original page's successful response events. New popup early-event/target timing requires a browser/target-level observer or equivalent verified mechanism; if attribution/coverage is incomplete mark unverified. Keep initial file document navigation in record as local expected load. Observe through geometry/screenshots and the declared image-review interval; record when listeners start/end, do not close early and claim later review was observed. The collector should support a genuine review window or document when all viewed images were assessed during that window. Do not approve network safety from offline/route-abort counts. [VERIFIED: 03-UI-SPEC.md:179-183; /home/Yuki/.local/lib/python3.12/site-packages/playwright/sync_api/_generated.py:13709-13748,15292-15310]. [CITED: https://playwright.dev/python/docs/network; https://playwright.dev/python/docs/api/class-browsercontext; https://chromedevtools.github.io/devtools-protocol/tot/Network/#event-requestWillBeSent]

**Read-only DOM geometry from file:** Load verifier-owned JS from `tools/wordfreq_html_geometry.js` through the automation API, not command-line inline code and not a script inserted into generated HTML. Collect DOM text/codepoints, UTF-16 offsets and per-codepoint associations (so future surrogate pairs are not silently lost), full text Ranges plus per-character getClientRects, empty arrays retained, original float coordinates unchanged. Record element getBoundingClientRect/getClientRects for main/h1/labels/values/caption/tr/th/td, viewport/document scroll metrics, every ancestor's boxes and computed overflow-x/y, borders/padding sufficient to derive clipping edges, relevant computed styles and actual used font information (Chromium font inspection where needed). Save raw and derived judgments separately, with explicit scroll offsets/coordinate space. [VERIFIED: 03-UI-SPEC.md:138,160-172]. [CITED: https://developer.mozilla.org/en-US/docs/Web/API/Range/getClientRects]

**Predicates:** Fail for page horizontal overflow, visible character outside viewport/appropriate column, clipping-ancestor loss, adjacent-column/previous-next-row/meta-table content overlap, missing glyph/data, unwrapped long nonspace run, wrong basename whitespace positions or computed break-spaces/tab-size. Derive clip box from actual ancestor content/padding geometry rather than assuming its outer border rectangle is the clip edge. Do not require strict own-element vertical containment; keep any such overhang in raw evidence and evaluate clip/nonoverlap/image readability. Never clamp/round/drop inconvenient raw rectangles. Synthetic predicate tests should demonstrate detection of horizontal overflow, clip, overlap, missed measurements and outside-own-height-but-valid content. [VERIFIED: 03-UI-SPEC.md:160-172; approved tasks.md:13-14]

**Screenshots / quality review:** Save full-page images at both sizes for empty, normal/top, long and injection matrix (also retain frequency/default/oversized/tie results per fixture expectations). If full image cannot be read at once, generate overlapping tiles covering all coordinates and keep an index of coverage. Every image must be actually opened/viewed with readable size and a recorded verdict, including all tiles. Independent quality decides readability, not a Boolean prefilled by the collector. If an image-viewing tool is unavailable, keep AC4/AC6 unverified; do not fabricate viewing logs. [VERIFIED: 03-UI-SPEC.md:140,176-183]

**Fail-closed evidence schema:** Each case-width record needs input/argv/cwd, head/role, exit/stdout/stderr, expectation, generated HTML, browser binary/version/OS/fonts/viewport/DPR, raw geometry, screenshot list + coverage + reviewed-image references, all network events + observation interval + attribution, static audit, computed predicates and AC mapping. Keep execution failure, detected product defect and pending manual review distinct. Collector execution failure/product assertion must exit nonzero, with case/selector/character index/expected/actual/artifact path. Capture completion alone is not acceptance: explicit pending-review status must block final verdict; a final evidence-check operation must reject missing reviews, cases, ranges, network interval, target-head match or artifacts. Do not allow empty manifests, missing browser or all-skipped loops to return a success verdict. These are proposed verifier contracts derived from [VERIFIED: 03-CONTEXT.md:21-26; 03-UI-SPEC.md:176-183].

### Sampling Rate / Phase Gate

- Per ranking task: preserved aggregator and CLI commands against real files; no HTML dependency until added.
- Per formatter/integration task: formatter + CLI commands, followed by tokenizer/source-boundary (and sources) regressions; execute at task completion.
- Per collector task: its new real-file predicate tests, then actual Builder collector with established external environment; do not mark image review automatically.
- Per sequential PLAN completion: `python -m pytest`, retaining all earlier PLAN coverage. Add real browser run once collector exists; no tests referring to later absent artifacts.
- Phase gate: full pytest green **and** independent quality regenerated target-head CLI/HTML for required matrix **and** both browser sizes/raw geometry/network/static safety evidence **and** every image viewed **and** AC1–AC6 evidence index complete. Recheck head/diff, unchanged CI/dependencies/scope. No acceptance if any required condition unexecuted.

[VERIFIED: 03-CONTEXT.md:24-26; approved tasks.md:16-19; 03-UI-SPEC.md:176-183]

### Wave 0 Gaps (for parent VALIDATION.md)

- [ ] Resolve/record working CPython3.12 + existing pytest environment without changing project dependencies; current default commands fail package discovery.
- [ ] Add HTML cases to existing formatter/CLI suites and first-occurrence tests; update current lexical expectations and current glossary/help.
- [ ] Add explicit permission-denial coverage and real-byte UTF-8 assertions; preserve existing error/text/json/source/tokenizer tests.
- [ ] Create proposed `tools/verify_wordfreq_html.py`, `tools/wordfreq_html_geometry.js`, `tests/test_html_verifier.py`, `docs/wordfreq-html-verification.md` before use; file paths/options remain proposals until Builder creates them.
- [ ] Fix exact UI-SPEC fixture construction in real verification code; no manually substituted filenames/shorter words.
- [ ] Actually launch Chromium through available local tooling; record fonts/version/viewport/DPR; verify failed-attempt/navigation observation capability with isolated negative cases.
- [ ] Establish actual image-viewing capability and independent quality review ledger; screenshot capture alone is insufficient.
- [ ] Parent writes VALIDATION.md from this architecture; this research does not create it or approve product evidence.

## Security Domain

Security enforcement is enabled at configured ASVS level1; each PLAN must contain a threat_model, per existing pre-hook. Relevant controls are output encoding, privacy and no executable/network surfaces, not a web authentication system. [VERIFIED: .planning/config.json:49-51; .planning/argonauts/t_bd1bf85e/plan-pre-hooks.json:117-131]

| ASVS category | Applicability in this static CLI | Standard control / test |
|---|---|---|
| V2 Authentication | Not introduced | No accounts/login/backend |
| V3 Session Management | Not introduced | No sessions/cookies/product storage |
| V4 Access Control | No new authorization layer | Keep OS file permissions and source error contract; no server |
| V5 Input validation/output encoding | Applies | Existing argparse positive top/choices, Unicode tokenizer preserved, html.escape text nodes, direct injection tests |
| V6 Cryptography | Not introduced | No crypto functionality or invented schemes |

This is a scoped applicability map, not a claim of ASVS certification. Source boundaries and scope: [VERIFIED: wordfreq/__main__.py:11-28; wordfreq/sources.py:17-22; approved design.md:6-16; 03-CONTEXT.md:23].

| Threat | STRIDE lens | Required mitigation / failure signal |
|---|---|---|
| Word/basename markup injection | Tampering / elevation | Standard escaping + fixed markup, parser roundtrip/extra-node rejection + browser event checks |
| Input directory disclosure | Information disclosure | Basename-only CLI seam; fixed title; full-document raw/escaped parent-marker audit |
| External exfiltration attempts | Information disclosure | No script/resource/navigation/CSS URLs; pre-open failed/success/navigation capture; attempts fail regardless of outcome |
| Wrong-head/missing evidence presented as pass | Repudiation / integrity | Independent generation, exact head/status/diff/argv/artifacts/AC and review index; fail closed |

[VERIFIED: approved design.md:12-25; 03-UI-SPEC.md:176-183]

## Runtime State Inventory (local order-contract change)

This phase changes a pure ranking function and adds an output format, not deployment identifiers or persistent schemas. Scope-limited inventory, not a host-wide claim: stored product data — no persistent datastore in the read four-component pipeline; live service config — no service in approved product scope; OS registrations — none required by approved changes; secrets/env keys — none renamed (verification-only environment/PYTHONHASHSEED is recorded, not product migration); build artifacts — no package rename/install/migration planned, runtime package remains `name = "wordfreq"`, version `"0.1.0"`. All actions are code/tests/docs and freshly regenerated evidence; historical HTML/results must not be relabeled as fresh output. [VERIFIED: wordfreq/sources.py:13-22; wordfreq/aggregator.py:6-13; wordfreq/formatters.py:1-13; wordfreq/__main__.py:19-32; pyproject.toml:5-14; approved design.md:27-28]

## State of the Art / Compatibility

The relevant change is an approved local contract migration: lexical ties → normalized first-occurrence ties for all formats, without a compatibility flag. This is not a framework modernization. Old source/learning examples advocating lexical ties remain historical references and must not override the new phase. Maintain current glossary/help while preserving completed Phase 1 evidence. [VERIFIED: approved spec.md:47-56; approved design.md:21,27-28; CONCEPTS.md:45-47; 03-CONTEXT.md:7,17]

## Assumptions Log

No unconfirmed product decision is used to expand scope. Newly proposed tool filenames/options/manifest fields above are implementation recommendations under delegated naming discretion, explicitly not claims of existing files. Browser/runtime compatibility, actual used fonts, complete network-observation coverage, geometry, image-view capability and test pass results are **unverified execution obligations**, not assumed passing facts. [VERIFIED: 03-CONTEXT.md:28-29; 03-UI-SPEC.md:136-140,183]

## Open Questions / Execution Risks

1. **Tool environment:** Default Python cannot see pytest/Playwright. Existing scoped discovery works; Builder must use/record a working environment and real-file execution before declaring tests run. No dependency addition is authorized.
2. **Browser protocol and observation coverage:** System Chromium156 vs discovered Python Playwright1.60.0 has not been launched together here. Popup/attempt provenance and fonts must be demonstrated, not assumed. If unavailable, mark browser acceptance unverified and return a concrete environmental blocker rather than substitute another viewport/browser or cached images.
3. **Image review coordination:** Collector must keep network observation active through the actual agreed review interval. A capture script exiting before an independent reviewer views images cannot truthfully claim observation through that later review. Define the real-file workflow/hold/finalization boundary before implementation.
4. **Permission fixture:** Effective UID/permissions at execution must genuinely deny a read for real CLI evidence. Deterministic mocked PermissionError tests cover mapping but cannot masquerade as real denied access.

These are execution mechanics within locked scope, not product questions for the absent user. Parent can create PLAN/VALIDATION with explicit gates and fails_when now. [VERIFIED: observed environment results; 03-CONTEXT.md:21-29; 03-UI-SPEC.md:176-183]

## Sources and Confidence

### Primary repository sources (opened this session)

- `03-CONTEXT.md`: approved scope and verbatim decisions; `03-UI-SPEC.md`: approved structure/CSS/exact fixtures/browser/evidence contract; `.planning/REQUIREMENTS.md:32-50`: REQ-09..14; `.planning/STATE.md` and `.planning/config.json`: history/settings.
- `openspec/changes/r-50053edc-wordfreq-html/{proposal,design,tasks}.md` and `specs/wordfreq-cli/spec.md`; same-request BMAD Brief/PRD and `.planning/argonauts/r-50053edc-prd.md`: approved feature/compatibility/task grounding.
- `wordfreq/{aggregator,formatters,__main__,sources,tokenizer}.py`, six existing `tests/test_*.py` modules, `pyproject.toml`, `.github/workflows/pytest.yml`, README/CONCEPTS: actual code/tests and declaration facts. File paths in NEW target rows are proposals, not verified pre-existing files.
- `.planning/argonauts/r-50053edc-learnings.md` and its three referenced solution articles: boundary preservation, isolated failure-discrimination, head/evidence attribution. Lexical sort advice explicitly superseded here.

### Official API references retrieved this session

- https://docs.python.org/3.12/library/html.html — escape with quote option; https://docs.python.org/3.12/library/os.path.html#os.path.basename — host path semantics.
- https://docs.python.org/3/library/collections.html#collections.Counter — remembered insertion order since3.7; https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts — stable sort. Generic `/3` docs currently link development source; use the stated longstanding guarantees, not an inferred new runtime version requirement.
- https://playwright.dev/python/docs/network and https://playwright.dev/python/docs/api/class-browsercontext — network observation/isolated context. Existing local Playwright generated API was read at :13709-13748 and :15292-15310 for actual event literals and Chromium CDP support.
- https://chromedevtools.github.io/devtools-protocol/tot/Network/#event-requestWillBeSent — initiator/documentURL/request metadata. Tip-of-tree API is reference only; execution must verify the installed Chromium's supported method/events.
- https://developer.mozilla.org/en-US/docs/Web/API/Range/getClientRects; https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/white-space; https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/overflow-wrap — real fragments and whitespace/long-word handling. Overflow-wrap extraction exposed last-modified 2026-07-21; no publication dates were fabricated for other pages.

### Research method / confidence limits

Official research-plan seam produced four documentation questions with provider `jina`; no Jina/Context7 tool or ctx7 command was exposed, so direct official-page extraction was used rather than installing a search client. Official classify-confidence for `webfetch --verified` returned **LOW**, retained in research-cache entries; no retrieved claim is upgraded to an empirical browser/test guarantee. API claims are explicitly CITED, local code facts VERIFIED with read line ranges, proposed implementation choices labeled as recommendations. The provenance/tier distinction prevents verified file reads and official prose from being misreported as executed acceptance. Version-command success is only module discovery, not a passing browser launch.

**Metadata:** Research date 2026-11-17; stable local design valid until scope/code/UI changes, environment facts recheck at execution. No commits/push, product implementation, test execution or browser acceptance performed by this research.
