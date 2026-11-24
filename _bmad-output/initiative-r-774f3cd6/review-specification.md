# 独立レビューと対応（r-774f3cd6）

対象：Brief、PRD、open-questions.md、OpenSpec proposal・spec・design・tasksの7文書。文書作成のレビューであり、実装の検証ではない。公式bmad-review設定を読み、adversarial・edge-case-hunter・structureを別々の同期委任で実施し、その後structure結果を渡してproseを委任した。全レンズは通常終了、打切りなし。Architecture変更なし、Architecture文書は作成しない。

## adversarial

以下は公式のlocation／trigger_condition／guard_snippet／potential_consequenceに対応する。指摘の重複は統合せず保持する。

|location|trigger_condition|guard_snippet|potential_consequence|対応|
|---|---|---|---|---|
|Brief Scope、PRD Change boundary|本runの出力範囲が文書一式と衝突する読みに見える|工程ローカルな制約と明記|OpenSpec等を範囲外と誤認|Brief作成工程、PRD作成工程へ修正|
|spec 未確定の元値|新設承認後の仕様改訂条件が不十分|Brief・PRD・OpenSpecの整合した改訂を必須化|古い連結契約と新設承認が衝突|spec/tasksへ反映|
|open-questions 選択肢①|正しい対象と現worktreeの対応が曖昧|repo・branch/commit・pathと現物一致を確認|別branchの値を無承認新設|open-questions/tasksへ反映|
|spec 未確定の元値|非文字列の場合が未明示|欠落・非文字列・解析不能を停止条件へ|型変換を独自判断|specへ反映|
|tasks 1.1–1.2|承認後に現物が変化する場合|編集直前に承認基準を再照合|古い値で上書き|tasks 1.3へ反映|
|spec 既存接尾辞scenario|実装承認の条件が一方だけ|両scenarioに実装承認を明記|元値確認を実装承認と誤認|specへ反映|
|design Decisions、tasks|検証コマンド確定の時点が曖昧|計画でコマンド・基準取得・期待結果を確定|比較方法が担当ごとに変わる|tasks 1.2へ反映|
|tasks RED確認|どんな失敗もRED扱い可能|解析・基準取得成功、未追加による一致検査失敗を区別|壊れた検証を信用|tasks 1.2へ反映|
|design/tasks 差分|git diffだけでは未追跡追加を見逃す|未追跡一覧も製品/工程へ分類|他製品ファイル追加が漏れる|tasks 1.3へ反映|
|design/tasks head識別|未コミット編集は同じheadでも変化する|製品commitと対象SHA-256を記録|品質と実装が違う内容を検証|tasks 1.3/follow-upへ反映|

## edge-case-hunter

公式返答：`[]`。追加指摘なし。既知のOQ-1を解決済みと判定したものではない。

## structure

|Pass|Original Text|Revised Text|Changes・対応|
|---|---|---|---|
|structure|tasks 1.2に準備・RED・編集・検証が集中|作業単位を分ける|1.1承認、1.2検証準備RED、1.3編集GREENへ分割|
|structure|open-questions末尾に担当行動と停止条件|状態を先頭へ移動|見送り：チーム規約の先頭3行（状況・決めること・選択肢）を優先。停止条件は明記済み|
|structure|選択肢が1段落|番号付きリストへ|見送り：先頭3行の質問形式を維持。①②③と結果は同じ行に保持|

## prose

|Pass|Original Text|Revised Text|Changes・対応|
|---|---|---|---|
|prose|tasks「承認済みbeforeとの値の完全一致」|変更後descriptionとbefore.descriptionにASCII ` (UAT)` を1回連結した値との一致|期待値を明確化して反映|

## 引継ぎ

OQ-1は未解決。BMADはpartial/draftとして保持する。文書一式の保存・CLI構造検査が成功しても、製品実装と受入は未完了。仕様承認PMはopen-questions.mdの一問を集約し、新設/元値を推測せず判断を得る。
