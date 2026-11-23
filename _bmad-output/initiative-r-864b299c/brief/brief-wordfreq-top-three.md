---
title: 'wordfreq の上位3件の実行例'
template: brief
version: 1.1.0
status: final
created: '2026-11-24'
updated: '2026-11-24'
---

# wordfreq の上位3件の実行例

## Table of Contents

- [要約](#executive-summary) — 上位3件のコマンドを見つけやすくする
- [課題](#problem) — 既存の実行例に `--top 3` がない
- [解決策](#solution) — README にコマンドを1例追加
- [選んだ理由](#what-makes-it-different) — CLI を変えず、既存の例を残す
- [対象読者](#who-it-serves) — 手元の UTF-8 ファイルを集計する人
- [成功条件](#success-criteria) — 例の件数・書式・変更範囲
- [範囲](#scope) — 製品の変更は README のみ

## Executive summary

手元の UTF-8 テキストを `wordfreq` で集計する人が、オプションの説明からコマンドを組み立てずに、上位3件の指定を試せるようにする。既存の CLI は `--top 3` に対応しているため、README に実行例を1つ足すだけでよい。

## Problem

README は `--top N` を説明し、上位1件と2件の例を載せているが、上位3件を指定する例はない。

## Solution

README.md の「wordfreq の実行」に、既存の `--top 2` の JSON 実行例と同じ書式で `--top 3` の実行例を1つ追加する。結果は最大3件で、3種類未満なら全件を表示する。

## What makes it different

読者は例のファイル名を手元の UTF-8 ファイルに置き換えるだけで試せる。既存例も引き続き参照できる。

## Who it serves

リポジトリ直下から `wordfreq` を実行し、結果を上位3件までに絞りたい README の読者。

## Success criteria

製品の差分が README.md の既存コードブロック内の1行追加のみで、既存行の変更や削除がないことを確認する。正規化後に4種類以上の語が残る入力で追加例を実行し、終了コード0と上位3件の出力を確かめる。

## Scope

実行例の追加だけを対象とする。CLI の仕様・挙動、プログラム、試験は変更しない。
