# READMEにwordfreqのJSON出力例を追加

## 目的・範囲
- 依頼: r-feab6bf8 / 流れ: light / 未決事項なし。
- 製品変更は `README.md` の「wordfreq の実行」の最初の `sh` コード例への1行追加だけ。
- `python -m wordfreq input.txt --min-count 3 --format json` を既存のJSON例の直後、HTML例の直前に追加する。
- 既存の本文・例・改行を保持し、コード・公開動作・設定・データ形式・依存を変えない。
- 工程文書は本PLANと `.planning/argonauts/r-feab6bf8/VERIFICATION.md` のみ。PRに含める。
- 比較用の変更前commit: `d2ee48b6c827628d937b0d6dfd14d26f43b86f39`。

## 受入条件（依頼本文から転記）
1. README.md の「wordfreq の実行」のコード例に、python -m wordfreq input.txt --min-count 3 --format json の1行を足す。
2. 変えるのは README.md だけ。
3. 未決事項は無い。

## 試験先行の手順
1. READMEを編集する前に、標準ライブラリだけの直接試験を `$TMPDIR` 内の `test_readme_json_example.py` に作る。
   試験は作業リポジトリ直下から `python3 <試験ファイルの絶対パス>` で実行する。
   試験ファイルはPRへ加えず、再実行できる全文をVERIFICATION.mdに載せる。
2. 試験は `git show <変更前commit>:README.md` と現在のREADMEのバイト列を取得し、次をassertする。
   - 見出し `## wordfreq の実行` の直後の最初の `sh` フェンス内に指定コマンドが独立した1行として1回だけ存在する。
   - 元の `python -m wordfreq input.txt --top 2 --format json` 行の直後への指定行追加で作った期待バイト列と、現在のREADMEが完全一致する。
     元のアンカーが1回だけ存在することも確認する。指定行以外の追加・削除・改行変更は失敗とする。
   - `git diff --name-only <変更前commit> --` の全件から工程文書の場所を除くと `README.md` だけである。
     工程文書の場所は `.planning/`、`openspec/`、`_bmad-output/`、`.compound-engineering/`、`docs/solutions/`。
     さらに、この依頼の工程文書の変更は上記PLANとVERIFICATIONの2パス以外を許さない。
   - `git ls-files --others --exclude-standard` の全件も確認し、上記2文書以外の未追跡ファイルがあれば失敗とする。
3. 変更前に実行し、指定行欠落によるassert失敗（RED）を確認する。実行環境エラーをREDとして扱わない。
4. 指定位置へ1行だけ追加する。同じ試験を再実行し、全assert成功・終了コード0（GREEN）を確認する。
5. `git diff --check` とREADMEの差分を確認し、製品差分が指定1行の追加のみであることを目視でも照合する。
6. READMEと許可された工程文書だけをcommit・依頼branchへpushし、リモートheadとの一致を確認する。
   最初の実装では依頼branchのdraft PRを確認・作成し、同じ実装カードを品質へrequest_reviewする。

## 条件ごとの直接の確かめ方・証拠
- 条件1: フェンス内の独立行検査と期待バイト列の完全一致で、コマンド・位置・追加数・既存内容保持を確認。
- 条件2: 変更前commitからの全差分・未追跡一覧で、工程文書を除いた製品変更がREADMEだけであることを確認。
- 条件3: 固定入力と受付の最新コメントを再読し、未決事項が無いことを確認。新しい判断が必要ならPMへ戻す。
- 品質は試験を独立再実行し、同じ条件でREADMEと全差分を確認する。画像・ブラウザ検証は不要。
- 品質はVERIFICATION.mdに対象head、条件別判定、試験全文・実行コマンド・終了コード、RED/GREENの実測結果、差分確認を文字で記録する。
- VERIFICATION.mdをpush・原本添付し、PMは標準read_fileで判断できるようにする。画像や圧縮ファイルを開かせない。
- この計画カードではREADMEの編集・実装試験を行わず、本PLANだけをcommit・push・原本添付して完了する。
