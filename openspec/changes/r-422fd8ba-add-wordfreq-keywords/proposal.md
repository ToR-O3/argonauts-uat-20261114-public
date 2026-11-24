# Proposal

## Why

依頼されたパッケージメタデータを設定するため、未定義のkeywordsを指定値で追加する。既存の設定やCLIの振る舞いを変更しない最小差分とする。

## What Changes

- `pyproject.toml` の既存 `[project]` に `keywords = ["wordfreq"]` の1行だけを追加する。
- TOML解析、値の完全一致、製品差分1行と既存設定の維持を確認する。
- 製品に試験ファイルを追加せず、必要な検証資料は工程文書の置き場に保存する。

## Capabilities

### New Capabilities

- `package-keywords`: パッケージの公開keywordsを指定値で宣言し、既存設定を維持する。

### Modified Capabilities

なし。既存 `wordfreq-cli` はCLI動作の仕様であり、パッケージkeywordsを規定していない。`readme-validation-b` も今回の対象外。

## Impact

製品変更は `pyproject.toml` の指定1行だけ。依存・ビルド方式・CLI・README・既存試験・CIは変更しない。Brief・PRD・OpenSpec・計画・検証資料は工程文書として別枠でPRに含める。`pyproject.toml` は危険なパスのため、人がマージする。構成変更がないため独立したArchitecture文書は不要。未決事項なし。
