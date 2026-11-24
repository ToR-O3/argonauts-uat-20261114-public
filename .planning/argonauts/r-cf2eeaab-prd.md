# Approved OpenSpec PRD: r-cf2eeaab

# Proposal

## Why

依頼者が指定したプロジェクト説明文を正確に記録する。現物にdescriptionがないため、最新判断（2026-11-24T19:13:42.938043+00:00）「新しく作ってよい。完成後の説明文は『argonauts-uat public (UAT)』とする。」に基づき、旧追記条件を新規追加・完成値一致へ置き換える。

## What Changes

- 後続実装で `pyproject.toml` の `[project].description` を新規追加し、解析後の値を厳密に `argonauts-uat public (UAT)` とする。完成値にさらに印を追加しない。
- 製品差分は当該項目のみ。他の製品ファイル・既存TOML項目と値・既存行は維持する。
- 変更後のTOML正常解析、文字列完全一致、対象項目以外の差分なしを直接検証する。
- full工程を維持し、工程文書をPRに含める。危険パスのためsmartでもマージは人が行う。

## Capabilities

### New Capabilities

なし。実行時のシステム動作を変えない、説明文メタデータのみの変更である。

### Modified Capabilities

なし。既存の `wordfreq-cli` と `readme-verification-note` の要求は変更しない。`.openspec.yaml` に `skip_specs: true` を明示する。仕様検証のために架空の能力を追加しない。

## Impact

製品対象は `pyproject.toml` の説明文1項目のみ。依存、ビルド設定、名称、バージョン、CLI、既存テスト、workflow、権限、外部通信、課金、データは変更しない。Architecture文書の追加は不要。

根拠は `_bmad-output/initiative-r-cf2eeaab/brief/brief-project-description-uat.md` と `_bmad-output/initiative-r-cf2eeaab/prd/prd-project-description-uat.md`。未決事項なし。このカードは文書を作成する工程であり、製品の実装・受入完了を意味しない。


# Tasks

仕様上の振る舞い変更がないためspecsはskip_specsで省略。要求と受入条件はproposal.mdおよびBMAD PRD、検証方式はdesign.mdを参照。未決事項なし。

## 1. 説明文の新規追加と直接検証

- [ ] 1.1 `.planning/argonauts/r-cf2eeaab/` に標準ライブラリのみの検証ファイルを用意する。起点 `c572613dc626160db2eb3bf4a41c95fc8283b828` と比較し、TOML正常解析、project.descriptionの完成値 `argonauts-uat public (UAT)` との厳密一致、当該キー以外の解析データ不変、追加行除外後のバイト列一致、工程文書以外の製品差分が対象ファイルだけであることを検査する。実装前にdescription欠落で失敗することを実コマンド・終了コードで確認し、工程文書に記録する。既存製品テストと依存は変更しない。
- [ ] 1.2 `pyproject.toml` の `[project]` へ `description = "argonauts-uat public (UAT)"` の1行だけを追加し、1.1と同じ検証を成功させる。完成値にさらに印を足さない。コマンド・起点と対象head・終了コード・値と差分・AC別結果を工程文書に記録し、既存TOML項目および他製品ファイルが不変であることを確認する。

## Workflow follow-up

- 品質が対象headで検証を独立実行し、VERIFICATION.md等の文字の証拠を添付する。PMは文字から条件別結果を判断できること。
- 仕様承認・計画・実装・レビュー・受入の各ゲートを経た後、最終化のカードでsync・archiveする。pyproject.tomlは危険パスのため、smartでも人がマージする。
