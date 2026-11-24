---
title: "README の --min-count 3 実行例"
template: brief
version: 1.1.0
status: final
created: "2026-11-25"
updated: "2026-11-25T06:53+09:00"
---

# README の --min-count 3 実行例

## Table of Contents

- [Executive summary — 最新判断と目的](#executive-summary)
- [Problem — 説明の不足](#problem)
- [Solution — 追加する例](#solution)
- [What makes it different — 最小の追記](#what-makes-it-different)
- [Who it serves — 読者と担当](#who-it-serves)
- [Success criteria — 受入は2条件だけ](#success-criteria)
- [Scope — 全差分と工程原本の扱い](#scope)
- [Decisions — 判断の日時・原文・失効](#decisions)
- [Assumptions — 前提](#assumptions)
- [Open questions — 未決事項](#open-questions)

## Executive summary

README の使い方に `python -m wordfreq input.txt --min-count 3` の実行例を1つ追加する。既存 CLI を使う読者への説明追加で、新機能ではない。最新の依頼者判断により、受入で確かめるのは「例が1つ追加されたこと」と「最終PRの全変更が README.md だけであること」の2点だけとする。

text・json・html の3形式実行とその入力・出力・実行証拠は対象外。full の Brief→PRD は維持する。本仕様工程は文書の更新であり、README 編集や製品の実行確認を行わない。文書の final は製品の受入済みを意味しない。

## Problem

従来の Brief が記録した不足は、README の使い方に閾値3の実行例がないこと。今回の更新は新たな利用者調査ではなく、依頼者が検証を2点に縮小した判断を反映する。損失額や利用効果は推測しない。

## Solution

追加例は `python -m wordfreq input.txt --min-count 3` の1つを維持する。既存例と説明を保ち、無関係な改稿や追加機能は含めない。判定には README 原本と差分の文字確認を用い、CLI を起動しない。

## What makes it different

現状維持では指定例の追加を満たさない。一方、3形式の実行確認まで広げると最新依頼を越える。指定例1つに絞ることが今回の価値であり、競争優位は主張しない。

## Who it serves

主読者は README の使い方を参照する CLI 利用者。後続 Builder が追記と自己確認、quality が独立確認、PM が原本文字証拠の読取りと受入を担当する。今回の文書セルフチェックと、親が行う更新原本の独立レビューは別である。

## Success criteria

1. README.md に `python -m wordfreq input.txt --min-count 3` の実行例が1つ追加されている。README 原本と差分を文字で確認する。
2. 最終PRの `base...head` の全変更ファイルが README.md だけである。工程文書を含む全差分を対象とし、パス除外による見かけ上の「READMEのみ」は認めない。

証拠はこの2条件を判断できる README 原本・差分・全変更ファイル一覧と文字判定に限定し、PM が read_file で読める形で渡す。製品CLIの実行結果は求めない。

## Scope

README の指定例1つが製品変更の範囲。実装、試験、ツール、依存、設定、公開入出力を変えない。3形式実行、検証用入力、期待出力、終了コード、stdout／stderr、語の残存／除外の実行証拠は対象外であり、追加の受入条件にしない。

Brief・full PRD・memlog・レビュー・HTML は工程原本であるが、Git差分から隠してよい例外ではない。full仕様工程では文書をGitへ保存・pushし、工程原本をカードへ添付する。最終PRを指定ファイルだけに整える後続工程で、チームD.5手順により工程文書をPRから外す。整理後の最終PRの `base...head` 全変更が README.md だけかを確認する。今回の委任ではGit・kanban操作や添付を実行しない。

Architecture は不要。説明追加だけで設計や公開契約を変更しないため。The ask はスポンサー提案でないため、Vision は長期構想を要しない限定変更のため省略する。

## Decisions

日時: 2026-11-25T06:53+09:00。親が受付正本で確認した最新依頼者判断の原文:

> 検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。

理由は依頼者による検証範囲の縮小。過去の3形式実行とその入力・出力・証拠の受入条件は失効し、現行要件から削除した。旧レビューは履歴であり、更新版への合格証ではない。full、指定追加例、Architecture不要、未決事項なしは維持する。

## Assumptions

未確認の要件上の前提なし。現在の README や最終PRの充足を本更新で確認したとは主張しない。

## Open questions

なし。README 追記、工程原本の保存・添付、D.5による最終PR整備と2条件の確認は後続作業であり、仕様上の未決事項ではない。
