---
title: "wordfreq 除外ファイル機能 Brief"
template: brief
version: 1.1.0
status: draft
created: "2026-11-28"
updated: "2026-11-28T07:17:58+00:00"
request: r-6442a149
---

# wordfreq 除外ファイル機能 Brief

## Table of Contents

- [Executive summary](#executive-summary)：回答済み仕様と位置づけ
- [Problem](#problem)：現行の制約
- [Solution](#solution)：採用した利用体験
- [What makes it different](#what-makes-it-different)：現状維持との差
- [Who it serves](#who-it-serves)：想定利用者
- [Success criteria](#success-criteria)：SC-01〜SC-06とPRD対応
- [Scope](#scope)：対象・今回の文書更新境界
- [Assumptions](#assumptions)：背景の推定 A-01〜A-03
- [Open questions](#open-questions)：背景不足 OQ-7・OQ-8のみ

## Executive summary

wordfreqへ任意の `--exclude FILE` を追加し、本文を書き換えずに指定語を集計対象から外す。回数・件数ではなく語そのものを選べる。不要語を外したい既存CLI利用者を想定するが、実在利用者や業務上のwhy nowは未確認であり、便益数値は置かない。

受付t_c172b029の人default回答（2026-11-28T06:59:36.405633+00:00）『提案のまま進めてください（1〜6のとおり。既存の集計に合わせ、追加の文法は設けない）。』、PM判断t_834ece37と差戻しt_14fbf7f0により、旧製品未決1〜6を解決した。[PRD](../prd/prd-wordfreq-exclude.md)が期待値の原本、[決定記録](../decisions-oq1-6.md)が回答と解決来歴である。casefoldやstripは未承認案ではなく採用仕様となった。

解決済みIDの索引（未決一覧ではない。採用値はSolutionとPRD、回答日時は上記）：

| ID | 解決した内容 |
| --- | --- |
| OQ-1 | casefold比較。SC-03を参照 |
| OQ-2 | 空白・コメント・改行。SC-02を参照 |
| OQ-3 | UTF-8/BOM・読込失敗。SC-04を参照 |
| OQ-4 | 行全体一語・最後FILE。SC-01/SC-02を参照 |
| OQ-5 | 全語除外の既存空結果。SC-06を参照 |
| OQ-6 | 引数→除外→本文の順序。SC-04を参照 |

今回はBrief・PRD・設計とレビューの更新のみ。機能実装、help／README／試験の追加、回帰合格は後続であり、本書は実装済みの報告ではない。背景不足OQ-7/8を残すためheadless結果partial／文書draftとするが、機能受入の停止理由や新条件にはしない。

## Problem

現行の `--min-count` は回数、`--top` は表示件数を絞るだけで、語を指定して除く選択肢はない（`wordfreq/__main__.py:13-19`）。特定語を外したい依頼はあるが、現在の回避策・頻度・負担の実測は未提供である。

## Solution

UTF-8の除外ファイルを読み、先頭BOMを除去する。行前後をstripし、空行と先頭#の行は無視、それ以外は行全体を一語としてcasefold比較する。行内コメント、分割、記号除去の文法は設けない。LF／CRLF／終端改行なしに対応する。

既存本文casefoldを維持し、本文 `STRASSE` も除外行 `Straße` で除く。`foo bar` はfoo/barを個別除外せず、`foo_bar`・`123`・`foo-bar` は文字列そのまま扱い、本文に現れない項目は無影響。重複は無影響、複数の `--exclude` は最後のFILEだけを読み、それ以前は読まない。

処理は既存引数検証→除外FILE→本文。除外読込失敗（不存在・権限不足・ディレクトリ・不正文字コード等）は対象と原因をstderr、exit2、stdout空。文言完全一致は不要。両ファイル失敗でも除外を先行し、除外成功＋本文失敗は既存exit1。全語除外は既存の各形式空結果、正常exit0で、除外専用メッセージを足さない。既存HTMLの空結果案内は残す。

## What makes it different

現状維持では回数と件数しか絞れない。本追加は元の本文を変更せずに語を選べる点に意味がある。市場優位・外部製品との比較や追加依存の提案には広げない。

## Who it serves

主利用者は不要語を外したい既存CLI利用者と想定する（A-01）。後続の要求・実装・試験担当は、採用仕様と背景不足を読み分ける読者。具体的利用者・部署・スポンサーは未提供である。

## Success criteria

以下は後続で確認する事項であり、本工程の試験合格を意味しない。詳細期待値と異常系はPRDの同じFR番号を参照する。

| ID | 確認事項・追跡先 |
| --- | --- |
| SC-01 | 任意の除外指定で全出現を除き、重複無影響、複数指定は最後だけ。PRD FR-1／RULE-1。 |
| SC-02 | strip→空／先頭#無視→全体一語、LF／CRLF／終端改行なし、分割・行内コメントなし。PRD FR-2。 |
| SC-03 | 本文・除外行ともcasefoldし、Straßeで本文STRASSEを除く。PRD FR-3、設計AD-3。 |
| SC-04 | UTF-8／先頭BOM、除外読込失敗のstderr・exit2・stdout空と検証→除外→本文の順を確認。PRD FR-4。 |
| SC-05 | 後続でhelp／READMEに採用仕様を説明し、対応試験を追加。PRD FR-5。 |
| SC-06 | 未指定互換性、各形式の既存空結果exit0、残存回数・相対初出順、除外後min-count/top前のHTML総数を維持。PRD FR-6／RULE-1。 |

例：本文 `Zoo apple APPLE zoo banana`、除外appleはzoo/count2、banana/count1、HTML総数3。min-count2/top1でも総数3。全語除外はtext空・JSON `[]\n`・HTML既存空表と案内、総数0。過去runの試験記録はmemlogの履歴であり、今回の新機能合格根拠にしない。

## Scope

対象は上記除外機能と未指定互換性。全形式共通で除外→計数→min-count→top、残存語の回数・相対初出順を保存し、HTML総数は除外後・min-count/top前とする。追加依存・権限変更・外部送信を必要としない。

今回変更するのはBMAD原本文書・決定／レビュー／手順記録のみ。製品・README・試験・initiative・GSD計画は変更せず、Git／Kanban操作も行わない。OpenSpecは親担当。The askはスポンサーへの提案でなく、Visionは根拠のない長期拡張になるため対象外という従前の節採否を維持する。

根拠は依頼原文・明示回答、既存原本とmemlog、frontmatterのみのinitiative、現行tokenizer・aggregator・CLI・formatter・sourcesの実読。本文抽出は `\w+`、正規化はcasefold、順位は回数降順・同数時初出順。これらを除外行の分割規則へ流用しない。

## Assumptions

- A-01（Problem / Who it serves）：[ASSUMPTION: 主利用者は不要語を外したい既存CLI利用者。実在利用者・負担・回避策は未確認。]
- A-02（Executive summary）：[ASSUMPTION: 今回の依頼を検討の契機と扱う。期限や事業上のwhy nowは推定しない。]
- A-03（全体）：[ASSUMPTION: 小規模内部CLI変更相当として分量を設定。公開・契約上の義務は未確認。]

## Open questions

未解決は[未決一覧](../open-questions.md)とPRDのOQ-7/8のみ。旧Q-01〜Q-05の製品境界は決定記録の旧OQ-1〜6で解決し、旧Q-06の背景不足はOQ-7へ統合した。

| ID | 背景不足 | 担当／再訪時点 |
| --- | --- | --- |
| OQ-7 | 具体的利用者・困り方・why now・業務成功尺度。 | PM→依頼者／価値評価時。機能受入へ新たな経済指標を加えない。 |
| OQ-8 | 公開・契約上の義務と引渡し条件。 | PM→依頼者／公開・引渡し条件設定時。現時点で義務を追加しない。 |

いずれも背景不足の記録であって停止理由ではない。後続は親の仕様統合と必要な要求整理へ渡し、この工程で実装・計画を開始しない。
