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
