# Design

## Context

動機と変更範囲は `proposal.md`、契約は `specs/package-keywords/spec.md` を参照。既存TOMLは14行で `[project]` に name、version、dependencies を持ち、keywordsはない。構成変更はないためBMAD Architectureは不要だが、製品差分を1行に保つ検証方法をここで固定する。

## Goals / Non-Goals

**Goals:** 全体再シリアライズをせず既存行をそのまま保持し、構文・値・バイト差分を別々に確認する。

**Non-Goals:** 設定の整形、他メタデータ追加、製品試験やCIの追加、配布物の公開。

## Decisions

- `[project]` の `version = "0.1.0"` の直後に指定1行を挿入する。TOMLライタでの全体再生成は書式を変えるため使わない。
- 後続の計画では `.planning/argonauts/r-422fd8ba/` に標準ライブラリだけの検証ファイルを置く。製品試験を追加する方法は製品範囲に反するため採用しない。
- 比較元は初期化済み依頼branch起点 `516d7c96a42bbb4e458ed413278b2a83729689aa`。検証ではそのcommitの `pyproject.toml` と変更後を比較し、指定1行を除いたバイト列一致、TOML解析結果からkeywordsだけ除いた一致、工程文書を除く変更パスがpyproject.tomlだけであることを確かめる。後続PLANで実在するスクリプトとコマンドを確定する。
- 既存pytestも回帰確認として変更せず実行する。品質は同じheadで独立に再実行し、コマンド・exit・対象SHA・条件別結果を文字の検証記録として添付する。UI変更がなく画像確認は不要。

## Risks / Trade-offs

- [他のテーブルへの誤配置・型や値の誤り] → TOML解析結果の `project.keywords == ["wordfreq"]` と厳密な1行追加を両方検証する。
- [値は正しいが既存設定・書式が変わる] → 元のバイト列と解析済み設定の両方を比較する。
- [工程資料と製品変更の混同] → 工程文書を許可済みの置き場に限定し、全件の変更パスを確認する。
- [危険なパスへの変更] → 品質確認後も人がマージする。

## Migration Plan

データ移行・依存導入・公開作業はない。戻す場合は追加した1行だけを取り除く。Botはマージしない。
