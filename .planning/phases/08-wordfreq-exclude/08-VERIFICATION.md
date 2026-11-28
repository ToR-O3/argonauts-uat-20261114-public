---
phase: 08-wordfreq-exclude
verified: 2026-11-28T18:49:53Z
status: passed
score: 38/44 must-haves verified
covered_files:
  - .planning/phases/08-wordfreq-exclude/08-01-PLAN.md
  - .planning/phases/08-wordfreq-exclude/08-01-SUMMARY.md
  - .planning/phases/08-wordfreq-exclude/08-02-PLAN.md
  - .planning/phases/08-wordfreq-exclude/08-02-SUMMARY.md
  - .planning/phases/08-wordfreq-exclude/08-03-PLAN.md
  - .planning/phases/08-wordfreq-exclude/08-03-SUMMARY.md
  - README.md
  - tests/fixtures/README.md
  - tests/fixtures/exclude-baseline-git-objects.json
  - tests/test_cli.py
  - wordfreq/__main__.py
  - wordfreq/exclusions.py
covered_digest: "v4:sha256:c5b071f9d84790f78ed3e38785c4537ab1e51d547abf3584803795b5802c4699"
behavior_unverified: 0
overrides_applied: 0
decision_coverage:
  honored: 11
  total: 11
  not_honored: []
insufficient_spec_items:
  - truth: "REQ-28/concurrency (08-01, verification: backstop)"
    reason: insufficient_spec
  - truth: "REQ-30/concurrency (08-02, verification: backstop)"
    reason: insufficient_spec
  - truth: "REQ-31/concurrency (08-03, verification: backstop)"
    reason: insufficient_spec
  - truth: "REQ-32/concurrency (08-03, verification: backstop)"
    reason: insufficient_spec
  - truth: "REQ-33/concurrency (08-03, verification: backstop)"
    reason: insufficient_spec
flagged_prohibitions:
  - id: P-08-01
    disposition: unverified
    flagged: true
    llm_judgment: "non-authoritative: 自動の除外辞書・推定除外は見当たらない（excluded は空集合か parse_exclusions の結果のみ）"
  - id: P-08-02
    disposition: unverified
    flagged: true
    llm_judgment: "non-authoritative: 本報告は Builder 結果を独立受入として扱わず、品質の対象head実行原本と本検証の独自実行に基づく"
human_verification:
  - test: "5件の並行・中断 backstop（REQ-28/30/31/32/33 concurrency）について、単発ローカルCLIに新しい中断・並列・原子的出力の保証を求めないことをPMが確認する（必要なら held-out 試験を追加）"
    expected: "保証を追加しない方針が承認される。保証が必要なら別の要求として起票される"
    why_human: "verification: backstop（非推論）。仕様に根拠がなく、明示的な証拠もないため検証者は判定を保留する（reason: insufficient_spec）"
  - test: "P-08-01（自動ストップワード・推定除外の禁止）を人が確認する"
    expected: "--exclude FILE に書いた語だけが除外され、他の語は暗黙に除外されない"
    why_human: "descriptor-less の禁止事項。自律モードでは非権威的な判断と flag のみ記録し、黙って合格にしない"
  - test: "P-08-02（Builder結果・履歴・未実行probe・未閲覧画像を独立受入として示すことの禁止）を人が確認する"
    expected: "受入の根拠が品質の対象head f3747b7 での独立実行原本と本 VERIFICATION.md に限られる"
    why_human: "descriptor-less の禁止事項。証拠の所有と透明性はコードから判定できない"
  - test: "日本語フォントのある環境で --format html の出力（通常・全件除外）をブラウザで開く"
    expected: "見出し・ラベル・caption・列見出し・空文言の日本語が読める。はみ出し・重なりがない"
    why_human: "08-UI-REVIEW で閲覧した画像2枚では、監査ホストにCJKフォントがなく日本語が表示されなかった。glyph の可読性は未確認（formatters.py は不変で、表示の変更は範囲外）"
  - test: "SC4: 親が本 VERIFICATION.md と .planning/argonauts/r-e0a2598f/quality/ のCLI文字原本を、PMが read_file できるパスで標準配布したことを確認する"
    expected: "PMは画像や圧縮ファイルを開かずに、各条件の文字原本を読める"
    why_human: "配布は本検証の後に親が行う工程で、コードベースからは確かめられない"
