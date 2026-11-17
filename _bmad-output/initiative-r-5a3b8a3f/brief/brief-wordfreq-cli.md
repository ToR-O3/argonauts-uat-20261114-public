---
title: "wordfreq CLI Brief"
template: brief
version: 1.1.0
description: "Why to build a product, or pitching it, in a page or two."
not_for: "Committed work that needs requirements (`prd`); a formal funding decision on cost and return (`business-case`); testing a problem before any solution exists (`opportunity`)."
paced: true
facilitation_order: [problem, solution, what-makes-it-different, who-it-serves, success-criteria, scope, the-ask?, vision?, executive-summary]
guidance: guidance-planning
rubric: rubric-planning
view: "/home/Yuki/workspace/argonauts-uat-20261116/home/.hermes/profiles/argonauts-uat-architect/skills/bmad-agent-analyst/assets/brief-view.html"
html_view: always
status: final
created: "2026-11-17"
updated: "2026-11-17"
---

# wordfreq CLI Brief

## Table of Contents

- [Executive summary](#executive-summary) — 何を作るか、誰のためか、なぜ今か
- [Problem](#problem) — 頻度集計を専用の形で行う必要性
- [Solution](#solution) — 1コマンドで決定的な頻度出力
- [What makes it different](#what-makes-it-different) — 即席手順・既存パッケージとの差
- [Who it serves](#who-it-serves) — テキスト頻度を数えるエンジニア
- [Success criteria](#success-criteria) — 検証可能な受け入れ基準（WF ID 対応付き）
- [Scope](#scope) — v1 の境界と設計決定 D-1〜D-3
- [Assumptions](#assumptions) — headless 実行で立てた推定
- [Open questions](#open-questions) — 未決なし

## Executive summary

wordfreq は、テキストファイルを読んで単語の出現回数を多い順に表示する小さなコマンドラインツールである。`python -m wordfreq <file>` で実行し、表示件数は `--top N`（既定 10）、出力形式は `--format text|json` の 2 種類を選ぶ。単語の切り出し・正規化（大文字・小文字の同一視）を行う部品と、集計・出力整形を行う部品を分離し、入力元（標準入力や URL）を後から追加できる構成にする。画面（UI）は作らない。

主利用者はこの repository を使うエンジニアで、依頼者自身が今このツールを必要としている。追加は小規模で、データ消失・権限・外部送信・課金のリスクは小さい。価値は性能ではなく、正規化・並び順・出力形式の標準化と、入力元を拡張できる設計の明確さにある。仕様未決だった 2 点（空白で区切られない言語の扱い、同回数ワードの並び順）は、本 Brief の Scope で D-1・D-2 として決定した。

## Problem

依頼者はテキストファイルの単語頻度を知る手段を必要とし、専用ツールを依頼している。依頼本文に現在の運用や困りごとの事実記述はない。

想像する運用として、コーパスの下見・ログの把握・文章の推敲といった場面で `sort | uniq -c | sort -rn` のような即席のパイプラインを使うと、正規化の扱いが回数ごとに揺れ（大文字・小文字の同一視を忘れやすい）、機械可読な出力がなく、結果の再現性が人依存になる。この運用とコストは作成した仮説である（A-4）。確実なのは、依頼者が同じことを繰り返さず済む決定的な形を求めている点である。

## Solution

1 コマンドで頻度集計の結果がそのまま出るツールを作る。

- 実行: `python -m wordfreq <file>`。
- 件数: `--top N` で表示件数を指定（既定 10）。
- 出力: `--format text|json`。text は人が読む行形式、json は機械可読な配列（単語と回数）。
- 正規化: 単語の切り出しと大文字・小文字の同一視を、集計・整形から独立した部品として作る。
- 拡張性: 入力元を差し込める構成にし、その構成判断を設計文書に残す（ファイル以外の入力元そのものは v1 の作業範囲にしない）。

UI は作らない。部品の分離と入力元抽象は、どちらも「あとで足しやすくする」という依頼者の要求に直接応える。

## What makes it different

対抗案は (1) 即席のパイプライン、(2) 既存の PyPI パッケージ、(3) 何もしない。

即席パイプラインに対する優位は、正規化・並び順・出力形式が決定的で、テストで固定されていること。既存パッケージに対しては、ランタイム依存を増やさない標準ライブラリ中心の構成を優先する（依頼チームの方針）。位置取りは「自社リポジトリに置かれた、挙動が確定した最小ツール」であり、性能や多言語対応ではない。この比較は詳細調査をしない早断である（A-3）。

## Who it serves

主利用者は、テキストの頻度を数えるエンジニア（依頼者自身と、同じ repository を使う開発者）。成功は「調べるのに 1 コマンドで足りた」状態。依頼者自身が必要な点は依頼本文に裏付けがあり、より一般的な利用者像の一般化は推定である（A-1）。

## Success criteria

すべて受け入れカードで検証可能な形に落とす。WF・D ID との対応を付す。

1. `python -m wordfreq <file>` が実行でき、出現回数の多い順に出力する。`--top N` で表示件数を指定でき、既定は 10。（WF-01, WF-02）
2. 切り出し・正規化の部品と集計・出力整形の部品が分離している。分離は試験で確認できる形（部品を独立に呼ぶ単体試験）とし、入力元を追加できる構成の判断は WF-06 の設計文書に残す。（WF-04, WF-06）
3. `--format text|json` の 2 形式で出力でき、JSON は機械可読な構造（単語と回数の配列）。（WF-03）
4. pytest の単体試験があり、CI で通る。（WF-07）
5. 「まだ決まっていない点」2 件は明確な挙動として決定し、試験で確認できる。（D-1, D-2, D-3, WF-08）
6. 工程側の要求として、作業中に気づいたこと（はまった点、次に活かせる判断）を学習の候補として 2 件以上がこの依頼の記録に残る。要求・仕様工程でも気づいた点を記録する。

## Scope

**v1 に含める:**

- WF-01: `python -m wordfreq <file>` での実行。
- WF-02: `--top N`（既定 10）。N は 1 以上の整数。不正値は使い方エラー（非 0 終了・stderr）で終了。
- WF-03: `--format text|json`（既定 text）。不正値は使い方エラーで終了。
- WF-04: 単語の切り出し・正規化（大文字・小文字を同一視）を、集計・出力整形から独立した部品にする。各部品を独立に呼ぶ単体試験を付け、分離を機械的に確かめられる形にする。
- WF-05: 同回数ワードの並び順は決定論的とする（決定 D-2）。
- WF-06: 入力元（ファイル以外に標準入力・URL）を後から追加できる構成とし、構成判断を設計文書（OpenSpec 変更の design.md。ADR に相当するもの）に残す。
- WF-07: pytest による単体試験。CI で通る。対象は CI が使う現代的な CPython 3 の 1 つの版とし、バージョン横断の互換コードは不要とする。
- WF-08: 入力ファイル不存在とテキストデコード失敗はエラーメッセージを stderr に出して非 0 で終了する。空ファイルは結果 0 件として正常終了する。

**v1 の決定:**

- D-1（空白で区切られない言語）: v1 では対象外。空白・句読点を区切りとするトークナイザ前提とし、日本語のような言語の形態素解析は明示的に範囲外。トークナイザは差し替え可能な部品として設計し、将来の決定余地を残す。
- D-2（同回数ワードの並び順）: 出現回数の降順、同じ回数の単語は正規化後単語の昇順（辞書順）。決定論的で試験可能な挙動。
- D-3（切り出しの定義）: 単語は「Unicode の単語構成文字（Python `re` の `\w`。英数字・ underscore を含む）の連続する最大長」として抽出し、`str.casefold()` で正規化する。句読点・記号は単語に含めない。テストで確認できる形として仕様化する。

**v1 の範囲外:** GUI・画面、URL 入力そのもの（WF-06 の拡張性だけ）、日本語形態素解析の実装（D-1 により将来の決定待ち）、標準ライブラリ以外のランタイム依存の追加。依存管理上 `pyproject.toml` 等の追加が避けられない場合は、smart マージ方針で人の承認対象になることを前提に、必要最小限に留める。

## Assumptions

- A-1: 依頼者以外に頻度集計を必要とするエンジニアがいるという利用者像の一般化は推定。依頼者自身が必要な点は依頼本文に裏付けがある。
- A-2: 「ランタイム依存を増やさない（標準ライブラリ中心）」は PM 指摘からの方向性。追加が必要な場合の例外は Scope に記載。
- A-3: 既存 PyPI パッケージとの比較は詳細調査をしない早断。価値の所在（標準化と拡張性）が変わらない限り再調査は不要と判断。
- A-4: 即席パイプラインでの現在の運用とそのコストは作成した仮説で、依頼本文に事実記述はない。
- A-5: ローカルパッケージ名 `wordfreq` と同名の PyPI パッケージの取り違えは、依存を追加せず repository 内で `python -m` 実行する範囲では問題にならないと判断。外部パッケージを CI に入れる日が来たら再評価する。

## Open questions

なし。依頼本文の未決 2 点は Scope の D-1・D-2 として決定し、切り出しの定義も D-3 として決定した。
