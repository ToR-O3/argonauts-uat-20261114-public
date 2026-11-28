# BMAD independent review

親workerが公式 bmad-review の customization を解決し、3つのレンズを別々のdelegate_taskで実行。すべて exit_reason=completed、truncated=false。初回作成担当による逐次fallbackを独立レビューの代用にせず、この記録を最終の独立結果とする。

対象: Brief、PRD、Architecture、open-questionsの4原本。docsであるためverification-gap(code専用)は非該当。copy-editing依頼ではないためproseは非該当。

## adversarial

各行は公式の location / trigger_condition / guard_snippet / potential_consequence の順。

| location | trigger_condition | guard_snippet | potential_consequence |
| --- | --- | --- | --- |
| OQ-2 / FR-2 / AD-2 | 生の行頭#とtrim後判定の承認範囲が曖昧 | 生の行頭#は最低限の確定であり唯一の方式の確定ではないと明記 | 字下げコメントの未承認固定 |
| OQ-4 / Glossary | 有効1語の語彙判定が未定義 | 数字・underscore・結合文字・hyphenを含む有効行判定も問いに含める | 受入の解釈が割れる |
| FR-2 / OQ-2・4 | LF/CRLF/最終改行なしの扱いが未記載 | 行終端除去をtrimとは分離して記録 | CR混入や最終行欠落 |
| API contract / Non-goals | --exclude複数回の扱い不明 | 複数FILE結合は対象外、重複指定の既存parser規則を確認 | 最後のFILEのみ黙って採用 |
| FR-1 / API contract | FILE '-'の解釈不明 | 標準入力を新設しないことを明記 | 無人実行の入力待ち |
| OQ-3 / FR-4 | 他の取得失敗のチャネルが不明 | 終了コードとstdout/stderr/Tracebackの扱いを確認 | 部分結果・Tracebackの流出 |
| OQ-5 / AD-3 | 同時失敗の例が不存在同士だけ | 優先規則は失敗種別全体で回答する | 組合せごとに未承認動作 |
| FR-5・7 / OQ-1 | 空本文と空除外FILEが混在 | 空本文・空/コメントのみ除外FILE・不一致・全除外を区別 | 空除外FILE不具合の見逃し |
| FR-7 | 比較元commitが未記載 | 既存headと比較入力を記録 | 自己生成期待値による循環検証 |
| OQ運用 / Open questions | 回答からゲート解除の追跡がない | 回答参照・決定・影響FR/AD・ゲート状態を記録 | 古い文書で実装承認 |

## edge-case-hunter

```json
[]
```

## structure

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| structure | Architecture Deferredに承認ゲートと裁量が混在 | 承認ゲートと裁量を明確に分離 | 誤読防止。現状にも区別が明記されているため再配置は任意 |
| structure | Structural Seedのデータフロー図 | Design Paradigmへ移動 | 可読性の提案、挙動の不足ではない |
| structure | PRD MVP scopeとStories | 重複を集約 | templateの必須節は保ち、今回は延期 |
| structure | OQの項目順が不統一 | 問い・根拠・影響・回答時点に統一 | 回答欄を追加して追跡性を補う |
| structure | 文書内のテンプレート選択説明 | 作成記録へ移動 | 任意の編集改善、今回は延期 |
| structure | 各FRの短い未決注記 | PRESERVE | 正本一覧への参照は維持 |

## Triage

adversarialの指摘は明確化か既存OQへの追記で受ける。複数回指定の新しい製品動作と標準入力対応は作らず、既存引数規則/通常パスのままとする提案であり承認ではない。有効行外の例はOQ-4の問いに集約する。追加の独立した製品ゲートは増やさない。構造の再配置や重複削減は任意提案として延期し、未決を消さない。5つの製品判断は未解決のままPMに渡す。レビューは仕様承認や実装試験の合格を意味しない。
