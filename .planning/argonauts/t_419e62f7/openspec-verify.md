## Verification Report: r-e476c11d-wordfreq-min-count

Using change: r-e476c11d-wordfreq-min-count (override: `openspec-verify-change <other>`).
Verifier: argonauts-uat-quality, kanban t_419e62f7 run 156. Target head: `afaa56fc022c895ee2243b8f67a239c7c0096086` (origin/argonauts/r-e476c11d = PR ToR-O3/argonauts-uat-20261114-public#8 headRefOid, OPEN, draft).
Inputs: `openspec status --change r-e476c11d-wordfreq-min-count --json` (schema spec-driven, proposal/specs/design/tasks done) and `openspec instructions apply --change ... --json` (taskTrackingConfigured true, progress 5/6, unavailableTrackingFiles null). Artifacts read: proposal.md, specs/wordfreq-cli/spec.md, design.md, tasks.md.

### Summary
| Dimension    | Status |
|--------------|--------|
| Completeness | 5/6 tasks (2.2 unchecked); 3 ADDED + 3 MODIFIED requirements, 6/6 found in code |
| Correctness  | 6/6 reqs covered; 17/17 scenarios covered by tests and quality-run CLI/browser evidence |
| Coherence    | Design decisions 1-4 followed; no pattern deviation in product code |

### Completeness
- Task Completion: 5/6. Incomplete: **2.2** (quality re-run CLI/HTML at verification head, view 1280x900 / 320x900 DPR1, attach evidence, match AC1/2/4/5/6/7, record filter->top source).
  - Quality technical part of 2.2 is now done at head afaa56f (see Correctness evidence): fresh root `.planning/argonauts/r-e476c11d/quality/final-01`, manifest verdict `accepted`, independent_acceptance `true`, AC1-AC7 `accepted`, errors `[]`, all 110 current + 32 baseline images viewed by quality, source_order lines 34/35/36/37/38/44 attested.
  - Not done by this card and kept open: PM reading of the delivered originals (separate gate, runbook §5.3), and the checkbox itself (quality does not edit openspec/; marking/sync/archive belong to the finalization Builder).
- Spec Coverage: all requirements implemented.
  - ADDED 最小出現回数オプション (MC-1): `wordfreq/__main__.py:17` (`--min-count`, type=int, default=1), `:27-28` (>=1 check before input read at `:30`), `:36-38` (filter then `top_words`).
  - ADDED 空結果と既定互換 (MC-2): empty pairs flow to unchanged formatters; total from `:35`.
  - ADDED 試験と独立確認 (MC-3): `tests/test_cli.py` min_count tests (12 `min_count` references) inside the full suite 694/694 pass exit 0; `openspec validate r-e476c11d-wordfreq-min-count --strict`: valid; quality browser evidence final-01.
  - MODIFIED 表示件数 (FR-2), 出力の順序決定論性 (FR-4/D-2), HTMLの入力情報と総出現回数 (HTML-2): `:36-38`, `:44`, `wordfreq/aggregator.py` `top_words` stable sort unchanged.
- REMOVED / RENAMED: none.

### Correctness (scenario -> evidence, all at head afaa56f)
| Scenario | Evidence |
|---|---|
| 下限未満と境界値と超過 (beta min2) | final-01 beta-text/json/html: beta3, alpha2; HTML viewed 1280/320 |
| topとの順序と独立値 (zoo) | zoo-top-* and zoo-reverse-* identical: zoo2 only; zoo-* min2: zoo2, apple2 |
| Unicode正規化してから閾値 | unicode-*: strasse 2 |
| 引数エラーは形式と入力読込みに優先 | quality CLI log `.planning/argonauts/t_419e62f7/run156/ac3-cli.txt`: 0, -1, 1.5, abc, missing x text/json/html -> exit 2, stdout 0 bytes, usage on stderr, nonexistent input never reported; `test_min_count_invalid_before_read` |
| 有効な閾値でも入力失敗は失敗 | same log: --min-count 2 with nonexistent file / directory -> exit 1, stdout empty |
| 未指定と1と従来の出力 | 24 baseline comparisons all bytes/raw/browser/images equal (manifest.comparisons); baseline images viewed |
| 語のある入力で全件除外 (zoo min3) | zoo-none-*: text empty, json `[]`+LF, HTML 0 rows, total 5 |
| 抽出語0件 | empty/whitespace/punctuation min2: empty in all formats, HTML total 0 |
| 試験と実画像の証拠 | suite.json (694 collected, exit 0), CLI argv/stdout/stderr/exit sidecars, images + reviews.json ledger |
| 内部順序と範囲の確認 | reviews.json source_order (sha256 ab897f88...); scope.json changed paths outside .planning: README, docs runbook, openspec tasks, tests x2, tools driver, wordfreq/__main__.py; CI pytest success (both runs) at afaa56f, no CI/dependency change |
| 既定は10件 / 件数指定と全件出力 / 不正な件数 | long-default-* (10 rows), long-99-* (12 rows, all kinds), existing top tests in suite |
| 同回数ワードは単語の昇順 (first-occurrence kept) | baseline-* hello3 zoo2 apple2 one2 order; zoo-* zoo before apple |
| 正規化とtop境界 | zoo-top (top1 zoo2), suite top tests |
| topを変えても総数は一定 / 異なる頻度の入力とtop / top既定と不正値 | HTML total 7 / 5 / 200 constant across min/top variants in viewed images; suite |
| 閾値とtopの両方で表示を絞る | beta-top-html: 1 row total 7; beta-none-html: 0 rows total 7 |

### Coherence
- Design Adherence: Decision 1 (argparse int + >=1 before read) `:17,:27-28`; Decision 2 (separate filtered Counter, original counts/total kept, existing `top_words`) `:34-38`; Decision 3 (formatters unchanged; no diff in formatters/CSS) confirmed by scope; Decision 4 (baseline before change, TDD, quality independent re-generation + source lines) confirmed by baseline index d3177989..., 04-02 RED/GREEN, final-01.
- Code Pattern Consistency: product change follows existing argparse/`parser.error` pattern. Phase code review (04-REVIEW.md): 0 critical, 2 warning, 4 info, all in verification code.

### Issues by Priority
1. CRITICAL
   - Incomplete task 2.2 (checkbox unchecked). Quality technical evidence now exists at afaa56f (final-01 accepted). Recommendation: after the PM reads the delivered originals, the finalization Builder marks 2.2 with the evidence reference before archive. Not fixable by quality (no openspec edits).
2. WARNING
   - none in implementation. (Code-review WR-01/WR-02 concern verification tests, recorded in 04-REVIEW.md.)
3. SUGGESTION
   - none.

### Final Assessment
1 critical issue(s) found. Fix before archiving (task 2.2 checkbox; its quality technical part is satisfied at afaa56f, the PM-reading gate is still pending). No check was skipped.

### Separate gates (not claimed here)
- PM reading of delivered originals: not performed (PM card).
- Final quality mark `argonauts/quality`, sync/archive, PR ready, merge: later stages.
- Any later head (including the .planning-only report commit of this card) needs the runbook §6 fresh-root re-run at final confirmation.
