# README に wordfreq の JSON 出力例を追加

## 固定情報
- 依頼: r-1633f4bd / 流れ: light / 目的: none
- repository: ToR-O3/argonauts-uat-20261114-public
- 基準branch: v112-a / 依頼branch: argonauts/r-1633f4bd
- 起点: b723480767c1f9ed37f478e38ce8b48c7e434085

## 目的と変更するファイル
- README の利用者が top 4 の JSON 出力の実行方法をコピーできるようにする。
- 製品変更は `README.md` のみ。既存の説明・実装・試験・設定は変更しない。
- 工程文書は本 PLAN と、品質が作る同じディレクトリの `VERIFICATION.md` のみ。
- PR掲載範囲の明示的な限定は無く、工程文書は通常どおりGitに保存する。
- BMAD・OpenSpec・GSD の導入、調査文書、追加の計画は行わない。

## 受入条件（依頼本文の原文）
1. README.md の「wordfreq の実行」のコード例に、python -m wordfreq input.txt --top 4 --format json の1行を足す。
2. 変えるのは README.md だけ。
- 未決事項は無い。

## 実装手順
1. 編集前に `README.md` を読み、対象節のコード例に指定行がまだ無いことを確認する。
2. 「wordfreq の実行」の既存 `sh` コードブロックで、top 3 の JSON 例の次に
   `python -m wordfreq input.txt --top 4 --format json` を独立した1行として追加する。
3. 以下の検証を実行して差分を確認し、commit・依頼branchへのpushを行う。
   最初の実装として依頼branchのPRを確認し、無ければdraftで作り、同じカードの品質レビューへ渡す。

## 条件別の直接の確かめ方
- 条件1（位置・完全一致）: `read_file` で README の対象節を読み、指定文字列が
  同じコードブロック内に独立した1行として1回存在することを確認する。
  `git diff b723480767c1f9ed37f478e38ce8b48c7e434085 -- README.md` で追加1行・削除0行を確認する。
- 条件2（変更範囲）: `git diff --name-status b723480767c1f9ed37f478e38ce8b48c7e434085 HEAD` と
  未commit差分を確認し、工程文書以外の変更が README.md だけであることを確認する。
- 実動作の補助確認: workspace内の一時ディレクトリに UTF-8 の `input.txt` を用意し、
  頻度が異なる5種類以上の語を入れる。repoをモジュール検索パスに設定した状態で、
  そのディレクトリから指定コマンドをそのまま実行する。stdout・stderr・終了コードを保存し、
  JSON配列が頻度上位4件で、各要素が `word` と整数 `count` を持つことを確認する。
  一時入力・出力はcommitしない。実行環境上 `python` が無ければ同じ環境のPythonで実行し差異を記録する。
- 既存の回帰試験: repo直下で `python3 -m unittest discover -s tests -v` を実行する。
- 品質は独立に条件別検証と試験を行い、コマンド・終了コード・結果・対象headを
  `.planning/argonauts/r-1633f4bd/VERIFICATION.md` に記録し、文字の原本を添付する。
  PMが `read_file` だけで判断できる形にし、画像・圧縮ファイルの閲覧は求めない。

## この計画カードの完了条件
- PLANだけをcommit・pushし、remote headとHEADの一致、クリーンな作業ツリーを確認する。
- PLAN原本をカードへ添付し、保存名とSHA-256を照合する。
- 完了metadataにflow・head_sha・acceptance_criteria、PLANの実パスと添付IDを渡す。
