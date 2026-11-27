# README.md に `--top 6` の実行例を追加 — r-665e20b3

## 目的と変更範囲

- `README.md` の「wordfreq の実行」の既存の `sh` ブロックで、テキスト出力の `--top 4` の直後に `python -m wordfreq input.txt --top 6` を1行追加する。既存例と説明は変えない。
- 製品の変更は `README.md` のみ。CLI・テスト・設定・依存は変えない。この PLAN と後続の確認記録は工程文書として扱う。

## 受入条件

1. README.md の使い方の説明に、--top 6 を指定した実行例を1つ足す。
2. 変えるのは README.md だけ。
3. 掲載例を実際に実行し、既存の --top 6 が最大6件を出力することを確認する。

未決事項は無い。

## 条件ごとの確認手順

1. `git diff origin/main...HEAD -- README.md` で「wordfreq の実行」のコードブロックに対象の実行例がちょうど1行追加され、既存行の変更・削除がないことを確認する。
2. `git diff --name-status --find-renames origin/main...HEAD` で全差分を見る。工程文書（`.planning/`、`openspec/`、`_bmad-output/`、`.compound-engineering/`、`docs/solutions/`）を別に記録し、製品差分が `M README.md` の1件だけであることを確認する。
3. リポジトリ直下で既存ファイルを上書きせず、検証専用の UTF-8 `input.txt` に次の1行を用意する。検証ファイルはコミットしない。

   ```text
   kiwi pear banana apple grape mango melon kiwi pear banana kiwi pear kiwi
   ```

   掲載例をそのまま実行する。終了コードは `0`、標準出力は `4<TAB>kiwi`、`3<TAB>pear`、`2<TAB>banana`、`1<TAB>apple`、`1<TAB>grape`、`1<TAB>mango` の順にちょうど6行。比較用に同じ入力で `python -m wordfreq input.txt --top 7` を実行し、7行目に `1<TAB>melon` が出ることを確認する。確認後は自分が作成した検証ファイルだけを削除する。

確認工程では、対象の head、追加行、実行コマンド・終了コード・標準出力、製品差分の判定を `.planning/argonauts/r-665e20b3/VERIFICATION.md` に文字で記録する。
