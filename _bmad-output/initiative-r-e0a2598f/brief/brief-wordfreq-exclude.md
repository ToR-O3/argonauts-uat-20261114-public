---
title: wordfreq 除外単語ファイル — Product Brief
template: brief
version: 1.1.0
status: draft
created: '2026-11-28'
updated: '2026-11-28'
sources:
  - ../initiative-r-e0a2598f.md
  - ../source-context.md
---
# wordfreq 除外単語ファイル

製品判断が未承認のため status は draft、headless 結果は partial。

## Table of Contents

- [Executive summary — 小さなCLI拡張](#executive-summary)
- [Problem — 不要語を結果から外す](#problem)
- [Solution — --exclude FILE](#solution)
- [What makes it different — 既存CLIとの一貫性](#what-makes-it-different)
- [Who it serves — 利用者と保守担当](#who-it-serves)
- [Success criteria — 受入の観測点](#success-criteria)
- [Scope — 変更範囲と除外範囲](#scope)
- [Assumptions — 未確認の利用背景](#assumptions)
- [Open questions — 製品判断ゲート](#open-questions)

## Executive summary

wordfreq に `--exclude FILE` を追加し、1行1語で指定した語を集計対象から外せるようにする。空行と `#` で始まる行は読み飛ばし、大小の違いは既存と同じ `str.casefold()` で同一視する。除外ファイルが存在しない場合は、分かる文をstderrへ出して終了コード2にする。CLI利用者が同じ除外語一覧を指定して実行できる、小さな既存機能拡張である。

実装だけでなく `--help`、READMEの使い方、追加試験を届ける。未指定時の既存動作、Unicode正規化、出力構造を壊さないことが成功の条件。利用者像と導入時期の業務上の理由は未確認であり、需要の証拠は今回の明示依頼に限られる。HTML総数などの未承認判断は共通の未決一覧に残し、下流で黙って確定しない。

## Problem

指定語を集計から外したいという依頼がある。現実装 `wordfreq/__main__.py` には top・min-count・format の選択肢があるが、語一覧による除外指定はない。従来の頻度閾値だけでは、回数の多い特定語を指名して外す要求を満たさない。

現場の手作業、発生頻度、時間損失、売上への効果は提示されていない。これらを数値や利用者の発言として補わない。

## Solution

利用者は除外語FILEを用意し、`python -m wordfreq input.txt --exclude excluded.txt` のように指定する。指定語の全出現が結果から消え、残る語は従来の規則で表示される。FILEがないときは成功した空結果ではなくstderrとexit2で失敗を認識できる。

大小同一視はASCIIのlower化ではなく、本文と同じcasefold。例えば本文の `Straße STRASSE` と除外語 `STRASSE` は同じ語として扱う。

## What makes it different

既存の抽出・並び・形式を維持しながら、回数によらず語を指名して除ける。min-countは回数で絞る既存の選択肢であり、この要求の代替ではない。外部ツールによる前処理も考えられるが、その利用実態や比較優位は未調査。競合優位や新しい市場は主張しない。

## Who it serves

既存CLIで特定語を外したい利用者が対象。保守担当と品質担当は、追加試験と未指定互換を根拠に変更を受け入れる。特定職種・個人・利用規模は未確認（Assumptions参照）。サーバー、Web UI、日本語形態素解析を必要とする利用者向けの拡張ではない。

## Success criteria

- 指定語の全出現が消え、未指定語の回数と同数初出順が保たれる。
- 空行と生の行頭 `#` コメントを無視し、Unicode casefold同値語を除外できる。
- 除外FILE不存在でstderrが理由を示し、exit2となる。
- helpとREADMEで使い方を発見できる。追加試験と既存試験により未指定互換を検証する。
- 対抗指標は既存出力・既存エラー・依存・CIの意図しない変更がないこと。現時点では機能の実装・試験は行っていない。

## Scope

含むものはオプション、除外語読込みと照合、help/README、回帰試験。text/json/htmlの結果語を共通に扱い、topとmin-countに除外語が表示枠を占有させない。

含まないものは新依存、外部通信、CI変更、正規化変更、並び変更、自動stopword辞書、複数ファイルの新しい利用方式、永続設定、HTMLデザイン変更。スポンサーへの予算要請ではないため The ask は省略。中長期ロードマップは依頼されていないため任意の Vision は省略。

## Assumptions

- [ASSUMPTION: Who it serves / Problem] 一覧を繰り返し指定できることが既存CLI利用者の価値になると推定する。依頼以外の利用者調査はない。
- [ASSUMPTION: Executive summary] 今回の変更要求を着手理由として扱う。業務上の締切、所有者名、投入時期は未提示。

## Open questions

未決の定義・根拠・回答者・必要時点・ブロック範囲は [共通一覧](../open-questions.md) に集約。HTML総数、空白とコメント、文字コードと他の読込み失敗、不正行、同時失敗の優先順位は未承認である。PRDはこの文書のパスを入力として使用し、承認済み範囲と未決を分離する。
