---
title: "r-774f3cd6 — pyproject description UAT"
template: brief
version: 1.1.0
status: draft
headless: true
intent: create
workflow: "Mary CREATE → bmad-facilitate"
output: "_bmad-output/initiative-r-774f3cd6/brief/"
created: "2026-11-24"
updated: "2026-11-24"
---

# r-774f3cd6 — pyproject description UAT

## Table of Contents

- [Executive summary](#executive-summary) — 依頼、実行境界、現状の障害
- [Problem](#problem) — description不在という根拠
- [Solution](#solution) — 正確な連結と停止条件
- [What makes it different](#what-makes-it-different) — 差分最小化
- [Who it serves](#who-it-serves) — 文書の利用者
- [Success criteria](#success-criteria) — AC-1〜AC-3
- [Scope](#scope) — full優先、文書のみ
- [Assumptions](#assumptions) — 推論の明示
- [Open questions](#open-questions) — Q-1の解消条件

## Executive summary

依頼原文は「pyproject.toml の [project] の description の末尾に『 (UAT)』を足す。変えるのは pyproject.toml だけ。未決事項は無い。」である。将来の製品変更は既存文字列に正確なASCII ` (UAT)` を1回連結することだけであり、他項目・依存・他の製品ファイルを変更しない。本runはその変更を実行するものではなく、Briefと公式工程成果物だけを作成する。

ただし、この作業場所の `pyproject.toml` を直接読んだ結果、`[project]` に `description` は存在しなかった。したがって既存値を前提とする受入条件は現状では評価できない。空文字を補う、別の項目から文章を作る、descriptionを新設する、といった代替は承認されていない。製品変更を開始せず、Q-1の解消を待つ。依頼者が「未決事項は無い」とした事実と、この現物上の矛盾を区別する。

## Problem

根拠は作業場所 `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-b/.worktrees/t_e422af74` の `pyproject.toml` 全文と、既存initiative文書 `_bmad-output/initiative-r-774f3cd6/initiative-r-774f3cd6.md`。後者はinitiative名だけを保持し、descriptionの値を指定していない。

現物の `[project]` は6〜8行の `name = "wordfreq"`、`version = "0.1.0"`、`dependencies = []` のみ。10行から別テーブルとなるため、既存descriptionの取り落としではない。依頼どおりの変換には入力文字列が欠けている。市場課題・利用者の損失・期限についての根拠はなく、創作しない。

## Solution

Q-1解消後の製品作業で、変更前TOMLから `[project].description` の文字列を取得し、その値にASCII ` (UAT)` をちょうど1回連結する。既存末尾を正規化・削除しない。既に同じ接尾辞があっても、依頼は重複除去ではなく既存値への1回の連結である。本runでは編集も編集後検証も行わない。

descriptionが欠落している現在は停止する。値や新設権限を推測せず、依頼者による入力・制約の明確化または正しい対象の提示を待つ。

## What makes it different

何もしない案ではUAT表記は加わらない。一方、descriptionの新設や依存更新は指定を逸脱する。本件の優先は拡張ではなく、既存値への厳密な連結と無関係な差分の排除にある。製品の独自性・市場優位性を主張する案件ではない。

## Who it serves

このBriefは、依頼された一点の変更を後続で実装・受入するための境界と検証条件を示す。利用者に関する推論はAssumptionsに分離する。製品の顧客像や新規ユーザー獲得は本件の入力にない。

## Success criteria

以下は後続の製品作業の受入条件であり、本runで合格を主張しない。

- **AC-1**: 変更前の `[project].description` が文字列として存在し、変更後が `before.description + ' (UAT)'` と完全一致する。現状は前提不成立。
- **AC-2**: `description` を除くTOMLの全項目が変更前後で一致し、依存を含め他項目は不変。他の製品ファイルも不変で、製品差分は当該descriptionだけ。工程管理成果物は別扱いとする。
- **AC-3**: 編集後の `pyproject.toml` がTOMLとして正常解析できる。解析成功だけでAC-1・AC-2を代替しない。

## Scope

製品変更の許可範囲は `pyproject.toml` の `[project].description` への正確なASCII ` (UAT)` の1回連結のみ。他項目、依存、他製品ファイル、書式の無関係な整形は対象外。

工程は受付light指定よりfullを優先する。理由は対象が危険なパス `pyproject.toml` に該当するという確定制約であり、変更量の大小ではない。この判断は後続文書にも引き継ぐ。

このBrief作成工程は文書だけを書く。製品・Git・Kanban操作、実装、不要な調査、Architectureは行わない。この工程の成果物は指定フォルダ内のBrief、merged template、memlog、必須レビュー記録、および必須例外の閲覧用HTMLに限定する。HTMLは `.template.md` の11〜12行にある公式view指定と `html_view: always` に従うもので、任意の追加出力ではない。任意のThe askはスポンサーへの提案ではないため除外し、任意のVisionは長期構想の依頼ではないため除外する。

## Assumptions

- **A-1 / Who it serves**: 文書の主な読者を後続実装担当者と受入確認担当者と推定する。固有名・組織・期限は設定しない。内部工程向けの小規模変更として文書を最小限にするための非重大な推論である。

## Open questions

- **Q-1 / blocker / 依頼者**: 現物にdescriptionがない状況で、どの既存文字列を連結元にするのか。既存descriptionを含む正しい対象を提示するか、description新設とその元値を明示的に承認し制約を改訂する必要がある。再確認条件は依頼者の明確化を受領した時点。headlessのため質問送信や推測による解決はしない。これは現物との矛盾に基づく項目であり、依頼者が未決事項を提示したという意味ではない。
