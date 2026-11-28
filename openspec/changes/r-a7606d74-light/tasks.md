## 1. Implementation

実施計画: `.planning/quick/261128-vh0-wordfreq-min-length/261128-vh0-PLAN.md`。同順のTask名を対応させる。

- [x] 1.1 変更前baselineを固定し最小文字数の実CLI縦sliceを通す
- [x] 1.2 入力前の正整数拒否とhelpを縦sliceごとに追加する
- [x] 1.3 全形式・Unicode・合成・空結果の回帰と独立品質用証拠を完成する

1.3の完了はBuilder担当範囲のみ（PM判断 t_8b54614f comment246）：Builderの追加263件・全pytest1311件成功、不変baseline/README、実CLI原本対応と未完品質条件の引継ぎ。PM許可の過去承認fixture局所修正と実測原本はSUMMARYを参照。3項目はGSD Task 1〜3と同順同名を維持する。

## 必須品質受入 — pending（Builder完了とは別判定）

独立qualityによる最終headのfresh対象pytest・全pytest、HTMLの1280×900/320×900・DPR1・zoom100%での実閲覧、全画像/必要tileとrawの対応および可読性・行/順位・元総数・空状態・見出しの文字記録は必須。省略/明示1互換・絞込み・全除外を含める。未閲覧/独立未確認はpendingであり、FR-5/LEN-4/SC-5の最終受入は未完了。製品要求は変更しない。旧Quick human_needed判定は履歴保存し、新判定は親のfresh verifierに任せる。
