---
title: "wordfreq --max-count Brief"
template: brief
version: 1.1.0
status: final
created: "2026-11-25"
updated: "2026-11-25"
request: r-d4bcda40
---

# wordfreq --max-count Brief

## Table of Contents

- [Executive summary](#executive-summary) — 変更の目的
- [Problem](#problem) — 現行CLIの制約
- [Solution](#solution) — 上限と下限の両条件
- [What makes it different](#what-makes-it-different) — 既存機能との差
- [Who it serves](#who-it-serves) — 利用者と読者
- [Success criteria](#success-criteria) — 固定受入 B1–B6
- [Scope](#scope) — 変更境界とArchitecture
- [Evidence and derivations](#evidence-and-derivations) — 原文・現状・導出
- [Assumptions](#assumptions) — 非阻害の利用者推定
- [Open questions](#open-questions) — 未決事項

## Executive summary

wordfreq に整数オプション `--max-count N` を追加し、正規化後の出現回数が N 以下の単語だけを表示する。省略時は上限を設けず、既存の出力と互換にする。`--min-count` と併用でき、両条件を満たした語に既存の並び順と `--top` を適用する。

これは既存CLIの頻度上限指定を求める依頼 r-d4bcda40 への局所的拡張である。低頻度語や頻度帯を選ぶ利用場面を想定するが、顧客調査・利用実績・事業指標は提示されていない。今扱う理由として確実なのは今回の変更依頼であり、外部締切や市場事情は主張しない。実装担当と品質担当は、以下の受入条件を PRD へ引き継ぐ。

## Problem

現行CLIは `--min-count` により下限未満を除外できるが、上限による除外はできない。`--top` は表示種類数の制限であり頻度上限の代用ではない。これは `wordfreq/__main__.py` の引数定義と選択条件で確認できる制約である。ユーザーの原文が機能需要の根拠であり、既存ユーザーの手作業やその費用を観測した証拠はない。

## Solution

同じ入力・同じ text/json/html 形式のまま、最大頻度を指定できるようにする。指定時の選択条件は `min_count <= count <= max_count`、省略時は既存の `min_count <= count` とする。非整数・値欠落は既存の argparse と同じ使い方エラー exit2。正常入力の全件除外は既存の空結果形式と exit0 を維持する。

## What makes it different

下限のみの現状と異なり、上限のみ、または両端を含む頻度帯を指定できる。何もしない場合はこの選択をCLI内で表現できない。外部での後処理は代替案になり得るが、採用状況は不明である。優位性は共通の選択処理で全形式に同じ語・回数・順序を渡せる点に限り、市場での独自性は主張しない。

## Who it serves

対象は既存 wordfreq の頻度選択を使うCLI利用者と想定する（推定の扱いは Assumptions）。文書の直接の読者は、この依頼を実装・検証する担当者である。成功は上限・下限を予測可能に指定でき、従来の利用を壊さないこととする。

## Success criteria

- **B1:** `--max-count` は整数オプションで、省略時は上限なし。未指定の既存出力・終了コードを維持する。
- **B2:** 指定値以下の語だけを残す。指定値と同じ出現回数の語を含み、指定値を超える出現回数の語を除く。
- **B3:** `--min-count` と同時指定でき、両条件を満たす語だけを残す。
- **B4:** 追加試験と全既存試験が成功する。境界・全形式・エラー・既存互換を検証する。
- **B5:** README.md に使い方の例を1つ追加する。候補は `python -m wordfreq input.txt --min-count 2 --max-count 3 --format json`。
- **B6:** 依存更新、CI変更、見た目変更、無関係変更を含めない。

## Scope

対象は引数、全形式に共通の頻度選択、その追加試験、README の例と新オプションに直接関わる説明である。Unicode抽出・casefold、回数降順・同数初出順、選択後top、HTMLの全フィルタ前総数、既存の空状態・UTF-8・escape・入力エラーを維持する。

新Architecture文書は不要。`wordfreq/__main__.py` の既存共通filterへの局所追加で足り、入力取得・集計・整形の境界、部品API、依存を変更しないためである。境界変更が必要と判明した場合のみ別途再判断する。スポンサーへの資金提案ではないので The ask は除外し、長期拡張を約束しないため任意の Vision も除外する。本作業は Brief と PRD の作成のみで、製品コード・試験・README 自体は変更しない。

## Evidence and derivations

**明示要求:** ユーザー原文は「整数」「指定しなければ上限なし」「出現回数がその値以下」「--min-count と一緒に使える」。固定受入 B1–B6 は依頼に基づく。

**確認済み現状:** `wordfreq/__main__.py:13–38` は min-count を `type=int`・既定1・1以上とし、元Counterから総数を求め、下限選択後にtopへ渡す。`aggregator.py:11–17` は回数のみの安定ソート。`formatters.py` と `tests/test_cli.py` は全形式の空結果・HTML総数・順序を規定する。README、OpenSpec、pyproject.toml も照合した。initiativeファイルは管理frontmatterのみで要件チケットではない。

**要求からの導出であって既存仕様ではない:** max-count に正値限定は指定されていないため、argparse `type=int` が受け取る0・負数を含む整数を受理する。実出現回数は正なので、上限0・負数では選択集合が空になる。下限が上限より大きい場合も両条件の共通部分が空になる。どちらも正常入力なら既存の全件除外と同じ exit0 とする。新しい正値制限・大小関係エラーは加えない。有効な整数でも入力読込みを省略してはならず、不存在等の入力失敗は exit1 を維持する。この導出に追加の製品判断は要らない。

## Assumptions

- [ASSUMPTION: Who it serves] 一次利用者は低頻度語・頻度帯を抽出したい既存CLI利用者と推定する。個別顧客と需要規模は不明。受入条件の解釈には影響しない。担当: 要求担当。実利用者への説明が必要になった際に再確認する。

## Open questions

なし。利用者像の非阻害推定は上記に明示した。未実施の製品試験を合格と扱わず、実装後の受入に残す。
