---
title: wordfreq HTML出力 Brief
template: brief
version: 1.1.0
status: final
created: 2026-11-17
updated: 2026-11-17
---
# wordfreq HTML出力 Brief

## Table of Contents
- [Executive summary](#executive-summary)
- [Problem](#problem)
- [Solution](#solution)
- [What makes it different](#what-makes-it-different)
- [Who it serves](#who-it-serves)
- [Success criteria](#success-criteria)
- [Scope](#scope)
- [Assumptions](#assumptions)

## Executive summary
依頼 r-50053edc は、既存CLI利用者からの今回の要望に応え、wordfreqの集計結果をブラウザで閲覧できる自己完結した静的HTMLを追加する。利用者はCLIの標準出力をファイルへ保存して開き、入力ファイル名と入力全体の総出現回数、順位・単語・回数の表を確認できる。外部通信もWebサーバーも不要とする。

既存の回数降順は保ち、同数時の語の昇順だけを初出順へ意図的に変更する。text・json・htmlの順序を揃える。明るい背景、切替なし、1からの表示行連番、画面の判定方法は依頼で決定済みであり、再質問しない。現時点は要求整理であり、実装・ブラウザ合格を示すものではない。

## Problem
現在の製品はtextとjsonだけを出力する。ブラウザでファイル名・総数と表をまとめて見るには利用者側の整形が必要になる。依頼者が求めた改善を根拠とし、利用人数、費用、需要の大きさは不明であり創作しない。

## Solution
`python -m wordfreq <file> --format html` が1枚のHTMLをstdoutに出す。表より上にbasenameのみと、top制限前の総出現回数を示す。簡素な明るい画面で、320 CSS pxを含むスマートフォン幅でも長い語・ファイル名を読めることを目指す。HTML特殊文字を安全に表示し、既存の単語認識・入力境界を保つ。

## What makes it different
textの直接閲覧やJSONの別ツール整形に対し、保存したHTMLだけで結果の文脈と表を確認できる。競合優位や市場の新規性は主張しない。初出順への変更は従来の語順と異なるため、互換性変更として仕様・試験に残す。

## Who it serves
対象は既存wordfreqのファイル集計結果をブラウザで見たいCLI利用者。固有の人物像や利用規模の証拠はない。品質担当は実CLIからHTMLを独立して生成し、画面と証拠を照合する。

## Success criteria
AC1–AC6の原文はuat-publicボードのカードt_db216d64、展開した要求は[同依頼PRD](../prd/prd-wordfreq-html.md)のFR-1–FR-6を参照する。
- AC1–AC2: 自己完結HTMLの3列表、basename、top前総数が実CLI出力と一致する。
- AC3: 同数語が語の昇順と異なる入力およびtop境界で、全形式が初出順になる。
- AC4: 通常幅・320 CSS pxで長文の横方向の収まり、切取り祖先内の収まり、隣接内容との非重複、実画像の可読性を満たす。文字範囲の実測原本を残す。要素自身への厳格な縦包含は必須にしない。
- AC5–AC6: 注入・外部通信を起こさず、空入力と既存エラーの回帰を試験する。品質担当の独立ブラウザ確認でhead・入力・コマンド・結果・文字範囲・画像を条件へ対応付ける。
対になる保護指標は、同数時順序以外の既存text/json構造・入力処理に不要な変更がないこと、CIの追加・変更がないこと。

## Scope
含むのはHTML出力、basenameとtop前総数、レスポンシブ表示、全形式の同数時初出順、安全性と検証証拠。生成日時、暗色・テーマ切替、対話操作、サーバー、標準入力・URL入力、単語認識の変更、CIの追加・変更は含めない。資金調達の提案ではないためThe askは省略し、長期Visionは今回の範囲外とする。新規アーキテクチャ文書は不要と判断する。既存の入力・トークナイズ・集計・整形境界を維持した局所変更としてOpenSpec designで決定を記録する。

## Assumptions
- [ASSUMPTION: Who it servesと閲覧場面では、詳細属性が未提供のため、既存CLI利用者がファイルへ保存して閲覧する場面を説明用に想定する。製品の追加要件ではない。]
未解決の製品判断はない。実装後の可否は後続の試験で判断する。
