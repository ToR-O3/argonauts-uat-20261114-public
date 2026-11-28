---
title: "READMEのwordfreq実行例にtop5・text指定を追加"
template: prd-light
version: 1.1.0
status: final
created: "2026-11-28"
updated: "2026-11-28"
---

# READMEのwordfreq実行例にtop5・text指定を追加

## Table of Contents

- [Vision](#vision) — READMEへの1行追加
- [Users and journeys](#users-and-journeys) — 実行例を読む利用者
- [Features and requirements](#features-and-requirements) — FR-1・指定行
- [Non-goals](#non-goals) — 既存内容・製品範囲の保持
- [Technical approach](#technical-approach) — 編集箇所・検証の引継ぎ
- [Success](#success) — 差分の文字確認
- [Open questions](#open-questions) — 未決事項なし

## Vision

README.mdの「wordfreq の実行」のコード例に、`python -m wordfreq input.txt --top 5 --format text` の1行を足す。既存CLIの実行例追加だけを扱う。

## Users and journeys

READMEを読む利用者が「wordfreq の実行」のコード例で、上位5件をtext形式で指定するコマンドを確認できる。

## Features and requirements

- **FR-1:** 利用者はREADME.mdの「wordfreq の実行」の既存コードブロック内で、次の行を確認できる。受入結果は、この行が正確に1行追加されていること。

```sh
python -m wordfreq input.txt --top 5 --format text
```

## Non-goals

- 製品変更はREADME.mdの指定行追加だけ。既存例・本文・順序・改行を保持し、削除・書換え・不要な空行追加をしない。
- コード・試験・設定・依存・既存CLI契約を変更しない。新機能や新しい要件を追加しない。
- 構成と既存契約を変えないためArchitectureは不要。画面・HTMLの変更もない。

## Technical approach

既存リポジトリのREADME.md内のコードブロックへ追加する。既存の`--top 5`と`--format text`の契約はREADMEおよび`openspec/specs/wordfreq-cli/spec.md`に記載されており、実装・構成の変更は不要。

計画段階ではREADME・コードを編集せず、実CLIや未作成の検証コマンドを実行しない。後続品質は既存テストと一時入力によって例の実CLI動作を確かめ、結果を文字で記録する。本書の完成は実装・試験の合格を意味しない。

「README.mdだけ」は製品変更の範囲を指し、工程文書をPRから除く指定ではない。工程文書と製品差分を区別して確認する。

## Success

後続の差分確認で、FR-1の指定行だけが1行追加され、READMEの既存内容が保存され、製品変更がREADME.mdだけであることを文字で確認できる。

## Open questions

なし。依頼に未決事項はなく、人への追加の問いは設けない。
