# r-111d114c: README --top 3 実行例（light）

## 目的
READMEの使い方から、既存CLIで上位3語を表示する方法をそのまま実行できるようにする。
依頼branch: `argonauts/r-111d114c`、基準branch: `v112-b`。

## 受入条件（依頼本文の原文）
- README.md の使い方の説明に、--top 3 を指定した実行例を1つ足す。
- 変えるのは README.md だけ。
- 未決事項は無い。

## 変えるファイルと範囲
- 製品変更: `README.md` の「wordfreq の実行」の既存shコードブロックに、次の1例を追加する。
  `python -m wordfreq README.md --top 3`
- 既存例・オプション説明は保持し、CLI・依存・設定・試験ファイルは変えない。
- 工程文書は本PLANと `.planning/argonauts/r-111d114c/VERIFICATION.md` のみ。
- フレームワーク成果物・追加検証スクリプト・SUMMARYは作らない。

## 実装と直接の確かめ方
1. 編集前にREADMEを読み、追加予定の例がまだ無いことを確認する。
   既存の `tests/test_cli.py::test_top_three_selects_three_sorted_words` が上位3語を検査済み。
   新規試験ファイルを作らず、文書差分と実CLIで受入を確認する。
2. 既存の `python -m wordfreq README.md --top 5` の隣に上記の1行を追加する。
3. 追加したコマンドをリポジトリ直下でそのまま実行する。
   終了コード0、stderr空、stdoutが `<count>\t<word>` の3行であることを確認する。
   3行でない、エラー、READMEの例と実行したコマンドが違う場合は不合格。
   `python` が無い環境では環境不足を記録し、勝手にREADMEの実行方法を変えない。
4. `python3 -m pytest -q` で既存試験を実行する。
   pytestが無い場合は `uv run --with pytest python -m pytest -q` を使い、依存定義は変えない。
5. `git diff origin/v112-b -- README.md` を読み、使い方への実行例追加が1つだけであることを確認する。
   `git diff --name-only origin/v112-b...HEAD` と未commit差分・未追跡ファイルを確認し、
   製品差分はREADME.mdのみ、工程文書差分は上記PLAN.md・VERIFICATION.mdだけと照合する。
6. 品質担当も対象headで例と既存試験を独立して実行する。
   条件ごとの合否、対象head、実行コマンド・終了コード・stdout/stderr・試験結果・全差分の範囲を
   VERIFICATION.mdに文字で記録し、原本を添付する。PMに画像や圧縮ファイルを開かせない。

## 引継ぎ
本カードはPLANだけをcommit・依頼branchへpushし、原本添付とSHA-256照合後に完了する。
README編集・実CLI実行・既存試験・draft PR作成は後続の実装カードで行う。
実装はpush後、同じカードの品質レビューへ渡す。未決事項は無い。
