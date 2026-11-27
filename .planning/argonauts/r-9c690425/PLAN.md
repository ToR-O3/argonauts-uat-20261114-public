# READMEにwordfreqの上位6件の実行例を追加

## 目的と範囲
- 受付: r-9c690425 / 流れ: light / 未決事項なし。
- 起点: 97d416108bbb9abd3227b21c6943026674be20df（依頼branchの計画開始時HEAD）。
- 製品変更は README.md の1行追加だけ。実装コード・試験・依存・設定は変更しない。
- 工程文書はこの PLAN.md と同じディレクトリの VERIFICATION.md のみ新規作成する。
- 「README.mdだけ」は製品範囲であり、工程文書をPRから除く指定ではない。
- BMAD・OpenSpec・GSDの生成・実行、調査文書、学習分岐は行わない。

## 受入条件（依頼原文）
1. README.md の「wordfreq の実行」のコード例に、python -m wordfreq input.txt --top 6 の1行を足す。
2. 変えるのは README.md だけ。

## 変えるファイル
- README.md: 「## wordfreq の実行」直下の既存 sh コードブロック内、
  `python -m wordfreq input.txt --top 5` の直後に次の1行だけを追加する。
  `python -m wordfreq input.txt --top 6`
- .planning/argonauts/r-9c690425/PLAN.md: 本計画（計画担当）。
- .planning/argonauts/r-9c690425/VERIFICATION.md: 条件ごとの証拠（品質担当）。

## 実装と直接の確かめ方
1. READMEを変える前に、一時領域に文書検査スクリプトを作る（追跡対象にはしない）。
   起点READMEは `git show 97d416108bbb9abd3227b21c6943026674be20df:README.md` で得る。
   期待値を「指定の既存行の直後に指定行を1回だけ挿入した全文」とし、現READMEと一致検査する。
   対象見出しの sh ブロック内に追加行が正確に1回あることも検査する。
   未変更READMEで指定行欠落による失敗（RED）を確認してから編集し、同じ検査を成功（GREEN）させる。
2. 条件1: 全文一致と `git diff -- README.md` で、位置・文字列の正確さ、追加1行・削除0行を確認する。
   通常例、top 5、min-count、text/json/html等の既存例・説明がすべて保持されることも全文一致で確かめる。
3. 条件1の実行確認: 一時領域の UTF-8 input.txt に `a a a a a a a b b b b b b c c c c c d d d d e e e f f g` を保存する。
   リポジトリのモジュールを PYTHONPATH で参照し、その一時ディレクトリで
   `python -m wordfreq input.txt --top 6` を実行する（pythonが無ければ一時venvで用意する）。
   終了0・stderr空、stdoutが `7\ta\n6\tb\n5\tc\n4\td\n3\te\n2\tf\n` と完全一致することを検査する。
   7種類中6件だけが回数降順で表示され、gが除外されることを確かめる。入力・出力はcommitしない。
4. 回帰確認: リポジトリ直下で `python -m unittest discover -s tests -v` を実行し、失敗0件を確認する。
5. 条件2: `git diff --name-status 97d416108bbb9abd3227b21c6943026674be20df HEAD` を全件読む。
   この依頼の PLAN.md / VERIFICATION.md 以外の変更が README.md だけであることを確認する。
   commit前の差分も含めて確認し、`git diff --check` を実行する。base差分も確認し、範囲外変更を混ぜない。

## 引継ぎと証拠
- 実装担当は実行した検査のコマンド・終了値・RED/GREEN・CLI出力・回帰結果をレビューに渡す。
- 品質担当は独立再実行し、対象head・条件別の合否・変更全件を VERIFICATION.md に文字で記録して原本添付する。
- PMが標準 read_file で判断できる証拠を残す。画面変更はなく、画像・圧縮ファイルの閲覧は求めない。
- 実装はpush後draft PRを作成または確認し、同じカードを品質へ request_review する。
- 確認・最終化・マージは予約済みの後続工程に任せ、この計画ではREADME編集・実試験を行わない。
