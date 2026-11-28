---
title: wordfreq --exclude FILE — PRD
template: prd
version: 1.1.0
status: draft
altitude: feature
created: '2026-11-28'
updated: '2026-11-28'
sources:
  - ../brief/brief-wordfreq-exclude.md
  - ../initiative-r-e0a2598f.md
  - ../source-context.md
---
# wordfreq --exclude FILE

該当実装と受入をブロックするため draft / partial。未決の正本は [open-questions.md](../open-questions.md)。

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
3. 指定語が消えた結果を既存形式で受け取る。FILE不存在ならstderrとexit2で原因を認識する。

この流れが指定語除外、説明、失敗の必要性を示す。利用背景の推定はAssumptionsに分離する。

## Glossary

- 本文: 従来の位置引数で指定するUTF-8入力ファイル。除外FILEとは別の役割。
- 除外FILE: `--exclude FILE` の引数。通常の有効行は1行1語、空行と `#` 開始行を除く。文字コード等の未決は共通一覧参照。
- 正規化語: 本文から既存 `\w+` 抽出後に `str.casefold()` した語。除外語も同じcasefold結果で照合する。
- 結果語: 除外条件とmin-countを満たし、既存の並びとtop制限で選ばれた語。
- HTML総数: 現在はmin-count/top前の入力全体の出現回数。除外指定時の意味は未決。

## Features and requirements

### FR-1 — 除外FILE指定

CLI利用者は `--exclude FILE` を任意で指定できる。未指定実行は従来の結果・終了状態を保つ。指定語の全出現を外し、残った語の回数を変えない。

受入例: 本文 `Zoo apple APPLE zoo banana` と除外行 `apple` で、text結果は `2\tzoo\n1\tbanana\n`、exit0。除外されない語だけに既存topを適用する。

### FR-2 — 行とコメント

通常の1行1語を読み、空行と生の行頭が `#` の行を無視する。

受入例: 除外FILEが `\n#banana\napple\n` ならappleだけが除外語で、本文中のbananaは残る。前後空白、空白だけの行、字下げコメント、不正行は未決のまま。これらをテストの隠れた仕様にしない。

### FR-3 — Unicode同一視

除外照合は既存正規化の `casefold()` に合わせる。lowerへの変更は不可。

受入例: 本文 `Straße STRASSE hello` と除外行 `STRASSE` はhelloだけを残す。本文の `HELLO hello` と除外行 `Hello` は全出現を外す。

### FR-4 — 除外FILE不存在

本文が有効で除外FILEが存在しない場合、FILEを特定できる分かる文をstderrへ出し、exit2で終了する。結果stdoutは空、TracebackやエラーHTMLは出さない。後半の診断形は既存CLI失敗契約の継承であり、メッセージ全文の固定はしない。

本文読込み失敗は既存exit1を保つ。他の除外読込み失敗と同時失敗の優先は共通一覧の承認待ち。

### FR-5 — 全形式と既存選択の併用

text/json/htmlの結果語は同じ語・回数・順序になる。除外した語がtop枠を消費しない。残った語へmin-countを適用し、回数降順・同数初出順でtopを制限する。指定除外語が存在しない場合は結果語不変。

受入例: 本文 `Zoo apple APPLE zoo banana` と除外行 `zoo`、min-count2/top1でapple2のみ。除外と閾値で全件消えると正常空結果となり、textは空、jsonは `[]\n`、htmlは既存の見出し・0データ行を保つ。HTML総数は決定前に期待値を固定しない。

### FR-6 — 発見できる使い方

`--help` は `--exclude FILE` の目的とファイル形式を説明しexit0となる。READMEの使い方に実行例、1行1語、空行/#開始行の無視、casefold同一視、不存在時のstderr/exit2、未指定互換を追記する。未決の構文を既に使えると記述しない。

### FR-7 — 試験と互換の証拠

互換比較の既存版は `79d83ba14dd59d289d2ecd3e33c85e8de437972e`。Builderはその版と変更後を同じ入力・argvで実行するか、その版から取得した期待値を固定して比較し、変更後自身の出力を根拠なく期待値にしない。入力は同数語・Unicode・10種類超・空本文を含む。空除外FILEとコメントのみFILE、不一致語、全語除外も区別する。

