# wordfreq 実行例の追加計画

- 依頼: r-f32a8f4a
- 流れ: light
- 対象: ToR-O3/argonauts-uat-20261114-public
- 基準branch: v112-a
- 作業branch: argonauts/r-f32a8f4a
- 計画時の起点: b73d4b4899d0177d8187bdc38607914f369a18d6

## 目的と最新の決定
README.md の既存の実行例を保ち、上位3件をJSONで表示する例を1行追加する。
判断日時: 2026-11-25T18:41:27.520592+00:00
依頼者の原文: 「既存の行はそのままにして、代わりに python -m wordfreq input.txt --top 3 --format json の1行を、同じコード例に足してください。変えるのは README.md だけです。」
旧依頼の min-count 行の追加は依頼者の判断により対象外。既存行を重複追加しない。
未決事項はない。製品の動作・設定・依存は変更しない。

## 変えるファイル
- 製品: README.md の「wordfreq の実行」にある既存の sh コードブロックのみ。
- 計画: .planning/argonauts/r-f32a8f4a/PLAN.md（本書）。
- 品質の確認記録: .planning/argonauts/r-f32a8f4a/VERIFICATION.md。
- 製品変更範囲の指定でありPR掲載範囲の明示指定ではない。工程文書もcommit・pushする。
- full用の文書や新しいテストファイルは作らない。

## 受入条件と直接の確かめ方
1. 「既存の行はそのままにして」: README.md を読み、`python -m wordfreq input.txt --min-count 3` を含む既存の行がすべて保持されていることを確認する。
2. 「代わりに python -m wordfreq input.txt --top 3 --format json の1行を、同じコード例に足してください」: 同じ sh コードブロックに指定文字列と完全一致する独立した行が1件増えたことを確認する。別の節・コードブロックへの追加や文字列の違いは不合格。
3. 「変えるのは README.md だけです」: `git diff origin/v112-a...HEAD -- README.md` で追加1行・削除なし、`git diff --name-only origin/v112-a...HEAD` で製品差分が README.md だけであることを確認する。許可する工程文書は上記2件のみ。

## 実装・確認の順序
1. 実装担当は受付と本書の最新判断を読み、編集前の README.md で新しい行が未掲載であることと、既存 min-count 行の存在を確認する（変更前の未達を記録）。
2. 同じ sh コードブロック内で既存の `--top 2 --format json` の行の直後に `python -m wordfreq input.txt --top 3 --format json` を1行だけ追加する。ほかの行を変えない。
3. `git diff --check` と編集差分・README.md の直接読取りで条件1〜3を確認し、commit・pushする。commit前の差分確認には `git diff -- README.md` を使う。
4. 依頼branchのPRを確認し、無ければ draft PR を作成する。同じ実装カードを品質レビューへ渡す。
5. 品質担当は対象headで受入条件を独立に再確認する。文書だけの変更なので画像・ブラウザ確認は不要。CLIの機能変更やサンプル入力の追加は範囲外。
6. 品質担当は各条件の合否、対象head、実行したコマンド・終了コード・差分の事実、変更前後の確認を VERIFICATION.md に文字で記録し、原本添付・pushする。PMは標準 read_file で判断でき、画像や圧縮ファイルを開く必要がない。
7. 実装レビューと後続の確認・最終化は予約済みカードで行う。本工程は計画の保存・push・原本添付まで。
