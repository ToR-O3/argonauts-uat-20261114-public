---
title: "wordfreq 除外ファイル PRD"
template: prd
version: 1.1.0
status: draft
created: "2026-11-28"
updated: "2026-11-28T07:17:58+00:00"
request: r-6442a149
---

# wordfreq 除外ファイル PRD

## Table of Contents

- [Document purpose](#document-purpose)：原本・判断範囲
- [Vision](#vision)：目的
- [Users and journeys](#users-and-journeys)：想定利用
- [Glossary](#glossary)：比較・行の意味
- [Features and requirements](#features-and-requirements)：FR-1〜FR-6と期待値
- [Rules](#rules)：RULE-1〜RULE-2・共通制約
- [Non-goals](#non-goals)：対象外
- [MVP scope](#mvp-scope)：今回の範囲
- [Success metrics](#success-metrics)：SM-1〜SM-2
- [Quality and constraints](#quality-and-constraints)：運用制約
- [Change boundary](#change-boundary)：互換境界
- [API contract and versioning](#api-contract-and-versioning)：CLI公開面
- [Developer experience](#developer-experience)：後続の案内
- [Decisions](#decisions)：承認根拠と節の採否
- [Assumptions](#assumptions)：背景の推定
- [Open questions](#open-questions)：背景不足 OQ-7・OQ-8のみ

## Document purpose

要求・実装・試験担当向けの単一機能仕様。受付t_c172b029の人default回答（2026-11-28T06:59:36.405633+00:00）『提案のまま進めてください（1〜6のとおり。既存の集計に合わせ、追加の文法は設けない）。』とPM判断t_834ece37、差戻しt_14fbf7f0に基づくupdateである。以前のOQ-1〜OQ-6は回答済みであり、以下に採用値と期待値を統合した。解決の来歴は[決定記録](../decisions-oq1-6.md)に保持する。

入力は[Brief](../brief/brief-wordfreq-exclude.md)とmemlog、frontmatterのみのinitiative、依頼原文・回答。現行根拠は `wordfreq/` のtokenizer・aggregator・CLI・formatter・sources。本工程は文書更新のみで、実装・試験合格・Requirements登録を主張しない。背景OQ-7/8によりpartial／draftだが、機能仕様の停止理由でも追加受入条件でもない。

## Vision

本文を書き換えずに列挙語を集計対象から外す。回数・件数でなく語を指定できる。利用者像・経済効果は未確認。

## Users and journeys

不要語を外したい既存CLI利用者を想定（A-01）。一覧と本文を指定し不要語のない集計を得る。単一操作CLIのため架空journeyは作らない。FR-1〜FR-3が除外、FR-4が失敗通知、FR-5が案内、FR-6が互換性を支える。

## Glossary

- **本文**：従来の位置引数で渡す集計元ファイル。
- **FILE／除外ファイル**：UTF-8で書いた1行1語の一覧。ファイル先頭のBOMを除去してから行を解釈する。
- **有効行**：各行の前後を `strip()` し、空なら無視、先頭が `#` なら行全体を無視し、それ以外は全体を一つの語とする。途中の `#` はコメントではない。
- **正規化**：既存本文・除外有効行の両方に `casefold()` を用いる。本文の抽出規則は変更せず、除外行を本文tokenizerで分割しない。
- **総出現回数**：除外後・min-count/top前の出現数合計。種類数や表示行の和ではない。

## Features and requirements

直接検証は後続実装の受入観点であり、実行結果ではない。旧OQ番号との対応は決定記録で追跡する。

**FR-1 — 除外指定**：任意の `--exclude FILE` で有効行と一致する本文語の全出現を除去する。残存語の回数・相対初出順は保存する。重複有効語は無影響。複数指定は最後のFILEのみ採用し、それ以前のFILEは読まない。

期待値・試験観点：本文 `Zoo apple APPLE zoo banana`、除外 `apple` はtext `2\tzoo\n1\tbanana\n`、JSON `[{"word":"zoo","count":2},{"word":"banana","count":1}]`（末尾改行付き）、HTMLは同じ語・回数と順位1・2。`--min-count 2 --top 1` はzoo/count2のみ、HTML総数は3のまま。除外をzooにしたtop1はapple/count2。`--exclude missing --exclude valid` は前の不存在を読まずvalidだけで成功し、逆順なら最後のmissingによりFR-4の失敗。最後が読める空ファイルなら前の一覧は適用しない。

**FR-2 — 行解釈**：BOM除去後、各行にstrip→空行／先頭#無視→全体一語の順を適用する。LF、CRLF、最終改行なしに対応する。行内コメント、語分割、記号除去の追加文法は設けない。

期待値・試験観点：空行・空白のみ・`  #apple  ` は無視し、`  APPLE  ` はappleを除外する。`apple#note` は全体が一語なのでappleもnoteも個別除外しない。`foo bar` はfoo/barを個別除外しない。`foo_bar` と `123` は本文抽出に現れる同じ語を除外でき、`foo-bar` は本文でfooとbarに分割されるためその両語に無影響。空／コメントのみ・本文にない行だけの一覧は未指定と同じ集計。LF／CRLF／終端改行なし、先頭BOM、重複行を組合せる。行読込の直接試験でも無視行と有効行を区別する。

**FR-3 — 既存casefoldに合わせる比較**：本文の既存casefoldを維持し、有効除外行もcasefoldする。lowerへ変更したり、lower済み情報から元表記を復元したりしない。

期待値・試験観点：本文 `Apple APPLE apple banana`、除外 `aPpLe` はbanana/count1のみ。本文 `STRASSE Straße banana`、除外 `Straße` もbanana/count1のみ。除外をSTRASSEにしても同じ。現行 `iter_tokens` は抽出後casefold済み語を入力順に返し、`count_words` はその列を数えるため、同じcasefoldキーで集計前比較すれば承認例の判定情報は失われない。元表記は失われるが今回の一致条件には不要。非一致語を変換し直して順位や表示を変えない（設計AD-3）。

**FR-4 — 読込失敗と優先順位**：既存引数検証→採用された除外FILE→本文の順に処理する。除外FILEの不存在・権限不足・ディレクトリ・不正文字コードなど読込失敗は、対象FILEと原因が分かる診断をstderrに出しexit2、stdoutは空。診断文言の完全一致は不要。除外を正常に読めて本文だけ失敗すれば既存exit1を維持する。

期待値・試験観点：各除外読込失敗を読める本文と組み合わせ、exit2／stderrの対象と原因／stdout空を確認する。両方読めない場合も除外のexit2。引数不正（top/min-countの範囲やformat等）を併発すれば既存引数エラーを先行しFILEを読まない。除外成功＋本文失敗はexit1。除外未指定の本文失敗も既存exit1。text/json/htmlの全形式で読込失敗時に途中結果を出さない。helpの既存終了動作は維持する。

**FR-5 — 後続の説明と試験**：実装時にhelpとREADMEの使い方へ構文・行の扱い・casefold比較・読込エラー・最後のFILEのみ採用・空結果を説明し、FR-1〜FR-4・FR-6・RULE-1を検証する試験を加える。

期待値・試験観点：実CLI helpとREADMEに採用仕様が矛盾なく記載され、一覧例と実行例が再現できること。本工程ではhelp／README／製品／試験を変更せず、機能試験合格も主張しない。

**FR-6 — 互換性と全語除外**：未指定時の既存本文抽出・casefold、text/json/html、順位、min-count/top、既存エラーを維持し、既存試験を通す。全語除外は各形式の既存空結果で正常exit0、除外専用メッセージを追加しない。

期待値・試験観点：全語除外のtextは空文字、JSONは `[]\n`、HTMLは既存空表・既存空結果案内を維持し総数0、いずれもexit0。既存HTMLの案内は残し「メッセージなし」と誤解しない。未指定回帰、空本文、Unicode、同数順、既存異常系を検証する。新機能・全件回帰の実行は後続であり、本工程は未実施。

## Rules

**RULE-1 — 共通集計境界**：全形式で除外→計数→min-count→top→formatter。HTML総数は除外後・min-count/top前。残存語の回数・相対初出順と、回数降順・同数時初出順を維持する。

期待値・試験観点：FR-1のHTML総数は3、min-count2/top1でも3。本文 `beta apple alpha`、除外appleならbeta、alpha各1の順。異表記重複apple/APPLE/aPpLeでも結果は一回指定と同じ。本文にない一覧は全形式の語・回数・順位・総数・終了状態を変えない。

**RULE-2 — 運用制約**：追加依存・権限変更・外部送信を必要としない。

## Non-goals

本文tokenizerの変更、日本語形態素解析、曖昧一致・正規表現指定、除外行の分割や記号除去・行内コメント文法、Webサービス化、一覧配布は対象外。既存本文のUTF-8／exit1を除外FILEへ自動流用しない。

## MVP scope

FR-1〜FR-6とRULE-1〜RULE-2を採用。背景不足から新条件を加えない。番号・期限は未提供。

## Success metrics

**SM-1 — 機能充足**：目標はFR-1〜FR-5と全語除外の直接検証合格。現行実装にexcludeはなく、新機能は未検証。

**SM-2 — 対抗指標**：SM-1に対し、FR-6の未指定互換性・既存試験とRULE-2を維持する。全件試験の現在値・時間短縮値は未取得。

## Quality and constraints

RULE-2を適用し、後続実装で依存宣言・変更範囲・通信不要のローカル処理を確認する。性能・可用性の数値目標は追加しない。

## Change boundary

追加は除外オプション・読込・集計前フィルタ・失敗通知・説明・試験。本文の抽出と正規化、書式、既存引数検証と本文exit1は保持する。本工程はBMAD文書と手順・レビュー記録のみ。製品／README／試験／initiative／GSD計画を変更せず、Git・Kanban操作も行わない。OpenSpecは親担当でありここでは変更しない。

## API contract and versioning

既存引数を置換せず任意 `--exclude FILE` を追加する。複数指定は最後のFILEだけ。版番号と廃止方針は決めない。

## Developer experience

後続のhelp／README／試験の入口はFR-5。インストール・権限付与・サービス登録を追加しない。

## Decisions

- 旧OQ-1〜OQ-6は明示回答の1〜6を採用し解決。以前の留保との違いは情報更新であり権威の競合ではない。根拠・日時・対応要求は決定記録へ保存する。

解決済みIDの索引（未決一覧ではない。採用値・期待値は対応FR、回答日時はDocument purpose）：

| ID | 解決した内容・要求 |
| --- | --- |
| OQ-1 | casefold比較。FR-3 |
| OQ-2 | 空白・コメント・改行。FR-2 |
| OQ-3 | UTF-8/BOM・読込失敗。FR-2/FR-4 |
| OQ-4 | 行全体一語・最後FILE。FR-1/FR-2 |
| OQ-5 | 全語除外の既存空結果。FR-6 |
| OQ-6 | 引数→除外→本文の順序。FR-4 |

- Rules／Quality／Change boundaryは横断制約と既存変更、API contract／Developer experienceはCLI公開面と案内のため採用。
- AI／Experience and platform／Integrations／Data and compliance／SLOs／Migration／Hardwareは対象根拠なし。組織・日程未提供のため架空の承認者やganttを作らず、Storiesと具体実装計画も本工程外。従前の節採否を維持する。

## Assumptions

- A-01（Vision / Users）：[ASSUMPTION: 不要語を外したい既存CLI利用者を想定。実在利用者・頻度・回避策は未確認。]
- A-02（Vision / Success metrics）：[ASSUMPTION: 依頼を検討契機と扱う。期限・経済効果・事業上のwhy nowは不明。]
- A-03（全体）：[ASSUMPTION: 小規模内部CLI変更相当として文書量を設定。公開・契約上の義務は未確認。]

## Open questions

未解決は次の背景不足のみ。機能受入の停止理由でも追加条件でもなく、回答済み1〜6を再質問しない。

| ID | 不足情報 | 担当／再訪時点 | 影響 |
| --- | --- | --- | --- |
| OQ-7 | 利用者・困り方・why now・業務成功尺度。A-01・A-02。 | PM→依頼者／価値評価時 | Visionの根拠。経済指標を機能受入へ追加しない |
| OQ-8 | 公開・契約上の義務と引渡し条件。A-03。 | PM→依頼者／公開・引渡し条件設定時 | ステークス再評価。現時点で義務を追加しない |

後続は親の仕様統合と必要な要求整理へ渡す。ここで実装・計画へ自動継続しない。実装後の学びは同じPRDのUpdateで反映する。