pytestに指定語除外、コメント/空行、ASCIIとUnicode同一視、除外FILE不存在、説明、未指定互換を追加する。全形式、top/min-count併用、同数順、空/全除外、既存本文エラーを検査する。既存全試験を保ち、未指定stdoutのバイト一致を確認する。追加試験と機能の実行結果はBuilder・品質の成果物であり、本作業では未実施。

## Rules

- RULE-1: 本文のUnicode抽出とcasefold、Counter初出順、min-count/topの既定値と既存構造を維持する。
- RULE-2: 取得境界と純粋な解析・集計・整形を分離する。終了コードはCLIが決め、整形部品に除外ファイルI/Oを持ち込まない。
- RULE-3: 新依存、外部通信、CI追加変更を行わない。HTMLの静的安全性、UTF-8、basename限定、escape、見た目を維持する。
- RULE-4: 未決の製品境界は依頼者の明示回答まで採用しない。仮実装、テスト期待値、READMEを承認の代用にしない。

## Non-goals

自動stopword辞書、regex除外、外部入力元、複数除外FILEの新しい仕様、永続設定、lower化、形態素解析、HTML総数の独断変更、コードの全面再設計は対象外。

## MVP scope

依頼のオプション・行処理・比較・失敗・説明・試験を一緒に届ける。既に小さい要求なので受入項目を削らない。製品未決の回答は先に必要。新規インフラ、サービス運用、移行作業は追加しない。

## Success metrics

- SM-1: FR-1、FR-2、FR-3、FR-5の承認済みシナリオを追加試験で検査できる。対抗指標は未指定stdout・初出順が変わらないこと。
- SM-2: FR-4の不存在を実CLIのexit/stderr/stdoutで検査できる。対抗指標は既存本文exit1を変えないこと。
- SM-3: FR-6、FR-7の説明・追加試験・既存全試験で受入を確認できる。対抗指標は依存/通信/CIの増加がないこと。現状値は追加機能未実装であり、合格件数を捏造しない。

## Change boundary

追加はCLI引数、除外FILE取得と行解析、共通結果語の選別、help/READMEと試験。既存 `count_words`、`top_words`、formattersの公開契約を不必要に変えない。全文Counterと表示候補を混同しない。HTML総数をどの集合から計算するかは未決のため、破壊的な早期フィルターで決定を先取りしない。

## API contract and versioning

公開面は既存 `python -m wordfreq <file>` に任意オプションを追加する形。未指定の引数・終了コード・形式契約は不変。値欠落は既存argparseと同じ使い方エラーで扱う。廃止、データ移行、新しい公開サービスはない。

## Developer experience

FR-6のREADME実行例は追加試験で実際に走らせる。現在 `tests/test_cli.py` は実subprocess、stdout/stderr分離、CLIHTML、casefold、エラーと既定互換を検査しており、同じ流儀を拡張する。未作成の検証ファイルを計画段階で実行しない。現存の検証面は source-context に記録した。

## Stories

小さな一つの機能として、FR-1からFR-7の受入例を満たす変更と説明・試験を一緒に作る。順序や細かな関数分割はBuilderが決めるが、共通未決が解ける前に当該期待値を固定しない。品質は対象版で独立して実CLIと既存回帰を確認する。

## Decisions

既存正本と依頼者の明示指示に従いcasefoldを採用し、lower案は採用しない。公式Brief/PRD/spineは変更要求の原本であり、薄いinitiativeのRequirements追加は本担当の範囲外。必要な技術整合は [architecture](../architecture/architecture.md) へ置く。

QualityはRulesとChange boundaryに統合した。AI、consumer UX、複数チームrollout、外部integrations、規制、SLO、consumer migration、hardwareは該当根拠がないため節を設けない。予算・担当名・日程・性能値を発明しない。

## Assumptions

- [ASSUMPTION: Users and journeys / Vision] 主対象を既存CLI利用者と推定する。Briefの利用背景推定を継承し、特定職種・効果量・期限は未確認。
- [ASSUMPTION: Document purpose] 単一機能なのでfeature altitudeのcapability-first構成にする。依頼者の明示template prdをprd-lightに置換しない。

## Open questions

[open-questions.md](../open-questions.md) が定義の正本。HTML総数、空白/コメント判定順、文字コード/他の読込み失敗、1語でない行、同時失敗の優先が未承認。回答後および各実装単位の完了後にPRDをUpdateし、推定と未決を退役させる。