---

# Phase 8: wordfreq exclude 検証報告

**Phase Goal:** 承認済み--exclude FILEを全形式へ追加し、Unicode行検証・除外先行の失敗処理・元HTML総数・未指定互換を試験と独立品質の文字証拠で確かめられる。
**Verified:** 2026-11-28T18:49:53Z（JST 2026-11-29）。対象 HEAD は `f3747b7e6235775b3c21fa13201d7921be77306c`。
**Status:** human_needed
**Re-verification:** No（初回の検証）

## 結論

製品の実装と試験で、目標は達成されています。gap はありません。
`passed` にしない理由は次の3つです。

- backstop の5件は判定を保留します（insufficient_spec）。
- 禁止事項の2件は flag 付きの未検証として残します。
- 日本語 glyph の見た目と、SC4 の配布確認は人の確認が必要です。

## Goal Achievement

### Observable Truths

ROADMAP の SC 4件と、PLAN の must_haves.truths 40件（01が9件、02が20件、03が11件）を合わせた44件です。

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| SC1 | 全3形式で、指定語の除外→min-count→安定した初出順→top の順に処理し、HTMLは元の総数を出す | ✓ VERIFIED | `__main__.py:50-52` の `selected_counts` が除外と min-count を一緒にかけ、その後 `top_words` を呼ぶ。`total=sum(counts.values())` は除外前の値。本検証で実行: `b.txt --exclude z.txt --min-count 2 --top 1` → `2\tapple` exit0、HTML は `<td>apple</td><td>2</td>` と `total-value 5` |
| SC2 | trim・改行・Unicode fullmatch の後の casefold、全不正例、読込み失敗の exit2・元の行番号・空stdout・本文取得0回、引数検査が先、本文は exit1 | ✓ VERIFIED | `exclusions.py:16-22`。`-k exclude` の 457件が通過（grammar 61、failures/precedence 117）。本検証で実行: line4 不正 → `l4.txt: line 4: expected one Unicode word` exit2。`--exclude` に値がない → exit2 |
| SC3 | help と README の実行例、79d83ba との未指定時のバイト互換、既存試験の全件、入力不変、範囲外の変更なし | ✓ VERIFIED | `test_exclude_baseline_exact_git_bytes` 64件が通過（Git オブジェクトをハッシュの連鎖で認証）。全体 1159 passed（品質の原本）。`git diff origin/v112-a...HEAD -- formatters/aggregator/tokenizer/sources/pyproject/.github` → 空。品質の入力 sha256 は実行の前後で同じ |
| SC4 | 品質が対象headで独立に実行し、VERIFICATION.md と CLI などの文字原本を添付する。画像を確認した場合は枚数・内容・結果を書く | ? UNCERTAIN（human） | 独立実行: `quality/head-before.txt`=f3747b7、`regression-gate.txt` は 1159 passed、`cli-log.txt` に実CLI 60件超と base 比較。画像: 08-UI-REVIEW に「images actually viewed: 2」と内容・結果がある。PM への添付と配布は親の工程なので未確認 |
| 1 | REQ-28/boundary: 除外は min-count と top より先。zoo を除外し min-count2/top1 → apple2、総数5 | ✓ VERIFIED | `test_exclude_selection_matrix`（150件）と本検証の実行 |
| 2 | REQ-28/adjacency: 同数でも別の語は統合しない。同数は正規化後の初出順 | ✓ VERIFIED | `test_exclude_selection_ties_permutations_seeds`。CLI log `E-tie-ex` → b,a,c,d |
| 3 | REQ-28/empty: 空の本文は総数0、1語は1行、全件除外は0行で元の正の総数、text は空、JSON は `[]`+LF | ✓ VERIFIED | `test_exclude_empty_results`（15件）。CLI log `E-all-*`、`E-emptybody-ex-html` |
| 4 | REQ-28/encoding: 既存の抽出と casefold を使う。STRASSE は Straße/STRASSE を両方除外する | ✓ VERIFIED | 本検証で実行: `s.txt --exclude x.txt(STRASSE\r\n)` → `[{"word": "keep", "count": 1}]` |
| 5 | REQ-28/ordering: 全形式が同じ pairs を受け取る。除外の重複や並びで順位は変わらない | ✓ VERIFIED | `test_exclude_selection_preserves_full_counter_and_shared_pairs`（pairs の identity を spy で確認）。`test_exclude_grammar_permutations_and_hashseeds`（seed 0/1/42） |
| 6 | REQ-28/precision: 整数の回数と元の総和が正確。平均・浮動小数・字句順の tie-break を入れない | ✓ VERIFIED | `__main__.py` の差分は membership 条件の1行だけ。Counter 非変更の spy が通過 |
| 7 | REQ-28/concurrency（backstop） | ⚠️ insufficient_spec | 明示的な証拠なし。判定を保留して人に回す |
| 8 | REQ-29/empty: 空・空白だけ・コメントだけは no-op。1行で除外できる。FILE 値がなければ引数エラー | ✓ VERIFIED | `test_exclude_grammar_noop`、`test_exclude_empty_noop_exact_bytes`（未指定時とバイト一致）。`--exclude` の値なし → exit2 |
| 9 | REQ-29/encoding: LF/CRLF/最終改行なし、trim、#、casefold 前に元の語を検証、数字・_・非ASCII・U+0130 を受理、不正6種を元の行番号で拒否 | ✓ VERIFIED | `test_exclude_grammar_original_before_casefold`（open を禁止した純粋な関数で `İ`→`i\u0307`）。`test_exclude_grammar_invalid_original_row`（6種×3形式、BOM は line1） |
| 10 | REQ-30/boundary: top/min-count の0・負・非整数・値なしは両方の読込みより前に失敗。値なしの --exclude は exit2 | ✓ VERIFIED | `test_exclude_precedence_argv_before_both_reads`（42件）。CLI log `AC4-badtop/badmin-before-ex` |
| 11 | REQ-30/adjacency: 除外と本文が同時に失敗したら除外側の診断で exit2、本文読込み0回。除外が有効なら本文失敗は exit1 | ✓ VERIFIED | `test_exclude_precedence_failed_exclusion_never_reads_body`（spy は本文の read で assert）。`test_exclude_failures_role_mapping` は 45件 |
| 12 | REQ-30/empty: 有効な空・コメントだけの除外も本文より先。missing は no-op にしない | ✓ VERIFIED | `test_exclude_precedence_success_order`。CLI log `AC4-missing` は exit2 |
| 13 | REQ-30/ordering: argv 検査 → 除外の取得と全行検証 → 本文。blank/comment/valid/invalid の順で line4 | ✓ VERIFIED | 上記の spy 試験。品質の FIFO probe では、不正な除外は即 exit2、有効な除外は本文 FIFO で待つ（124） |
| 14 | REQ-30/precision: 行番号は無視行も数える1始まり。除外は exit2、本文は exit1 | ✓ VERIFIED | `exclusions.py:16` の `enumerate(..., 1)` は ignore より前。試験で line 4 を確認 |
| 15 | REQ-30/concurrency（backstop） | ⚠️ insufficient_spec | 明示的な証拠なし |
| 16-29 | UI-E1..E4 の14状態（overflow/long-text/empty/loading/partial/error/populated/zero-one-many） | ✓ VERIFIED（14件） | `test_exclude_ui_static_presentation`、`test_exclude_empty_results`、`formatters.py` は不変（差分なし）。08-UI-REVIEW の 14/14 は、HeadlessChrome 1280/320 DPR1 の DOM 計測 18 render と画像2枚の閲覧（直接観測）。E1/E4 の日本語 glyph の可読性は human 項目へ |
| 30 | REQ-31/concurrency（backstop） | ⚠️ insufficient_spec | README に「中断や並列実行について新しい保証は追加しません」とある。保証の有無の判断は人に回す |
| 31 | REQ-32/boundary: 逆字句の同数・Unicode・10語超・top 1/2/99・min-count 1/2・閾値で空になる場合を比較し、既存試験を残す | ✓ VERIFIED | baseline の parametrize（2本文×4形式×8オプション）。差分で test_cli.py の削除は0行 |
| 32 | REQ-32/adjacency: 同じ interpreter・パス・argv・env、別の module root。候補自身を期待値にしない | ✓ VERIFIED | `_exclude_baseline_roots`: PYTHONPATH を除き、historical と candidate を分けて生成 |
| 33 | REQ-32/empty: 空の本文の比較を含む。empty/comment-only/no-match/all-excluded を区別する | ✓ VERIFIED | baseline の `empty` id、`test_exclude_empty_*` |
| 34 | REQ-32/encoding: 79d83ba と raw stdout バイトを比較し、入力はバイト不変 | ✓ VERIFIED | `after.stdout == before.stdout` と `path.read_bytes()==original` |
| 35 | REQ-32/ordering: 固定版に逆字句の同数・正規化 Unicode・10語超。handoff は独立品質を後続の義務とする | ✓ VERIFIED | `check_quality_handoff.py` を本検証で実行 → exit0 `HANDOFF_READY_ONLY`、quality_status pending |
| 36 | REQ-32/precision: 整数・終了状態・バイト単位の比較。報告は実際に取得した値から作る | ✓ VERIFIED | decode せずに bytes を比較。品質 CLI log は od と sha256 |
| 37 | Builder の handoff（manifest/head/原本/義務） | ✓ VERIFIED | checker exit0（target 526b89c、reporting f3747b7、edges 26、UI 14、prohibitions 2） |
| 38 | REQ-32/concurrency（backstop） | ⚠️ insufficient_spec | 明示的な証拠なし |
| 39 | REQ-33/boundary: 既定値・exit・純粋な関数の signature・取得の境界・formatter/CSS は不変。範囲外のファイルなし | ✓ VERIFIED | 製品の差分は6ファイルのみ。`count_words`/`top_words`/`format_*` に変更なし |
| 40 | REQ-33/precision: 整数の Counter、安定した同数順、元の総数、既存出力のバイト | ✓ VERIFIED | baseline 64件と既存の min-count baseline 試験が通過 |
| 41 | REQ-33/concurrency（backstop） | ⚠️ insufficient_spec | 明示的な証拠なし |

