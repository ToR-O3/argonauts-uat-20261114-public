# Proposal

## Why

元依頼は `pyproject.toml` の既存description末尾への正確な ` (UAT)` 追加だったが、現物にはdescriptionが無かった。依頼者は2026-11-24T13:00:38.567271+00:00に新設を明示承認した。指定連結元 `argonauts-uat public` は現物の旧値ではなく、依頼者指定の入力である。

## What Changes

- `[project].description` を新設し、完成値を正確に `argonauts-uat public (UAT)` とする。ASCII ` (UAT)` の連結は1回。
- 他のTOML項目、依存、他製品ファイル、無関係な書式は保持する。
- TOML解析、固定完成値との完全一致、description以外の構造・生テキスト差分を検証する。検証スクリプトは工程管理領域に置く。
- OQ-1は回答済み。Brief・PRD・本変更を同じ判断へ改訂する。本カードでは製品を編集せず、改訂後の仕様承認と計画・実装は後続工程に委ねる。

## Capabilities

### New Capabilities

- `package-metadata`: パッケージdescriptionのUAT表記とメタデータの保持。

### Modified Capabilities

なし。既存の `wordfreq-cli` と `readme-validation-b` は対象外。

## Impact

製品編集は `pyproject.toml` のdescription新設のみ。CLI、API、依存、CI、Architectureは変えない。工程管理成果物は製品差分と分ける。危険なパス `pyproject.toml` のため受付light指定よりfullを優先した理由を最終報告まで引き継ぐ。設定の実値を変えるためskip_specsは使用しない。

## Decision source

受付t_78c8849eの依頼者判断（2026-11-24T13:00:38.567271+00:00）原文：「②を選ぶ。description を新設してよい。連結元の文字列は「argonauts-uat public」、完成値は「argonauts-uat public (UAT)」とする。」
