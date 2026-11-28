---
phase: quick-261128-vh0-wordfreq-min-length
verified: 2026-11-28T14:34:04Z
status: human_needed
score: 5/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
head: 1d3a99abbb7d3166c168e1acf43db3bf52856459
independent_quality: pending
browser_verification: pending
acceptance_status: pending
covered_files: [".planning/argonauts/r-a7606d74/baseline/index.json", ".planning/argonauts/r-a7606d74/baseline/input.txt", ".planning/argonauts/r-a7606d74/builder/resume-fixture/EVIDENCE.md", ".planning/argonauts/r-a7606d74/builder/resume-fixture/all.exit", ".planning/argonauts/r-a7606d74/builder/resume-fixture/all.stderr", ".planning/argonauts/r-a7606d74/builder/resume-fixture/all.stdout", ".planning/argonauts/r-a7606d74/builder/resume-fixture/all.xml", ".planning/quick/261128-vh0-wordfreq-min-length/261128-vh0-PLAN.md", ".planning/quick/261128-vh0-wordfreq-min-length/261128-vh0-SUMMARY.md", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/composition.exit", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/composition.stderr", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/composition.stdout", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/contracts.exit", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/contracts.stderr", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/contracts.stdout", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/fixture.exit", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/fixture.stderr", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/fixture.stdout", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/invalid.exit", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/invalid.stderr", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/invalid.stdout", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/unicode.exit", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/unicode.stderr", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/unicode.stdout", "README.md", "_bmad-output/initiative-r-a7606d74/prd/agent-spec-wordfreq-min-length.md", "openspec/changes/r-a7606d74-light/specs/wordfreq-cli/spec.md", "pyproject.toml", "tests/fixtures/max_count_scope/__main__.py", "tests/test_cli.py", "tests/test_max_count_verifier.py", "tools/verify_wordfreq_max_count.py", "wordfreq/__main__.py", "wordfreq/aggregator.py", "wordfreq/formatters.py", "wordfreq/sources.py", "wordfreq/tokenizer.py"]
covered_digest: "v4:sha256:ddf4bd7b60feacbd4c8743682a890c1da5255d06f8d3505fed3bddfc64f88269"
decision_coverage:
  honored: 0
  total: 0
  not_honored: []
human_verification:
  - test: "独立qualityが同カードの最終HEADで対象pytestと全pytestを実行しfresh原本を記録する"
    expected: "head・環境・command・件数・exitと入力/argv/stdout/stderr対応が揃い、既存assertを弱めず成功する"
    why_human: "Builderプロファイル内のgsd-verifierのspot検査は別quality担当の実行・受入ではない。現在未実施。"
  - test: "独立qualityが今回のHTMLを1280×900と320×900、DPR1/100% zoomで実閲覧する"
    expected: "省略/明示1互換、絞込み、全除外、元総数、順位・行・見出し・可読性を全画像/必要tileとraw原本に対応付け文字で記録する"
    why_human: "HTML構造assertや保存stdoutは実ブラウザの見た目・可読性・画像閲覧の証拠ではない。現在未実施。"
---

# Quick 261128-vh0: wordfreq minimum length Verification

**Goal:** `--min-length N` によりcasefold後のUnicodeコードポイント数で短い語を除外し、既定1・既存互換・入力前検証・AND/top前選択・helpを満たし、READMEを変えない。
**Status:** human_needed — 自動検査は成功。独立qualityとHTML実閲覧はpending、全受入完了ではない。
**Verifier:** Hermes / gsd-verifier（Builderプロファイル内。独立quality役ではない）。
**Mode:** 初回Quick --validate Step6.5。既存VERIFICATIONなし。ROADMAPの通常phaseではなく、このQuick PLANとBMAD/OpenSpec契約を対象にした。PLAN/SUMMARYは全文読了。

## Observable Truths

| # | PLAN must-have | Status | 独立検査の根拠 |
|---|---|---|---|
| 1 | 正整数・既定1、casefold済みUnicode lenの包含境界 | VERIFIED | `wordfreq/__main__.py:18–22,35–36,42–47`。tokenizer:18でcasefold後に集計しそのキーをlen判定。unicode spot 15 passed、保存省略/明示1比較も成功。ß→ss、CJK/数字/下線、N1/2/3/大きいNを全形式の固定期待pairsに照合。 |
| 2 | 0/負数/非整数/欠落を入力前exit2、stdout空、開いたstdinを読まない | VERIFIED | parser type=intと `<1` がFileSourceより前。`test_min_length_invalid_before_read` はspy calls0と実CLI不存在入力を両方検査。open-stdin試験はEOF送信せずwait(timeout=3)、stdin未closeを確認。合わせて36 passed。 |
| 3 | 長さと頻度ANDをtop前に適用し、初出順・選択前totalを維持 | VERIFIED | 新Counterは元items順、安定sort後top、totalは元Counter由来。composition/internal_order spot 147 passed。長さのみtop前判別と独立不適格語、指定順交換、上限なし/0/負数/逆転、shared pairs/元Counter不変を確認。 |
| 4 | 省略/明示1が変更前bytesと一致、空/全除外/入力失敗契約 | VERIFIED | `test_cli.py:1265–1275` は旧indexのhex bytes/exit/stderrと両呼出しを照合し生成し直さない。contracts spot内で固定24ケース、空12、有効N入力失敗12を実行。EACCESをPermissionErrorで実確認しfinallyで復元。 |
| 5 | ファイルなしhelp全説明、README/依存/CI/抽出/正規化/HTML外観の非変更 | VERIFIED | help spotでexit0/stderr空と全説明句を検査。開始HEAD対現HEADの製品差分はmainの8行追加だけ。README・pyproject・.github・tokenizer/aggregator/sources/formatters・過去verifierの差分なし。外観コード不変は確認、実描画の確認は別pending。 |
| 6 | Builder/独立qualityの対象・全pytest、HTML実ブラウザと文字原本対応。未実施を合格にしない | UNCERTAIN — WARNING / human decision requested | Builder原本は存在・実結果を確認。独立qualityの同カード実行とHTML実閲覧は未実施。PLANのpending引継ぎ規則と今回PM許可に従い受入保留。未実施部分をVERIFIED/overrideにしない。 |

**Score: 5/6.** 製品のbehavior-unverified truthは0。第6項は独立受入の未実施であり、実装stub/製品FAILEDではない。機能blockerは発見しなかったが、受入条件の完了は主張しない。

## Artifacts / Wiring / Data Flow

公式 `gsd_run query verify.artifacts <PLAN>` は4/4成功：main、test_cli、baseline index/input。手読みによりmainは実処理、testは実CLI subprocessと値assert、baselineは旧出力bytesでありstubではないことを確認した。

公式 `gsd_run query verify.key-links <PLAN>` は0/4、全て `Target not referenced in source` を返した。これはソース内のrepo相対path文字列を探すヒューリスティックの結果であり、そのままWIREDと主張しない。以下の実import/呼出し/動的path構成と実行試験で4リンクを手動で解決した（PLANは変更していない）。

| From → To | 接続・実データの追跡 | Final status |
|---|---|---|
| main → tokenizer | `.tokenizer import iter_tokens` (10)、`count_words(iter_tokens(text))` (42)、tokenizer:18のcasefold、main:46のlen。Unicode実CLI spotで裏付け。 | WIRED / FLOWING |
| main → aggregator | import (7)、元counts/total (42–43) → 順序保持AND新Counter (44–47) → top_words (48)。aggregator:17のstable sort後slice。composition/internal_orderで裏付け。 | WIRED / FLOWING |
| main → formatters | import (8)、同一pairs → HTML/json/text (54–58)、HTMLだけ元total。FileSource実入力から生成され、静的mockではない。internal_orderのidentity/metadata assertと全形式出力比較で裏付け。 | WIRED / FLOWING |
| test_cli → baseline | `ROOT / ".planning/argonauts/r-a7606d74/baseline"` (1171) + `"index.json"` (1267)、stdout/stderr hex比較 (1273–1275)。captureは明示env必須・既存index上書き拒否・製品min-length未追加をassert。 | WIRED / 固定旧oracle |

## Fresh Named Behavioral Spot-Checks

Workspace: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-b/.worktrees/t_ab9d2c45`。
全commandのprefixは `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`、suffixは `-q -p no:cacheprovider`。保存先は本Quick配下の `verifier/<stem>.{stdout,stderr,exit}`。各exit原本は0、pytest出力に失敗/skipなし。

| stem | 実行した既存nodeid（省略名も `tests/test_cli.py::` prefix） | 実測 |
|---|---|---|
| unicode | `tests/test_cli.py::test_min_length_unicode` | 15 passed in 0.57s |
| invalid | `test_min_length_invalid_before_read`、`test_min_length_invalid_open_stdin` | 36 passed in 1.27s |
| composition | `test_min_length_composition`、`test_min_length_internal_order` | 147 passed in 4.26s |
| contracts | `test_min_length_saved_default_bytes`、`test_min_length_help`、`test_min_length_empty`、`test_min_length_valid_input_failure` | 49 passed in 2.16s |
| fixture | `tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only` | 1 passed in 0.16s |

各spot commandは10秒以内。全suiteを再実行していない。これらはgsd-verifierの検査であり、別qualityによる全suite実行を代替しない。

### Existing Builder Original Results (Not This Verifier's Full Run)

`.planning/argonauts/r-a7606d74/builder/resume-fixture/` を直接読取り：

- `all.stdout`: **1311 passed in 213.95s**。`all.exit`: **0**。`all.stderr`: 空。`all.xml`先頭testsuite属性: tests=1311、failures=0、errors=0、skipped=0。巨大XML本文全体を再パースしたという主張はしない。
- `min-length.stdout`: **263 passed, 650 deselected in 8.34s**。
- `max-verifier.stdout`: **54 passed in 7.56s**。
- `final-provenance.txt`: 現HEAD、Python3.12.15/pytest9.0.3、baseline checksum、fixture-only commitに対応。SUMMARYの旧失敗1310/1を消していない点も確認した。

### Authorized Historical Fixture Audit

`builder/resume-fixture/EVIDENCE.md` の出典と実git原本を照合した。

- source commit `31953e1c3f1bd0b5da09484f079f0027976ec737`、blob `6c3d7429a0b61b3578db469065c33c2acd08374f`。
- `git show <source>:wordfreq/__main__.py | sha256sum` と同梱fixtureへの `sha256sum` はともに `9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba`。
- mainとfixtureを全文読取り、fixtureはmin-length追加前のコード。tests fixtureのcopy元だけが変更され、既存assert/拒否契約と過去verifier承認hashは無変更。実行時に親repo過去履歴を参照しない。
- 独立named clean/append-only spotが成功。PM許可を超えて承認hashを更新する回避ではない。

### Immutable Baseline Audit

indexのheadは `6aae84890f8ddbd17e186b9a4732df6dd92d2976`、product_diff_hexは空、jqで24ケースを確認。旧出力captureは互換oracleであって新機能の正しさoracleではない。新機能は独立のliteral expected pairsで判定される。

今回sha256sumと既存source-hashes.txtが一致：
- index.json: `2ec8db3041583a2defb94279315a6dd71876a0ae781c678877d69a6f00fb1de0`
- input.txt: `36862295d293157114143e3e825e6df8a037fe7ed25c04cd7c39cc84cb78eaa4`

## Requirements Coverage

| Requirement | Source | Result |
|---|---|---|
| FR-1 / LEN-1 / SC-1 | BMAD + OpenSpec | SATISFIED: Unicode/boundary/positive validation、fresh unicode+invalid spots。 |
| LEN-2 / SC-4 | OpenSpec + BMAD | SATISFIED: 入力前spy/未EOF stdin、正常N入力失敗、help。 |
| FR-2 / SC-2 | BMAD | SATISFIED: 旧24case bytesと省略/明示1比較。 |
| FR-3 / LEN-3 / SC-3 | BMAD + OpenSpec | SATISFIED: AND/top前/初出順/元total/空、fresh composition/internal/empty。 |
| FR-4 | BMAD | SATISFIED: ファイルなしhelp全意味句、exit0/stderr空。 |
| FR-5 / LEN-4 / SC-5 | BMAD + OpenSpec + PLAN | PARTIAL / NEEDS HUMAN: Builder試験とREADME不変は証拠あり、独立quality/実ブラウザ受入はpending。LEN-4の機能・互換・help部分は確認済み。 |

通常ROADMAP phaseへの要件マッピングはこのQuickに適用せず、PLANが列挙した全FR/LENと外部仕様SCを照合した。見つけた未達を後続phaseへ黙ってdeferする処理は行っていない。

## Test Quality / Anti-Patterns / Adversarial Checks

- min-length追加領域にskip/disabled試験なし。旧POSIX byte-filenameのskipifは今回追加ではなく、既存全suite XMLのskipped=0。値/bytes/順序/metadata/実CLI終了状態まで検査し、存在やstatusだけで合格にしていない。
- captureの明示env/上書き防止/追加前製品guardを読取り。通常試験で新製品の出力を期待値へ書き戻す循環はない。
- `test_min_length_internal_order` はcount_wordsをpatchするため、それ単独ではtokenizer/casefold統合の証拠ではない。この弱点は実CLI unicode/compositionで補完した。
- top後適用、casefold前len、OR選択、total再計算という誤実装仮説を、区別可能なliteral期待値と実処理順に照合した。
- 不正Nで入力待ちに入る経路と、大Nで入力失敗を隠す経路をfresh実行した。未試験の入力エラー経路を発見したという根拠はない。
- 変更main/test_cli/test_max_count_verifierのTBD/FIXME/XXX/TODO/HACK/PLACEHOLDER検索は0件。同梱fixtureの全文にもstub/debt markerなし。空出力は空入力契約でありstubではない。
- scope diffは開始HEADから4ファイルのみ（製品8行、追加CLI tests、歴史fixture局所修正）。README/非対象製品/依存/CIと過去verifierは不変。現在のREADME worktree/staged diffもexit0。commit数は実測8、HEADは依頼と一致。
- PLAN/SUMMARYに独立shell probe宣言なし。本機能のprobe相当は実在pytest nodeidを直接実行した。

### Decision Coverage

公式 `query check.decision-coverage-verify` 結果: **No CONTEXT.md - nothing to check.** skipped=true、total=0、honored=0。agent-skills --skills-onlyは空、project HERMES.md/.agents/.hermes skillsなし。

## Human Verification Required — Acceptance Pending

1. **独立qualityの同カードレビュー・実行。** 最終HEADのfresh quality rootで対象pytestと全pytestを実行し、環境/command/件数/exitと入力・argv・raw bytes・文字索引を残す。Builder原本やこのverifier spotの流用は不可。
2. **HTML実ブラウザ/全画像閲覧。** 省略/明示1、絞込み、全除外、元総数を1280×900・320×900、DPR1/100% zoomで確認する。全画像/必要tileを開き、文字可読性・順位/行・見出し・空状態とraw対応を文字で記録する。保存HTML・構造assertのみでは完了しない。

第6must-haveとPLANのhuman-checkをこのリストへ保持した。PMはpendingの正直な引継ぎを許可したが、免除/合格の許可ではない。機能検証は確認できた範囲で成功、独立受入は未完了。したがって `passed` ではなく **human_needed**。

## Integrity / Handoff

公式 `verification.fingerprint` を全検査後に実行し、covered_files/covered_digestをそのまま転記した。自動追加のPLAN/SUMMARYを含み、このreport自身は除外される。作成物はこのVERIFICATIONと `verifier/` のspot原本だけ。製品/PLAN/SUMMARY/STATE/ROADMAP/OpenSpecは編集していない。commit/push/branch/Kanban/PR操作なし。