**Score:** 38/44 truths verified。present かつ behavior 未検証は0件、insufficient_spec が5件、UNCERTAIN（配布）が1件。
自律モードの完了表示は「complete with 5 unverified non-inferable checks, 2 flagged prohibitions」です。

### 禁止事項（flagged-unverified）

| ID | Statement | Disposition | 非権威的な判断 |
|----|-----------|-------------|----------------|
| P-08-01 | 自動ストップワードや推定除外を黙って適用しない | ⚠️ unverified — human review recommended | 違反は見当たらない。`excluded` は空集合か、ファイルから作った集合だけ |
| P-08-02 | Builder 結果などを独立した exact-head 受入として示さない | ⚠️ unverified — human review recommended | 本報告は独自に実行した結果と品質原本に基づく |

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `wordfreq/exclusions.py` | 純粋で eager な行解釈と行番号付きの例外 | ✓ VERIFIED | 23行。I/O なし（open を禁止した試験が通過）。`__main__` から import して使っている |
| `wordfreq/__main__.py` | 任意の除外取得を本文より先に行う | ✓ VERIFIED | 72行。exit2 と exit1 の範囲を分けている |
| `tests/test_cli.py` | tracer・文法・失敗・選別・baseline・docs | ✓ VERIFIED | 追加 712行。exclude 試験は457件すべて通過。新しい skip なし |
| `README.md` | 実行例と行の契約 | ✓ VERIFIED | `test_exclude_docs_complete_contract_and_literal_example` が README の記載どおりのコマンドを実行する |
| `tests/fixtures/exclude-baseline-git-objects.json` | 79d83ba の生 Git オブジェクト9個 | ✓ VERIFIED | hash-object で認証。改ざん4種の対照が失敗する |
| `.planning/argonauts/r-e0a2598f/{builder-evidence.md, quality-handoff.md/json, check_quality_handoff.py, test_quality_handoff.py}` | Builder の原本と handoff | ✓ VERIFIED | verify.artifacts は 6/6。checker の実行は exit0 |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `__main__.py` | `sources.py` | 本文より先に除外ファイルを `FileSource.read_text` | ✓ WIRED | `from .sources import FileSource, InputError`、35行目。CLI の `verify.key-links` が NOT と出すのは、相対 import にパス文字列が含まれないため |
| `__main__.py` | `exclusions.py` | eager な `parse_exclusions` | ✓ WIRED | 8行目で import、36行目で呼び出し |
| `__main__.py` | `aggregator.py` | 別の Counter を変更されない `top_words` に渡す | ✓ WIRED | 7行目と50-52行目 |
| `tests/test_cli.py` | `sources.py` | open と read_text の注入 | ✓ WIRED | `test_exclude_failures_role_mapping` が `builtins.open` と `FileSource.read_text` を spy する |
| `__main__.py` | `formatters.py` | 同じ pairs と basename/total | ✓ WIRED | 58-62行目。pairs の identity を spy で確認 |
| `tests/test_cli.py` | `__main__.py` | subprocess で baseline と候補を比較 | ✓ WIRED | verify.key-links で verified |
| `check_quality_handoff.py` | `quality-handoff.json` | `--handoff` 引数で検証 | ✓ WIRED | パスを埋め込まず引数で受け取る。実行は exit0 |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `__main__.py` → formatter | `pairs` / `total` | `FileSource(filename)` → `iter_tokens` → `count_words` → 除外と min-count → `top_words` | Yes（本検証の実行で apple2 と総数5） | ✓ FLOWING |
| `__main__.py` | `excluded` | `FileSource(args.exclude)` → `parse_exclusions` | Yes（STRASSE で Straße と STRASSE を除外） | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 除外に関わる全試験 | `uv run --extra dev python -m pytest tests/test_cli.py -q -k exclude` | 457 passed, 358 deselected（19.06s） | ✓ PASS |
| 除外→min-count→top と元の総数 | `python -m wordfreq b.txt --exclude z.txt --min-count 2 --top 1 [--format html]` | `2\tapple` exit0。HTML は row apple/2、total-value 5 | ✓ PASS |
| casefold した除外と CRLF | `s.txt --exclude x.txt(STRASSE\r\n) --format json` | `[{"word": "keep", "count": 1}]` | ✓ PASS |
| 遅れて現れる不正行で本文に行かない | `nobody.txt --exclude l4.txt` | `l4.txt: line 4: ...` exit2（存在しない本文の exit1 ではない） | ✓ PASS |
| --exclude の値なし | `b.txt --exclude` | `expected one argument` exit2 | ✓ PASS |
| handoff の検査 | `python3 .planning/argonauts/r-e0a2598f/check_quality_handoff.py --repo-root . --handoff ...json` | exit0 `HANDOFF_READY_ONLY` | ✓ PASS |
| 全試験（再実行していない） | 品質原本 `quality/pytest-full-stdout.txt`、`regression-gate.txt` | 1159 passed、exit=0（HEAD f3747b7） | ✓ PASS（原本を参照） |

