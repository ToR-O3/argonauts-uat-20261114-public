---
title: wordfreq --exclude FILE — PRD
template: prd
version: 1.1.0
status: final
altitude: feature
created: '2026-11-28'
updated: '2026-11-28'
sources:
  - ../brief/brief-wordfreq-exclude.md
  - ../initiative-r-e0a2598f.md
  - ../source-context.md
  - ../decision-update.md
---
# wordfreq --exclude FILE

5件の製品判断は [採用決定](../decision-update.md) で解消済み。公式レビュー・reconciliationを終えた更新文書である。後続仕様承認は t_91b92aed の担当であり、本書のfinal状態は実装・受入承認ではない。

## Table of Contents

- [Document purpose — 入力と権限](#document-purpose)
- [Vision — 特定語を外す](#vision)
- [Users and journeys — CLIの利用](#users-and-journeys)
- [Glossary — 本文と除外FILE](#glossary)
- [Features and requirements — FR-1 to FR-7](#features-and-requirements)
- [Rules — RULE-1 to RULE-4](#rules)
- [Non-goals — 広げない範囲](#non-goals)
- [MVP scope — 最小の変更](#mvp-scope)
- [Success metrics — SM-1 to SM-3](#success-metrics)
- [Change boundary — 維持する契約](#change-boundary)
- [API contract and versioning — CLI互換](#api-contract-and-versioning)
- [Developer experience — 説明と試験](#developer-experience)
- [Stories — 小さな実装単位](#stories)
- [Decisions — 確定根拠](#decisions)
- [Assumptions — 未確認の推論](#assumptions)
- [Open questions — 実装前の確認](#open-questions)

## Document purpose

Builderと品質担当が既存wordfreqへ単一機能を追加するためのfeature-level要件。明示template `prd` を使用し、入力Briefは `_bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md`。薄いinitiativeにはRequirementsがなく、依頼原文と現行正本 `openspec/specs/wordfreq-cli/spec.md`、wordfreq/、tests/、READMEを照合した。証拠と依頼原文は [source-context](../source-context.md)。このPRDは既存正本の書換えでも実装承認でもない。

## Vision

利用者が指定した語を、大小を区別せずに結果から外せるCLIにする。除外のために本文の抽出や既存出力の意味を壊さず、未指定実行は従来どおりにする。期限、収益目標、利用者数は提示されていない。

## Users and journeys

単一CLI操作なので、架空の人物を作らず利用の流れだけを記す。

1. 利用者が1行1語の除外FILEを用意する。
2. 本文パスと `--exclude FILE` を指定して実行する。
3. 指定語がランキングから消えた結果を既存形式で受け取る。HTML総数は元入力全体のまま。除外FILEの読込み失敗・不正行ならstderrとexit2で原因を認識する。

この流れが、指定語除外、使い方の説明、失敗時の原因通知の必要性を示す。利用背景の推定はAssumptionsに分離する。

## Glossary

- 本文: 従来の位置引数で指定するUTF-8入力ファイル。除外FILEとは別の役割。
- 除外FILE: `--exclude FILE` のUTF-8ファイル。前後空白除去後に空行と `#` 開始行を除き、残る行全体が既存 `\w+` に一致する1行1語。
- 正規化語: 本文から既存 `\w+` 抽出後に `str.casefold()` した語。除外語も同じcasefold結果で照合する。
- 結果語: 除外対象ではなく、min-countを満たし、既存の並びとtop制限で選ばれた語。
- HTML総数: 除外指定の有無によらず、除外/min-count/top前の元入力全体の出現回数。

## Features and requirements

### FR-1 — 除外FILE指定

CLI利用者は `--exclude FILE` を任意で指定できる。未指定実行は従来の結果・終了状態を保つ。指定語の全出現をランキングから外し、残った語の回数とHTML元総数を変えない。

受入例: 本文 `Zoo apple APPLE zoo banana` と除外行 `apple` で、text結果は `2\tzoo\n1\tbanana\n`、exit0。除外されない語だけに既存topを適用する。

### FR-2 — 行とコメント

各行の前後空白を除去した後に空行と `#` 開始行を無視する。LF・CRLF・最終改行なしを受け付ける。残る行は既存のUnicode `\w+` に行全体が一致する場合のみ有効で、数字とunderscoreは可。検証後にFR-3のcasefoldを適用し、本文の単語分割は変更しない。

受入例: 除外FILEが ` \r\n  #banana\r\n apple `（最終改行なし）ならappleだけが除外語で、本文中のbananaは残る。LF版も同じ結果になる。行 `123` と `_word_` は有効。`foo bar`、`foo,`、`foo-bar`、単独の結合文字、`foo # note`、先頭BOM付きの語は不正行としてFR-4に従う。複数語への分割、句読点の除去、インラインコメント化、BOMの自動除去で受理しない。

### FR-3 — Unicode同一視

除外照合は既存正規化の `casefold()` に合わせる。lowerへの変更は不可。

受入例: 本文 `Straße STRASSE hello` と除外行 `STRASSE` はhelloだけを残す。本文の `HELLO hello` と除外行 `Hello` は全出現を外す。

### FR-4 — 除外FILEの失敗と優先順位

除外FILEはUTF-8で読む。不在・権限不足・ディレクトリ指定・不正文字コードなどすべての読込み失敗は、FILEと理由が分かるstderrを出してexit2で終了する。FR-2の不正行はファイル名と行番号が分かるstderrとexit2にする。どちらも結果stdoutは空、集計結果・HTML・Tracebackを出さない。メッセージ全文の固定はしない。

既存の引数構文・top/min-count数値検査を最初に行い、次に除外FILEの取得と全行検証、成功した後に本文を読む。除外に問題があればその説明とexit2を優先し、本文は読まない。除外未指定または有効なら本文読込み失敗は既存exit1を保つ。

受入例: 本文不存在と除外不存在が同時でも除外の説明/exit2。本文不正UTF-8と除外不正行が同時でも除外のファイル名・行番号/exit2で本文未読。空行、字下げコメント、有効語、不正行を順に含むFILEでは元ファイルの4行目と診断し、途中の有効語が本文に一致しても本文取得は一度も呼ばない。除外が有効で本文不存在なら既存exit1。`--top 0` または `--min-count 0` と除外不存在が同時なら既存数値エラーが先で、どちらのファイルも読まない。

### FR-5 — 全形式と既存選択の併用

text/json/htmlの結果語は同じ語・回数・順序になる。除外した語がtop枠を消費しない。残った語へmin-countを適用し、回数降順・同数初出順でtopを制限する。指定除外語が存在しない場合は結果語不変。

受入例: 本文 `Zoo apple APPLE zoo banana` と除外行 `zoo`、min-count2/top1でapple2のみ、HTML総数は元入力の5。除外と閾値で全件消えると正常空結果となり、textは空、jsonは `[]\n`、htmlは既存の見出し・0データ行を保ち総数は5。空本文なら総数0。空除外FILE・コメントのみ・不一致語ではHTML総数を含む既存結果を保つ。

### FR-6 — 発見できる使い方

`--help` は `--exclude FILE` の目的とファイル形式を説明しexit0となる。READMEの使い方に実行例、UTF-8の1行1語、前後空白除去後の空行/#開始行無視、LF/CRLF/最終改行なし、既存 `\w+` 全体一致と不正行、casefold同一視、読込み失敗/不正行のstderr・exit2、除外先行、HTML元総数維持、未指定互換を追記する。説明をFR-2/FR-4/FR-5の受入と一致させる。

### FR-7 — 試験と互換の証拠

互換比較の既存版は `79d83ba14dd59d289d2ecd3e33c85e8de437972e`。Builderはその版と変更後を同じ入力・argvで実行するか、その版から取得した期待値を固定して比較し、変更後自身の出力を根拠なく期待値にしない。入力は同数語・Unicode・10種類超・空本文を含む。空除外FILEとコメントのみFILE、不一致語、全語除外も区別する。

pytestに指定語除外、コメント/空行、ASCIIとUnicode同一視、除外FILE失敗、説明、未指定互換を追加する。FR-2のtrim/行終端/有効語/全不正行例、FR-4の全読込み失敗と入力優先順位（本文が読まれないことも含む）、全形式、HTML元総数、top/min-count併用、同数順、空/全除外、既存本文エラーを検査する。既存全試験を保ち、未指定stdoutのバイト一致を確認する。追加試験と機能の実行結果はBuilder・品質の成果物であり、本作業では未実施。

## Rules

- RULE-1: 本文のUnicode抽出とcasefold、Counter初出順、min-count/topの既定値と既存構造を維持する。
- RULE-2: 取得境界と純粋な解析・集計・整形を分離する。終了コードはCLIが決め、整形部品に除外ファイルI/Oを持ち込まない。
- RULE-3: 新依存、外部通信、CI追加変更を行わない。HTMLの静的安全性、UTF-8、basename限定、escape、見た目を維持する。
- RULE-4: 製品境界は採用決定の明示回答に従う。仮実装、テスト期待値、READMEを新たな承認の代用にしない。新未決が出た場合は推測で埋めず返す。

## Non-goals

自動stopword辞書、regex除外、外部入力元、FILE `-` による標準入力対応の追加、複数除外FILEの新しい仕様、永続設定、lower化、形態素解析、HTML総数の独断変更、コードの全面再設計は対象外。

## MVP scope

依頼のオプション・行処理・比較・失敗・説明・試験を一緒に届ける。既に小さい要求なので受入項目を削らない。採用決定を反映した文書レビューと後続仕様承認を経て実装へ渡す。新規インフラ、サービス運用、移行作業は追加しない。

## Success metrics

- SM-1: FR-1、FR-2、FR-3、FR-5の承認済みシナリオを追加試験で検査できる。対抗指標は未指定stdout・初出順が変わらないこと。
- SM-2: FR-4の全読込み失敗・不正行・複合失敗の優先を実CLIのexit/stderr/stdoutと本文未読で検査できる。対抗指標は既存本文exit1と引数検査先行を変えないこと。
- SM-3: FR-6、FR-7の説明・追加試験・既存全試験で受入を確認できる。対抗指標は依存/通信/CIの増加がないこと。現状値は追加機能未実装であり、合格件数を捏造しない。

## Change boundary

追加はCLI引数、除外FILE取得と行解析、共通結果語の選別、help/READMEと試験。既存 `count_words`、`top_words`、formattersの公開契約を不必要に変えない。全文Counterと表示候補を混同せず、HTML総数は除外/min-count/top前の全文Counterから取る。入力本文・除外FILEは書き換えない。

## API contract and versioning

公開面は既存 `python -m wordfreq <file>` に任意オプションを追加する形。未指定の引数・終了コード・形式契約は不変。値欠落は既存argparseと同じ使い方エラーで扱う。廃止、データ移行、新しい公開サービスはない。

## Developer experience

FR-6のREADME実行例は追加試験で実際に走らせる。現在 `tests/test_cli.py` は実subprocess、stdout/stderr分離、CLIHTML、casefold、エラーと既定互換を検査しており、同じ流儀を拡張する。未作成の検証ファイルを計画段階で実行しない。現存の検証面は source-context に記録した。

## Stories

小さな一つの機能として、FR-1からFR-7の受入例を満たす変更と説明・試験を一緒に作る。細かな関数分割はBuilderが決めるが、入力検査順と受入期待値は採用決定に従う。品質は対象版で独立して実CLIと既存回帰を確認する。

## Decisions

既存正本と依頼者の明示指示に従いcasefoldを採用し、lower案は採用しない。公式Brief/PRD/spineは変更要求の原本であり、薄いinitiativeのRequirements追加は本担当の範囲外。必要な技術整合は [architecture](../architecture/architecture.md) へ置く。

[採用決定](../decision-update.md) の判断日時は `2026-11-28T14:45:42.849521+00:00`、依頼者原文は「提案のまま進めてください（1〜5 すべて提案どおり）。」。5件をそれぞれHTML元総数維持、trim後判定、UTF-8/全読込み失敗exit2、既存 `\w+` 全体一致/不正行診断、引数→除外→本文の順として反映した。過去の保留を解消する決定であり、既存本文契約を置き換えない。

QualityはRulesとChange boundaryに統合した。AI、consumer UX、複数チームrollout、外部integrations、規制、SLO、consumer migration、hardwareは該当根拠がないため節を設けない。予算・担当名・日程・性能値を発明しない。

## Assumptions

- [ASSUMPTION: Users and journeys / Vision] 主対象を既存CLI利用者と推定する。Briefの利用背景推定を継承し、特定職種・効果量・期限は未確認。
- [ASSUMPTION: Document purpose] 単一機能なのでfeature altitudeのcapability-first構成にする。依頼者の明示template prdをprd-lightに置換しない。

## Open questions

[open-questions.md](../open-questions.md) のとおり、現在の未解決製品事項はなし。過去の5件は採用決定で解消した。Assumptionsの利用背景・構成上の推定は維持し、レビュー完了や仕様承認と同一視しない。各実装単位の完了後は学びに応じてPRDをUpdateする。
