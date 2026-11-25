---
title: "wordfreq HTMLの表示語種類数 — Brief"
template: brief
version: 1.1.0
status: final
created: "2026-11-26"
updated: "2026-11-26"
request: r-6ae2cbf2
persona: Mary
---

# wordfreq HTMLの表示語種類数 — Brief

## Table of Contents

- [Executive summary — 目的と今回の変更](#executive-summary)
- [Problem — 現状の不足](#problem)
- [Solution — 表示件数の追加](#solution)
- [What makes it different — 現状維持との差](#what-makes-it-different)
- [Who it serves — 読者](#who-it-serves)
- [Success criteria — 受入条件](#success-criteria)
- [Scope — 対象と対象外](#scope)
- [Evidence — 根拠](#evidence)
- [Assumptions — 推定](#assumptions)
- [Open questions — 未決事項](#open-questions)

## Executive summary

wordfreq の `--format html` 出力に、実際に表示した語の種類数を追加する。表の上の総出現回数の横で `表示 N 種類` を読めるようにし、表の行を数えなくても表示範囲を把握できるようにする。今回扱う理由は依頼 r-6ae2cbf2 による明示的な機能追加であり、利用調査や市場需要を根拠にした主張ではない。

N は固定の3ではなく、`--min-count`・`--max-count` による絞込みと `--top` 適用後の表示データ行数である。空入力や全件除外時は `表示 0 種類` とする。総出現回数の意味、text/json の出力は変更しない。後続の実装でテストと README の HTML 説明1行を追加する。本作業の成果物は文書のみである。

## Problem

現状の HTML は表の上に basename と総出現回数を示すが、表示語種類数を示さない。総出現回数は絞込み・top 前の値であり、表示行数ではないため、この値から表示種類数は分からない（根拠 E1、E2、E3）。手動で表を数える方法はあるが、その作業時間や不満の実測値は提供されていない。要求の根拠は依頼者の明示指定である。

## Solution

- **B1:** HTML の表より上、既存の総出現回数の横に `表示 N 種類` を追加する。
- **B2:** N は最終表示対象の件数と一致する。top の指定値、元入力の全種類数、出現回数の合計は使わない。空なら0。
- **B3:** 総出現回数は従来どおり全入力の集計値を維持する。表の順位・語・回数、並び順、既存の空結果案内も変えない。

## What makes it different

現状維持では表示種類数を手で数える。新表示なら総出現回数と表示種類数を別の値として同じ場所で確認できる。CLI 引数や別レポートを増やす案は不要で、既存 HTML のメタデータ内だけで要求を満たす。競争優位や新しい集計方式は主張しない。

## Who it serves

対象は wordfreq の HTML 出力を読む人。表の表示範囲を確認する際、総出現回数と混同せず表示語種類数を読めることを成功とする。具体的な利用者像は Assumptions に分離する。後続の Builder・品質担当には、件数の算出境界と互換性境界を渡す。

## Success criteria

- **B4:** 通常、top 制限、候補が top 未満、min/max 絞込み、空入力、全件除外で、`表示 N 種類` と実際の表データ行数が一致する。1種類など3以外の例も検証し、固定値実装を拒否する。
- **B5:** text/json の文字列・末尾改行・順序、既存総出現回数、終了コード・stderr の契約を維持する。HTML の安全なエスケープと静的文書の性質も維持する。
- **B6:** 後続実装で自動テストを追加し、README.md の既存 HTML 説明へ表示種類数の意味を説明する1行を足す。文書作成時点では製品実装・テスト実行済みとは扱わない。

## Scope

含むのは B1〜B6 の小変更と、そのために必要な既存 HTML テストの期待値更新のみ。HTML は意図的に変わるため、古い HTML 全バイト一致の期待値は新契約へ整合させるが、text/json の期待値は変更しない（E4）。

依存追加、権限変更、外部送信、データ移行、新 CLI 引数、集計やソートの変更、HTML 全体の再設計は含まない。スポンサーへの提案ではないため The ask は省略し、長期構想の依頼がないため Vision は省略する。

Architecture 文書は不要。既存 `format_html(pairs, basename, total)` は最終表示対象と総数を既に受け取り、メタデータを表の前に出す。部品境界や引数を変えずに表示対象の件数を示せるため、新たな設計判断を要しない（E1、E2）。次の引継ぎ先は John の PRD 作成とし、外部工程への実行は行わない。

## Evidence

- **E1:** `wordfreq/formatters.py:22–38,108–124` — 最終 pairs を順に出力し、既存メタデータは表より上。空結果案内あり。
- **E2:** `wordfreq/__main__.py:35–46` — 総数算出、min/max 絞込み、top、HTML 呼出しの順。
- **E3:** `README.md:19–29,55` — HTML の性質、総数の意味、形式と部品の契約。
- **E4:** `tests/test_formatters.py:94–134,164–175,218–262`、`tests/test_cli.py:201–260,425–441,711–741,858–908,1017–1029` — 厳密な構造・メタデータ・CSS・空結果・HTML を含む既存バイト期待値。
- **E5:** `_bmad-output/initiative-r-6ae2cbf2/initiative-r-6ae2cbf2.md` — frontmatter のみ。要求本文はこの依頼原文を用いた。

## Assumptions

- [ASSUMPTION: Who it serves] 主な利用者は、生成した HTML をローカルブラウザで読む既存 CLI 利用者とする。新たな利用者層・利用規模は仮定しない。
- [ASSUMPTION: 文書の深さ] 小規模な既存機能改善として扱う。規制・契約・公開期限など追加の条件は提示されていない。

## Open questions

なし。対象・件数境界・空結果・非変更範囲は依頼により確定している。