### Probe Execution

Step 7c: 該当なし。PLAN が宣言する `scripts/*/tests/probe-*.sh` はありません。PLAN の検証コマンドのうち handoff checker は、上の Spot-Checks で実行しました。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| REQ-28 | 08-01/02/03 | FR-1、FR-5: 共通の選別、順序、元の総数 | ✓ SATISFIED | truths 1-6、SC1 |
| REQ-29 | 08-01/02/03 | FR-2、FR-3: 行の文法、casefold | ✓ SATISFIED | truths 8-9 |
| REQ-30 | 08-01/02/03 | FR-4: 失敗、優先順位、本文を読まない | ✓ SATISFIED | truths 10-14、SC2 |
| REQ-31 | 08-01/02/03 | FR-6: help と README | ✓ SATISFIED | docs と help の試験、CLI log `AC5-help`（help の文言が短い点は Info） |
| REQ-32 | 08-01/02/03 | FR-7: 網羅的な試験、baseline、非変更、独立品質 | ✓ SATISFIED（配布は human 項目） | truths 31-37、品質原本、本報告 |
| REQ-33 | 08-01/02/03 | RULE-1..4: 境界と範囲 | ✓ SATISFIED | truths 39-40、範囲外の差分なし |

REQUIREMENTS.md で Phase 8 に割り当てられた ID は REQ-28..33 の6件で、すべての PLAN の `requirements` に入っています。どの PLAN にも属さない要求（ORPHANED）はありません。

