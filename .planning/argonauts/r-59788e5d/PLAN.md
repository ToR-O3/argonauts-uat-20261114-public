# READMEにwordfreqの上位8件の実行例を追加

## 固定情報と目的
- 受付番号: r-59788e5d / 流れ: light / 未決事項: 無し。
- repository: ToR-O3/argonauts-uat-20261114-public
- 基準branch: v112-a / 依頼branch: argonauts/r-59788e5d
- 計画開始HEAD: 4133d2da72ff4ba8babaa02b1a06a898160b2c3a
- 目的: READMEの既存の実行例に、上位8件を表示する1行を加える。

## 受入条件（依頼本文から転記）
1. README.md の「wordfreq の実行」のコード例に、python -m wordfreq input.txt --top 8 の1行を足す。
2. 変えるのは README.md だけ。
- 「未決事項は無い。」
- 条件2は製品の変更範囲。PR掲載ファイルの限定ではない（受付PMの記録）。

## 変えるファイル
- 製品: README.mdだけ。既存の `--top 7` の次に `python -m wordfreq input.txt --top 8` を1行追加。
- 工程文書: このPLAN.mdと、後続品質の `.planning/argonauts/r-59788e5d/VERIFICATION.md` だけ。
- CLI実装・既存テスト・依存・設定・既存の工程資料は変更しない。
- BMAD・OpenSpec・GSDの導入やfullの成果物生成は行わない。

## 実装と条件ごとの直接の確かめ方
1. 先に受入確認用のPythonスクリプトを管理対象外の `$TMPDIR` に作る。
   - READMEを読み、「## wordfreq の実行」節のshコードブロック内に指定行が完全一致で1回あることをassertする。
   - `git show 4133d2da72ff4ba8babaa02b1a06a898160b2c3a:README.md` をsubprocessで読み、
     指定行1行だけを既存のtop7行の直後へ足した内容と現在のREADME全体が一致することをassertする。
   - 条件1と既存内容の保存を検査する。欠落・重複・節外・別の変更はいずれも非0で失敗させる。
2. READMEを変える前にスクリプトを `python3 <保存したスクリプトの絶対パス>` で実行する。
   - 指定行の欠落によるassert失敗（RED）を確認し、環境エラーとは区別する。
3. READMEへ指定の1行だけを追加し、同じスクリプトを再実行して成功（GREEN）を確認する。
4. 条件2: `git diff --name-status 4133d2da72ff4ba8babaa02b1a06a898160b2c3a` と
   `git diff 4133d2da72ff4ba8babaa02b1a06a898160b2c3a -- README.md` を全件読む。
   - 製品差分はREADMEの指定行追加のみ、工程差分は今回のPLANとVERIFICATIONのみと照合する。
   - `git diff --check` が成功することも確認する。
5. 実CLI: `$TMPDIR` 内に9種類以上の語を含むUTF-8の実ファイル `input.txt` を作る。
   - subprocessのcwdをその一時ディレクトリ、PYTHONPATHをrepo絶対パス、実行ファイルをPythonにし、
     引数 `-m wordfreq input.txt --top 8` を実行する（環境にpythonが無ければpython3を使い記録）。
   - exit0・stderr空・stdoutが期待した上位8件のtext出力と完全一致することをassertする。
   - 入力と期待値を証拠に残す。一時ファイルや検証スクリプトはcommitしない。
6. 回帰確認: repo直下で `python3 -m unittest discover -s tests` を実行し結果を記録する。

## 品質への引継ぎと終わり方
- BuilderはREADME変更をpushし、依頼PRが無ければdraftで作り、同じ実装カードで品質へrequest_reviewする。
- 品質は受入条件を独立確認し、コマンド・終了コード・入力・期待値・実出力・差分範囲・headを文字で記録する。
- 後続の確認ではVERIFICATION.md原本を添付し、PMがread_fileだけで条件別の合否を判断できるようにする。
- 今回はREADMEの文書変更のみ。画面・画像・圧縮ファイルの確認をPMに求めない。
- 計画カードではPLANのみcommit・依頼branchへpush・原本添付して完了し、README実装は後続へ渡す。
