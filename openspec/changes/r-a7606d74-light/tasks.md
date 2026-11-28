## 1. Implementation

実施計画: `.planning/quick/261128-vh0-wordfreq-min-length/261128-vh0-PLAN.md`。同順のTask名を対応させる。

- [x] 1.1 変更前baselineを固定し最小文字数の実CLI縦sliceを通す
- [x] 1.2 入力前の正整数拒否とhelpを縦sliceごとに追加する
- [ ] 1.3 全形式・Unicode・合成・空結果の回帰と独立品質用証拠を完成する

1.3: Builderの追加263件・全pytest1311件は成功。独立品質の同カード実行とHTML実ブラウザ確認は未実施のため未完了。公式Quick検証は human_needed。PM許可の過去承認fixture局所修正と実測原本はSUMMARYを参照。