### Decision Coverage

All trackable CONTEXT.md decisions are honored by shipped artifacts.（`check.decision-coverage-verify`: honored 11/11、not_honored [] ）

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|------------|--------|---------|----------|-----------------|---------|
| tests/test_cli.py（exclude 群） | REQ-28..33 | 457 | 0 | No | Value / Behavioral（バイト一致、spy、終了状態） | ✓ |
| baseline 群 | REQ-32/33 | 69 | 0 | No。期待値は Git 79d83ba の生オブジェクトをハッシュで認証したもの（VALID） | Value（raw bytes） | ✓ |

- 要求に結びつく試験で無効化されたもの: 0件。既存の `skipif(os.name != "posix")` は2件あり、Phase 8 の前からあるもので、この環境（posix）では実行されます。
- 循環した期待値: 0件。
- assertion が不十分なもの: 0件。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| 変更した6ファイル | - | TBD/FIXME/XXX/TODO/HACK/PLACEHOLDER | なし | 走査の exit 1（該当なし） |
| `wordfreq/__main__.py` | 20 | `--exclude` の help が「one word per line」だけ | ℹ️ Info | コメント行や不正例は README にだけある（08-UI-REVIEW Fix 3）。FR-6 は README も含めて満たしている |
| `tests/test_cli.py` | 1352-1376 | shallow-checkout 試験の subprocess に timeout がない | ℹ️ Info | 08-REVIEW IN-02。機能への影響はない |
| `wordfreq/formatters.py`（不変） | 34-38, 51 | 全件除外でも空ファイル用の文言のまま。フォントに CJK の指定がない | ℹ️ Info（契約で固定） | 変更するには PM と UI-SPEC の判断が要る。範囲外 |

