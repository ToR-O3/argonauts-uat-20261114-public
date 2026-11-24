# 文脈（intel）

以下は DOC 原本からの抜粋。実装・検証の記述は今回の実行指示や検証結果ではない。

## 読者・課題・解決策と範囲（Brief）
- source: _bmad-output/initiative-r-864b299c/brief/brief-wordfreq-top-three.md:22-48

DATA_de7fd060_START
## Executive summary

手元の UTF-8 テキストを `wordfreq` で集計する人が、オプションの説明からコマンドを組み立てずに、上位3件の指定を試せるようにする。既存の CLI は `--top 3` に対応しているため、README に実行例を1つ足すだけでよい。

## Problem

README は `--top N` を説明し、上位1件と2件の例を載せているが、上位3件を指定する例はない。

## Solution

README.md の「wordfreq の実行」に、既存の `--top 2` の JSON 実行例と同じ書式で `--top 3` の実行例を1つ追加する。結果は最大3件で、3種類未満なら全件を表示する。

## What makes it different

読者は例のファイル名を手元の UTF-8 ファイルに置き換えるだけで試せる。既存例も引き続き参照できる。

## Who it serves

リポジトリ直下から `wordfreq` を実行し、結果を上位3件までに絞りたい README の読者。

## Success criteria

製品の差分が README.md の既存コードブロック内の1行追加のみで、既存行の変更や削除がないことを確認する。正規化後に4種類以上の語が残る入力で追加例を実行し、終了コード0と上位3件の出力を確かめる。

## Scope

実行例の追加だけを対象とする。CLI の仕様・挙動、プログラム、試験は変更しない。
DATA_de7fd060_END

## 提案の変更範囲と影響（Proposal）
- source: openspec/changes/r-864b299c-readme-top-three/proposal.md:3-24

DATA_4e8fd818_START
## Why

`wordfreq` はすでに `--top 3` に対応しているが、README の使い方には上位3件の実行例がない。既存の書式で1例を加え、読者がコマンドを組み立てずに試せるようにする。

## What Changes

- README.md の「wordfreq の実行」の既存 `sh` コードブロックに、有効な `--top 3` の実行例を1行だけ追加する。
- 既存例・書式・説明を変更せず、CLI の仕様や挙動、プログラム、試験には手を加えない。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `wordfreq-cli`: README に上位3件の実行例を掲載する要件だけを追加する。既存の CLI 契約は変更しない。

## Impact

製品の変更対象は README.md のみ。実行コード、試験、API、依存関係、設定、外部連携への変更はない。
DATA_4e8fd818_END

## 実行例の追加と受入確認（Tasks）
- source: openspec/changes/r-864b299c-readme-top-three/tasks.md:3-5

DATA_af1d9499_START
## 1. README の使い方に実行例を追加

- [ ] 1.1 README.md の「wordfreq の実行」の既存 `sh` コードブロックで、`--top 2` の JSON 例の直後に `python -m wordfreq input.txt --top 3 --format json` を1行追加する。実装前後のコミットの差分で、製品の変更は README の該当1行追加だけ（削除0行、既存例・フェンス・説明・プログラム・試験の変更なし）と確認する。追加行の `input.txt` だけを一時 UTF-8 ファイルのパスに置き換えてリポジトリ直下で実行し、入力 `delta gamma beta alpha beta gamma alpha beta alpha alpha` に対して終了コード0、JSON 配列が順に `alpha:4`、`beta:3`、`gamma:2` の3件であることを照合する。既存の `input.txt` は上書きせず、一時入力はコミットしない。
DATA_af1d9499_END
