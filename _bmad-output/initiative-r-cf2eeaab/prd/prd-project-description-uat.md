---
title: "r-cf2eeaab — project.description 確定要件"
template: prd
version: 1.1.0
status: final
created: "2026-11-25"
updated: "2026-11-25"
author: John
---

# r-cf2eeaab — project.description 確定要件

## Table of Contents

- [Document purpose — 入力と引継ぎ](#document-purpose)
- [Vision — 確定した説明文](#vision)
- [Users and journeys — 利用する役割](#users-and-journeys)
- [Glossary — 用語の境界](#glossary)
- [Features and requirements — FR-1](#features-and-requirements)
- [Rules — RULE-1〜RULE-4](#rules)
- [Non-goals — 追加しないもの](#non-goals)
- [MVP scope — 今回と後続の範囲](#mvp-scope)
- [Success metrics — SM-1〜SM-3](#success-metrics)
- [Change boundary — 不変条件](#change-boundary)
- [Stories — AC-1〜AC-3](#stories)
- [Decisions — 判断の優先順位](#decisions)
- [Open questions — 未決なし](#open-questions)

## Document purpose

依頼者が指定した説明文を、余分な変更なくプロジェクトのメタデータに反映できる状態にする。既存の`description`がないため、旧指示の機械的な追記ではなく、確定済みの完成値を新規追加する。

本PRDは、実装担当者・受入担当者・仕様承認PMが同じ完成状態と変更境界を扱うためのinitiative要件である。入力は[Brief](../brief/brief-project-description-uat.md)全文、[initiative](../initiative-r-cf2eeaab.md)、現物の`pyproject.toml`、本カードの依頼原文と最新依頼者判断。initiativeには題名のみがあり、追加要件の根拠とはしない。

今回は本PRDと公式工程の付随文書だけを作り、製品・テストは変更しない。直近の引継ぎは **PRD → OpenSpec → 仕様承認PM**。Briefの一般BMAD案内より本カードの指定を優先し、別の工程へ置き換えない。独立レビューは親が別委任で補う。

## Vision

価値は新機能や市場上の差別化ではなく、依頼者判断と実装・受入の一致にある。期限、利用増加、収益効果は根拠がなく設定しない。

## Users and journeys

依頼者は確定値を得る。実装担当者はFR-1と変更境界を読み、仕様承認後の実装で当該項目だけを追加する。受入担当者はAC-1〜AC-3をすべて確認し、人のマージ担当者が最終的にマージする。

これは既存設定の単一変更で、画面や利用者操作の追加はない。テンプレートの技術的PRDの例外に従い、架空の人物や画面遷移を作らず、役割と引継ぎに縮約する。

## Glossary

- **対象項目:** `pyproject.toml`の`[project]`に属する単一の`description`キー。現在は存在しない。
- **完成値:** 解析後の文字列`argonauts-uat public (UAT)`。接尾辞を含む全体の値であり、追加加工しない。
- **製品差分:** 製品ファイルに対する変更。今回許されるのは対象項目の新規追加だけ。
- **工程文書:** Brief、PRD、OpenSpecなどの計画・承認・検証記録。製品差分とは区別し、PRに含めてよい。
- **full / smart:** 本カードの工程・マージ方針の指定。fullを維持し、smartでも危険パス`pyproject.toml`のマージは人が行う。

## Features and requirements

### 確定した説明文の登録

**FR-1:** 依頼者は、`[project].description`が新規追加され、解析後の値が厳密に`argonauts-uat public (UAT)`であるプロジェクトメタデータを得られる。

根拠は最新依頼者判断。説明文の推測、既存値への追記、完成値への二重追記はこの機能に含めない。受入はAC-1で確認し、不変条件と解析可能性はAC-2・AC-3で確認する。

## Rules

- **RULE-1:** 最新依頼者判断を旧追記条件に優先し、完成値の前後に空白や追加の` (UAT)`を付けない。
- **RULE-2:** 製品差分は`pyproject.toml`の対象1項目だけ。他の製品ファイル、既存TOML項目とその値は不変。工程文書はPRに含めてよい。
- **RULE-3:** 変更後の`pyproject.toml`はTOMLとして正常解析できなければならない。
- **RULE-4:** fullを維持する。architecture変更は不要。危険パスのためsmartでも人がマージし、本PRDは自動マージを許可しない。

## Non-goals

動作の変更、依存関係の追加・更新、他設定の追加、名称・バージョンの変更、他製品ファイルの編集、テスト追加・変更は行わない。新しいAPI、画面、データ処理、配布や移行方式も設けない。説明文から製品名や用途の変更を推定しない。

## MVP scope

後続実装の対象はFR-1とその検証だけ。既に最小の確定要求であり、機能の分割や次版への延期はない。

本タスクの対象はPRDと公式工程の付随文書のみ。kanban操作、commit、push、実装・製品・テスト変更は行わない。後続で検証用ファイルが必要なら工程文書の置き場所に置くことは許されるが、製品テストの追加は許されない。

## Success metrics

- **SM-1:** 現在は対象項目なし。目標は対象項目が存在し、その値が完成値と厳密一致すること。FR-1を検証する。
- **SM-2:** SM-1の対抗指標として、対象項目以外の製品差分はゼロ。説明文追加を理由とする付随変更を防ぐ。
- **SM-3:** 変更後のTOML解析が成功すること。SM-1の達成と引き換えに設定を壊さない。

これらは後続実装の受入指標であり、本PRD完成をもって達成済みとは扱わない。

## Change boundary

追加するのは`[project].description`だけ。現物では`name = "wordfreq"`、`version = "0.1.0"`、`dependencies = []`であり、これらを含む既存TOML項目と値はすべてそのまま保つ。`[build-system]`、`[project.optional-dependencies]`、`[tool.setuptools]`も変更しない。

他の製品ファイルやテストも変更しない。工程文書は許容するが、その許可を製品変更の拡大に利用しない。外部送信、権限変更、課金、データ消去は行わない。

## Stories

単一の変更として、依頼者が指定どおりの説明文を得られるようにする。受入条件はBriefのIDを保持する。

- **AC-1:** `[project].description`を新規追加し、解析後の文字列が厳密に`argonauts-uat public (UAT)`と一致する。前後の空白、接尾辞の重複は不可。
- **AC-2:** 製品差分は`pyproject.toml`の当該1項目のみ。他の製品ファイルと既存TOML項目・値は不変。工程文書はPRに含めてよい。
- **AC-3:** 変更後の`pyproject.toml`がTOMLとして正常解析できる。

受入担当者は、解析結果の文字列厳密比較、製品差分の確認、TOML解析結果で判定する。どれか一つでも不成立なら受入不可。検証方法の具体化は後続仕様で行い、テスト追加を必須にしない。

## Decisions

依頼原文は「pyproject.toml の [project] の description の末尾に「 (UAT)」を足す。変えるのは pyproject.toml だけ。未決事項は無い。」である。しかし実物に対象項目はない。

**2026-11-24T19:13:42.938043+00:00**の最新依頼者判断を採用する。

> 新しく作ってよい。完成後の説明文は「argonauts-uat public (UAT)」とする。

この判断で不存在の問題は解決済み。何もしない案、存在しない値への追記、完成値への二重追記は採用しない。full工程の維持とarchitecture変更が不要であることは両立する。architecture変更が不要であることを、工程省略の根拠にはしない。

条件不成立のため、AI評価、ブランド体験、複数チームの展開計画、統合・運用、個人情報・法令、API変更、SLO、移行、開発者導入、ハードウェアの節は設けない。共通品質条件はRULE-3で扱う。後続の実装完了時に学びや境界変更があれば本PRDをUpdateで見直すが、確定値や範囲を無断で拡大しない。

## Open questions

未決事項なし。採用した未確認の推測もない。独立レビューと仕様承認は後続工程のゲートであり、依頼内容の未解決点ではない。
