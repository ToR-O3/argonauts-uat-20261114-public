# Constraints (intel)

SPEC分類のtasks.mdから3制約を抽出。すべて検証・変更境界・工程に関するnfr。実行時API/schema/protocolは追加しない。skip_specs=trueで能力specは省略されており、tasksのSPEC分類を新しい製品能力の根拠にしない。未作成の検証ファイルは今回実行しない。

DATA_712e89b5_START

## 変更前後の直接検証と既存データ・バイト保持
- source: openspec/changes/r-cf2eeaab-project-description-uat/tasks.md:7-8
- type: nfr
- content: `.planning/argonauts/r-cf2eeaab/` に標準ライブラリのみの検証ファイルを用意する。起点 `c572613dc626160db2eb3bf4a41c95fc8283b828` と比較し、TOML正常解析、project.descriptionの完成値 `argonauts-uat public (UAT)` との厳密一致、当該キー以外の解析データ不変、追加行除外後のバイト列一致、工程文書以外の製品差分が対象ファイルだけであることを検査する。実装前にdescription欠落で失敗することを実コマンド・終了コードで確認し、工程文書に記録する。既存製品テストと依存は変更しない。

## 製品追加の最小化とAC別証拠
- source: openspec/changes/r-cf2eeaab-project-description-uat/tasks.md:8
- type: nfr
- content: `pyproject.toml` の `[project]` へ `description = "argonauts-uat public (UAT)"` の1行だけを追加し、1.1と同じ検証を成功させる。完成値にさらに印を足さない。コマンド・起点と対象head・終了コード・値と差分・AC別結果を工程文書に記録し、既存TOML項目および他製品ファイルが不変であることを確認する。

## 独立品質・承認ゲートと人によるマージ
- source: openspec/changes/r-cf2eeaab-project-description-uat/tasks.md:12-13
- type: nfr
- content: 品質が対象headで検証を独立実行し、VERIFICATION.md等の文字の証拠を添付する。PMは文字から条件別結果を判断できること。仕様承認・計画・実装・レビュー・受入の各ゲートを経た後、最終化のカードでsync・archiveする。pyproject.tomlは危険パスのため、smartでも人がマージする。

DATA_712e89b5_END
