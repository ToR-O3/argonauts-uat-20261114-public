# Proposal

## Why

wordfreqの集計結果を変換ツールやWebサーバなしで保存し、スマートフォンを含むブラウザで読めるようにする。今回の依頼を契機にHTML出力を追加し、明示された同数時の順位規則を初出順へ変更する。

## What Changes

- `--format html`を追加し、単語・回数の表を持つ自己完結HTMLをstdoutへ出力する。表より前に入力ファイル名と単語総出現数を表示する。
- **BREAKING**: text/json/htmlすべてで、回数降順は維持し、同数時の「正規化後語の昇順」を「正規化後語の初出順」へ置換する。top境界で選ばれる語も変わり得る。
- 320px・375pxのmobile viewportと1280pxのdesktopで長語・長い入力名を欠落なく読める簡素な表とする。
- HTML出力境界で入力をescapeし、JS・外部asset・外部通信は不要とする。入力名や語は保存HTMLに残るため共有前確認を案内する。
- 配色（明るい/暗い）と順位列の有無は未決。総数はtop前の全入力出現数、入力名はbasenameを推奨するが未承認。仕様案として記載し、仕様承認PMが一括確認する。詳細は`_bmad-output/initiative-r-5c041156/open-questions.md`。無回答を同意とせず、承認前に実装へ進めない。

## Capabilities

### New Capabilities

なし。既存CLI能力を拡張し、重複する能力は作らない。

### Modified Capabilities

- `wordfreq-cli`: 出力形式にhtmlを追加し、全形式の同数順位を初出順へ変更する。HTMLの総数・入力名・安全性・レスポンシブ可読性・検証条件を追加する。

## Impact

- 対象: `wordfreq/aggregator.py`、`formatters.py`、`__main__.py`、関連する単体/CLI試験、`CONCEPTS.md`等の利用説明。入力境界・Unicode抽出/casefoldは維持する。
- 既存text/JSON構造・既定top10・入力1ファイル・終了値は維持する。stdin/URL、Webサーバ、upload、対話sort、graph、theme切替は追加しない。
- ランタイムは標準ライブラリのみ。依存およびCIの追加・変更は範囲外。既存試験は維持し、ブラウザ検証は後続品質工程で実施する。
- 根拠文書: `_bmad-output/initiative-r-5c041156/brief/brief-wordfreq-html.md`、`_bmad-output/initiative-r-5c041156/prd/prd-wordfreq-html.md`（ともに未決を残すpartial/draft）。独立Architectureは小変更のため不要、構成判断は本変更のdesignに記載する。
