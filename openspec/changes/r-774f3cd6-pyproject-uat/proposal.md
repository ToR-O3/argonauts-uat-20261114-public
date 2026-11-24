# Proposal

## Why

依頼は `pyproject.toml` の既存description末尾へ正確な ` (UAT)` を追加することである。現在の依頼branchではdescriptionが存在しないため、元値や新設権限を推測せず仕様承認で明確化する。

## What Changes

- 承認済みの連結元が確定した後、`[project].description` を `before.description + ' (UAT)'` にする。
- 他のTOML項目、依存、他の製品ファイルを保持する。
- TOML解析、値の完全一致、最小差分を検証する。
- 未決事項OQ-1：実装前commit `b34cba0d008923e7f5267ce52d5403492ea53925` のdescriptionが欠落している。正しい対象と元値、または新設とその元値への明示承認が必要。承認前は製品を編集しない。

## Capabilities

### New Capabilities

- `package-metadata`: パッケージdescriptionのUAT表記とメタデータの保持。

### Modified Capabilities

なし。既存の `wordfreq-cli` と `readme-validation-b` は対象外。

## Impact

製品編集は `pyproject.toml` のdescriptionのみ。CLI、API、依存、CI、Architectureは変えない。工程管理成果物は製品差分と分ける。危険なパス `pyproject.toml` のため受付light指定よりfullを優先した理由を最終報告まで引き継ぐ。設定ファイルの実値を変える依頼であり、文書のみとしてのskip_specsは使用しない。
