# Proposal

## Why
wordfreqの集計を、別の整形ツールや通信なしでブラウザ閲覧できるようにする。依頼r-50053edcの確定事項を反映し、小画面で文脈と順位表を一緒に読めるようにする。

## What Changes
- `--format html` で自己完結した静的HTMLをstdoutに出力する。表は順位・単語・回数の3列。
- 表より上にbasenameのみと、top適用前の全単語の総出現回数を表示する。
- 明るい背景のみ、切替なし、順位は1始まりの表示行連番。通常幅と320 CSS pxを含む幅で長い語・名前を読めるようにする。
- **BREAKING**: 同数時の語の昇順を初出順に変更する。回数降順を維持し、text・json・htmlで一致させてからtopで制限する。
- エスケープ、空入力、入力・エラー処理、既存形式の回帰を検証する。品質担当の実CLI再生成による独立ブラウザ確認と、文字範囲の実測原本・画面画像・head等の追跡可能な証拠を要求する。

## Capabilities

### New Capabilities
なし。既存CLIの出力形式の追加として扱う。

### Modified Capabilities
- `wordfreq-cli`: formatへhtmlを追加し、全形式の同数時初出順、HTMLのメタ情報・安全性・小画面表示・検証証拠を定める。

## Impact
対象候補は `wordfreq/__main__.py`、`aggregator.py`、`formatters.py`、関連するtestsと利用説明。入力取得・トークナイザの境界と標準ライブラリのみの実行を維持する。text/jsonへHTMLメタ情報を追加しない。
CIの追加・変更、生成日時、テーマ切替、対話操作、サーバー、入力元拡張は対象外。BMAD原本は `_bmad-output/initiative-r-50053edc/brief/brief-wordfreq-html.md` と `prd/prd-wordfreq-html.md`（後者も同initiative配下）。製品実装・製品検証の合格をこの提案で宣言しない。
