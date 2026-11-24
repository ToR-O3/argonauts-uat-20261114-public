---
title: "r-774f3cd6 — pyproject description UAT"
template: brief
version: 1.1.0
status: final
headless: true
intent: update
workflow: "Mary UPDATE → bmad-facilitate"
output: "_bmad-output/initiative-r-774f3cd6/brief/"
created: "2026-11-24"
updated: "2026-11-24"
---

# r-774f3cd6 — pyproject description UAT

## Table of Contents

- [Executive summary](#executive-summary) — 新設許可、完成値、文書のみの改訂
- [Problem](#problem) — description不在と依頼者回答
- [Solution](#solution) — 指定連結元からの新設
- [What makes it different](#what-makes-it-different) — 最小差分
- [Who it serves](#who-it-serves) — 後続工程の利用
- [Success criteria](#success-criteria) — AC-1〜AC-3
- [Scope](#scope) — full優先、禁止事項
- [Assumptions](#assumptions) — A-1
- [Open questions](#open-questions) — OQ-1回答済み、未解決なし

## Executive summary

依頼 r-774f3cd6 は `pyproject.toml` の `[project].description` にUAT表記を付ける一点変更である。現物にdescriptionがないため、依頼者は新設を明示許可し、連結元を `argonauts-uat public`、完成値を `argonauts-uat public (UAT)` と指定した。指定連結元は現物の旧値ではない。OQ-1（Brief旧Q-1）は回答済みで、未解決事項はない。

本Briefは仕様承認 t_1efee04f の差戻しに対する文書改訂であり、後続の仕様確認・実装・受入に一点変更の境界を渡す。実装、製品受入、PM再承認は本runでは行わない。危険パス `pyproject.toml` のため受付lightよりfullを優先し、この判断を最終報告まで引き継ぐ。市場価値や期限は入力になく補作しない。

## Problem

元依頼は「pyproject.toml の [project] の description の末尾に『 (UAT)』を足す。変えるのは pyproject.toml だけ。未決事項は無い。」だった。現作業場所の `pyproject.toml` を全文確認すると、`[project]` は `name = "wordfreq"`、`version = "0.1.0"`、`dependencies = []` のみでdescriptionはない。initiative文書は名称だけを保持し、値を指定していない。

この相違について、受付 `t_78c8849e` のdefaultコメント、日時 `2026-11-24T13:00:38.567271+00:00` にある依頼者の最新明示判断を今回の入力として採用する。原文は「②を選ぶ。description を新設してよい。連結元の文字列は「argonauts-uat public」、完成値は「argonauts-uat public (UAT)」とする。」。旧文書の「新設未承認・連結元未確定」という停止前提をこの回答で置換する。

## Solution

後続の承認された製品作業で `[project].description` を新設し、値を正確に `argonauts-uat public (UAT)` とする。これは依頼者指定の `argonauts-uat public` に、先頭ASCII空白を含むASCII ` (UAT)` を1回連結した値である。欠落値を空文字扱いしたり、nameから生成したり、存在しない旧descriptionを基準にしない。

本runはこの合意を文書化するだけで、製品を編集しない。依頼者による新設許可を、PM再承認や実装開始の承認と読み替えない。

## What makes it different

何もしない案では指定のUAT表記は加わらない。値の推測、依存更新や無関係な整形も必要ない。承認された新設と厳密な完成値、無関係な差分の排除を優先する。製品の市場優位性を主張する案件ではない。

## Who it serves

このBriefは後続の仕様確認・実装・受入で、許可された一点変更と禁止範囲を判断するために使う。読者像についての非重大な推論はA-1に分離し、製品の顧客像や固有の人物は創作しない。

## Success criteria

以下は後続の製品作業の受入条件であり、本runで合格を主張しない。

- **AC-1**: `[project].description` を新設し、完成値が正確に `argonauts-uat public (UAT)` と一致する。連結元は依頼者指定の `argonauts-uat public` であり、現物の旧値ではない。ASCII ` (UAT)` は完成値内に1回だけ含まれる。
- **AC-2**: description以外のTOML項目・依存・他製品ファイル・無関係な書式は不変。製品差分は `pyproject.toml` の当該キー新設だけ。検証スクリプトを作る場合は工程管理領域に限定し、他製品ファイルを増やさない。
- **AC-3**: 編集後の `pyproject.toml` がTOMLとして正常解析できる。解析成功だけでAC-1・AC-2を代替しない。

## Scope

製品変更の許可範囲は上記descriptionの新設のみで、他項目・依存・他製品ファイル・無関係な整形は対象外。工程は受付light指定より**full**を優先する。対象が危険パス `pyproject.toml` に該当するためであり、変更量の大小ではない。

本UPDATEは既存Briefフォルダ内の文書、merged template、memlog、必要なBMADレビュー記録、公式テンプレートが `html_view: always` とする既存閲覧用HTMLの更新に限定する。製品・OpenSpec・共通configは編集しない。実装、PM再承認、commit/push、Kanban操作、Architecture作成は行わない。次はPRDを同回答へ改訂し、後続の仕様承認へ渡すが、本runでその承認は実行しない。

The askはスポンサーへの提案ではないため、Visionは長期構想の依頼ではないため除外する。

## Assumptions

- **A-1 / Who it serves**: 主な読者を後続実装担当者と受入確認担当者と推定する。非重大・未承認の推論であり、固有名・組織・期限は設定しない。

## Open questions

未解決のopen_questionsは空（`[]`）。**OQ-1（Brief旧Q-1）は回答済み**。Problemに引用した依頼者回答によりdescription新設と指定連結元・完成値が確定した。旧未承認記述は履歴としてmemlogに保持し、現行前提にはしない。回答済みであることはPM再承認・実装・最終受入の完了を意味しない。
