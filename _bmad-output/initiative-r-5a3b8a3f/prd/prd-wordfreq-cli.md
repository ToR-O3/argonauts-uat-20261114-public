---
title: "wordfreq CLI PRD"
template: prd
version: 1.1.0
description: "Requirements a team builds from, at any altitude."
not_for: "Deciding whether to build (`opportunity`) or writing down why (`brief`); a very simple project (`prd-light`); one feature for a coding agent (`agent-spec`); a regulated or contracted baseline (`srs`); what a business signs for when the builder is a separate party (`brd`)."
facilitation_order: [document-purpose, vision, users-and-journeys, glossary, features-and-requirements, rules?, non-goals, mvp-scope, success-metrics, quality-and-constraints?, change-boundary?, ai-behavior-and-evaluation?, experience-and-platform?, stakeholders-risks-and-rollout?, integrations-and-operations?, data-and-compliance?, api-contract-and-versioning?, slos-and-performance-budgets?, consumer-migration?, developer-experience?, hardware-and-deployment?, stories?, decisions?, open-questions]
guidance: guidance-planning
rubric: rubric-planning
status: final
created: "2026-11-17"
updated: "2026-11-17"
---

# wordfreq CLI PRD

## Table of Contents

- [Document purpose](#document-purpose)
- [Vision](#vision)
- [Users and journeys](#users-and-journeys)
- [Glossary](#glossary)
- [Features and requirements](#features-and-requirements)
- [Non-goals](#non-goals)
- [MVP scope](#mvp-scope)
- [Success metrics](#success-metrics)
- [Decisions](#decisions)
- [Open questions](#open-questions)

## Document purpose

この PRD は、依頼 r-5a3b8a3f「wordfreq CLI」を実装・検証・受け入れの各工程が builds-from する要求仕様である。入力は同ディレクトリの Brief（`../brief/brief-wordfreq-cli.md`。動機・WF ID・設計決定 D-1〜D-3・推定 A-1〜A-5 の出典）と、受付カードの依頼全文・受入条件案。本工程の成果として OpenSpec 変更（proposal・specs・design・tasks）が作られ、本 PRD の FR ID を引き継ぐ。

単一機能の小規模作業なので、capability spec として軽く書く（テンプレの hobby/solo 上限に従う）。

Brief との ID 対応: WF-01→FR-1、WF-02→FR-2、WF-03→FR-3、WF-04→FR-5、WF-05→FR-4、WF-06→FR-6、WF-07→FR-7、WF-08→FR-1。FR-8 は PM 方針由来の全体制約（特定の journey ではなく全 FR に掛かる）。

## Vision

wordfreq は、テキストファイルを読むと単語の出現回数を多い順に並べて出す小さなコマンドラインツールである。`python -m wordfreq notes.txt` と打つと、上位 10 語がすぐに出る。件数も出力形式（人が読むテキスト、機械が読む JSON）もフラグで選べる。

中身は「切り出し・正規化」と「集計・整形」の部品に分かれており、入力元（標準入力や URL）を後から足せる。価値は性能ではなく、挙動が決定的であること（正規化・並び順・エラー出口がテストで固定されていること）と、拡張点が明らかなことにある。

## Users and journeys

主利用者はこの repository を使うエンジニア（依頼者自身を含む）。依頼は小規模な社内ツールとしての追加なので、journey は 1 行ずつ書く（利用者数の事実は依頼にない。ブリーフ A-1 参照）。

- UJ-1: 依頼者がテキストファイルの語頻度を調べたい。`python -m wordfreq <file>` を実行すると、正規化された単語の頻度が降順（同数は単語の昇順）で上位 N 件表示される。満たす FR: FR-1〜FR-4（FR-5・FR-6 はこの挙動を支える構造上の要求）。
- UJ-2: 依頼者が結果を別のスクリプトで使いたい。`--format json` で機械可読な配列が得られる。満たす FR: FR-3。
- UJ-3（失敗）: 存在しないファイルを渡すと、エラーメッセージが stderr に出て非 0 で終了し、黙って空結果にならない。満たす FR: FR-1。

## Glossary

- 単語（トークン）: 入力テキストから抽出した単位。定義は D-3（Unicode の単語構成文字 `\w` の連続最大長）。
- 正規化: 抽出したトークンに `str.casefold()` を適用し、大文字・小文字の差をなくすこと。
- 集計: 正規化後単語ごとに出現回数を数え、ソート規則（FR-4）で並べること。
- 入力取得: テキストを得る経路を指す構成上の境界。v1 の実装はファイルのみ。標準入力・URL は将来の拡張候補。
- 表示件数: `--top N` で指定する出力上位件数。既定 10。
- 使い方エラー: 実行条件不正（不正なオプション値・ファイル引数個数）による終了 exit 2。環境エラー（ファイルアクセス・デコード）は exit 1。

## Features and requirements

### F1. 頻度表示コマンド（UJ-1, UJ-2, UJ-3）

- FR-1: 利用者は `python -m wordfreq <file>` で、ファイル引数ちょうど 1 個を UTF-8 として読み、頻度集計の結果を得られる。ファイルが存在しない・開けない・UTF-8 としてデコードできない場合は、エラーメッセージを stderr に出して exit 1 で終了する。ファイル引数が 0 個・2 個以上の場合は使い方エラー（exit 2）。空ファイルは結果 0 件として exit 0 する。
- FR-2: 利用者は `--top N` で表示件数を指定できる。既定は 10。N は 1 以上の整数で、それ以外の値（整数でない、0 以下）は使い方エラー（exit 2）。結果の種類数が N より少ない場合は全件を出す。
- FR-3: 利用者は `--format text|json` で出力形式を選べる。既定は text。不正な形式指定は使い方エラー（exit 2）。text は 1 語 1 行で単語と回数を読むことのできる形式、json は `{"word": <str>, "count": <int>}` のオブジェクト配列（FR-4 の並び順どおり）で、`json.loads` で機械可読であること。結果 0 件のとき json は `[]`、text は出力なし。text の正確な列書式は design.md で決める。
- FR-4: 出力は常に同じ順序である: 出現回数の降順、同数の単語は正規化後単語の昇順（D-2）。同じ入力・同じオプションでの出力は決定的（識別子とする）。

### F2. 部品分離と拡張構成（UJ-1）

- FR-5: 切り出し・正規化を行う部品は、集計・出力整形を行う部品から分離している。各部品はそれ単体で呼んで検証でき、対応する単体試験を持つ（分離の機械的確認はこの試験とする）。
- FR-6: テキストを得る「入力取得」は解析・集計から境界として分離し、v1 のファイル入力もその境界の背後で動く。検証形: 解析・集計が入力取得境界を介してのみテキストを受け取ることを通す試験（境界越しの試験）を持ち、標準入力などの将来の入力元がその境界の実装追加で足りることを design.md（OpenSpec 変更。ADR に相当）に構成判断として記録する。標準入力・URL 入力の実装自体は v1 の作業範囲ではない（Non-goals 参照）。

### F3. 試験と配布（UJ-1）

- FR-7: pytest による単体試験があり、このリポジトリの CI の pytest 実行ジョブで通る。FR-1〜FR-5・FR-6 のエッジ（不存在ファイル、空ファイル、ファイル引数個数、不正な `--top`・`--format`、同数語の順序、大文字小文字の同一視、UTF-8 失敗、JSON 構造、境界越し試験）をテストケースに含む。対象 Python は当該 CI ジョブの CPython 3 の版とし（版番号は CI 設定が持つ。本では固定しない）、バージョン横断互換コードは書かない。
- FR-8: ランタイム依存は標準ライブラリのみとする。PM 方針「標準ライブラリ中心を優先」をここで決定に格上げし、依存追加が必要になる場合は人の承認を要する範囲変更として扱う。パッケージ化に最低限必要な設定ファイル（`pyproject.toml` 等）の変更は許容するが、smart マージ方針で人の承認対象になり得ることを前提に必要最小限に留める。ローカルパッケージ名 `wordfreq` と同名 PyPI パッケージの取り違えは、依存を増やさず repository 内で `python -m` 実行する範囲では問題にならない前提（Brief A-5）。

## Non-goals

- GUI・画面（依頼明記）。
- URL 入力の実装（FR-6 の拡張性だけを残す。取得そのものは将来）。
- 日本語など空白区切りでない言語の形態素解析（D-1。トークナイザ差し替えの余地を残す）。
- 標準ライブラリ以外のランタイム依存（FR-8。必要になったら範囲変更として人へ）。
- 単語頻度の統計的補正（停止詞の除外、語幹抽出など。要求されたのは生カウントのみ）。
- 大規模ストリーミング最適化・並列化。

## MVP scope

**含む**: FR-1〜FR-8（ファイル入力のみ、text/json 出力、pytest 試験）。
**あとまわし**: 標準入力入力元（構成判断は v1 の design.md に残す。次の版の候補）、URL 入力元（標準入力の次）、日本語形態素解析（D-1 の将来決定待ち）。いずれも「先に作った構成が教えることを待って決める」。

本作業は十分に小さいので lean coaching は行わない（依頼範囲＝MVP）。

## Success metrics

- SM-1: 頻度調査が 1 コマンドで済む（FR-1〜FR-3 が受け入れカードで検証できる）。現行値「専用の形なし」は推定（依頼に現在の運用の記述なし。Brief A-4）。hobby stakes なので counter-metric は置かない。
- SM-2: 学習候補がこの依頼の記録に 2 件以上残る（工程側要求。要求・仕様・実装・検証で気づいた点を記録）。

## Decisions

- D-1（空白で区切られない言語）: v1 範囲外とし、トークナイザを差し替え可能な部品として設計に残す。代替（v1 から形態素解析）は依存追加（FR-8）と要求スコープ拡大を招くため退けた。
- D-2（同回数ワードの並び順）: 回数降順、同数は正規化後単語の昇順。代替（挿入順・ランダム）は非決定的で試験が書けないため退けた。
- D-3（切り出し定義）: Unicode `\w` の連続最大長 + `str.casefold()`。代替（空白分割のみ）は「hello, world」で句読点を語に引きずり、正規化の趣旨（同一視）と崩れるため退けた。underscore を語に含める副作用は受け入れる（試験で固定）。
- D-4（終了コード）: 成功 0、使い方エラー 2、環境エラー（ファイルアクセス・デコード失敗）1。決定的で試験可能な識別子として先に固定する。

## Open questions

なし。依頼本文の未決 2 点は D-1・D-2 で決定済み。text 形式の列書式のみ design.md（下位レベル）の決定事項として残す。
