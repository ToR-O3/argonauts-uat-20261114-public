---
phase: quick-261128-jaf-wordfreq-min-length-option
verified: 2026-11-28T05:23:32Z
status: gaps_found
score: 5/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
covered_files:
  - .planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-EVIDENCE.md
  - .planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-PLAN.md
  - .planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-SUMMARY.md
  - .planning/quick/261128-jaf-wordfreq-min-length-option/baseline-corrected.log
  - .planning/quick/261128-jaf-wordfreq-min-length-option/blocker-reproduction.log
  - .planning/quick/261128-jaf-wordfreq-min-length-option/regression.log
  - README.md
  - openspec/changes/r-1bae0a69-light/specs/wordfreq-cli/spec.md
  - openspec/changes/r-1bae0a69-light/tasks.md
  - tests/fixtures/min-length-default.html
  - tests/test_cli.py
  - tests/test_max_count_verifier.py
  - tools/verify_wordfreq_max_count.py
  - wordfreq/__main__.py
  - wordfreq/aggregator.py
  - wordfreq/formatters.py
  - wordfreq/tokenizer.py
covered_digest: "v4:sha256:d2af157f0d5390de8e61467fab7738d3131ec72c64d54f06125606ec9cd3f161"
gaps:
  - truth: "追加試験と既存全pytestの実測証拠があり、未知引数REDと比較境界の検出証拠を区別できる。加えてML-FR-4・ML-3・Task 3が要求する全回帰失敗なしを満たす。"
    status: partial
    reason: "実測証拠とREDの区別は存在するが、全回帰は1076 passed / 1 failed / exit1。修正済み開始baselineは1048 passed / exit0であり、新たな失敗を既存失敗として除外できない。Task 3とOpenSpec 1.3は未完了。"
    artifacts:
      - path: tests/test_max_count_verifier.py
        issue: "scope_repoが現在の製品をコピーし、test_scope_contract_clean_and_append_onlyが歴史的固定hashを持つ検証器で拒否される。"
      - path: tools/verify_wordfreq_max_count.py
        issue: "488–492行の過去max-count承認hashと現在のwordfreq/__main__.pyが不一致。既存原本は変更していない。"
      - path: openspec/changes/r-1bae0a69-light/tasks.md
        issue: "1.3は未チェックのまま。"
    missing:
      - "過去の承認証拠を改竄・弱体化しない方法で、歴史的scope fixtureと現在製品の衝突を解消する範囲判断と修正。"
      - "修正後の既存全回帰失敗なしの実測証拠、およびそれに基づくTask 3・OpenSpec 1.3の完了判断。"
---

# Quick 261128-jaf — Verification

## 判定

**gaps_found — 機能の追加は確認したが、Quick全体は未達。** 初回検証。通常ROADMAP phaseの完了判定、seal、advance、受入承認は行っていない。

目標: `--min-length N` を追加し、既定1、casefold後の長さによる全形式共通選択、既定互換、help、README無変更、全回帰成功を満たす。

