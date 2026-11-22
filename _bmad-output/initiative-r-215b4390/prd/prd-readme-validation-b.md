---
title: "README 検証B・1行追記 PRD"
template: prd
version: 1.1.0
status: final
created: "2026-11-22"
updated: "2026-11-22"
---

# README 検証B・1行追記 PRD

## Table of Contents

- [Document purpose](#document-purpose) — 入力と読み手
- [Vision](#vision) — 1行追加の目的
- [Users and journeys](#users-and-journeys) — 依頼者と後続担当
- [Glossary](#glossary) — 指定行
- [Features and requirements](#features-and-requirements) — FR-1
- [Rules](#rules) — RULE-1〜RULE-3
- [Non-goals](#non-goals) — 実装しない範囲
- [MVP scope](#mvp-scope) — 最小の変更単位
- [Success metrics](#success-metrics) — SM-1〜SM-3
- [Change boundary](#change-boundary) — 保持する既存内容
- [Stories](#stories) — 1件の受入条件
- [Open questions](#open-questions) — 未解決事項なし

## Document purpose

依頼者と後続の実装・検証担当が、README.md に追加する文字列と変更境界を共有する。入力は依頼全文および `_bmad-output/initiative-r-215b4390/brief/brief-readme-validation-b.md` 全文。リポジトリ直下の README.md も全文確認した。本PRDは small work の仕様であり、本工程ではREADMEを変更しない。

## Vision

README.md の末尾に依頼者の指定行を正確に記載する。追加を v1.12 の検証合格の証拠とは扱わない。事業目標や追加機能は設定しない。

## Users and journeys

依頼者が1行の追記を求め、後続担当が既存内容を保持して追加し、検証担当が文字列・位置・出現回数・差分を照合する。画面や利用者像を伴うジャーニーは、この文書変更には不要なため作成しない。

## Glossary

**指定行**は次の文字列そのものを指す。コードブロックの囲みは追加対象ではない。

```text
検証B: v1.12 の通しの確かめ（2026-11-22）
```

## Features and requirements

- **FR-1:** 後続担当は README.md の末尾に指定行を追加する。追加後は引用符・見出し・囲み記号を含まない独立した最終行とし、README.md 全体でその出現は1回のみとする。依頼全文とBriefの SC-01・SC-02 を実現する。

## Rules

- **RULE-1:** README.md の既存内容を保持し、製品差分は指定行1行の追加だけとする。既存行の削除・置換・移動、余分な空行、説明の追加は禁止する。Briefの SC-03 に対応する。
- **RULE-2:** コード・試験を含む他の製品ファイルは変更しない。仕様・計画・検証などの工程記録は製品差分とは別扱いとする。Briefの SC-04 に対応する。
- **RULE-3:** 本PRD作成工程では README.md は読むだけとし、実装・外部handoff・commit・push・カード操作は行わない。

## Non-goals

コード・試験の変更、機能追加、既存文書の整形・文言修正、検証合格の認定は対象外。構成変更がないためarchitectureは不要。外部調査、APIや運用の変更も行わない。

## MVP scope

後続実装の対象はリポジトリ直下の README.md への指定行追記だけであり、すでに最小の変更単位である。段階リリースや後回しの追加機能は設けない。本工程の成果物はPRDとその工程記録に限定する。

## Success metrics

- **SM-1:** 現在のREADMEに指定行はない。追加後の最終行が指定行と完全一致し、出現回数が1回であることを照合する。FR-1 を検証する。
- **SM-2:** 変更前後の差分が指定行1行の追加のみで、既存行の削除・変更と余分な追加がないことを照合する。RULE-1 を検証し、SM-1 だけを満たす過剰編集を防ぐ。
- **SM-3:** 変更ファイル一覧で、工程記録を除く製品変更が README.md のみであることを照合する。RULE-2 を検証する。

すべてを満たした場合のみ受入可能とする。これは後続実装の判定基準であり、本PRDでは達成済みと主張しない。

## Change boundary

README.md の既存本文、書式、既存行の順序を保持し、最終行に指定行だけを追加する。コード・試験・他の製品文書・構成は変更しない。工程記録の追加を、製品変更の許可拡張と解釈しない。

## Stories

依頼者として、README.md の最後に指定行が1回だけ記載され、他の製品内容が変わらないことを求める。受入条件は FR-1、RULE-1、RULE-2 および SM-1〜SM-3 の全充足とする。未充足が1つでもあれば受入不可。

## Open questions

未解決の質問・未確認の仮定はない。構成変更なしのためarchitecture工程は不要。子に委任ツールがないため、本工程のレビューは同一実行者による逐次確認であり、独立レビューは未実施。親が独立レビューを行う。実装・検証後に学びや変更があればPRDをUpdateし、スコープと受入条件を再確認する。
