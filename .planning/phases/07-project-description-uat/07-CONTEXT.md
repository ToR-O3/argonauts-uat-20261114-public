# Phase 7: Project description UAT - Context

**Gathered:** 2026-11-25
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-cf2eeaab-prd.md)
**Approval:** t_8a187e42; source t_62c33f31 run59, head40be2dc5df129e7b77bbcac55559ffda58dd1343

<domain>
承認済みr-cf2eeaab-project-description-uatの全体、tasks1.1/1.2。製品変更はpyproject.toml description新規1行だけ。REQ-25, REQ-26, REQ-27をPhase7で扱う。公式phase.addが7を返した。旧phaseのstaleや残存成果は再利用・修復しない。UI/AI/API変更なし。
</domain>

<decisions>
## Implementation Decisions (locked)
- D-01: [project].descriptionを新規追加し解析値を厳密に `argonauts-uat public (UAT)` とする。さらに印を足さない。判断日時2026-11-24T19:13:42.938043+00:00、原文「新しく作ってよい。完成後の説明文は『argonauts-uat public (UAT)』とする。」
- D-02: 製品は当該1行だけ。既存TOML項目・値、既存行・改行・バイト、他製品ファイルを変えない。全体再シリアライズしない。
- D-03: 検証ファイルを `.planning/argonauts/r-cf2eeaab/` に作る。標準ライブラリのみ。既存製品テスト・依存・CI・CLIを変更しない。
- D-04: 固定起点 `c572613dc626160db2eb3bf4a41c95fc8283b828` と比較。TOML正常解析、完成値完全一致、description以外の解析データ一致、追加行除去後の生バイト一致、工程文書以外の製品差分がpyproject.tomlだけであることを検査。HEAD比較だけで未commit/未追跡の製品変更を見逃さない。
- D-05: 検証ファイルを先に実体として作成→description欠落の実測RED→最小1行追加→同じ検証でGREEN。環境エラー・import失敗・TOML破損を期待REDとしない。違反を確実に落とす検証設計にする。
- D-06: コマンド・終了コード・値・差分・起点・検証対象head・AC別結果を工程文書に記録。品質は対象headで独立再実行しVERIFICATION.mdとCLI文字証拠原本を標準添付。PMはread_fileで判断できること。画像不要は0枚・理由を記す。画像が必要なら品質の実閲覧枚数と結果を文字化し、PMへ画像・圧縮ファイルを開くよう求めない。
- D-07: full、skip_specs=true（振る舞い変更なし）、未決事項なし。危険パスpyproject.tomlのためsmartでも人がマージする。最終化sync/archiveは後工程。
- D-08: 各PLAN3tasks以内、同じ依頼branchへ番号順に直列積上げ。各task終了時点に検証入力が実在し、独立PLANは他PLANの有無に依存せず検証可能。phase検証では先行PLAN含む全成果が同branchに揃う。automatedに無人実行できる検証ファイルのコマンドをそのまま書き、外側cd/grep/インラインコードを付けない。fails_whenは対象誤動作を失敗として観測する条件。

### Claude's Discretion
検証ファイルの局所的な構成、工程記録、PLAN分割。製品範囲や完成値の変更は裁量外。
</decisions>

<canonical_refs>
- .planning/argonauts/r-cf2eeaab-prd.md — 承認proposal→tasks（spec省略）
- openspec/changes/r-cf2eeaab-project-description-uat/proposal.md
- openspec/changes/r-cf2eeaab-project-description-uat/tasks.md
- openspec/changes/r-cf2eeaab-project-description-uat/design.md
- _bmad-output/initiative-r-cf2eeaab/brief/brief-project-description-uat.md
- _bmad-output/initiative-r-cf2eeaab/prd/prd-project-description-uat.md
- .planning/ROADMAP.md — Phase7
- .planning/REQUIREMENTS.md — REQ-25, REQ-26, REQ-27
- .planning/argonauts/r-cf2eeaab-learnings.md — 参考のみ、PRDではない
</canonical_refs>

<deferred>
依存・既存製品テスト・CI・画面・実行時動作・旧phase修復は範囲外。実装・実検証・受入・最終化は後続カード。
</deferred>
