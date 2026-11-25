# r-8b038fcd — README.md に `--top 9` の実行例を追加

## 目的と対象

利用者が上位9語まで表示するコマンドをコピーして実行できるようにする。`README.md` の「wordfreq の実行」の既存 `sh` ブロックに `python -m wordfreq input.txt --top 9` を1行だけ足す。既存の例と同じくリポジトリ直下の UTF-8 入力ファイルを使う。出力例は掲載しない。CLI・テスト・CI は変更しない。工程文書は本 PLAN と確認工程の `VERIFICATION.md` のみ。

## 受入条件（依頼の原文）

1. README.md の使い方の説明に、--top 9 を指定した実行例を1つ足す。
2. 変えるのは README.md だけ。

## 条件ごとの確認

1. `git diff origin/main...HEAD -- README.md` で、使い方の既存 `sh` ブロックに該当コマンドの追加が1件だけで、既存例を変更していないことを確かめる。リポジトリ直下で、`input.txt` が既にあれば上書きせず新しい検証用 worktree を使う。未存在の場合は次の内容で一時入力を作り、README の該当行をそのまま実行する。

   ```sh
   (set -C; printf '%s\n' 'alpha alpha beta gamma delta epsilon zeta eta theta iota kappa' > input.txt)
   python -m wordfreq input.txt --top 9
   ```

   終了コード `0`、標準エラーなし、標準出力が9行で `alpha`（2回）が先頭、`iota` が末尾、`kappa` が出ないことを確認し、自分で作成した `input.txt` を削除する。計画時の試行では終了コード `0` と上記9行を確認済み。出力を掲載する場合は、同じ入力で実行して採取した標準出力と掲載ブロックを `diff -u` で照合する（順序・タブ・末尾改行を含め差分なし）。
2. `git diff --name-status origin/main...HEAD` の全件を確認し、工程文書（当依頼の `PLAN.md` と、確認工程で追加する場合の `VERIFICATION.md`）を除くと、変更が `README.md` のみであることを確かめる。

既存回帰試験はワークフロー `.github/workflows/pytest.yml` と同じ `python -m pytest` を使う。CI は確認時点の対象 head の結果を記録する。確認担当は対象 head・実行コマンドと終了コード・出力の要点・変更ファイル一覧・試験と CI の結果を、文字で読める `VERIFICATION.md` にまとめて添付する。
