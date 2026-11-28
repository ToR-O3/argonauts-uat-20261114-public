## 変更の説明

wordfreqに`--min-length N`を追加し、N文字未満の単語を結果から除外します。既定値は1で、`--help`に説明を追加しました。README.mdは変更していません。

まだ全試験が通っていないため、マージできる状態ではありません。

## 作業の記録

- 要求: `_bmad-output/initiative-r-1bae0a69/prd/prd-light-wordfreq-min-length.md`
- 計画: `.planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-PLAN.md`
- 証拠と検証: 同ディレクトリのEVIDENCE・SUMMARY・VERIFICATION
- 追加試験29件成功。全回帰1076件成功・1件失敗。
- 過去max-count検証器の固定CLIハッシュと今回の製品変更が衝突。承認ハッシュを更新したり試験をskipしていません。
- 過去のscope試験を歴史的製品fixtureへ分離する修正範囲についてPM判断待ち。Quickはgaps_found、Task 3とOpenSpec 1.3は未完了。
- 品質の同じカードのレビュー・受入・CIの合格は未実施です。
