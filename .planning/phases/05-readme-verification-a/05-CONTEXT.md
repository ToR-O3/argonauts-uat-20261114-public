# Phase 5: README verification A - Context

**Gathered:** 2026-11-22
**Status:** Ready for planning
**Source:** PRD Express Path (.planning/argonauts/r-8ac79daf-prd.md)
**Approval:** t_327d2f8f run7 approved; source t_bdf6acb4 run6 at fb500ae864e6fb734e26e899f65fe78ca2aa20f7

<domain>
## Phase Boundary
承認済みOpenSpec r-8ac79daf-readme-verification-aの全体、tasks 1.1と2.1。README末尾への指定1行掲載のみ。既存GSDへ要求追加だけのmergeを行い公式phase.addが返した5を使う。旧phase1/3/4のstale検証や歴史的な要求表記は表示するが今回へ混ぜない。画面、コード、試験、依存、CIを変更しない。
</domain>

<decisions>
## Implementation Decisions (locked)
- **D-01:** README.mdに `検証A: v1.12 の通しの確かめ（2026-11-22）` を独立した最後の1行として追加。かぎ括弧、句点、余分な前後文字なし（REQ-22）。
- **D-02:** 指定行の後に空行・別文言なし。既存行へ連結しない。既存内容・順序・改行形式を保持し、削除・書換え・不要空行を加えない（REQ-23）。変更前の末尾・改行を確認して記録する。
- **D-03:** 既存CLIで文字列完全一致・末尾位置・README全差分を確認し、新旧コード・試験ファイルは一切変更しない。新規検証スクリプトも作らない（OpenSpec1.1）。
- **D-04:** 依頼全体の全ファイル差分を確認し、工程仕様・計画・検証文書を別分類。利用者向け変更がREADME当該1行のみであり、コード・試験不変であることをCLI結果とともに文字の検証記録へ保存する（REQ-24、OpenSpec2.1）。
- **D-05:** 文言掲載は通し検証の実施・合格を認定しない。API・認証・権限・データ・外部送信・費用変更なし。別件の句点追加を混ぜない。
- **D-06:** 品質が対象headで独立に再確認しVERIFICATION.mdとCLI証拠文書を標準添付する。PMはread_fileで判定できる形。画像が不要なら0枚・理由を書く。画像があれば品質自身の実閲覧枚数・確認内容・結果を文字に記録し、PMに画像・圧縮物を開くことを求めない。
- **D-07:** 各PLAN最大3tasks、同じ依頼branch argonauts/r-8ac79dafへ番号順に直列で積む。task終了時の検証入力はその時点で実在し、独立PLANは他PLANの成果の有無に依存しない。phase検証は先行PLAN含む全成果がある同branchで行う。fails_whenは対象の誤動作が既存CLIで失敗として観測される条件にする。

### Claude's Discretion
既存CLIを使う実行可能な確認の組み合わせ、工程文書の詳細とPLAN分割。コード・試験・補助スクリプト追加は裁量に含めない。承認された既存検証方法をそのまま使い、確認のためのインラインコードを作らない。
</decisions>

<canonical_refs>
## Canonical References
- .planning/argonauts/r-8ac79daf-prd.md — proposal→全spec→tasksの承認済み結合PRD
- openspec/changes/r-8ac79daf-readme-verification-a/proposal.md
- openspec/changes/r-8ac79daf-readme-verification-a/specs/readme-verification-note/spec.md
- openspec/changes/r-8ac79daf-readme-verification-a/tasks.md
- _bmad-output/initiative-r-8ac79daf/brief/brief-readme-verification-a.md
- _bmad-output/initiative-r-8ac79daf/prd/prd-readme-verification-a.md
- .planning/REQUIREMENTS.md — REQ-22, REQ-23, REQ-24
- .planning/ROADMAP.md — Phase 5 goal
- .planning/argonauts/r-8ac79daf-learnings.md — 学習参考。PRD入力ではない
</canonical_refs>

<specifics>
検証は文字列の見た目・末尾・既存バイト・全差分を別々に確認する。statusだけで内容保持を合格にしない。
</specifics>

<deferred>
コード/試験/CI/依存/画面/新サービス、別件句点追加、過去phase修復。READMEの実装、品質、受入、sync/archiveは該当する後工程。
</deferred>
