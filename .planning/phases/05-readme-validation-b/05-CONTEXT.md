# Phase 5: README validation B - Context

**Gathered:** 2026-11-22
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-215b4390-prd.md)

<domain>
## Phase Boundary
承認済みr-215b4390。README.mdへの指定1行追記のみ。REQ-22、OpenSpec task 1.1。既存のwordfreq機能は変更しない。
</domain>

<decisions>
## Implementation Decisions
### Locked: 指定の文書状態
- **D-01:** `検証B: v1.12 の通しの確かめ（2026-11-22）` を引用符なしの独立した最終行として1回だけ追加する。文字列の言い換えは禁止。
- **D-02:** 既存内容・書式・改行形式を保持する。README差分は上記1行追加のみ、削除・置換・移動・余分な空行や説明なし。
- **D-03:** コード・試験・他の製品ファイルは変更しない。新しい製品の振る舞い・試験ファイル・自動追記機能や検証スクリプトを追加しない。工程記録は別扱い。
- **D-04:** 完了時CLIで最終行完全一致・README全体の指定行出現1回・差分1行追加のみ・工程記録を除く製品変更README.mdのみを確認し、文字の工程検証記録へ残す。指定行自体は検証合格の証拠ではない。
- **D-05:** 人の回答によりskip_specsは使わず、最小specは指定行存在の1要求のみ。機能要件を増やさない。
- **D-06:** 所定の実装レビュー・phase検証・受入の後に最終化工程でsync/archiveする。この計画工程では実装しない。
### Claude's Discretion
既存CLIで承認条件を確認する具体的なコマンドと、工程記録の構成のみ。範囲の拡張や新規試験は裁量外。
</decisions>

<canonical_refs>
## Canonical References
- .planning/argonauts/r-215b4390-prd.md — 承認proposal、spec、tasksを順に結合したPRD入力。
- openspec/changes/r-215b4390-readme-validation-b/proposal.md — 変更境界。
- openspec/changes/r-215b4390-readme-validation-b/specs/readme-validation-b/spec.md — 唯一の文書要件。
- openspec/changes/r-215b4390-readme-validation-b/design.md — 直接追記と既存CLI確認。
- openspec/changes/r-215b4390-readme-validation-b/tasks.md — task 1.1。
- _bmad-output/initiative-r-215b4390/brief/brief-readme-validation-b.md
- _bmad-output/initiative-r-215b4390/prd/prd-readme-validation-b.md
- .planning/REQUIREMENTS.md — REQ-22。
- .planning/ROADMAP.md — Phase 5。
- .planning/argonauts/r-215b4390-learnings.md — 計画参考。製品要求へ混ぜない。
</canonical_refs>

<specifics>
## Specific Ideas
品質はVERIFICATION.mdとCLI証拠文書にhead・コマンド・結果・受入条件対応を書き標準添付する。画像を見た枚数は0（UI変更なし）と理由を記録し、PMへ画像や圧縮ファイルの閲覧を要求しない。
複数PLANなら同一依頼branchへ直列に積み上げる。各task終了時とphase検証時で実行できる検証とし、独立PLANは他PLANの有無に依存させない。誤動作を既存CLIの非0終了/差分で観測する。
</specifics>

<deferred>
## Deferred Ideas
機能・API・依存・権限・データ・外部送信・費用の変更、既存文書の整形、新しい試験は対象外。過去phaseのstale検証は今回の範囲外。未決事項なし。
</deferred>
