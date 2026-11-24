# 独立レビューと対応（r-774f3cd6、revise=1）

対象はBrief・PRD・open-questions.md・OpenSpec proposal/design/specs/tasksの7文書の改訂差分。公式bmad-review設定を解決し、adversarial・edge-case-hunter・structureを独立委任、proseをstructure結果付きで後続委任した。全レンズ通常終了・打切りなし。実装レビューではない。Architecture変更不要。

判断原本：受付t_78c8849e、defaultコメント、2026-11-24T13:00:38.567271+00:00。
原文：「②を選ぶ。description を新設してよい。連結元の文字列は「argonauts-uat public」、完成値は「argonauts-uat public (UAT)」とする。」

## adversarial

公式の4欄と親の対応。重複指摘も保持する。

|location|trigger_condition|guard_snippet|potential_consequence|対応|
|---|---|---|---|---|
|tasks 1.1|承認文書revision未指定|文書commit/hashで承認対象固定|旧仕様承認の流用|design Verification contractへ反映|
|design 基準|他製品の比較tree不明|repo全体の基準固定|混入差分を見落とす|同節へ反映|
|design git差分|index/commit差分の範囲不明|基準〜製品commit、index、worktree確認|通常diffだけで合格|同節へ反映|
|tasks 1.3|検証hashとcommit blobの対応不明|blob hashと検証ファイルhash一致|未commitの結果を別commitに付与|同節へ反映|
|design 工程除外|ディレクトリ単位で任意コード除外可能|具体的pathと用途記録|範囲迂回|同節へ反映|
|design 書式|空白無視diffで見落とす|追加行除外後のbyte一致|無関係整形が残る|同節へ反映|
|tasks 1.2|欠落だけでは検証器の誤りを見逃す|重複・別値・他項目・不正TOMLの負例|誤検証器を信用|同節へ反映、負例は工程管理領域のみ|
|tasks 1.2|期待失敗と基盤失敗が曖昧|解析/取得成功と条件不一致を区別|実行エラーをRED扱い|同節へ反映|
|tasks 1.3|編集後失敗時の扱い不明|未完了停止、差分と理由を返す|失敗状態で完了や範囲外修復|同節へ反映|
|tasks follow-up|archive条件と全条件の結合不足|全task・同一commit検証・受入を必須化|部分完了でarchive|反映。ただしチーム規約どおりsync/archiveは受入後の最終化で行い、その後に品質最終確認する|

## edge-case-hunter

公式結果：`[]`。追加指摘なし。製品受入やPM承認の合格を意味しない。

## structure

|Pass|Original Text|Revised Text|Changes・対応|
|---|---|---|---|
|structure|tasks 1.3に編集・検証・記録が集中|1.3/1.4/1.5へ分割|既存OpenSpec task IDの維持を優先し番号追加は見送り。計画内で別substepとして表示する条件をfollow-upへ追記|

## prose

|Pass|Original Text|Revised Text|Changes・対応|
|---|---|---|---|
|prose|対象・descriptionの欠落・その他の基準内容が承認記録と異なる|対象が異なる、descriptionが存在する、その他の基準内容が異なる|停止条件を直接表現へ修正し反映|

## 引継ぎ

Brief・PRDはfinal。OQ-1は回答済みで未解決質問は空。既存OpenSpec変更名を維持した。上記修正後の7文書を親が照合し、指定連結元は現物の旧値ではないこと、固定完成値、新設許可、その他不変、TOML有効、検証スクリプトの工程領域限定が整合することを確認する。実行コマンドは次の計画で確定し、製品試験・実装・PM再承認は本工程では行わない。pyproject.tomlの危険パスによりfullを優先した理由を最終報告まで引き継ぐ。
