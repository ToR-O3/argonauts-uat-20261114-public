# Tasks

実装順は部品（内側）から外側。各 task はその時点で pytest が通る状態を保つ。

## 1. 部品: トークナイザと集計

- [x] 1.1 `wordfreq/tokenizer.py` を作成する（`\w` 連続抽出 + `casefold()`、差し替え可能な関数/注入点）。単体試験: 大文字小文字の同一視、句読点を語に含めない、underscore 語の固定、日本語テキストで決定的な出力（spec「単語の切り出しと正規化」）
- [x] 1.2 `wordfreq/aggregator.py` を作成する（`count_words`、FR-4 ソートの `top_words`）。単体試験: 回数降順、同数は単語昇順、`--top` 超過時の全件、空入力

## 2. 部品: 入力取得と出力整形

- [x] 2.1 `wordfreq/sources.py` を作成する（`TextSource` プロトコル + `FileSource`、UTF-8 デコード、`InputError`）。単体試験: 正常読み込み、不存在ファイル、デコード失敗、空ファイル
- [x] 2.2 `wordfreq/formatters.py` を作成する（design D-A の `<count>\t<word>` 1行 と D-E の JSON 配列、0件は `[]`）。単体試験: text/json 双方の出力構造、順序の保持、`json.loads` 可読性
- [x] 2.3 入力取得境界越しの試験を追加する（集計経路が `TextSource` を介してのみテキストを受け取ること、aggregator 系試験が FileSource 非経由であること。spec「部品分離と入力元拡張の構成」）

## 3. CLI 合成と実行形態

- [ ] 3.1 `wordfreq/__main__.py` を作成する（argparse: ファイル引数ちょうど1個、`--top` 既定10・1以上整数、`--format text|json` 既定 text。exit code 0/1/2 の分岐を design D-C どおりに）。CLI 試験: 正常系、`--top` 既定と指定、`--format json` 構造、不正値の exit 2、不存在ファイルの exit 1、引数個数エラー
- [ ] 3.2 `pyproject.toml` を追加する（`wordfreq` パッケージ、ランタイム依存ゼロ、pytest 開発依存）。`python -m wordfreq <file>` が repo 直下で動くことを確認
- [ ] 3.3 CI の pytest ジョブの有無を確認し、無ければ workflow 変更（人の対応）として block 判定の準備をする（proposal Impact 参照）
