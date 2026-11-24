# Phase 6: pyproject description UAT - Context

**Gathered:** 2026-11-24
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-774f3cd6-prd.md)

<domain>
## Phase Boundary
依頼r-774f3cd6、REQ-23。pyproject.tomlの[project].descriptionを1行新設する。CLI/API/画面/依存/CI/Architectureは変えない。製品実装は後続Builder。本計画は製品を編集しない。
</domain>

<decisions>
## Implementation Decisions

### 承認と固定入力
- D-01: 受付t_78c8849eの依頼者判断日時2026-11-24T13:00:38.567271+00:00、原文「②を選ぶ。description を新設してよい。連結元の文字列は「argonauts-uat public」、完成値は「argonauts-uat public (UAT)」とする。」が正本。OQ-1は回答済み、再質問不要。
- D-02: 改訂仕様head56b70bdca4349c6d2f9eaeb62be2e340a3e04b49はPM t_b8e9c36c run37 approved。元の未改訂仕様承認と新設回答を組み合わせず、この改訂承認を照合する。
- D-03: 完成値は正確に `argonauts-uat public (UAT)`。ASCII ` (UAT)` の連結1回。指定連結元 `argonauts-uat public` は現物の旧値ではない。正規化、重複、空文字補完は禁止。
- D-04: 不変比較元treeは `b34cba0d008923e7f5267ce52d5403492ea53925`。基準/現物のdescription欠落、repo ToR-O3/argonauts-uat-20261114-public、依頼branch argonauts/r-774f3cd6、対象パス/全内容を実装直前にも再照合。不一致・description既存・解析不能なら製品を編集せずPMへ返す。

### 変更の境界
- D-05: 製品変更はdescription新設1行のみ。全体再シリアライズせず既存バイトを保持。他TOML項目、依存、他製品ファイル、無関係な書式、空白/改行/末尾改行は不変。製品試験・CIの追加変更禁止。検証スクリプト/負例/証拠は工程管理領域に限定する。
- D-06: 比較先は製品commitに固定。基準→製品commitの全追跡差分（追加/削除/改名/mode含む）、index、作業ツリー、未追跡一覧を確認。工程成果物の除外パスと用途を全件列挙し、任意コードを工程ディレクトリというだけで除外しない。

### 試験と直接観測
- D-07: OpenSpec1.1で承認・対象・基準と欠落を証拠に固定。1.2で工程領域の検証スクリプトを先に作り具体的コマンドと基準取得方法を確定。編集前は正常解析/基準取得が成功し、固定完成値条件だけ不一致の期待失敗を記録。欠落キーへの無条件参照の異常終了は期待失敗ではない。
- D-08: スクリプトの正しい完成値成功と、工程領域内負例（欠落、suffix重複、異なる値、他項目変更、不正TOML）拒否を確認。要件不一致と実行エラーを区別。製品へ負例を書かない。
- D-09: OpenSpec1.3は(a)直前照合/1行新設、(b)条件別検証、(c)証拠記録のsubstepとして進捗表示。tomllib全体解析、固定完成値完全一致、編集後からdescriptionだけ除いた構造と基準の完全一致、追加1行を除いた生バイトと基準の完全一致、生テキストgit差分/未追跡で他製品不変を検証。必須失敗・実行不能は未完了停止し残存差分を記録、無関係な修復/他者差分一括復元は禁止。
- D-10: 基準commit、製品commit、検証対象head、ファイルSHA-256、コマンド、終了コード、条件別結果を文字の証拠に残す。品質は同一製品commit blobのSHA-256と検証ファイルの一致を独立再確認し、VERIFICATION.mdとCLI証拠を標準添付、PMはread_fileだけで判断可能とする。画像/圧縮ファイルを求めない。

### 工程境界
- D-11: 全タスク完了・同一製品commitの独立品質合格・全受入条件成立・PM受入の後だけ、最終化でsync/archive。文書final/OQ解消だけでは実行しない。
- D-12: pyproject.tomlは危険なパスのため受付lightよりfullを優先した理由を最終報告まで引継ぐ。既存閉じたphase/過去の決定を書き換えない。既存phase1/3/4/5のstale検証は今回対象外。

### Claude's Discretion
工程領域のファイル名、標準ライブラリだけの検証CLI詳細、PLAN分割（各3task以内）、証拠文書の配置。順序は同じ依頼branch上へ直列に積み、各task終了時点で検証コマンドと入力が存在するようにする。品質はBuilderと別主体で同じ対象を確認する。
</decisions>

<canonical_refs>
## Canonical References
**Downstream agents MUST read these before planning or implementing.**
- `.planning/argonauts/r-774f3cd6-prd.md` — proposal→全spec→tasks結合の承認入力
- `openspec/changes/r-774f3cd6-pyproject-uat/proposal.md`
- `openspec/changes/r-774f3cd6-pyproject-uat/specs/package-metadata/spec.md`
- `openspec/changes/r-774f3cd6-pyproject-uat/design.md` — Verification contractも必須
- `openspec/changes/r-774f3cd6-pyproject-uat/tasks.md` — 1.1〜1.3と品質/最終化境界
- `_bmad-output/initiative-r-774f3cd6/brief/r-774f3cd6-brief.md`
- `_bmad-output/initiative-r-774f3cd6/prd/prd-r-774f3cd6.md`
- `.planning/REQUIREMENTS.md` — REQ-23
- `.planning/ROADMAP.md` — Phase6
- `.planning/argonauts/r-774f3cd6-learnings.md` — 計画参考。承認入力に混ぜない
</canonical_refs>

<specifics>
## Specific Ideas
固定基準はdescription欠落の不変比較元、指定連結元は依頼者入力。両者を証拠でも別項目にする。最小1行でも解析構造・生バイト・全Git状態の検証を省かない。
</specifics>

<deferred>
## Deferred Ideas
CLI/API/画面/依存/CI/Architecture変更、製品試験追加、他製品編集、過去phase修復は対象外。sync/archiveは最終化工程のみ。
</deferred>

*Phase: 06-pyproject-description-uat*
*Context gathered: 2026-11-24 via PRD Express Path*
