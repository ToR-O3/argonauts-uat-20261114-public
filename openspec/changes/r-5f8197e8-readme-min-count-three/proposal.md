# Proposal

## Why

READMEの使い方には閾値2の例があるが、依頼された `--min-count 3` の実行例がない。既存CLIの振る舞いを変えず、例を補い実行証拠で裏付ける。

## What Changes

- README.mdの「wordfreq の実行」に `python -m wordfreq input.txt --min-count 3` の実行例を1つ追加する。既存の例・説明・末尾の検証A行を保持する。
- 追加例と同一内容のUTF-8入力・閾値3で、既定text、`--format json`、`--format html` を実際に実行して確認する。READMEに3例を追加する要求ではない。
- 3以上の語が残り3未満が除かれる入力を使い、3形式の語・回数・順序と形式固有の出力を確認する。実行コマンド、作業場所、入力内容、各終了コード、stdout/stderrと確認結果を文字の工程証拠へ保存する。未実行を合格にしない。

## Capabilities

### New Capabilities

なし。文書のみの変更で新しい製品動作は導入しない。

### Modified Capabilities

なし。`wordfreq-cli` の既存契約を確認対象とするだけで変更しない。`readme-verification-note` は過去の末尾追記の契約であり、その行を保つ。本変更は純粋な文書補足のため `.openspec.yaml` に `skip_specs: true` を設定し、CLI公式の省略経路を使う。specsを捏造しない。

## Impact

利用者向け変更はREADME.mdだけ。コード・設定・依存・公開入出力・試験ファイルの追加変更は禁止。BMAD、OpenSpec、計画・検証文書は工程成果物として区別する。Architectureと新しいUI設計は不要。HTML出力の確認自体は省略しない。PMは文字の検証原本を `read_file` で判断し、画像や圧縮ファイルを開く必要がない。

根拠: `_bmad-output/initiative-r-5f8197e8/brief/brief-readme-min-count-3.md`、`_bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md`。未決事項はなし。この提案は仕様であり、README変更・3形式実行の完了報告ではない。