反証の確認（Confirmation Bias Counter）:

1. 一部だけ満たしている点: help の説明が最小限です（README で補っています）。
2. 通るが弱い試験: `test_exclude_baseline_corruption_is_not_skipped` は広い例外型を受け入れます。ただし4種の改ざんすべてで失敗を確認しているので受容できます。
3. 試験のない経路: CR 単独の区切りや、BOM だけ・BOM 付きコメントの行は、承認された範囲の外です（WR-01）。

### Human Verification Required

1. **並行・中断 backstop 5件（insufficient_spec）**
   - 内容: REQ-28/30/31/32/33 について、新しい中断・並列の保証を求めない方針を確認する。必要なら held-out 試験を書く。
   - 期待: 保証を追加しない方針の承認、または別要求としての起票。
   - 人が必要な理由: 非推論の項目で、明示的な証拠がないため。
2. **P-08-01 / P-08-02（descriptor-less の禁止事項）**
   - 内容: 上の表の非権威的な判断を人が確認する。
   - 人が必要な理由: 自律モードでは flag を付けて残すだけで、黙って合格にしない決まりのため。
3. **日本語 glyph の表示**
   - 内容: CJK フォントのある環境で、HTML（通常と全件除外）を開く。
   - 期待: 日本語の文言が読め、はみ出しや重なりがない。
   - 人が必要な理由: 監査で閲覧した画像2枚では、ホストにフォントがなく日本語が表示されなかったため。
4. **SC4 の配布**
   - 内容: 親が本報告と `quality/` の CLI 文字原本を、PM が read_file できる形で配布したことを確認する。
   - 人が必要な理由: 本検証より後の工程のため。

### Gaps Summary

gap はありません。

