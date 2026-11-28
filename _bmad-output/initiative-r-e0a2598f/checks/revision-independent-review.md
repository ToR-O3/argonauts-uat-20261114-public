# 更新原本の独立レビューと採否

対象: Brief、PRD、Architecture、OpenSpec proposal/design/spec/tasksの更新差分。製品コードは対象外。
公式 bmad-review のcustomizationをresolveし、adversarial・edge-case-hunter・structureを独立して並列委任した。proseはstructureの結果を渡して別委任した。すべて completed / exit_reason=completed / truncated=false。

## adversarial

公式レンズが返した10指摘を、location / trigger_condition / guard_snippet / potential_consequenceの意味を保って以下に記録する。

|location|trigger_condition|guard_snippet|potential_consequence|採否と根拠|
|---|---|---|---|---|
|Architecture Structural Seed|データフロー図が取得の必須順序を示さない|データ依存だけの図と明記しAD-3を参照|本文先行・並列取得を選び得る|採用。図直後に制御順の注意を追加。AD自体は変更しない|
|PRD FR-4 / 不正行scenario|無視行の後の元の行番号を例示していない|空行・コメント・有効語・不正行の4行例を追加|圧縮後の添字を診断に使い得る|採用。元ファイル4行目の期待値をPRDとspecへ追加|
|PRD FR-4 / 除外先行scenario|後方の不正行に対する全行検証の例がない|有効行の後に不正行があっても本文取得ゼロ|遅延検証で本文を読んでしまい得る|採用。上記4行例に本文取得ゼロを明記|
|PRD FR-2/3|casefold前後の検証順を区別するUnicode例がない|casefoldで結合文字を含む有効語の例|casefold後検証へ誤って入れ替え得る|今回は追加例を見送る。FR-2/AD-2は検証後casefoldを既に明記、FR-7はその検査を要求。新しい単語例を未確認で創作しない|
|spec EX-2|大小変化なしの非ASCII有効語例がない|日本語等の有効語の除外例|ASCII限定検証へ狭め得る|今回は追加例を見送る。既存Unicode規則を契約として明記し、FR-7のUnicode試験要求を保持。新仕様は不要|
|AD-2 / PRD FR-7|除外FILEの語順・重複不変の検証が明示されない|異なる順序・重複ありのFILE比較|除外順が本文順位へ混入し得る|今回は独立の受入例追加を見送る。AD-2の規則とFR-7同数順検査は既存のまま保持。計画時に検査へ具体化できる|
|spec EX-4|除外後に同数の複数語が残る例がない|残存語の本文初出順とtop境界の例|集合順・辞書順による再構築を見逃し得る|今回は例追加を見送る。EX-1/4の残存初出順とPRD FR-7の同数順試験が明示済み。採用5決定の範囲を広げない|
|spec EX-4|top/min-count併用とHTML元総数が別scenario|併用scenarioに総数5を追加|フィルタ後の総数を使う実装を見逃し得る|採用。併用scenarioへHTML総数5を追記|
|spec 各読込み失敗|各読込み失敗のscenarioに全形式の指定がない|text/json/htmlを明記|HTMLだけ部分出力する不整合を見逃し得る|採用。各形式で実行と明記|
|PRD Non-goals / 旧未決一覧|FILE `-`の標準入力対応を追加しない制約が一覧削除と共に消えた|PRD Non-goalsへ移す|新しい入力元を追加し得る|採用。既存の範囲外制約をPRDへ移動。通常パスや重複指定の新規則は決めない|

## edge-case-hunter

公式結果: `[]`。具体的な製品契約矛盾なし。

## structure（doc_standards）

公式tableの提案は2件: AD-2/3のRuleを同じ内容の箇条書きへ分割するCONDENSE、source-contextの実行管理説明をhandoffへ移すMOVE。両方とも削減0語。任意の走査性改善として今回は不採用。IDと既存の文書構造を維持し、製品決定の差戻し範囲に集中する。情報の欠落はない。

## prose（structure後のdoc_standards）

公式tableの2提案を採用: (1) PRD GlossaryとAD-4の「除外条件を満たす」を「除外対象ではなく、min-countを満たす」に変更。(2) PRD journeyの「説明、失敗の必要性」を「使い方の説明、失敗時の原因通知の必要性」へ明確化。契約変更なし。

## その他の公式レビュー

Brief/PRD: rubricとfresh-readerはPASS、critical/high/mediumなし。rubricの任意短縮・成功指標の言い換えは不採用（成功条件は各FRの明示受入と対抗指標で既に検査可能）。
Architecture: good-spine rubric、reconciliation、reality-check、divergenceをすべて完了。blocking指摘なし。FR-7比較基準のspineへの重複追記はPRD参照で足りるため見送る。
入力reconciliation: 原依頼/initiative/Brief/PRD/採用決定の重大な取りこぼしなし。tasksから最終引継ぎへの未作成参照だけが指摘されたため、同じパスにREVISION-HANDOFF.mdを正式作成する。

文書状態はレビュー集約後finalにした。これは後続PMによる仕様承認を代行せず、製品試験が合格したという意味でもない。
