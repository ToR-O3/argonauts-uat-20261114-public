---
title: "README末尾への検証A追記 — PRD"
template: prd
version: 1.1.0
status: final
created: "2026-11-22"
updated: "2026-11-22"
---

# README末尾への検証A追記 — PRD

## Table of Contents

- [Document purpose — 入力と用途](#document-purpose)
- [Vision — 指定文言の掲載](#vision)
- [Users and journeys — 依頼者と後続担当](#users-and-journeys)
- [Glossary — 指定行と工程成果物](#glossary)
- [Features and requirements — FR-01](#features-and-requirements)
- [Rules — RULE-01〜RULE-03](#rules)
- [Non-goals — 変更しないこと](#non-goals)
- [MVP scope — 最小の変更](#mvp-scope)
- [Success metrics — SM-01〜SM-02](#success-metrics)
- [Change boundary — 既存内容の保持](#change-boundary)
- [Stories — 受入条件](#stories)
- [Open questions — 未解決事項なし](#open-questions)

## Document purpose

依頼者の確定したREADME追記を、後続の仕様・実装・品質担当が同じ条件で扱うためのPRDである。入力は[Brief原本](../brief/brief-readme-verification-a.md)と依頼全文・確定事項。BriefのBR-01〜BR-04を具体的な受入条件にする。本工程ではREADME・コード・試験を変更しない。

## Vision

README.mdの末尾に指定文言を正確に掲載する。新機能や製品構想は追加しない。指定行のバージョンと日付は文字列の一部であり、通し検証の実施・合格を証明しない。

## Users and journeys

依頼者は指定行の掲載を求め、実装担当が追記し、品質担当が文字列・位置・変更範囲を確認する。文書1行の変更なので、架空の人物や画面操作の旅程は設けない。

## Glossary

- **指定行**：次節のコードブロックにある文字列。かぎ括弧と追加の句点は含まない。
- **工程成果物**：本PRDなどの仕様・計画・検証用文書。READMEへの利用者向け変更とは別扱い。

## Features and requirements

**FR-01：指定行の掲載。** READMEを読む人が、次の指定行を独立した最後の1行として読めること（入力：Brief BR-01・BR-02）。前後に余分な文字を加えない。

```text
検証A: v1.12 の通しの確かめ（2026-11-22）
```

## Rules

- **RULE-01：既存内容保持。** 既存READMEの削除・書換えをせず、不要な空行を追加しない（Brief BR-03）。
- **RULE-02：変更範囲保持。** 利用者向け変更は指定行の追記だけとし、コードと試験は変更しない。工程成果物は別扱いとする（Brief BR-04）。
- **RULE-03：意味の限定。** 指定行の掲載を、検証実績の証明として扱わない（Brief Executive summary）。

## Non-goals

既存説明やバージョン表記の修正、別途の句点追加、追加機能、コード・試験変更は対象外。新技術・依存がない文書1行の変更なのでArchitectureは不要。PRD作成の委任ではKanban操作、git commit/push、外部引継ぎや新工程の実行を行わない。親担当による工程成果物のcommit/pushと仕様承認への引継ぎは、この制限の対象ではない。

## MVP scope

対象は指定行の末尾追記のみであり、既に最小の確定依頼である。段階リリースや将来版への追加機能の延期は設けない。本PRD作成の成果物はPRDと作成・照合・レビュー記録に限る。

## Success metrics

- **SM-01：掲載一致。** 実装後、最後の行の内容が指定行と一致し、独立していることを確認する。FR-01を満たす。Briefでは指定行は未掲載と報告されているが、本PRD工程ではREADMEの現状や実装が完了しているかどうかを改めて認定しない。
- **SM-02：最小差分。** SM-01の対抗指標として、既存READMEの削除・書換え、不要な空行、コード・試験の変更がないことを確認する。RULE-01・RULE-02を満たす。

いずれも後続の実装・品質工程で確認する条件であり、このPRD作成による達成実績ではない。

## Change boundary

追加するのは指定行だけ。既存READMEの内容と順序、コード、試験は保持する。不要な空行は追加せず、指定行の後に空行や別の文言を置かない。工程成果物の存在をREADME以外の製品変更の許可と解釈しない。

## Stories

依頼者として、READMEの末尾に指定した1行だけを掲載したい。

受入条件は次のとおり。

- 最後の行の内容がFR-01の指定行と完全一致し、かぎ括弧・追加の句点・前後の余分な文字を含まない。
- 指定行が既存行に連結されず、独立した末尾1行になっている。
- 差分は当該追記のみで、既存READMEの削除・書換えと不要な空行追加がない。
- 工程成果物を除き、コード・試験などREADME以外を変更していない。

## Open questions

なし。未確認の仮定や、依頼者の判断を要する未確定事項はない。
