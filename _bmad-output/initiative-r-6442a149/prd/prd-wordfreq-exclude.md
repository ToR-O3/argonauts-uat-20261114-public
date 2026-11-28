---
title: "wordfreq 除外ファイル PRD"
template: prd
version: 1.1.0
status: draft
created: "2026-11-28"
updated: "2026-11-28"
request: r-6442a149
---

# wordfreq 除外ファイル PRD

## Table of Contents

- [Document purpose](#document-purpose)：原本・判断範囲
- [Vision](#vision)：目的
- [Users and journeys](#users-and-journeys)：想定利用
- [Glossary](#glossary)：用語
- [Features and requirements](#features-and-requirements)：六条件 FR-1〜FR-6と直接検証
- [Rules](#rules)：帰結と制約 RULE-1〜RULE-2
- [Non-goals](#non-goals)：対象外
- [MVP scope](#mvp-scope)：今回の範囲
- [Success metrics](#success-metrics)：SM-1〜SM-2
- [Quality and constraints](#quality-and-constraints)：運用制約
- [Change boundary](#change-boundary)：互換境界
- [API contract and versioning](#api-contract-and-versioning)：CLI公開面
- [Developer experience](#developer-experience)：案内
- [Decisions](#decisions)：節の採否
- [Assumptions](#assumptions)：未確認前提
- [Open questions](#open-questions)：担当・必要時点・影響 OQ-1〜OQ-8

## Document purpose

要求整理・実装・試験担当向けに、`wordfreq --exclude FILE` の六つの受入条件と未決境界を整理する。チーム指定の `prd` で単一機能を扱う。未決があるためdraft／headless結果partialであり、実装受入済みでもinitiativeのRequirements登録済みでもない。

原本：依頼文、`../brief/brief-wordfreq-exclude.md`、`../brief/.memlog.md`、`../initiative-r-6442a149.md`（frontmatterのみ）。現行根拠はリポジトリルート（本runから `../../..`）の `README.md`、`wordfreq/` 全実装、`tests/test_cli.py`・`tests/test_tokenizer.py`・`tests/test_aggregator.py`。

## Vision

本文を書き換えず、列挙した語を集計対象から外せるようにする。回数の `--min-count`、件数の `--top` と違い、語そのものを指定できる。利用者像・経済効果は推定であり、実測値や市場優位は主張しない。

## Users and journeys

不要語を外したい既存CLI利用者を想定する（A-01）。単一操作CLIなので架空の実名journeyを作らず能力仕様とする。利用者は一覧を作り、本文とともに指定し、不要語を含まない結果を得る。FR-1・FR-3が除外、FR-4が不存在の通知、FR-5が案内を支える。

## Glossary

- **本文**：従来の位置引数で渡す集計元ファイル。
- **FILE／除外ファイル**：1行1語で除外語を指定する一覧。
- **空行／コメント行**：内容のない行／先頭文字が `#` の行。空白付きの解釈は未決。
- **正規化**：大文字小文字を区別しない比較処理。現行本文は `casefold()`、単純lowerとの差はOQ-1。
- **総出現回数**：集計対象語の出現数合計。HTMLではmin-count/top前であり、表示行の和や種類数ではない。

## Features and requirements

六条件を要求IDで引き継ぐ。直接検証は後続の受入方法で、実測結果ではない。

**FR-1 — 除外指定**：利用者は任意の `--exclude FILE` で、1行1語の指定語の全出現を集計から外せる。残存語の回数は変えない。

直接検証：本文 `Zoo apple APPLE zoo banana`、除外行 `apple` で実CLIを実行する。textは `2\tzoo\n1\tbanana\n`、JSONはzoo/count2・banana/count1、HTMLは同じ語・回数で順位1・2。`--min-count 2 --top 1` ではzoo/count2のみ。除外行を `zoo` にした `--top 1` ではapple/count2となり、表示後の削除でないことも確認する。

**FR-2 — 行の読飛ばし**：空行と先頭文字が `#` の行は除外語として扱わない。

直接検証：本文 `apple marker banana`、除外一覧を空行・`#marker`・`apple` の各行とし、marker・bananaが各1で残る。空ファイルや空行・コメントのみでは有効除外語がなく計数は変わらない。空白付き行はOQ-2と分離する。

**FR-3 — 大文字小文字を区別しない比較**：依頼の「今の集計と同じく小文字にそろえて比較」に従い、大文字小文字の違いで除外結果が変わらない。Unicode差分はOQ-1で未決。

直接検証：本文 `Apple APPLE apple banana`、除外行 `aPpLe` でbanana/count1のみ。除外指定時の `Straße` / `STRASSE` 等の期待値はOQ-1解消まで固定しない。未指定時の既存casefoldはFR-6で維持する。

**FR-4 — 不存在の通知**：本文を読め、除外FILEが存在しない場合、原因が分かる文と終了コード2を返す。

直接検証：読める本文と不存在の除外パスを指定し、exit2と、除外ファイルの不存在だと分かる通知を照合する。文言完全一致・出力先・行数を新たな受入条件にしない。複合失敗はOQ-6。

**FR-5 — 説明と試験**：`--help`・READMEの使い方に説明を追加し、対応試験を追加する。

直接検証：実CLIのhelpとREADMEで構文、1行1語、空行・`#`、大文字小文字、不存在exit2の説明を確認する。READMEの一覧例・実行例を再現する。追加試験がFR-1〜FR-4とFR-6を検証し実行結果を残す。未決のUnicode方式を確定説明しない。

**FR-6 — 互換性**：既存試験を通し、未指定時の既存動作を維持する。

直接検証：既存試験全件の失敗がないことと、未指定のtext/json/html・順位・min-count/top・空入力・Unicode casefold・既存エラーを照合する。本文不存在のexit1をFR-4の2に変えない。本工程では新機能・回帰試験とも未実施。既存CLI試験にはgit操作・権限変更があり、今回の禁止範囲と区別する。

## Rules

**RULE-1 — 論理的帰結**：除外は表示抑制でなく集計対象からの除去なので、min-count/top前に反映し、全形式に共通する。HTML総数も除外後・min-count/top前となる。同じ有効除外語の重複で計数は変わらない。これはFR-1の意味の整理であり未確認の製品提案ではない。

直接検証：FR-1のHTML総数は3、min-count2/top1でも3。`apple`・`APPLE`・`aPpLe` 行を重複しても語・回数・総数は不変。本文に存在しない語だけの一覧を指定したときは、未指定と各形式の語・回数・順位・総数・終了状態が同じであることを確認する。残存語の同数順は既存の初出順を維持する（本文 `beta apple alpha`、除外 `apple` ならbeta、alphaの順）。空行・コメント行が有効な除外項目に入らないことは、CLI出力だけでなく読込処理の直接試験でも確認する。全語除外時は各形式の空結果とHTML総数0を確認し、専用案内・終了状態はOQ-5の決定後に期待値を揃える。Briefの重複行・HTML総数・通常絞込みの未決はこの範囲で整理する。

**RULE-2 — 運用制約**：追加依存・権限変更・外部送信を必要としない。

## Non-goals

市場調査、Webサービス化、本文の分割規則変更、日本語形態素解析、曖昧一致や正規表現指定、一覧配布機能は対象外。既存本文の読込契約を除外FILEへ自動適用しない。

## MVP scope

FR-1〜FR-6とRULE-1〜RULE-2が今回の範囲。既に小さい変更なので削減しない。未決は将来機能への延期ではなく、初回の仕様確定前に確認する境界。リリース番号・期限は未提供。

## Success metrics

**SM-1 — 機能充足**：目標はFR-1〜FR-5の直接検証合格。現行CLIにexcludeはなく、新機能は未検証。Unicode境界はOQ-1解消後に判定する。

**SM-2 — 対抗指標**：SM-1に対し、FR-6の既存試験と未指定互換性、RULE-2の維持を確認する。全件試験の現在値・利用者の時間短縮値は未取得。

## Quality and constraints

RULE-2を全体に適用し、後続で依存宣言・変更範囲と、通信不要のローカル処理を確認する。性能・可用性の数値目標は追加しない。

## Change boundary

追加は除外オプション・処理・不存在通知・説明・試験。未指定時はUnicode単語抽出とcasefold、回数降順・同数時の正規化後初出順、min-count→top、既存書式とエラー契約を維持する。

本工程はPRDと手順・レビュー記録のみ。実装、README・試験・initiative変更、git/Kanban操作、GSD計画を行わない。

## API contract and versioning

公開面は任意CLIオプションの追加。既存引数を置換せずFR-6を守る。版番号・廃止方針は決めない。複数指定はOQ-4。

## Developer experience

案内と検証の入口はFR-5。インストール・権限付与・外部サービス登録を追加しない。

## Decisions

- チーム指定のprdを使い、未決の製品判断を代行しない。casefold前提はOQ-1、論理的帰結はRULE-1として分離。
- 横断制約・既存変更のためRules／Quality／Change boundaryを採用。CLIの公開面・案内にAPI contract／Developer experienceを限定適用。
- AI／Experience and platform／Integrations／Data and compliance／SLOs／Migration／Hardwareは、モデル判断・消費者体験・外部連携・規制・性能義務・移行・機器の根拠がなく対象外。
- Stakeholders, risks and rolloutは組織・日程未提供のため架空の承認者やganttを作らず、判断依存はOQへ。Storiesは本数未確定かつPRDのみの依頼なので後続へ残す。

## Assumptions

- A-01（Vision / Users）：[ASSUMPTION: 不要語を外したい既存CLI利用者を想定。実在利用者・頻度・回避策は未確認。]
- A-02（Vision / Success metrics）：[ASSUMPTION: 依頼を検討契機と扱う。期限・経済効果・事業上のwhy nowは不明。]
- A-03（全体）：[ASSUMPTION: 小規模内部CLI変更相当のステークスで分量を設定。公開・契約上の義務は未確認。]

## Open questions

すべて保留で、追加受入条件ではない。担当は引継先の役割で、実名割当て・承認を意味しない。後続で確認課題として管理し、本工程ではticketを作らない。

| ID | 判断事項・Brief対応 | 担当／必要時点 | 影響 |
| --- | --- | --- | --- |
| OQ-1 | 原文の「小文字」とcasefoldの差。`Straße` と `STRASSE` はcasefoldで同一、lowerでは異なる。Briefの新除外時のcasefold前提は未確認提案へ戻す。本文の正規化変更は提案しない。 | PM→依頼者／仕様・期待値確定前 | FR-3・FR-5のUnicode、最終受入 |
| OQ-2 | 前後空白、空白のみ、空白の後の#、行内コメント、LF/CRLF・最終改行なしの扱い。strip前提なし。Brief Q-01。 | 要求・仕様担当→依頼者／行仕様確定前 | FR-1・FR-2 |
| OQ-3 | 文字コード・BOM、不存在以外の読込エラー（権限・ディレクトリ・復号等）の通知・終了コード、診断の出力先と失敗時stdoutの扱い。本文のUTF-8/exit1を自動流用しない。Brief Q-02。 | 要求・仕様担当→依頼者／読込仕様確定前 | FR-1・FR-4・FR-5 |
| OQ-4 | 1行複数語・記号等の有効性未決の行（foo_bar、123、ハイフン付き語を含む）、複数指定、除外行への本文トークン分割流用。重複有効語だけRULE-1で整理。Brief Q-03。 | 要求・仕様担当→依頼者／引数・行仕様確定前 | FR-1・FR-2・FR-5 |
| OQ-5 | 全語除外時の案内を変更するか、各形式の空結果と終了状態。専用文は未承認提案。HTML総数はRULE-1へ。Brief Q-04。 | PM／要求・仕様担当→依頼者／空結果仕様確定前 | FR-1・FR-5 |
| OQ-6 | 本文・除外FILEの両方の読込失敗、不正引数との併発等の優先順位。通常絞込みとの関係はRULE-1へ。Brief Q-05。 | 要求・仕様担当→依頼者／異常系仕様確定前 | FR-4・FR-6 |
| OQ-7 | 利用者・困り方・why now・業務成功尺度。Brief Q-06、A-01・A-02。 | PM→依頼者／価値評価時 | Vision。経済指標を機能受入へ追加しない |
| OQ-8 | 公開・契約上の義務と引渡し条件。A-03由来。 | PM→依頼者／公開・引渡し条件設定時 | ステークス再評価。現時点で義務を追加しない |

PRD作成時点の引継ぎ予定は、独立レビュー、PM経由の未決確認、必要ならSofia（bmad-agent-po）によるinitiativeのRequirements整理、その後の設計であった。現在は本カードで設計原本と独立レビューも保存し、未決を仕様承認PMへ渡す。ここで計画・実装へ自動継続しない。後続で事実が分かったらPRDをUpdateし、AssumptionsとOpen questionsを更新する。
