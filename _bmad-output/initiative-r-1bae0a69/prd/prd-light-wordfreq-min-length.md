---
title: "wordfreq 最小文字数指定"
template: prd-light
version: 1.1.0
status: final
created: "2026-11-28"
updated: "2026-11-28"
---

# wordfreq 最小文字数指定

## Table of Contents

- [Vision — 変更の目的](#vision)
- [Users and journeys — CLI利用](#users-and-journeys)
- [Features and requirements — ML-FR-1〜4と受入確認](#features-and-requirements)
- [Non-goals — 変更しない範囲](#non-goals)
- [Technical approach — 既存経路への最小追加](#technical-approach)
- [Success — 完了条件](#success)
- [Open questions — 判断の扱い](#open-questions)

## Vision

wordfreq に `--min-length N` を1つ追加し、短い単語を結果から除けるようにする。既定値は1で、指定しない既存利用は変えない。本書はPM計画レビューに渡す小規模機能の要求文書である。

## Users and journeys

既存のCLI利用者が `python -m wordfreq <file> --min-length N` で最小文字数を指定する。指定を省略すれば従来どおり利用でき、`--help` で選択肢と働きを確認できる。

## Features and requirements

- **ML-FR-1 — 最小文字数**: 利用者は `--min-length N` を指定できる。既存の抽出・casefoldを終えた単語の文字数がN未満なら結果の集計対象から除き、NちょうどとN超は文字数によって除外しない。text/json/htmlに共通して適用する。
- **ML-FR-2 — 既定互換**: 既定値は1。省略と明示1は、既存引数による従来の出力・終了コードを維持する。抽出規則、casefold、同頻度の初出順、頻度上下限、topの働き、HTMLの入力全体の元総数を変更しない。
- **ML-FR-3 — CLI説明**: `--help` は `--min-length N` に相当する選択肢、N文字未満の除外、既定値1を説明する。README.mdは変更しない。
- **ML-FR-4 — 試験**: 追加試験で下記の受入確認を行い、既存の全試験も実行して回帰がないことを確かめる。

| 確認 | 条件と期待結果 | 対応 |
| --- | --- | --- |
| 追加・境界 | 入力 `a bb ccc bb`、N=2で `bb` 2回、`ccc` 1回を残し、`a` を除く。N未満・ちょうど・超を全形式で確認する。 | ML-FR-1 |
| 正規化後 | 入力 `ß ss a`、N=2でcasefold後の `ss` を2回として残す。抽出前やcasefold前の文字数で除外しない。 | ML-FR-1 |
| 既定 | 同じ既存入力・引数で省略および明示1を変更前の固定期待値と比較し、全形式で一致させる。 | ML-FR-2 |
| 併用 | 入力 `a a a bb cc bb cc dddd`、N=2・min-count=2・max-count=2・top=1で `bb` 2回のみを表示する。同頻度初出順を保ち、HTML元総数は8のまま。 | ML-FR-2 |
| 全除外 | 入力 `a bb`、N=3で既存形式の正常な空結果になり、HTML元総数は2を保つ。 | ML-FR-1、ML-FR-2 |
| 説明・回帰 | helpの選択肢・説明・既定値を確認し、追加試験と既存全試験を実行する。差分でREADME.mdが未変更であることも確認する。 | ML-FR-3、ML-FR-4 |

## Non-goals

README.md、抽出・正規化、既存の並びや頻度選択、HTML表示仕様の改変は行わない。新しい入力元や依存、別の文字認識方式、アーキテクチャ文書の追加は不要。今回の文書作成では製品、OpenSpec、`.planning`を編集しない。

## Technical approach

既存Python CLIを使う。確認済みの `wordfreq/__main__.py` は引数解析・集計・頻度上下限・top・出力を接続し、`wordfreq/tokenizer.py` はUnicodeの `\w+` 抽出後にcasefoldする。`openspec/specs/wordfreq-cli/spec.md` は既存動作の参照元であり、今回書き換えない。

既存の正規化後単語に文字長の選択条件を足す最小追加とする。HTML元総数は文字長選択前の入力全体から保持し、表示対象には文字長・頻度上下限を適用してからtopを適用する。短い語を表示対象から除くことと、HTML元総数から消すことを混同しない。具体的な関数配置は実装担当に委ね、部品の再設計は要求しない。

## Success

ML-FR-1〜4の受入確認と既存回帰試験が通り、README.mdに差分がないことを完了条件とする。本書の作成は実装や試験成功の報告ではない。次工程はPM計画レビュー。

## Open questions

依頼内容に未決事項はない。無効なNの受理・拒否範囲や新しいエラー文言は依頼に含まれず、本書で依頼者の決定として追加しない。次工程で新しい製品判断が不可避と分かった場合は、PM計画レビューへ戻し、実装側だけで要件として確定しない。
