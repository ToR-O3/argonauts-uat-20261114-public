---
title: "r-cf2eeaab — project.description の確定"
template: brief
version: 1.1.0
status: final
created: "2026-11-25"
updated: "2026-11-25"
author: Mary
---

# r-cf2eeaab — project.description の確定

## Table of Contents

- [Executive summary — 変更目的と判断](#executive-summary)
- [Problem — 追記対象の不存在](#problem)
- [Solution — 確定値の新規追加](#solution)
- [What makes it different — 代替案との違い](#what-makes-it-different)
- [Who it serves — 依頼者と工程担当者](#who-it-serves)
- [Success criteria — AC-1〜AC-3](#success-criteria)
- [Scope — 製品差分と工程境界](#scope)
- [Decision record — 判断原文と優先順位](#decision-record)
- [Open questions — 未決なし](#open-questions)

## Executive summary

依頼者の確定判断に従い、`pyproject.toml` の `[project]` に、現在存在しない `description` を新規追加し、値を厳密に `argonauts-uat public (UAT)` とする。旧依頼は既存説明文への追記だったが、実物には対象項目がない。今この作業で必要なのは、その不一致を解消し、実装者と受入担当者が同じ完成値を扱えるようにすることである。

製品差分はこの1項目だけとし、他のTOML項目・製品ファイルを変更しない。変更後のTOML解析成功も受入条件とする。本Briefは判断と境界を記録する工程文書であり、製品やテストの変更自体は行わない。flowはfull固定で、`pyproject.toml` は危険パスのためsmartでも人がマージする。

## Problem

依頼原文:

> pyproject.toml の [project] の description の末尾に「 (UAT)」を足す。変えるのは pyproject.toml だけ。未決事項は無い。

しかし現物の `[project]` は `name = "wordfreq"`、`version = "0.1.0"`、`dependencies = []` のみであり、`description` が存在しないことを直接確認した。旧条件だけでは追記先がなく、完成値を決められない。この点はPM確認済みであり、下記の最新依頼者判断で解決している。利用者の不満、金銭的損失、市場需要などは本依頼の根拠ではなく、主張しない。

## Solution

後続の実装で `[project].description` を新設し、完成値を `argonauts-uat public (UAT)` にする。これは既に接尾辞を含む確定値であり、さらに ` (UAT)` を追加しない。名称・バージョン・依存関係を含む他の項目は現状を保つ。

## What makes it different

何もしなければ説明文の追加要求を満たさない。存在しない既存値への機械的な追記や、確定値への二重追記も採用しない。最新判断をそのまま採用する方法だけが、推測で説明文を補わずに指定された完成状態を満たす。これは市場上の差別化ではなく、今回の変更判断の比較である。

## Who it serves

依頼者は指定した説明文を得る。PM、実装担当者、受入担当者、人によるマージ担当者は、旧指示との優先関係と検証可能な完成条件をこの文書で共有する。新しいユーザー像や製品用途は設定しない。

## Success criteria

- **AC-1:** `[project].description` を新規追加し、解析後の文字列が厳密に `argonauts-uat public (UAT)` と一致する。前後の空白や接尾辞の重複も不可。
- **AC-2:** 製品差分は `pyproject.toml` の当該1項目のみ。他の製品ファイル、既存のTOML項目とその値は不変とする。工程文書はPRに含めてよい。
- **AC-3:** 変更後の `pyproject.toml` がTOMLとして正常解析できる。

後続工程では文字列の厳密比較、製品差分の確認、TOML解析の結果で判定する。一つでも不成立なら受入不可。本Brief完成は製品の受入完了を意味しない。

## Scope

含むのは、後続の説明文1項目追加とその検証、および必要な工程文書。flowはfull固定とする。architecture変更は不要であり、動作・依存・他設定の追加、テストの追加・変更、他製品ファイルの編集は範囲外。外部調査は不要で、外部送信・権限変更・課金・データ消去は行わない。

本タスクで作成するのはBriefと公式工程上の付随文書のみ。kanban操作、git commit/pushは親が行う。`pyproject.toml` は危険パスであり、smartでも人がマージする。このBriefに自動マージの許可は含まれない。

`The ask` はスポンサーへの資金・時間の提案ではないため対象外。任意の `Vision` は長期構想が依頼範囲外のため設けない。次工程ではSofia（bmad-agent-po）が要求を文書化し、要求をさらに引き出す必要がある場合はJohn（bmad-agent-pm）が先にPRDを作成する。full固定の工程を省略する判断はしない。

## Decision record

最新依頼者判断の時刻は **2026-11-24T19:13:42.938043+00:00**。原文は次のとおり。

> 新しく作ってよい。完成後の説明文は「argonauts-uat public (UAT)」とする。

この判断が旧追記条件に優先する。PM確認済みの項目不存在を前提に、新規追加を採用し、完成値への追加の `(UAT)` は行わない。根拠は依頼原文、最新判断、現物 `pyproject.toml`、initiative文書 `_bmad-output/initiative-r-cf2eeaab/initiative-r-cf2eeaab.md`。initiative文書には題名のみがあり、新たな要件の根拠とはしない。

## Open questions

未決事項なし。未確認の重要入力や採用した推測はない。