対象workspace: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-b/.worktrees/t_23cd547e`。
独立確認時HEAD: `075ac7f06869b1dd400c2f365e29aac5b6936df8`。開始HEAD: `7ba06e8e757fb86f93ca6a63b13bdc8110df2777`。
確認開始時の `git status --short` は `?? .planning/quick/` のみ。製品・試験に未commit差分なし。

## Observable Truths

| # | PLANのtruth / 必須完了条件 | 判定 | 根拠 |
|---|---|---|---|
| 1 | N未満のみ除外、Nちょうど・超過を全形式で保持、抽出・casefold後の長さ | VERIFIED | `__main__.py:37–42`、`tokenizer.py:18`。boundary/casefold/unicodeの実CLI試験が独立再実行で成功。 |
| 2 | 長さ・頻度上下限をtop前に選択、同頻度の正規化後初出順 | VERIFIED | `__main__.py:39–43`、`aggregator.py:17`の安定ソート。composition/tie_orderが全形式で成功。 |
| 3 | HTML元総数は全入力の総出現数で、選択・top・全除外で減らない | VERIFIED | `__main__.py:38,49`、`formatters.py:115`。compositionのtotal8、emptyのtotal2を実CLI試験で確認。 |
| 4 | 省略と明示1が全形式で変更前固定stdout/stderr/exitに一致 | VERIFIED | `test_cli.py:820–831`。固定text/json literalと完全HTML fixtureへの個別比較6例が成功。Builderの製品編集前確認は `default-before.log` / EVIDENCE:55,71参照。現在の2出力同士だけを比較する試験ではない。 |
| 5 | helpが選択肢・N文字未満除外・既定1を説明しREADME不変 | VERIFIED | `__main__.py:19–20`、help試験成功。HEAD/worktree、index、開始HEAD→現在HEADのREADME差分は全て空。 |
| 6 | 追加・既存全pytestの証拠とRED区別、かつ全回帰失敗なし | FAILED — BLOCKER | 証拠とRED区別は成立。ただしPLAN Task 3 done・success criteria、PRD ML-FR-4、OpenSpec ML-3が要求する全回帰成功は不成立。`regression.log:69–70`は1 failed, 1076 passed。 |

**Score: 5/6。** 第6truthの字義上の「証拠がある」は満たすが、PLAN全体の全回帰成功条件を弱めないよう同じ行へ統合した。証拠不足や未実施ではなく、実行済みの失敗である。behavior-unverified項目、受諾済みoverride、後続phaseへの明示的deferはない。

## Required Artifacts / Key Links / Data Flow

公式 `gsd_run query verify.artifacts <PLAN>` は **all_passed=true, 4/4**。`wordfreq/__main__.py`、`tests/test_cli.py`、固定HTML fixture、EVIDENCEを実際に読んで内容を確認した。fixtureはtotal4とbb/a/cccの完全文書で、実行時に製品から期待値を生成していない。

公式 `gsd_run query verify.key-links <PLAN>` は **all_verified=false, 1/4**（fixture参照のみ検出）。他の3件は `Target not referenced in source`。これを成功へ読み替えず、以下のPython相対import・実呼出しを手動追跡し、実CLI試験で配線を確認した。tokenizerがmainを参照する必要はなく、mainがtokenizerを呼ぶ。

| PLAN key link | 実配線・データ源 | 判定 |
|---|---|---|
| tokenizer → main | main:10のimport、main:33の実ファイル読取り → main:37の `count_words(iter_tokens(text))`。tokenizer:18でcasefold済み語を生成。 | WIRED / FLOWING |
| main → aggregator | main:7、37–43。全countsからtotal保存、挿入順を保つ新Counterで選択し `top_words` へ渡す。 | WIRED / FLOWING |
| main → formatters | main:8、43–58。同じpairsを全形式へ渡し、HTMLは選択前totalを使用、stdoutへ書込み。 | WIRED / FLOWING |
| CLI試験 → 固定fixture | test_cli:828–831でfixtureをread_bytesし、省略・明示1のstdoutと個別比較。 | WIRED |

## 独立実行と保存済み実ログ

### このverifierによる追加試験の独立再実行

repo rootで実行（追加installなし、既存cache環境を使用）:

```sh
unset PYTEST_ADDOPTS
PYTHONDONTWRITEBYTECODE=1 /home/Yuki/.cache/uv/archive-v0/93Y_xVGwEKUhHy-t/bin/python -m pytest tests/test_cli.py -k min_length -q -p no:cacheprovider --basetemp="$TMPDIR/quick-261128-jaf-verifier-targeted"
```

実出力: **`29 passed, 650 deselected in 2.74s`、exit0**。boundary/casefold/unicode/composition/tie_order/empty/default_fixed/tracer/helpと3種のcold-copy判別試験を含む。管理scratch以外の製品コピーを編集していない。

### 全回帰と単独失敗の証拠（Builderの保存済み実ログを読取り）

| 証拠 | 実行 | 実測 | 判定 |
|---|---|---|---|
| `baseline-corrected.log` / `.exit` | cache Python `-m pytest tests -q --basetemp="$TMPDIR/quick-261128-jaf-baseline"` | 1048 passed in 246.37s / exit0 | 製品変更前の修正済みbaseline |
| `final-targeted.log`（EVIDENCE対応表） | cache Python `-m pytest tests/test_cli.py -k min_length -q`、管理basetemp指定 | 29 passed, 650 deselected / exit0 | Builder追加試験。上記独立実行と区別 |
| `regression.log` / `.exit` | cache Python `-m pytest tests -q --basetemp="$TMPDIR/quick-261128-jaf-regression"` | 1 failed, 1076 passed in 248.70s / exit1 | **全回帰未達** |
| `blocker-reproduction.log` | cache Python `-m pytest tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only -q --basetemp="$TMPDIR/quick-261128-jaf-blocker"` | 1 failed in 0.09s、ValueError | 同じ衝突を単独再現した保存済み証拠 |

全件再実行は依頼に従い行っていない。baselineの最初の環境設定失敗17件を合格扱いせず、PYTEST_ADDOPTS継承を解消した **1048 passed** のbaselineを比較対象とした。現在の1件はそのbaselineには存在しない新たな回帰であり、「既存の無関係な失敗」として免責しない。

### 根本原因

`tests/test_max_count_verifier.py:216–233`のscope_repoは現在製品をcold copyして一時repoを作成する。`test_scope_contract_clean_and_append_only:236–243`はtest追加だけを許容することを検査するが、`tools/verify_wordfreq_max_count.py:488–492`は過去max-count受入時のCLI SHA-256を固定している。

- 旧承認SHA-256: `9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba`
- 現在CLIの独立 `sha256sum`: `76d94464a947552d8036d1848440acca1c6975424c966bf37a8d5ed702cba246`
- 実例外: `ValueError: unapproved product/README change: wordfreq/__main__.py`

min-length機能の値計算に誤りがあるという結果ではなく、歴史的承認契約と可変の現在製品を組み合わせたscope試験の衝突である。それでも「既存全試験成功」の必須条件は失敗している。原本hash更新・試験skip・期待値緩和で隠してはならない。過去製品へのfixture隔離などは次の修正範囲判断が必要で、本検証では実施しない。

## Test Quality / REDの区別

- 追加区間 `tests/test_cli.py:820–960`にskip/xfailなし。既存POSIX限定試験のskipifを追加試験の無効化と誤認しない。
- expected pairsと既定text/jsonは固定値。完全HTMLは固定fixture。出力captureスクリプトの生成物を期待値へ逆流させる試験ではない。値・終了コード・stderr・順序・total・空状態を検査する。
- 未配線REDは `tracer-unwired.log:1` のCLI exit2 / unknown argument。**境界比較誤りの検出証拠ではない。**
- 配線後・長さ条件追加前のREDは保存済み `tracer-selection-red-verdict.json` のexit1、tests1/fail1、actualにaが残る意味的失敗。helpも `help-red-verdict.json` でtests1/fail1。両公式分類はRED_EVIDENCE_OK。
- 独立再実行したdiscrimination試験はcontrolの子3件成功、ignore-lengthとexclusiveの子各3件の期待値AssertionErrorを要求する。errors/skipped=0、対象件数3、exit0/1と失敗箇所も検査し、未知引数・collection/import/syntax失敗を境界検出と混同しない。
- SUMMARY/EVIDENCEが申告する手順差異（Task 1の公式RED分類がGREEN後、独立RED-only commitなし）は残る。保存済みREDを事前機械認可の証拠へ読み替えず、完全なTDD手順準拠とは認定しない。
- PLANにshell probeの明示なし。probe成功や過去のmax-count sealは今回の合格根拠として使用していない。

## Requirements / Task Coverage

| 要求・工程 | 判定 | 根拠 |
|---|---|---|
| ML-FR-1 / ML-1 | SATISFIED | 全形式境界、casefold、Unicode、併用・順序の独立試験成功 |
| ML-FR-2 / ML-2 | SATISFIED（今回の固定ケースとコード経路） | 既定1、省略/明示1の固定比較、元総数・空状態成功。全回帰保証とは区別 |
| ML-FR-3 / ML-3のhelp・README部分 | SATISFIED | help試験、README差分なし |
| ML-FR-4 / ML-3の全試験成功部分 | BLOCKED | 1 failed / 1076 passed / exit1 |
| PLAN Task 1/2、OpenSpec 1.1/1.2 | 機能・試験成果を確認 | 実装と独立29件成功。手順差異は上記のとおり |
| PLAN Task 3、OpenSpec 1.3 | **未完了** | 全回帰成功条件未達。tasks.md:7の未チェックとSUMMARYのincompleteが実測と整合 |

## 範囲・Anti-Patterns

独立 `git diff <開始HEAD>..HEAD --stat` はCLI3行追加、CLI試験143行追加、固定HTML91行、OpenSpec tasks7行の4ファイル。製品・試験・PLANを本検証では編集していない。READMEの3比較は差分なし、`git diff --check`は出力なし（コマンド群はexit0）。依存・tokenizer・aggregator・formattersの製品変更はない。読取りした追加区間に未実装stubや未参照TBD/FIXME/XXXは認めない。BLOCKERは上記の具体的な全回帰失敗1件。

### Decision Coverage

公式 `gsd_run query check.decision-coverage-verify` の結果: **No CONTEXT.md - nothing to check.** `skipped=true`, `reason=CONTEXT.md missing`。Quickに架空のCONTEXT決定数やROADMAP phaseを割り当てない。公式agent-skillsのgsd-verifier設定は空、repo内HERMES.mdとプロジェクトSKILL.mdは検索結果なし。

## Human Verification / Gaps Summary

人手でないと確認できない新規項目は追加しない。既知の失敗は不確実なUX判断ではなく再現済みBLOCKERであり、human_neededへ格下げしない。PM受入・CI・Quick完了は未認定。

**未達は全回帰成功の1 concern。** 既存原本と試験を保護したまま修正方針を決め、修正後の全回帰を実測するまでTask 3とOpenSpec 1.3を完了にしない。SUMMARY/EVIDENCE/PLAN/製品/試験は変更せず、このVERIFICATIONだけを作成した。commit/push/branch/kanban操作、通常phaseの完了やsealの発行は行っていない。

fingerprintのcovered_files/covered_digestは公式 `gsd_run query verification.fingerprint` の出力をそのまま転記した。
