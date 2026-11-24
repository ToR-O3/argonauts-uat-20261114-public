---
title: "r-774f3cd6 — pyproject description UAT PRD"
template: prd
version: 1.1.0
status: draft
headless: true
intent: create
workflow: "John CREATE → bmad-facilitate"
created: "2026-11-24"
updated: "2026-11-24"
---

# r-774f3cd6 — pyproject description UAT PRD

## Table of Contents

- [Document purpose](#document-purpose) — 入力とpartialの位置付け
- [Vision](#vision) — 一点の変更という成果
- [Users and journeys](#users-and-journeys) — 内部工程向け
- [Glossary](#glossary) — beforeとASCII suffix
- [Features and requirements](#features-and-requirements) — FR-1
- [Rules](#rules) — RULE-1〜RULE-3
- [Non-goals](#non-goals) — 推測、新設、Architectureを除外
- [MVP scope](#mvp-scope) — 最小の変更範囲
- [Success metrics](#success-metrics) — SM-1〜SM-3
- [Change boundary](#change-boundary) — 製品差分と工程成果物
- [Stories](#stories) — 条件付きの受入
- [Decisions](#decisions) — full優先と次工程
- [Assumptions](#assumptions) — A-1
- [Open questions](#open-questions) — OQ-1（Brief Q-1）

## Document purpose

入力は全文を確認したBrief `_bmad-output/initiative-r-774f3cd6/brief/r-774f3cd6-brief.md`、同initiativeの `initiative-r-774f3cd6.md`、現物 `pyproject.toml` および依頼原文・工程制約である。本PRDは後続の仕様承認と実装・受入に必要な境界をまとめる。initiativeは名称だけを持ち、descriptionの値を与えていない。

**partial / 実装未承認**: 現物の `[project]` に `description` がない。Brief Q-1をOQ-1として引き継ぎ、この文書作成は止めない。後続の仕様承認PMが質問を一度に集約するため、ここでは質問送信も推測による解決もしない。OQ-1解消前には実装できない。

## Vision

依頼原文は「pyproject.toml の [project] の description の末尾に『 (UAT)』を足す。変えるのは pyproject.toml だけ。未決事項は無い。」である。求める成果は既存descriptionへの正確な連結だけであり、製品機能や依存の拡張ではない。

「未決事項は無い」という依頼と、description不在という現物の矛盾は別々に記録する。市場価値、期限、利用者の損失、元のdescription値を補作しない。

## Users and journeys

内部の一点変更のため、実利用者の物語やUI導線は設けず、能力と受入条件を中心にする。読者に関する非重大な推論はA-1に分離する。製品顧客・固有の人物像は未提示であり、創作しない。

## Glossary

- **before**: 承認された実装前基準のTOML値。参照可能な今回依頼branchの実装前commitは `b34cba0d008923e7f5267ce52d5403492ea53925`。本runではGit操作せず、現物全文を根拠にdescription不在を確認した。
- **suffix**: 先頭にASCII空白1文字を含む正確なASCII文字列 `' (UAT)'`。
- **製品差分**: `pyproject.toml` の指定値の変更。PRD、merged template、memlog、必須レビュー等の工程管理成果物とは区別する。

## Features and requirements

### descriptionのUAT表記

- **FR-1**: OQ-1が解消し、連結元の文字列と変更権限が確定した後、依頼対象の `[project].description` を `before.description + ' (UAT)'` にできる。チェック可能な結果は変更後の値との完全一致。Brief AC-1に対応する。欠落値を空文字と見なすことはできない。現在は前提不成立であり、このPRDは新設権限を与えない。

## Rules

- **RULE-1**: suffixを1回連結する。既存値の正規化、既存末尾の削除、重複除去を行わない。既にsuffixがあっても、基準文字列への今回1回の連結を意味する。
- **RULE-2**: 他の設定・依存・他製品ファイルと無関係な書式を変更しない。Brief AC-2に対応する。
- **RULE-3**: 変更後TOMLが正常解析できること。解析成功だけでFR-1やRULE-2の成立を代替しない。Brief AC-3に対応する。

## Non-goals

descriptionの無承認新設、空文字補完、name等からの文章生成、別フィールドへの代替変更、依存更新、リファクタリング、Architecture変更は対象外。実装・Git・Kanban操作・外部引継ぎも本runでは行わない。

## MVP scope

対象はFR-1のみで、既に最小の確定依頼である。削減候補や追加リリースを設けない。OQ-1解消を実装開始条件とし、文書作成から実装へ進むこと自体を承認と扱わない。

## Success metrics

以下は後続実装の受入指標であり、本runで達成したとは主張しない。

- **SM-1**: 現在はdescription不在で評価不能。目標はFR-1の式との完全一致。OQ-1が新設案で解決する場合は、元値と受入基準を明示承認に整合させてから評価する。
- **SM-2**: SM-1のcounter-metric。description以外の解析済みTOML項目と他製品ファイルの変更をゼロとし、RULE-2を検証する。工程管理成果物は製品ファイル数に混在させない。
- **SM-3**: SM-1のcounter-metric。変更後TOMLの解析失敗をゼロとし、RULE-3を検証する。

## Change boundary

現物の `[project]` は `name = "wordfreq"`、`version = "0.1.0"`、`dependencies = []` のみ。後続の製品編集先は `pyproject.toml` だけで、変更対象はdescriptionだけ。他設定・他製品ファイルは不変で、新しい製品要素は追加しない。descriptionの新設は現時点の範囲外であり、必要ならOQ-1で元値とともに明示承認し、制約を改訂する。

PRD作成工程は指定の `_bmad-output/initiative-r-774f3cd6/prd/` 内の最小限の工程管理文書のみを作成する。任意のHTMLは出力しない。

## Stories

一点変更なので、FR-1を実現する受入単位を一つとする。OQ-1解消後に、確定したbeforeを使ってsuffixを連結し、SM-1〜SM-3の全てを満たすこと。欠落したまま、又は明示承認がない場合は製品を編集せず仕様承認PMへ未解消条件を返す。AC-1〜AC-3の一部だけの合格を完了扱いしない。

## Decisions

- 受付light指定より**full**を優先する。対象が危険なパス `pyproject.toml` に該当するという確定制約のためであり、変更量の大小ではない。Architecture変更はない。
- ユーザー明示の `template: prd` を公式mergeして使用する。小規模でもprd-lightへの置換はしない。
- 次は仕様承認PMでOQ-1を一度の質問に集約する。外部への引継ぎは実行しない。正式な後続文書化ではSofiaによるinitiative Requirementsへの反映が経路となるが、本runでは起動しない。各実装単位の完了後、学びをUpdateで反映して仮定と未決を見直す。

## Assumptions

- **A-1 / Document purpose, Users and journeys**: Brief A-1を継承し、主な読者を後続実装担当者と受入確認担当者と推定する。非重大・未承認の推論であり、固有名、組織、期限は設定しない。

## Open questions

- **OQ-1 / Brief Q-1 / owner: 依頼者、集約: 後続仕様承認PM**: 現物にdescriptionがないため、連結元はどの文字列か。正しいbefore値を含む対象を提示するか、description新設とその元値を明示的に承認して制約を改訂する必要がある。空値は仮定しない。必要時点はFR-1実装前。FR-1とSM-1〜SM-3による最終受入を止めるが、本PRD作成は止めない。再確認条件は明確化・明示承認の受領。headlessのため未解消のままdraft / partialを維持する。
