# Proposal

## Why

HTMLの総出現回数だけでは、絞込み・top制限後に実際に何種類の語を表示したか分からない。依頼 r-6ae2cbf2 に従い、表を数えず確認できる表示を加える。

## What Changes

- 表より上の総出現回数の横に `表示 N 種類` を追加する。Nは最終表示データ行数で、空結果は0。
- text/jsonの出力・集計・選択順・終了コード・stderrは変更しない。HTMLの既存総数・basename・表・空状態・安全性も維持する。
- 自動テストを追加し、README.mdのHTML説明に1行追加する。
- 過去仕様のHTMLバイト不変・見た目不変は今回の件数表示に必要な差分だけ例外とし、封印済み過去baselineは保存する。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `wordfreq-cli`: HTMLメタ情報に実表示語種類数を追加し、既存のHTML互換条件をこの意図した差分に整合させる。

## Impact

対象は `wordfreq/formatters.py`、`tests/test_formatters.py`、`tests/test_cli.py`、`README.md`。既存HTML期待値の必要な調整を含む。CLI引数・部品境界・依存・CI・権限・外部送信・データ移行は変更しない。

要求の根拠は `_bmad-output/initiative-r-6ae2cbf2/brief/brief-wordfreq-displayed-types.md` と `_bmad-output/initiative-r-6ae2cbf2/prd/prd-wordfreq-displayed-types.md`。未決事項はない。独立したArchitecture文書は、既存の最終表示対象と総数を使う局所変更のため不要。
