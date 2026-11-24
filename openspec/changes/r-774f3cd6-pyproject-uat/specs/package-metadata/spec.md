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
