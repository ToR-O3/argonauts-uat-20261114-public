# Spec Delta

## Purpose

パッケージメタデータのdescriptionに依頼されたUAT表記を正確に付与し、他の設定や依存、製品ファイルを保持するための契約を定める。現物の元値と承認済みの入力を区別し、未承認の新設や値の推測を防ぐ。

## ADDED Requirements

### Requirement: descriptionへの正確なUAT追加

変更後の `[project].description` は承認済みの実装前文字列にASCII ` (UAT)` を1回連結した値と完全一致しなければならない（MUST）。正規化や既存末尾の削除は行わない。

#### Scenario: 既存の文字列がある
- **WHEN** 変更前descriptionが文字列Dとして確認され、実装が承認されている
- **THEN** 変更後descriptionはDと正確な ` (UAT)` の連結となる

#### Scenario: 同じ接尾辞が既に存在する
- **WHEN** 実装が承認され、承認済みの変更前descriptionが既に ` (UAT)` で終わる
- **THEN** 今回の連結は追加1回であり、既存接尾辞を削除したり重複除去したりしない

### Requirement: 未確定の元値を推測しない

descriptionが欠落・非文字列、またはTOML解析不能の場合、値の補完や型変換を推測してはならない（MUST NOT）。対象と元値・変更権限の承認、必要なら新設の明示承認とBrief・PRD・OpenSpecの受入条件の整合した改訂が完了するまで製品編集を開始しない（MUST）。

#### Scenario: 現在のdescription欠落
- **WHEN** 実装前commit `b34cba0d008923e7f5267ce52d5403492ea53925` のように `[project].description` が存在しない
- **THEN** 未決事項OQ-1を仕様承認へ返し、製品ファイルを変更しない

### Requirement: 他項目と他製品ファイルを保持する

変更は `pyproject.toml` のdescriptionだけとし、他のTOML項目・依存・他製品ファイル・無関係な書式を保持しなければならない（MUST）。工程管理成果物は製品差分と別に数える。

#### Scenario: 差分の確認
- **WHEN** 承認済みの実装前基準と変更後を比較する
- **THEN** descriptionを除いた解析済みTOML値は全て一致し、製品差分は当該descriptionのみとなる

### Requirement: 有効なTOMLを保持する

変更後の `pyproject.toml` はTOMLとして正常解析できなければならない（MUST）。解析成功は他の受入条件の代替としない。

#### Scenario: 編集後の解析
- **WHEN** descriptionの編集後にTOMLパーサでファイル全体を解析する
- **THEN** 構文エラーがなく、値の完全一致と不変条件も個別に確認される
