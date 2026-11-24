# Tasks

仕様上の振る舞い変更がないためspecsはskip_specsで省略。要求と受入条件はproposal.mdおよびBMAD PRD、検証方式はdesign.mdを参照。未決事項なし。

## 1. 説明文の新規追加と直接検証

- [ ] 1.1 `.planning/argonauts/r-cf2eeaab/` に標準ライブラリのみの検証ファイルを用意する。起点 `c572613dc626160db2eb3bf4a41c95fc8283b828` と比較し、TOML正常解析、project.descriptionの完成値 `argonauts-uat public (UAT)` との厳密一致、当該キー以外の解析データ不変、追加行除外後のバイト列一致、工程文書以外の製品差分が対象ファイルだけであることを検査する。実装前にdescription欠落で失敗することを実コマンド・終了コードで確認し、工程文書に記録する。既存製品テストと依存は変更しない。
- [ ] 1.2 `pyproject.toml` の `[project]` へ `description = "argonauts-uat public (UAT)"` の1行だけを追加し、1.1と同じ検証を成功させる。完成値にさらに印を足さない。コマンド・起点と対象head・終了コード・値と差分・AC別結果を工程文書に記録し、既存TOML項目および他製品ファイルが不変であることを確認する。

## Workflow follow-up

- 品質が対象headで検証を独立実行し、VERIFICATION.md等の文字の証拠を添付する。PMは文字から条件別結果を判断できること。
- 仕様承認・計画・実装・レビュー・受入の各ゲートを経た後、最終化のカードでsync・archiveする。pyproject.tomlは危険パスのため、smartでも人がマージする。
