---
title: "r-774f3cd6 — pyproject description UAT PRD"
template: prd
version: 1.1.0
status: final
headless: true
intent: update
workflow: "John UPDATE → bmad-facilitate"
output: "_bmad-output/initiative-r-774f3cd6/prd/"
created: "2026-11-24"
updated: "2026-11-24"
---

# r-774f3cd6 — pyproject description UAT PRD

## Table of Contents

- [Document purpose](#document-purpose) — 依頼者回答を反映、実装・再承認なし
- [Vision](#vision) — description新設という一点変更
- [Users and journeys](#users-and-journeys) — 内部工程向け
- [Glossary](#glossary) — 指定連結元、完成値、実装前基準
- [Features and requirements](#features-and-requirements) — FR-1
- [Rules](#rules) — RULE-1〜RULE-3
- [Non-goals](#non-goals) — 無関係な変更の排除
- [MVP scope](#mvp-scope) — 最小変更と承認境界
- [Success metrics](#success-metrics) — SM-1〜SM-3
- [Change boundary](#change-boundary) — 製品と工程管理領域
- [Stories](#stories) — 一つの受入単位
- [Decisions](#decisions) — full優先、回答根拠、後続工程
- [Assumptions](#assumptions) — A-1
- [Open questions](#open-questions) — OQ-1回答済み、未解決なし

## Document purpose

依頼 r-774f3cd6 の仕様承認 `t_1efee04f` 差戻しに対し、依頼者の明示回答をBriefに反映・Finalizeした後、このPRDを改訂する。入力は `_bmad-output/initiative-r-774f3cd6/brief/r-774f3cd6-brief.md`、同initiativeの `initiative-r-774f3cd6.md`、現物 `pyproject.toml`、元依頼、最新回答と工程制約である。読者の非重大な推論はA-1に分離する。

**OQ-1は回答済み、未解決事項なし。実装・PM再承認は本runでは行わない。** 文書のfinalは文書改訂の完了のみを意味し、製品受入や実装開始の承認ではない。後続の仕様承認で本改訂を確認する。

## Vision

元依頼は「pyproject.toml の [project] の description の末尾に『 (UAT)』を足す。変えるのは pyproject.toml だけ。未決事項は無い。」である。現物にdescriptionがないことを踏まえ、依頼者はdescription新設を明示許可した。成果は `[project].description` の完成値を正確に `argonauts-uat public (UAT)` とする一点変更である。

指定連結元 `argonauts-uat public` は依頼者の指定であり、現物の旧descriptionではない。製品機能や依存は拡張せず、市場価値・期限・元のdescription値を補作しない。

## Users and journeys

内部の技術的な一点変更なのでUI導線や顧客物語を設けず、FR-1と受入指標を中心にする。製品顧客・固有の人物像は入力にないため創作しない。

## Glossary

- **指定連結元**: 依頼者が指定した文字列 `argonauts-uat public`。現物の旧値を意味しない。
- **suffix**: 先頭にASCII空白1文字を含む正確なASCII文字列 ` (UAT)`。
- **完成値**: 指定連結元にsuffixを1回連結した `argonauts-uat public (UAT)`。
- **実装前基準**: 他項目・依存・書式・他製品ファイルの不変を比較する実装前状態。以前の入力に記録されたcommitは `b34cba0d008923e7f5267ce52d5403492ea53925` で、本runはそのcommitの内容をGitで再検証していない。descriptionの連結元を取得するための基準ではない。
- **製品差分**: `pyproject.toml` のdescriptionキー新設。Brief/PRD、template、memlog、必須レビューや検証スクリプトなど工程管理成果物と区別する。

## Features and requirements

### descriptionのUAT表記

- **FR-1**: 後続の承認された製品作業で、`[project].description` を新設し、完成値を正確に `argonauts-uat public (UAT)` にできる。指定連結元は `argonauts-uat public` であり、欠落値やnameから導出しない。結果はキーの存在と文字列の完全一致で確認でき、Brief AC-1に対応する。旧 `before.description` への連結式は現行要件ではない。

## Rules

- **RULE-1**: 完成値内のASCII ` (UAT)` は1回のみ。指定連結元・完成値を正規化、推測、重複付与しない。
- **RULE-2**: description以外のTOML項目・依存・他製品ファイル・無関係な書式は不変。検証スクリプトは工程管理領域だけに置き、他製品ファイルを増やさない。Brief AC-2に対応する。
- **RULE-3**: 編集後TOMLが正常解析できること。解析成功だけでFR-1やRULE-2を代替しない。Brief AC-3に対応する。

## Non-goals

空文字補完、name等からの文章生成、別フィールドへの代替変更、依存更新、リファクタリング、無関係な整形、他製品ファイル追加、Architecture変更は対象外。本runの製品・OpenSpec・共通config編集、実装、PM再承認、commit/push、Kanban操作、外部引継ぎ実行は禁止する。明示許可されたdescription新設は対象内であり、旧「新設未承認」は現行前提にしない。

## MVP scope

FR-1だけが対象で既に最小の確定依頼であり、削減候補や追加リリースを設けない。OQ-1の回答を再質問せず、後続の仕様承認ではこの改訂内容を確認する。文書更新を実装開始の承認と扱わない。

## Success metrics

以下は後続実装の受入指標であり、本runで達成したとは主張しない。

- **SM-1**: 現在はdescription不在。目標はキーを新設し、文字列が正確に `argonauts-uat public (UAT)` と一致し、ASCII ` (UAT)` が1回のみ含まれること。FR-1とRULE-1を検証する。
- **SM-2**: SM-1のcounter-metric。description以外の解析済みTOML項目・依存・他製品ファイル・無関係な書式の変更をゼロとする。検証スクリプトの工程管理領域への限定を含めRULE-2を検証する。工程成果物を製品差分に混在させない。
- **SM-3**: SM-1のcounter-metric。編集後TOMLの解析失敗をゼロとしRULE-3を検証する。SM-1〜SM-3すべての成立が必要。

## Change boundary

現物の `[project]` は `name = "wordfreq"`、`version = "0.1.0"`、`dependencies = []` のみ。後続の製品編集は `pyproject.toml` のdescription新設だけで、その他TOML項目・依存・他製品ファイル・無関係な書式を変えない。指定連結元を現物の旧値と主張しない。

本PRD UPDATEの出力先は既存 `_bmad-output/initiative-r-774f3cd6/prd/`。文書、merged template、memlog、必要なBMADレビュー記録と工程管理領域の検証スクリプトに限定する。任意のPRD HTMLは出力しない。製品・OpenSpec・共通configやinitiative直下の旧工程記録は更新しないため、そこにある回答前の停止条件を現行判断の根拠にしない。実装前の後続工程で改訂の整合を確認し、本runではその更新・承認を実行しない。

## Stories

受入単位はFR-1の一つ。後続の承認された実装でdescriptionを新設し、完成値・suffix回数・その他不変・TOML解析の全条件（SM-1〜SM-3、Brief AC-1〜AC-3）を確認する。一部の合格や文書のfinalだけで製品完了としない。

## Decisions

- 受付light指定より**full**を優先する。対象が危険パス `pyproject.toml` のためで、変更量の大小ではない。最終報告まで理由を引き継ぐ。
- OQ-1（Brief旧Q-1）は回答済み。回答根拠は受付 `t_78c8849e` のdefaultコメント、日時 `2026-11-24T13:00:38.567271+00:00`。原文：「②を選ぶ。description を新設してよい。連結元の文字列は「argonauts-uat public」、完成値は「argonauts-uat public (UAT)」とする。」新設未承認・元値不明という旧決定を置換する。
- ユーザー明示の `template: prd` を公式mergeして使用し、prd-lightには置換しない。BriefのUPDATE・Finalizeを先に完了した。
- 次は後続PMによる仕様再承認であり、本runでは行わない。正式なBMAD後続経路ではSofiaがinitiative Requirementsへ反映するが、ここでは起動しない。各実装単位の完了後に学びをUpdateへ反映し、仮定と未決を見直す。

## Assumptions

- Briefの仮定 `A-1` を継承（Document purpose, Users and journeys）: 主な読者を後続実装担当者と受入確認担当者と推定する。非重大・未承認の推論であり、固有名・組織・期限は設定しない。

## Open questions

未解決のopen_questionsは空（`[]`）。**OQ-1 / Brief旧Q-1: 回答済み**。Decisionsの依頼者回答によりdescription新設、指定連結元 `argonauts-uat public`、完成値 `argonauts-uat public (UAT)` が確定した。旧未承認記述はmemlogの履歴であって現行の停止前提ではない。PM再承認・実装・製品受入の未実施は工程状態であり、依頼者への未解決質問ではない。
