---
title: "wordfreq keywords 追加 Brief"
template: brief
version: 1.1.0
status: final
created: "2026-11-25"
updated: "2026-11-25"
---

# wordfreq keywords 追加 Brief

## Table of Contents

- [Executive summary — 目的と引継ぎ](#executive-summary)
- [Problem — 未設定のメタデータ](#problem)
- [Solution — 指定1行](#solution)
- [What makes it different — 最小差分](#what-makes-it-different)
- [Who it serves — 実装・品質・マージ担当](#who-it-serves)
- [Success criteria — 検証条件](#success-criteria)
- [Scope — 境界と除外](#scope)

## Executive summary

依頼は、`pyproject.toml` の `[project]` に `keywords = ["wordfreq"]` の1行を追加すること。現状のファイルには keywords がない。既存設定を保ち、製品の変更をこの1行に限定する。

このBriefと後続PRDは、実装・品質確認・人によるマージの判断に必要な境界を記録する。変更理由は明示された依頼への適合であり、市場効果や利用者増加を主張しない。工程は決定済みの full。ここでは製品を変更せず、後工程でTOML解析、値の一致、製品差分1行を確かめる。危険パスである `pyproject.toml` は人がマージする。

## Problem

`[project]` に指定の keywords が未設定で、依頼されたメタデータ状態を満たしていない。確認できたのはファイルの現状と依頼のみであり、利用者の困りごと、損失額、緊急性は追加で推測しない。

## Solution

既存の `[project]` 内に、独立した1行として `keywords = ["wordfreq"]` を追加する。名前、バージョン、依存関係、ビルド設定、既存の書式は維持する。実行時の振る舞いは変更対象にしない。

## What makes it different

何もしなければ依頼を満たさない。一方、設定全体の整形や他メタデータの修正は依頼範囲を超える。指定1行だけの追加なら、要求への適合と既存設定維持を小さな差分で確認できる。製品の独自性を売り込む変更ではない。

## Who it serves

Builderは指定1行を実装する。品質担当は内容と差分の両方を独立に確認する。人のマージ担当は危険パスの変更を判断する。この文書はその引継ぎ用であり、新しい顧客像は定義しない。

## Success criteria

後工程で、次の全条件を満たすこと。

- 変更後の `pyproject.toml` がTOMLとして正常に解析できる。
- 解析結果の `project.keywords` が配列 `["wordfreq"]` と完全一致する。
- 製品差分が `pyproject.toml` の指定1行の追加だけで、既存行の削除・書換えや他の製品ファイル変更がない。

本Briefの作成は検証成功を意味しない。実装後に実在する検証ファイルをBuilder・品質が実行し、結果を残す。

## Scope

製品変更は `pyproject.toml` だけ。工程文書は許可され、PRに含める。製品にテストファイルを追加しない。必要な検証スクリプトを工程文書配下に置く計画は許可されているが、本工程では作成・試行しない。

外部調査とArchitectureは、一つのメタデータ追加で構成変更がないため不要。スポンサー向けの提案ではないので The ask は対象外。単一変更の確定依頼なので任意の Vision は設けない。未決事項・追加仮定はない。次はJohnがこのBriefを入力としてPRDを作成する。
