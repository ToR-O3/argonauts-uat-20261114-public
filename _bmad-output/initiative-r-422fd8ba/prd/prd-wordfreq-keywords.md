---
title: "wordfreq keywords 追加 PRD"
template: prd
version: 1.1.0
status: final
created: "2026-11-25"
updated: "2026-11-25"
---

# wordfreq keywords 追加 PRD

## Table of Contents

- [Document purpose — 入力と読者](#document-purpose)
- [Vision — 指定状態への適合](#vision)
- [Users and journeys — 作業の役割](#users-and-journeys)
- [Glossary — 製品と工程文書](#glossary)
- [Features and requirements — FR-1](#features-and-requirements)
- [Rules — RULE-1〜RULE-4](#rules)
- [Non-goals — 追加しないもの](#non-goals)
- [MVP scope — 今回の全範囲](#mvp-scope)
- [Success metrics — SM-1〜SM-3](#success-metrics)
- [Change boundary — 維持する設定](#change-boundary)
- [Stories — 受入条件](#stories)
- [Decisions — 確定事項と節の除外](#decisions)
- [Open questions — 未決なし](#open-questions)

## Document purpose

指定1行の追加を、Builder・品質担当・人のマージ担当が実行・判断できる要件にする。入力は依頼原文と確定事項、および [final Brief](../brief/brief-wordfreq-keywords.md)。本PRDは単一変更のinitiativeレベルで、full工程に引き継ぐ。製品はここでは変更しない。

## Vision

`pyproject.toml` の `[project]` に `keywords = ["wordfreq"]` を追加し、依頼されたメタデータ状態にする。現状は keywords 未定義であり、それ以上の利用者被害や商業効果は主張しない。

指定値と最小差分を一緒に確認できることが目的である。既存の動作・設定を維持し、危険パスのマージ判断は人に残す。

## Users and journeys

Builderが追加し、品質担当が内容と差分を確認し、人がマージする。製品の画面操作を変えない技術的変更なので、人物像や利用セッションを創作せず、この役割の流れだけを示す。必要性はFR-1に対応する。

## Glossary

- **製品差分**: 比較元に対する製品ファイルの変更。工程文書の差分は別枠。
- **工程文書**: 本依頼のBrief、PRD、後続の計画・レビュー・検証資料。PRに含めることが許可されている。
- **完全一致**: 解析結果の `project.keywords` が要素1個の配列 `["wordfreq"]` であり、別の型・値・追加要素でないこと。

## Features and requirements

**FR-1. 指定keywordsの追加** — Builderは既存の `[project]` に独立した1行 `keywords = ["wordfreq"]` を追加できる。結果はTOMLとして解析可能で、`project.keywords` は完全一致する。必要性は、現状にない指定メタデータを依頼どおり設定すること。

## Rules

- **RULE-1. 製品の最小差分** — 製品差分は `pyproject.toml` の指定1行の追加だけ。既存行の削除・書換え・並べ替えや他の製品ファイル変更は禁止。
- **RULE-2. 既存設定維持** — 名前、バージョン、依存関係、ビルド設定と既存書式を維持する。工程文書はPRに含めてよい。
- **RULE-3. 検証資料の置き場** — 製品にテストファイルを追加しない。必要な検証スクリプトは工程文書配下に置く計画が可能。本工程では検証ファイルが未作成のコマンドを試さない。後工程でBuilder・品質担当が、実在する検証ファイルを使って検証を実行する。
- **RULE-4. マージ権限** — `pyproject.toml` は危険パスとして人がマージする。自動マージを完了条件にしない。

## Non-goals

他のメタデータ追加、バージョン変更、依存関係変更、設定の一括整形、ランタイム機能、公開・配布作業、製品テスト追加は対象外。外部調査・Architectureも不要。将来機能や改善バックログを新設しない。

## MVP scope

今回の全範囲はFR-1だけで、分割・機能削減の余地を作らない。工程文書は許可された別枠。後続PLANは実在する検証ファイルの配置と実行方法を定めるが、製品の変更範囲を拡大しない。

## Success metrics

実装後、以下をすべて満たす。FR-1を検証する指標であり、この文書作成時点では検証成功を宣言しない。

- **SM-1. 構文** — 変更後のTOML解析が成功すること。現時点では解析未実行。併せて確認する指標はSM-2: 構文が正しいだけで値の誤りを見逃さない。
- **SM-2. 値** — `project.keywords` が `["wordfreq"]` と完全一致すること。現在は未定義。併せて確認する指標はSM-3: 正しい値でも余分な製品変更を許さない。
- **SM-3. 差分** — 製品への追加は指定1行だけ、削除・書換え0、他の製品ファイル変更0。工程文書差分は別に確認する。併せて確認する指標はSM-1とSM-2: 小さい差分だけを理由に構文・意味を見逃さない。

## Change boundary

追加先は既存の `[project]`。`[build-system]`、`[project.optional-dependencies]`、`[tool.setuptools]` は変更しない。既存の `project.name = "wordfreq"`、`project.version = "0.1.0"`、`project.dependencies = []` もそのまま保持する。製品コードと既存テストは変更しない。

## Stories

**単一作業: パッケージメタデータを指定状態にする。** BuilderはFR-1を実装し、品質担当が独立に確認する。受入条件はSM-1〜SM-3すべてとRULE-1〜RULE-4の順守。失敗時は未受入とし、範囲外の修正で成功扱いにしない。人のマージ判断の前に検証結果を残す。

## Decisions

full工程は決定済み。構成変更がないので外部調査とArchitectureを省く。一般的な性能・安全性・運用要件は追加せず、必要な制約をRulesへ集約した。

AI behavior、Experience、Integrations、Data/compliance、API、SLO、Migration、Developer experience、Hardwareの節は、その挙動・UI・契約・環境を変更しないため対象外。複数チームやenterprise展開ではないためStakeholders/rolloutの独立節とganttは不要で、人の承認条件はRULE-4に保持した。任意の追加意思決定はない。

次は要件・計画へ引き継ぐ。必要ならSofiaがinitiativeのRequirementsに採用する。各epic完了後はPRDを見直し、得られた事実で仮定・未決事項を更新する。今回の記録には仮定はない。

## Open questions

なし。実装後の検証・品質確認・人のマージは未決事項ではなく、残っている実行工程である。