- `--exclude FILE` は全3形式に入っています。
- 除外ファイルの取得と全行検証は本文より先に行い、Unicode fullmatch の後に casefold します。
- 読込み失敗と不正行は exit2 で本文を読まず、本文の失敗は exit1 のままです。
- HTML は元の総数を出し、未指定時の出力は 79d83ba とバイト単位で一致します。

以上を、実際のコード、457件の名前付き試験、本検証の実CLI実行、品質の対象head原本で確認しました。
`human_needed` は、backstop の判定保留・禁止事項の flag・見た目・配布の確認によるもので、実装の欠陥ではありません。

---

## 再開の記録: PM判断の反映（品質・2026-11-28T19:02:33Z）

この節は追記です。上の公式の判定（`status: human_needed`、38/44、insufficient_spec 5件、flagged-unverified 2件）は書き換えていません。

- PM判断: t_6e92d0db（元カードのコメント232）。依頼者の最新判断 2026-11-28T14:45:42.849521+00:00「提案のまま進めてください（1〜5 すべて提案どおり）。」に照らして出されたもの。
- 今回の受入範囲（受付の6受入条件）: **passed**。品質が対象head f3747b7 で独立に実行した結果に基づく。製品ファイルは f3747b7 と今回の報告の起点 b50af63 で同じ（`git diff --name-only f3747b7 b50af63` は `.planning/` の下だけ）。
- 保持する未保証・未確認の項目:
  - 並行・中断の backstop 5件（REQ-28/30/31/32/33）: insufficient_spec のまま。新しい保証は追加しない方針をPMが承認した（08-UAT.md 項目1 は pass。保証そのものは未検証）。
  - P-08-01 / P-08-02: flagged-unverified のまま。PMは禁止事項を免除せず、品質の観測を受入判断の根拠とした。
  - 日本語 glyph の表示: 未確認のまま（検証ホストに日本語フォントなし）。合格にしない。
- SC4（配布）: 解決した。品質が文字原本14件を標準添付し（添付ID 270〜283、全件 SHA-256 照合済み）、PMが文字原本を読んで判断した（PM判断の根拠に添付 270/271/272/273/276/278/281 を記載）。
- 公式の phase 完了: この時点では行っていない。公式 `init.verify-work 8` が `ready_to_transition: false` を返した（理由: VERIFICATION が human_needed、UAT 項目2〜4 が skipped）。公式の決まり（VERIFICATION が passed のときだけ transition）に従い、`phase.complete` を呼ばず、結果を passed に書き換えなかった。

## 再開の記録2: 追加の人の確認の後回し（品質・2026-11-29）

この節も追記です。上の判定の本文（38/44、insufficient_spec 5件、flagged-unverified 2件、日本語 glyph 未確認）は履歴として残し、書き換えていません。

- PM判断: t_bdb96733（元カードのコメント234）。08-UAT.md 項目2〜4 の追加の人による確認を、今回の工程では後回し（deferred）として公式に記録し、ROADMAP の 999.x バックログへの追記を許可した。禁止事項の免除や合格認定ではない。
- 08-UAT.md: 項目2〜4 は `result: skipped` のまま、公式の書式 `reason: "Deferred follow-up: …"` と `## Deferred Follow-Ups` で記録した。元の理由（P-08-01/02 は flagged-unverified、日本語の描画は未確認）は同じ行に残した。公式 `uat.complete-session` が status を complete にした。
- ROADMAP: `## Backlog` に Phase 999.1〜999.3 を追記した。今回の next_phase にはせず、実行も予約もしない。
- 公式の判定（実際の出力）: `phase uat-passed 8 --uat-only` → passed: true（項目2〜4 は deferred: true）。公式 verify-work の canonicalization に従い `frontmatter.set status passed` を実行。`verification.status` → passed、`phase uat-passed 8 --require-verification` → passed: true、blockers なし、stale 判定不明なし。08-SECURITY.md の threats_open は 0、08-VALIDATION.md は nyquist_compliant: true。
- 品質の判定: 今回の受入範囲（受付の6受入条件）は passed。未保証・未確認の項目は上記のまま。

---

_Verified: 2026-11-28T18:49:53Z_
_Verifier: Claude (gsd-verifier)_
