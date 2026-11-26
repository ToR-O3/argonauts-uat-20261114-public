# r-34320c15 実装計画

## 目的と範囲
- 流れ: light。READMEの実行例に上位5件を表示する例を足す。
- 起点: 依頼branch `argonauts/r-34320c15` の最新head。
- 計画作成時の起点: `25fc37a04d3c490f98a0248b89c9c8863fc490ec`。
- 製品で変えるファイルは `README.md` のみ。コード・依存・設定は変えない。
- 工程文書はこのPLANと、品質の `.planning/argonauts/r-34320c15/VERIFICATION.md` のみ。
- PLANはcommit・依頼branchへpushし、原本を計画カードに添付する。
- BMAD・OpenSpec・GSD・調査文書の生成は行わない。

## 受入条件（依頼原文）
1. README.md の「wordfreq の実行」のコード例に、python -m wordfreq input.txt --top 5 の1行を足す。
2. 変えるのは README.md だけ。
3. 未決事項は無い。

## 実装手順
1. 変更前のREADMEと差分を確認し、対象コード例に指定行が無いことを記録する（RED）。
2. `README.md` の「wordfreq の実行」直下の既存 `sh` コードブロックで、
   `python -m wordfreq input.txt` の直後に次の1行だけを追加する。
   `python -m wordfreq input.txt --top 5`
3. 既存行・順序・改行・他の節を維持する。受入条件を再確認する（GREEN）。
4. 下記の検証後にcommit・pushし、依頼branchのPRを確認する。
   無ければdraft PRを作成し、同じ実装カードを品質レビューへ渡す。

## 条件ごとの直接の確かめ方
- 条件1: 標準 `read_file` でREADMEの該当節を読み、指定行が同じコードブロック内に
  完全一致で1回だけあり、基本例の直後に追加されていることを確認する。
  `git diff 25fc37a04d3c490f98a0248b89c9c8863fc490ec -- README.md` で
  追加が指定の1行、削除が0行であることを確認する。行欠落・誤字・別の節なら不合格。
- 条件2: `git diff --name-status 25fc37a04d3c490f98a0248b89c9c8863fc490ec HEAD` の
  全件を読み、製品変更がREADMEのみであることを確認する。
  この依頼のPLAN・VERIFICATIONは工程文書として区別し、それ以外の追加変更は不合格。
  `git diff --check` と `git diff --check 25fc37a04d3c490f98a0248b89c9c8863fc490ec HEAD`
  で未commit・commit済みの空白エラーを確認する。
- 条件3: 依頼本文・受付の最新コメントと照合し、未決事項が増えていないことを確認する。
- 実行例の確認: 一時領域のUTF-8入力ファイル（6種類以上の語、出現回数を変える）で
  リポジトリ直下から `python -m wordfreq <一時入力の絶対パス> --top 5` を実行し、
  終了コード0、text形式5行、回数降順を実際の入力と照合する。入力をrepoへ追加しない。
  Python実行名が `python3` のみならその代替と理由を記録し、READMEの指定文字列は変えない。

## 品質への引継ぎ
- 品質は差分・該当コードブロック・実行例を独立して確かめる。画面の変更は無い。
- 条件別の合否、実行コマンド、終了コード、実出力、確認したheadをVERIFICATION.mdに記す。
- VERIFICATION原本を添付し、PMが標準 `read_file` で判断できる文字の証拠にする。
  画像や圧縮ファイルを開くことをPMに求めない。
