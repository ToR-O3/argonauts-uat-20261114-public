---
title: "README: wordfreq の text 形式・上位5件の実行例"
template: prd-light
version: 1.1.0
status: final
created: "2026-11-28"
updated: "2026-11-28"
---

# README: wordfreq の text 形式・上位5件の実行例

## Table of Contents

- [Vision — 目的](#vision)
- [Users and journeys — README 読者の利用](#users-and-journeys)
- [Features and requirements — FR-1・FR-2 と受入確認](#features-and-requirements)
- [Non-goals — 変更対象外](#non-goals)
- [Technical approach — 文書だけの変更](#technical-approach)
- [Success — 完了の判定](#success)
- [Open questions — 未決事項なし](#open-questions)

## Vision

README を読む利用者が、text 形式で上位5件を表示するコマンドをコード例から参照できるようにする。依頼された1行だけを追加し、既存記述は保持する。本書は実装前の要求原本であり、この計画工程では README.md を変更しない。

## Users and journeys

README の「wordfreq の実行」を読む利用者が、実ファイル `input.txt` を用意して追加されたコマンド例を参照・実行する。入力ファイルの作成や同梱は変更に含めない。

## Features and requirements

- **FR-1:** 利用者は、README.md の「wordfreq の実行」にある既存の `sh` コードブロック内で、次の1行を追加の実行例として参照できる。

  ```sh
  python -m wordfreq input.txt --top 5 --format text
  ```

  **受入条件・直接確認:** 実装後に `read_file` で README.md を開き、対象見出し直下の既存コードブロック内に上記と完全一致する行が1行追加されていることを確認する。

- **FR-2:** 利用者は追加後も既存の README 記述・実行例をそのまま参照できる。製品変更は README.md のこの1行追加だけとし、工程文書は PR に含めてよい。

  **受入条件・直接確認:** 実装直前の基準リビジョンと実装後を `git diff -- README.md` で比較し、差分が指定コマンドの追加1行のみで、削除・既存行の変更がないことを確認する。併せて `git diff --name-status` と `git status --short` で未追跡ファイルも含めて変更一覧を確認し、工程文書と公式setupによる工程用 `_bmad` 修復差分を区別したうえで、製品ファイルの変更が README.md のみであることを確認する。

## Non-goals

CLI 実装、動作・契約、テスト、依存関係、他の製品文書、既存 README 記述は変更しない。動作・契約変更がないため設計原本は作成しない。この計画工程では README を編集しない。工程原本の保存・共有とレビュー依頼は行う。

## Technical approach

既存リポジトリの README.md を対象とする Markdown 編集のみ。既存の `--top 3 --format text` 例も残す。追加位置の細部は実装者に委ねるが、同じ既存コードブロック内に置く。新しい実装、構成、保存領域、連携、ホスティングの判断は不要。直接確認は文書と差分で行い、新規機能の動作試験は要求しない。

## Success

実装後に FR-1・FR-2 の直接確認がともに通れば完了。本書の確定は README への実装完了を意味しない。

## Open questions

なし。依頼内容は確定済み。次工程は本書に従う README の1行追加と独立した受入確認であり、追加の設計工程は不要。
