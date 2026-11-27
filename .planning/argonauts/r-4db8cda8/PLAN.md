# README.md に `--top 4` の実行例を追加 — r-4db8cda8

## 目的と変更範囲

- `README.md` の「wordfreq の実行」の既存の `sh` ブロックに、テキスト出力の `--top 2` の直後へ `python -m wordfreq input.txt --top 4` を1行追加する。既存例と説明は変えない。
- 製品として変更するファイルは `README.md` のみ。CLI・テスト・設定・依存は変えない。この PLAN と後続の確認記録は工程文書として扱う。

## 受入条件（原文）

1. README.md の使い方の説明に、--top 4 を指定した実行例を1つ足す。
2. 変えるのは README.md だけ。

未決事項は無い。

## 確認手順

1. `git diff origin/main...HEAD -- README.md` を読み、「wordfreq の実行」のコードブロックに上記コマンドの追加がちょうど1行あり、既存行の変更・削除がないことを確認する。リポジトリ直下で、既存ファイルを上書きせず、UTF-8 の検証用 `input.txt` に次の1行を用意する。

   ```text
   kiwi pear banana apple melon kiwi pear banana apple kiwi pear banana kiwi pear kiwi
   ```

   README に追加したコマンドをそのまま実行する。終了コードが `0` で、標準出力が `5<TAB>kiwi`、`4<TAB>pear`、`3<TAB>banana`、`2<TAB>apple` の順にちょうど4行あり、5位の `melon` が出ないことを確かめる。検証用に作成した `input.txt` は確認後に削除し、コミットしない。
2. `git diff --name-status --find-renames origin/main...HEAD` で PR 相当の全差分を確認する。工程文書（`.planning/`、`openspec/`、`_bmad-output/`、`.compound-engineering/`、`docs/solutions/`）を別記し、製品差分が `M README.md` の1件だけであることを確認する。

確認工程では、確認した head、README の追加行、コマンド・終了コード・出力、差分の判定を `.planning/argonauts/r-4db8cda8/VERIFICATION.md` に文字で記録する。
