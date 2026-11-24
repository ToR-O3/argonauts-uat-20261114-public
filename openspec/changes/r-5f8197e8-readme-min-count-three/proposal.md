# Proposal

## Why

READMEの使い方へ依頼された `--min-count 3` の実行例を補う。既存CLIの振る舞いは変えない。例の追加は06-01で実施済み。

## 最新判断（旧記述より優先）

2026-11-24T21:20+09:00 の受入条件は「(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。」。
2026-11-24T13:39:57.048159+00:00 の原文: 「Aを選ぶ。この依頼に限り、原本の保全→最終化→品質の最終確認→受入の判断、の順を許可する。」
根拠: `.planning/argonauts/r-5f8197e8-fix-1.md`、受付 t_dbab0a34。条件2は工程差分が残るため未達。最終化前のphase passed/受入approvedを前提にしないが、受入前の自動マージ予約は禁止し手動待ちとする。

## What Changes

- README.mdの「wordfreq の実行」に `python -m wordfreq input.txt --min-count 3` の実行例を1つ追加する。既存の例・説明・末尾の検証A行を保持する。
- 旧要求の3形式実行、実入力・出力・実行ログの保存は、依頼者の判断により対象外（2026-11-24T21:20+09:00）。実行済み・合格とはしない。
- 独立品質が指定例1つと、工程文書をfilterしない最終PR全差分がREADME.mdだけという2条件を文字で判断し、原本を非commitで標準添付する。PM本人のread_fileによる受入判断は別の未完gate。

## Capabilities

### New Capabilities

なし。文書のみの変更で新しい製品動作は導入しない。

### Modified Capabilities

なし。`wordfreq-cli` の既存契約を確認対象とするだけで変更しない。`readme-verification-note` は過去の末尾追記の契約であり、その行を保つ。本変更は純粋な文書補足のため `.openspec.yaml` に `skip_specs: true` を設定し、CLI公式の省略経路を使う。specsを捏造しない。

## Impact

最終PRで変えるファイルはREADME.mdだけ。コード・設定・依存・公開入出力・試験ファイルの追加変更は禁止。BMAD、OpenSpec、計画・検証文書は必要原本を標準添付保全してから最終化担当のみが基準branch相当へ復元・除外する。工程を除いて数えるだけでは条件2達成にならない。Architectureと新しいUI設計は不要。HTMLを含む動作確認は対象外。PMは文字の検証原本を `read_file` で判断する。画像0枚（文字のみ）、zip不要。

旧仕様の根拠: `_bmad-output/initiative-r-5f8197e8/brief/brief-readme-min-count-3.md`、`_bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md`。最新判断が旧実行要求より優先する。本注記は最終受入の完了報告ではない。
