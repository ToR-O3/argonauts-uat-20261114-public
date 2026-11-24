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


# Spec Delta

## Purpose

依頼者が承認したdescription新設とUAT表記を正確に実現し、他の設定・依存・製品ファイルを保持する。指定連結元と現物の旧値を混同しない。

## ADDED Requirements

### Requirement: 承認されたdescriptionの新設

`pyproject.toml` の `[project].description` を新設し、文字列 `argonauts-uat public (UAT)` と完全一致させなければならない（MUST）。これは依頼者指定連結元 `argonauts-uat public` にASCII ` (UAT)` を1回連結した値である。正規化・重複追加・空文字からの補完をしてはならない（MUST NOT）。

#### Scenario: descriptionが存在しない承認対象
- **WHEN** 改訂仕様承認後の実装で、対象のdescription欠落と指定入力を確認する
- **THEN** descriptionを新設し、その値は正確に `argonauts-uat public (UAT)` となる

#### Scenario: 接尾辞の重複または異なる値
- **WHEN** 完成値が `argonauts-uat public (UAT) (UAT)` または他の文字列となる
- **THEN** 固定完成値との完全一致検証は失敗する

### Requirement: 指定入力と現物を区別する

実装前commit `b34cba0d008923e7f5267ce52d5403492ea53925` にはdescriptionが無い。指定連結元を現物に存在した旧値として記録してはならない（MUST NOT）。新設権限と指定値は受付t_78c8849eの依頼者判断（2026-11-24T13:00:38.567271+00:00）による。OQ-1は回答済みであり再質問を必要としない。実装は改訂仕様のPM承認と計画の後に行わなければならない（MUST）。

#### Scenario: 回答済みの新設承認
- **WHEN** Brief・PRD・本変更と依頼者回答を照合する
- **THEN** 新設承認・指定連結元・完成値が一致し、未解決OQ-1として扱わない

#### Scenario: 実装直前に前提が変わった
- **WHEN** 対象が承認記録と異なる、descriptionが存在する、その他の基準内容が承認記録と異なる、またはTOML解析不能である
- **THEN** 値や型を推測せず、製品を編集せずPMへ不一致を返す

### Requirement: 他項目と他製品ファイルを保持する

製品変更は `pyproject.toml` のdescription新設だけとし、他のTOML項目・依存・他製品ファイル・無関係な書式を保持しなければならない（MUST）。検証スクリプトは工程管理領域に置き、製品試験ファイルやCIを増やしてはならない（MUST NOT）。工程管理成果物は製品差分と別に数える。

#### Scenario: 差分の確認
- **WHEN** 実装前基準と変更後を比較する
- **THEN** 変更後からdescriptionだけを除いた解析済みTOML値は変更前と完全一致し、生テキスト差分と未追跡ファイル一覧でもdescription新設以外の製品変更が無い

### Requirement: 有効なTOMLを保持する

変更後の `pyproject.toml` はTOMLとして正常解析できなければならない（MUST）。解析成功は他の受入条件の代替としない。

#### Scenario: 編集後の解析
- **WHEN** description新設後にTOMLパーサでファイル全体を解析する
- **THEN** 構文エラーがなく、固定完成値との一致と不変条件も個別に確認される


# Tasks

OQ-1は2026-11-24T13:00:38.567271+00:00の依頼者回答で解消済み。本一覧は改訂仕様承認後の実装作業を定義するもので、この文書改訂だけで実装着手を承認しない。

## 1. description新設と直接検証

- [ ] 1.1 依頼者回答と改訂仕様のPM承認を照合する。対象repo・branch・パス、不変比較基準commit `b34cba0d008923e7f5267ce52d5403492ea53925`、現物description欠落、指定連結元 `argonauts-uat public`、完成値 `argonauts-uat public (UAT)`、新設許可を工程検証記録に固定する。検証：承認原文・日時との一致、指定連結元は現物の旧値ではないこと、前提の再照合を確認する。不一致なら製品を編集せずPMへ返す。回答済みOQ-1の再質問はしない。
- [ ] 1.2 工程管理領域に受入検証スクリプトを用意し、具体的コマンドと基準取得方法を計画で確定する。検証：未編集TOML解析と基準取得は成功し、description欠落による固定完成値の検査失敗を編集前に記録する。欠落キーへの無条件アクセスで異常終了するだけの試験にしない。製品試験ファイルやCIは追加変更しない。
- [ ] 1.3 編集直前の照合後、descriptionを1行だけ新設し、指定連結元にASCII ` (UAT)` を1回連結した完成値を設定する。検証：TOML解析成功、descriptionが正確に `argonauts-uat public (UAT)` と一致、変更後からdescriptionだけを除いた構造が変更前と完全一致、gitの生テキスト差分と未追跡ファイル一覧で他項目・書式・依存・他製品ファイル不変を確認する。製品commit・ファイルSHA-256・コマンド・終了コード・条件別結果を文字の証拠に記録する。

## Workflow follow-up

- 品質は同じ製品commitと対象ファイルSHA-256を照合して独立検証し、文字の検証記録を添付する。PMに画像や圧縮ファイルを開かせない。
- 計画ではdesignのVerification contractを1.1〜1.3の検証へ具体化する。1.3内は直前照合・新設、全条件検証、証拠記録を別々のsubstepとして進捗表示する。
- 全タスク完了と同一製品commitの品質検証合格、全受入条件の成立、PM受入の後、最終化工程でOpenSpecをsync・archiveし、続いて品質の最終確認へ渡す。文書finalやOQ-1回答済みだけで実行しない。危険なパスpyproject.tomlのため受付lightよりfullを優先した理由を最終報告へ引き継ぐ。
