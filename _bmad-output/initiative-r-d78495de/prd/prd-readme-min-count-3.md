---
title: "README --min-count 3 実行例"
template: prd
version: 1.1.0
status: final
created: "2026-11-25"
updated: "2026-11-25T06:53+09:00"
---

# README --min-count 3 実行例

## Table of Contents

- [Document purpose — fullと更新入力](#document-purpose)
- [Vision — 例1つと2条件](#vision)
- [Users and journeys — 読者の必要](#users-and-journeys)
- [Glossary — 原本・全差分・証拠](#glossary)
- [Features and requirements — FR-1・FR-4](#features-and-requirements)
- [Rules — RULE-1・RULE-4・RULE-5](#rules)
- [Non-goals — 実行確認は対象外](#non-goals)
- [MVP scope — 担当と工程原本](#mvp-scope)
- [Success metrics — SM-1・SM-4](#success-metrics)
- [Change boundary — 最終PRの全変更](#change-boundary)
- [API contract and versioning — 不変](#api-contract-and-versioning)
- [Developer experience — 追加例と文字証拠](#developer-experience)
- [Stories — 受入の2条件](#stories)
- [Decisions — 最新判断と失効](#decisions)
- [Assumptions — 前提](#assumptions)
- [Open questions — 未決事項](#open-questions)

## Document purpose

Builder、quality、PM が README 追記と受入を行うための full PRD。公式 UPDATE（intent:update、headless:true）として、更新済み [Brief](../brief/brief-readme-min-count-3.md)、initiative 原本 `../initiative-r-d78495de.md`、既存 .template／memlog、および親が受付正本で確認した最新依頼者判断を入力とする。旧文書に引用されたソース観察は今回の実行確認ではない。

initiative 内の限定的な文書変更スライス。full の指定を維持し、prd-light に変更しない。本委任は文書更新だけで、README 編集・Git・kanban操作・製品CLI実行確認を行わない。文書の final と製品受入は別である。

## Vision

README 利用者が閾値3のコマンド例を参照できるように、指定例を1つ追加する。受入の確認は「例の追加」と「最終PRの全変更が README.md だけ」の2点だけに縮小する。

既存 CLI の説明追加であり、機能追加や利用効果の数値目標は置かない。実行による裏付けは最新判断により不要となった。

## Users and journeys

主読者は README から既存 CLI の使い方を知る利用者。その必要を FR-1 の例追加、FR-4 の変更範囲確認で満たす。文書変更のため journey は必要の記述に縮小し、架空の人物や実体験は作らない。

## Glossary

- 追加例: `python -m wordfreq input.txt --min-count 3` の使用コマンド1つ。
- 最終PRの全差分: 最終PRの `base...head` に含まれる全変更。工程文書も除外しない。
- 工程原本: Brief、PRD、memlog、レビュー、HTMLなど、カードに添付して保持する工程文書。
- 文字証拠: 2条件を判断する README 原本、差分、全変更ファイル一覧と判定。CLI出力の記録ではない。

## Features and requirements

### README の例追加

**FR-1.** 読者は README の使い方で `python -m wordfreq input.txt --min-count 3` という追加実行例を1つ参照できる。既存例と説明を維持し、例を置換したり別の実行例を増やしたりしない。README 原本と差分の文字確認で追加を判断する。

### 最終PRの変更範囲

**FR-4.** quality と PM は、最終PRの `base...head` 全差分の変更ファイル一覧が README.md だけであることを文字で確認できる。工程文書を含む他ファイルが残れば未達。製品コードだけを抽出した比較や、工程文書を除外した一覧を受入根拠にしない。

## Rules

**RULE-1.** 変更対象は README.md の指定例だけ。実装、試験、ツール、依存、設定、公開入出力、無関係な README 本文を変更しない。

**RULE-4.** 受入の確認は Stories の2条件に限定する。text・json・html の実行、その検証用入力・出力・実行証拠を要求しない。

**RULE-5.** 工程原本をカードへ添付して保持する。full仕様工程では文書をGitへ保存・pushし、最終PR整備は後続でチームD.5の指定ファイル限定手順により工程文書をPRから外す。全差分から工程文書を隠して条件充足と扱わない。

## Non-goals

3形式のCLI実行、サンプル入力の作成、形式別期待値、終了コード、stdout／stderr、語の残存／除外、ブラウザ確認、それらの実行証拠は対象外であり、受入条件にも残作業にも含めない。新機能、閾値の変更、README全面改稿、新規試験・検証ツール、依存・設定・公開入出力の変更も行わない。Architecture 文書は不要。

## MVP scope

製品成果物は指定例1つの README 追記のみ。Builder が追記と自己確認、quality が2条件の独立確認、PM が原本文字証拠の読取りと受入を担当する。現在はどちらの条件も実施済みと主張しない。

工程成果物は Brief、full PRD、memlog、レビュー、Brief HTML。工程原本のGit保存・push・カード添付と最終PR整備は担当する後続工程へ渡す。本委任では実行しない。これは最終PRに工程文書を含めてよいという例外ではない。範囲は既に最小で、要件延期や将来版の指定は不要。

## Success metrics

- **SM-1.** FR-1: 差分上、指定実行例の追加が1つ。counter-metric は既存例・説明の削除または置換0件。現在の充足は本更新で未確認。
- **SM-4.** FR-4: 最終PRの `base...head` 全変更ファイルは README.md のみ。counter-metric は README.md 以外の変更ファイル0件、比較対象から隠した工程文書0件。最終PRでの判定は後続。

## Change boundary

README の使い方への指定例追記以外は不変とする。既存例・説明・無関係な本文を保ち、`wordfreq/`、`tests/`、`tools/`、依存宣言、設定を変更しない。

full仕様工程の文書保存と、最終PRのファイル限定は時点を分ける。工程原本は先に保存・pushし、カード添付を保持したうえで、後続がチームD.5によりPR対象から外す。最終判定では実際のPRの base と head を特定し、その `base...head` 全差分を用いる。単なる作業ツリー比較、直前commit比較、README限定diff、工程文書をpath除外した一覧は2条件目の代用にならない。他ファイルが含まれれば整備未完了として戻す。

## API contract and versioning

既存 CLI の引数、形式、エラー、出力契約は変更しない。公開面の変更、移行、バージョニング作業はない。CLI契約を実行で再認定することも今回の受入には含めない。

## Developer experience

README に追加するのは次の1例のみ。これは追加する文字列であり、本仕様工程で実行するコマンドではない。

```sh
python -m wordfreq input.txt --min-count 3
```

文字証拠には README 原本の実パスと追加箇所、追記を示す差分、最終PRで用いた base・head、全変更ファイル一覧、2条件の判定を記す。PM が read_file で原本と証拠を読めるよう実パスを渡す。証拠は2条件の文字確認に限定し、製品CLIの実コマンド・入力内容・exit・出力は不要。

自己確認と quality の独立確認を担当名で区別し、未確認を合格と記録しない。本更新の文書セルフチェックは親による更新原本の独立レビューを代替しない。

## Stories

文書追加と確認の1ストーリー。受入で確かめるのは次の2点だけ。

1. README.md に `python -m wordfreq input.txt --min-count 3` の実行例が1つ追加されている（FR-1）。
2. 最終PRの `base...head` 全変更が README.md だけである（FR-4）。

それ以外の実行受入条件はない。文書の完成はこの2点の実施完了を意味しない。

## Decisions

日時: 2026-11-25T06:53+09:00。親が受付正本で確認した最新依頼者判断の原文:

> 検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。

依頼者が検証範囲を縮小したため、過去の3形式実行と入力・出力・実行証拠の受入条件は失効した。旧実行要件・規則・指標は現行本文から削除し、そのIDは再利用せず履歴のmemlogだけに残す。変更範囲確認には新IDを割り当てた。古いレビューの合格は更新版へ持ち越さない。

full と指定追加例は維持。Architecture は説明だけの変更で設計・公開契約が変わらないため不要。工程原本は保存・添付し、後続のD.5でPRから外す。差分除外でREADMEのみと見せる方法は採らない。

節の適用: Rules／Change boundary は変更制限、API contract は互換性維持、Developer experience は例と文字証拠、Stories は2条件、Decisions は判断変更の追跡に必要。独立したQuality節は具体的な規則へ統合する。AI評価、ブランド体験、企業横断rolloutとgantt、外部連携・運用、規制データ、SLO、利用者移行、ハードウェアは今回変更しないため省略する。後続作業完了時に学びや差異があれば公式Updateで見直す。

## Assumptions

未確認の要件上の前提なし。最終PRの状態やREADME追記の成功を推定しない。

## Open questions

なし。README追記、工程原本の保存・添付、D.5による最終PR整備、2条件の文字確認、親の独立レビューは後続作業であり、仕様の未決事項ではない。
