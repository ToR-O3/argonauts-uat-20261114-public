---
title: 'README に wordfreq の上位3件の実行例を追加'
template: prd
version: 1.1.0
status: final
created: '2026-11-24'
updated: '2026-11-24'
---

# README に wordfreq の上位3件の実行例を追加

## Table of Contents

- [目的](#document-purpose) — 依頼・Brief と読者
- [目指す状態](#vision) — コマンドを組み立てずに試せる
- [利用の流れ](#users-and-journeys) — UTF-8 ファイルで上位3件を表示（UJ-1）
- [用語](#glossary) — `input.txt` と `--top 3`
- [機能要件](#features-and-requirements) — 実行例を1つ追加（FR-1）
- [制約](#rules) — 既存例の維持と製品の変更範囲（RULE-1、RULE-2）
- [対象外](#non-goals) — CLI・試験・外部への影響
- [最小範囲](#mvp-scope) — 既存コードブロックへの1行追加
- [成功指標](#success-metrics) — 追加数・変更数・実行結果（SM-1）
- [変更境界](#change-boundary) — README のみ
- [開発者向けの使い方](#developer-experience) — 既存例に沿うコマンド表記
- [受入条件](#stories) — 差分確認と実行確認
- [未決事項](#open-questions) — なし

## Document purpose

実装・検証・仕様承認の担当者が、依頼 `r-864b299c` の範囲と合否を判断するための文書。根拠は依頼本文、[Brief](../brief/brief-wordfreq-top-three.md)、[現行 README](../../../README.md) の「wordfreq の実行」と [OpenSpec の wordfreq-cli](../../../openspec/specs/wordfreq-cli/spec.md) の表示件数・出力形式・出力順序。

## Vision

上位3件を表示したい読者が、実行例の `input.txt` を手元のファイル名に置き換えて試せる。

## Users and journeys

**UJ-1:** UTF-8 のテキストファイルを持つ README の読者は、「wordfreq の実行」で例を見つけ、`input.txt` を手元のファイル名に置き換えてリポジトリ直下で実行し、上位3件までを確認する（FR-1）。

## Glossary

- `input.txt`: 既存例と同じ、読者が用意する UTF-8 入力ファイルの例示名。リポジトリの同梱ファイルではない。
- `--top 3`: 現行 CLI が表示結果を最大3件に絞る指定。

## Features and requirements

**FR-1:** README.md の「wordfreq の実行」に、既存 CLI が受理する `--top 3` の実行例をちょうど1件追加する（UJ-1）。

## Rules

- **RULE-1:** 既存のコマンド行と Markdown 書式を維持する。
- **RULE-2:** 製品の変更は README.md のみとし、プログラムと試験は変更しない。

## Non-goals

CLI の仕様・挙動、出力形式、試験、データ消去、権限変更、外部送信、課金に変更を加えない。

## MVP scope

既存の `sh` コードブロック内のコマンド1行。新しいファイルを製品に追加しない。

## Success metrics

**SM-1:** 上位3件の例は現状0件から1件（FR-1）。既存行の変更・削除と README.md 以外の製品差分はいずれも0件（RULE-1、RULE-2）。合否には「受入条件」の実行確認も必要となる。

## Change boundary

README の既存コードブロックに例を足すだけで、既存の同ブロックの行・フェンスや説明文は変更しない。CLI の公開契約に変更はない。

## Developer experience

既存の `--top 2` の JSON 実行例の直後に `python -m wordfreq input.txt --top 3 --format json` を載せる。既存例と異なるのは `--top` の値だけ。

## Stories

- **差分確認:** 実装前の基準コミットと実装後のコミットを比較し、製品差分は README の既存ブロックへの該当1行追加（削除0行）のみと確認する。工程の文書（`_bmad-output/`、`openspec/`、`.planning/`）は製品差分と区別する。
- **実行確認:** 追加行の `input.txt` だけを一時 UTF-8 ファイルのパスに置き換え、リポジトリ直下で実行する。入力 `delta gamma beta alpha beta gamma alpha beta alpha alpha` では、終了コード0で標準出力の JSON 配列が順に `alpha:4`、`beta:3`、`gamma:2` の3件（`word` と整数 `count`）になることを確認する。既存の `input.txt` は上書きせず、一時入力はコミットしない。

## Open questions

なし。
