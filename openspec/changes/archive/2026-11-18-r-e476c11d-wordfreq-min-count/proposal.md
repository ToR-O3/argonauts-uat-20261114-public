# Proposal

## Why

wordfreqには表示件数の上限しかなく、今回依頼された出現回数の下限を全出力形式へ一貫して指定できない。既存CLIに最小限の`--min-count`を追加し、既定互換とHTMLの元総数を保つ。具体的な利用背景・期限は未提示であり、事業効果は主張しない。

## What Changes

- `--min-count N`を追加。既定1、1以上の整数のみ受理し、不正値・欠落は使い方エラーexit2。
- casefold後の集計からN未満を表示対象から除き、**その後で**既存の`--top`を適用する。両値は独立。同数時の初出順は不変。
- text/json/htmlで同じ表示対象を使い、空入力・全件除外も既存の空形式を維持する。
- HTML総数はmin-count/top適用前の全出現回数。CSS・構造・既存文言は変えない。
- pytestの正常・境界・異常・互換・併用試験とREADME説明を追加。品質が実CLI生成HTMLの独立ブラウザ確認証拠を残す。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `wordfreq-cli`: 最小出現回数オプション、表示対象選択、HTML元総数、試験・互換性の契約を拡張する。

## Impact

対象は既存CLI引数解析・表示対象選択（`wordfreq/__main__.py`・必要最小限の`aggregator.py`）、pytest、README。formatterの公開契約・入力境界・Unicode抽出・casefold・同数初出順・HTMLの静的安全性は維持する。

CIの追加変更、依存追加、見た目変更、入力元追加、外部送信・権限・課金・削除は対象外。新たなアーキテクチャ層やサービスは不要で、既存部品内の設計をdesign.mdに記録する。BMAD原本は`_bmad-output/initiative-r-e476c11d/brief/brief-wordfreq-min-count.md`と`prd/prd-wordfreq-min-count.md`。背景の未決事項Q-01/Q-02は別紙で仕様承認PMへ渡す。
