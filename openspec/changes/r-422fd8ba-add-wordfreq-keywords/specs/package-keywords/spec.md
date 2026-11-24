# Spec Delta

## Purpose

wordfreqパッケージの公開メタデータにkeywordsを宣言し、設定を読む利用者とツールが指定された単一のキーワードを取得できるようにする。既存設定と製品の振る舞いは維持する。

## ADDED Requirements

### Requirement: 指定keywordsの宣言

パッケージは既存の `pyproject.toml` の `[project]` に独立した1行 `keywords = ["wordfreq"]` を持たなければならない（MUST）。ファイルは有効なTOMLであり、解析された `project.keywords` は要素1個の配列 `["wordfreq"]` と完全一致しなければならない（MUST）。

#### Scenario: 設定を読み取る

- **WHEN** 変更後の `pyproject.toml` をTOMLとして解析する
- **THEN** 解析が成功し、`project.keywords` が `["wordfreq"]` と完全一致する
- **AND** keywordsは別テーブルでなく既存 `[project]` に指定どおりの1行として存在する

### Requirement: 既存製品設定の維持

この変更の製品差分は `pyproject.toml` の指定1行の追加だけでなければならない（MUST）。既存行・設定・書式と他の製品ファイルを維持しなければならない（MUST）。工程文書の変更は製品差分と別に扱う。

#### Scenario: 元の設定と差分を比較する

- **WHEN** 変更前の依頼branchの起点と変更後を比較する
- **THEN** 製品ファイルの変更は `pyproject.toml` だけで、追加は `keywords = ["wordfreq"]` の1行、削除は0行である
- **AND** 変更後からこの追加行だけを除くと、元のファイルのバイト列と一致する
- **AND** 解析結果から追加した `project.keywords` だけを除くと、元の解析結果と一致する
