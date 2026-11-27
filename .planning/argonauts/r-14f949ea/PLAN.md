# READMEにwordfreqの上位7件の実行例を追加

- 依頼: r-14f949ea / 流れ: light / 目的: none
- 対象: ToR-O3/argonauts-uat-20261114-public
- 基準branch: v112-a / 依頼branch: argonauts/r-14f949ea
- 計画の起点: d4db1c0ee1d29c53eadae3fcbf4b6c814d37c0b1

## 目的と変更ファイル
READMEの既存の実行例を保ち、上位7件を表示する使い方を1行追加する。
製品の変更はREADME.mdだけ。「wordfreq の実行」のshコードブロックで
`python -m wordfreq input.txt --top 6`の直後に次の1行を追加する。
`python -m wordfreq input.txt --top 7`
コード・依存・設定・既存例は変更しない。
工程文書は本PLAN.mdと同じディレクトリのVERIFICATION.mdのみ新規作成可。
PRの掲載範囲はREADMEだけに限定されていないため、工程文書も通常どおり保存する。
BMAD・OpenSpec・GSDの生成、割振り・学習分岐は行わない。

## 受入条件（依頼本文から転記）
1. README.md の「wordfreq の実行」のコード例に、python -m wordfreq input.txt --top 7 の1行を足す。
2. 変えるのは README.md だけ。
3. 未決事項は無い。
補足: 既存例は保持する。2は製品の変更範囲を指す。

## 実装と条件ごとの直接の検証
1. READMEを変更する前に、scratchに標準ライブラリの検証スクリプトを作る。
   保存先は `$TMPDIR/r-14f949ea-check.py`、実行は `python "$TMPDIR/r-14f949ea-check.py"`。
   スクリプトは作業ディレクトリのREADMEと、Gitで取得した計画起点のREADMEを読む。
   対象見出し内のshコードブロックに追加行が完全一致で1回あることをassertする。
   現READMEからその行と改行を1回除いた内容が起点のREADMEとバイト単位で等しいこともassertする。
   これで位置違い・重複・既存例削除・他のREADME変更を失敗として観測する（条件1・既存例保持）。
   変更前は追加行欠落で失敗（RED）、1行追加後は同じスクリプトで成功（GREEN）を記録する。
2. 実CLI検証も同じscratchスクリプトに実装する。リポジトリのファイルは増やさない。
   scratchのUTF-8 input.txtに `a a a b b c d e f g h` を書き、
   作業ディレクトリから `sys.executable -m wordfreq <inputの絶対パス> --top 7` をsubprocessで実行する。
   終了0・stderr空・stdoutが `3\ta\n2\tb\n1\tc\n1\td\n1\te\n1\tf\n1\tg\n` と完全一致することをassertする。
   入出力と終了コードを記録する。READMEの `python` と同じ実行環境で検証する。
3. 既存の回帰試験は `uv run --with pytest python -m pytest -q` を実行し、結果を記録する。
4. `git diff --check` と `git diff d4db1c0ee1d29c53eadae3fcbf4b6c814d37c0b1 -- README.md` で1行追加だけを確認する。
   `git diff --name-status d4db1c0ee1d29c53eadae3fcbf4b6c814d37c0b1` で全ファイルを確認する。
   READMEと本依頼のPLAN.md・VERIFICATION.md以外に差分があれば失敗とする（条件2）。
5. 条件3は受付本文と最新コメントを読み、未決事項が追加されていないことを確認する。

## 品質への引継ぎと証拠
実装者はRED/GREEN・実CLI・回帰試験の実結果を品質へ渡し、push後にdraft PRを作成または照合する。
品質は独立して同じ条件を検証し、条件別の合否・実行コマンド・出力・終了コード・対象head・差分範囲を
VERIFICATION.mdに記録して原本添付する。README文書のみなので画像確認は不要（0枚）と記す。
PMは標準read_fileでPLANとVERIFICATIONの文字を読めば判断でき、画像・圧縮ファイルを開く必要はない。
このカードは計画のみ。READMEの編集と試験実行は後続の実装・品質カードが担当する。
