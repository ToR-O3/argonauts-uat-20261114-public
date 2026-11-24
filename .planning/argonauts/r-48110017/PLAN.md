# r-48110017 README --top 5 実行例（light）

## 目的と範囲
READMEの既存CLIの使い方に実行例を1つ追加する。CLIの機能は変えない。
製品変更は `README.md` のみ。計画時点の起点は `6e8ceb26f590630eedb1dbc63e83ccff0d310778`。
工程文書はこのPLANと同じディレクトリの `VERIFICATION.md` のみ許可する。
新規スクリプト・試験・依存・GSD/BMAD/OpenSpec成果物は作らない。

## 受入条件（依頼本文の原文）
- README.md の使い方の説明に、--top 5 を指定した実行例を1つ足す。
- 変えるのは README.md だけ。
- 未決事項は無い。

## 変更するファイルと内容
- `README.md` の「wordfreq の実行」にある既存のshコードブロック内で、
  `python -m wordfreq input.txt` の直後に次の1行だけを追加する。
  `python -m wordfreq README.md --top 5`
- 自身のREADMEは既存のUTF-8実ファイルなので、入力ファイルの準備なしで実行できる。
- 既存の説明・例・末尾の検証Bの行は保持する。
- `wordfreq/__main__.py` のfilename、整数top、既定text出力と整合していることを読取り確認済み。

## 実装・品質が直接行う検証（リポジトリ直下）
1. 編集前にREADMEを読み、上記の追加例が使い方のブロックに無いことを確認する。
2. 1行を追加し、`git diff -- README.md` で該当ブロックへの追加が1行のみであることを確認する。
3. `python -m wordfreq README.md --top 5` を実行する。
   終了コード0、stderrなし、stdoutが5行で各行が回数・タブ・単語であることを確認する。
   READMEの文字列に依存するため具体的な単語と回数は固定せず、実出力を証拠に残す。
   `python` が無ければ `python3` の利用可否を確認し、置換した実行コマンドと理由を記録する。
4. 既存試験は `uv run --with pytest python -m pytest -q tests/test_cli.py` を実行する。
   既存CLI試験の失敗0件を確認する。環境・依存取得の失敗は試験成功として扱わない。
5. `git diff --check` と `git diff --name-status origin/v112-b...HEAD` を実行する。
   未commitの差分も `git diff --name-status` と `git status --porcelain` で確認する。
   製品差分がREADMEだけで、工程文書が本依頼のPLAN/VERIFICATIONだけであることを確認する。
   例の欠落・重複・別の場所への追加、実行失敗、5行以外、余計な製品変更は不合格とする。

## 証拠と引継ぎ
実装と品質は各自で上記を実行し、対象head、実行コマンド、終了コード、
stdout/stderr、試験集計、条件ごとの合否、変更ファイル一覧を
`.planning/argonauts/r-48110017/VERIFICATION.md` に文字で記録する。
品質は独立した実行の結果を区別して記載し、VERIFICATION原本を添付する。
画像・圧縮ファイルをPMへ要求しない。画面変更・ブラウザ確認は対象外。
実装はpush後にdraft PRを確認・作成し、同じカードの品質レビューへ渡す。
本カードはPLANだけをcommit・依頼branchへpush・原本添付して完了する。
