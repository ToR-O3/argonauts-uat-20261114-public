# Design

## Context

[提案](proposal.md)を参照。README.md の「wordfreq の実行」では、既存の `--top 2 --format json` のすぐ後に HTML の例が並ぶ。

## Goals / Non-Goals

**Goals:** 既存例と同じ書式の具体例を選び、そのコマンドの有効性を再現できるようにする。

**Non-Goals:** コード、試験、CLI 契約の改訂。新しいアーキテクチャや移行は不要。

## Decisions

- 既存の `--top 2 --format json` の直後に `python -m wordfreq input.txt --top 3 --format json` を追加する。既定のテキスト形式でも `--top 3` は使えるが、JSON の例を踏襲すれば同じ形式の例と並び、件数の違いだけを示せる。
- 受入では変更前後の差分と実行結果を別々に確認する。既存の試験やフィクスチャは変更しない。

## Risks / Trade-offs

- 既存行まで変更する → README の追加1行・削除0行と、それ以外の製品差分がないことを確認する。
- 入力が3種類以下で件数制限を確認できない → 正規化後に4種類残る一時 UTF-8 ファイルを使い、出力の順位・語・回数を照合する。既存の `input.txt` は上書きしない。
