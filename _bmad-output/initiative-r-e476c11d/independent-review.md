# BMAD独立レビュー記録

対象: Brief/PRD。公式bmad-reviewのresolve結果に従い、docsに適用されるadversarial・edge-case-hunter・structureを別々の同期delegate_taskで実行し、その後structure結果を渡してproseを独立委任した。全4レンズはcompleted、truncated=false、exit_reason=completed。codeのみのverification-gapは対象外。Brief/PRD作成workerの逐次自己レビューとは別のレビューである。

## adversarial（10指摘、全件を記録）

| 位置 | 問題・発生条件 | 提案された手当て | 放置した場合 | 判定 |
|---|---|---|---|---|
| FR-1 | 巨大整数の環境上の変換制限が不明 | 既存topと同じint変換範囲を明記 | 不要な制限解除や合否の不一致 | 採用、PRD検証具体化とdesignへ |
| FR-1 | 重複指定の扱いなし | 通常argparse方式の継承 | wrapper等で挙動差 | 採用、PRD/designへ |
| AC2 | 比較元revision不特定 | 実装前headと原本保存 | 変更後同士で回帰見逃し | 採用 |
| RULE-4 | 変更前画像/比較環境なし | 同条件の旧画像も保存 | 見た目不変を証明不能 | 採用 |
| AC7 | CI対象/非存在の扱い曖昧 | head/contextの明示 | 別head greenを誤用 | チームの有限回CI確認として採用、待機や新CIは不可 |
| RULE-1 | Unicode合算が閾値を左右する例なし | Straße STRASSE/N2 | 新経路で正規化前に除外 | 採用 |
| AC3 | 異常値×形式の確認不明 | 全形式の異常値行列 | 形式別エラー経路の回帰 | 採用 |
| 変更境界 | 有効minで入力失敗の新経路未検証 | N>1の各形式exit1 | 空成功への誤変換 | 採用、権限試験不能は未検証 |
| FR-3/README | 全除外でも既存空状態文言 | READMEで閾値調整案内 | 入力の誤修正 | 採用、HTML文言は維持 |
| AC4 | 内部順序の証拠形式がない | ソース行/diffを記録 | 出力一致だけで順序承認 | 採用 |

## edge-case-hunter

FR-3/AC5の「非空入力なら正の総数」は、空白・句読点だけの抽出0語入力で矛盾する。抽出0語は総数0、抽出語ありの閾値全除外は元総数正、と分離する提案を採用。Brief/PRD/spec/design/tasksへ反映した。

## structure

- PRD冒頭で背景質問は非ブロッカーである旨を先出し: 採用。
- 目指す状態を文書の目的より前へ: 不採用。最初の短い目的節が入力とdraft/非ブロッカーを示し、次節で結論を示す現構成を維持。
- Briefスポンサー/将来像の省略理由を本文外へ: 不採用。公式テンプレートの各節を明示的にsettleした監査記録として短く維持。
- PRDの節の取捨を別記録へ: 不採用。同じ理由で短い1段落を維持。いずれも製品判断を変えない編集提案。

## prose

Brief AC-MC-05の「非空入力」の残存を指摘。抽出語がある入力を閾値で全除外した場合、と修正し解決。

## 最終再確認

修正後のBrief・PRD・proposal・spec・design・tasksを別のedge-case-hunterに独立再照合し、公式findingsは`[]`。completed、truncated=false。OpenSpecの厳格検証成功、isPlanningComplete=trueを確認。BMADの各文書単独check_idsはundefined/duplicate/withdrawn/tocが空。文書間のQ-01/Q-02重複は同じ質問の明示的な継承であり、別問題のID衝突ではない。

## 結果と限界

機能上の未決判断なし。Q-01/Q-02の背景質問は未解決のままopen-questions.mdへ転記し、仮定は未承認。BMAD文書はpartial/draftを維持。別立てArchitectureは新たな構成/依存/移行がない小規模拡張なので作らず、OpenSpec designに最小設計を記録する。本レビューは文書のレビューであり、新機能のpytest成功や製品ブラウザ受入ではない。
