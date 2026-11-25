# 要求・仕様 revise=1 最終検証

## 対象

- repo: ToR-O3/argonauts-uat-20261114-public、依頼branch: argonauts/r-d29f1519。
- 開始head／旧文書版: 71b7a0a19992d03e63d2b71fbb85661c59aba159。
- 比較原本: 69b97f1c9dfa7211367a9bdd0af885d80d8bf380:README.md。
- 現行文書: 本commitのBrief/PRD（revision:1）とOpenSpec proposal/design/tasks（revise=1）。最終headは本カード完了metadata.head_shaで特定する。検査はcommit前の作業ツリーを対象とし、commit後にcleanとremote一致を追加確認する。
- 決定元: t_c5dd0fce completed run91。t_296a5f28 completed run92はchanges_requested。依頼者の日時付き判断は受付に存在せず、PM決定を依頼者選択としない。

## 内容照合

現行5文書の確定文は「Argonauts v1.10 の動作を確認するための公開受入テスト用リポジトリです。」。版更新・省略なし。完全一致、品質担当の1行単独・補足なしの平易な言換え、非対象バイト保持、全差分・作業状態の範囲検査、コマンド/終了値/原本/head/判定のテキスト記録を必須とした。未決事項は解消、仮説は未確認のまま維持し追加調査を要求しない。再承認後だけ計画へ進む。

旧版をGit履歴に残し、memlogは追記だけ。過去のreview記録は変更しない。子のVERIFICATION.mdは途中の部分検査であり、親の追補・OpenSpec更新・独立レビューは本記録とindependent-review-revise1.mdを正とする。

## 実コマンドと結果

以下を標準terminalで実行した。試験コードは作らず、製品の受入試験は実施していない。

| コマンド | 終了値・結果 |
|---|---|
| `openspec list --json` | 0。nearest rootが本worktree、変更名一致 |
| `openspec status --change r-d29f1519-clarify-readme --json` | 0。isPlanningComplete=true、specs=skipped |
| `openspec instructions proposal/design/tasks --change r-d29f1519-clarify-readme --json`（各artifact個別） | 各0、既存具体pathとrules/templateを確認 |
| `openspec validate r-d29f1519-clarify-readme --strict --json` | 0。valid=true、failed=0。skip_specs=trueのためzero deltas accepted |
| `uv run <bmad-facilitate>/scripts/check_ids.py <Brief> <PRD>` | 最終0。undefined/unknown_prefix/duplicate/withdrawn/toc全空。初回はSHA-256を要求IDと誤認したため本文をsha256ハッシュへ表記修正し再実行 |
| `uv run <bmad-facilitate>/scripts/render_view.py <Brief> --layout <bmad-agent-analyst>/assets/brief-view.html` | 0、最新BriefからHTML再生成。HTMLは補助表示でPM必読ではない。ブラウザ等の検証なし |
| `git diff --check` | 0、指摘なし |
| `git diff --name-status 69b97f1c9dfa7211367a9bdd0af885d80d8bf380` | 0、全出力を読み本依頼の既存工程文書だけと確認 |
| `git diff --cached --name-status`、`git ls-files --others --exclude-standard`、`git status --porcelain` | 各0、staged/unstaged/untrackedを確認、製品変更なし、無関係工程成果物なし |
| `git diff --exit-code 69b97f1c9dfa7211367a9bdd0af885d80d8bf380 -- README.md` | 0、README全体不変 |
| `git rev-parse 69b97f1c9dfa7211367a9bdd0af885d80d8bf380:README.md`、`git hash-object README.md` | 各0、共に3625ed42efa55c9929e47952698c25decd5050b7 |
| `sha256sum README.md` | 0、57d55ff9557764227811f2ee2d8da52c14c0de5ac3553f770ce38c29d5dc8291 |

`<bmad-facilitate>`等は本profile skillsの絶対path。Brief/PRDはmetadata.bmad_artifactsの各path。公式のcheck_idsは結果JSONの空欄も読み、終了値だけで判定しなかった。

## 今回の許可成果物

旧文書版からの変更は以下を個別照合した。5工程領域の丸ごと除外はしていない。

- `_bmad-output/initiative-r-d29f1519/brief/.memlog.md`、`brief/brief-readme-description.md`。
- `brief/VERIFICATION.md`、`brief/brief-readme-description.html`、`brief/verification-revise1.txt`。
- `brief/review-reconciliation-revise1.md`、`brief/review-rubric-revise1.md`、`brief/review-fresh-reader-revise1.md`、`brief/review-structure-revise1.md`、`brief/review-prose-revise1.md`。
- `_bmad-output/initiative-r-d29f1519/prd/.memlog.md`、`prd/prd-readme-description.md`、`prd/VERIFICATION.md`。
- `prd/review-reconciliation-revise1.md`、`prd/review-rubric-revise1.md`、`prd/review-fresh-reader-revise1.md`、`prd/review-structure-revise1.md`、`prd/review-prose-revise1.md`。
- `_bmad-output/initiative-r-d29f1519/open-questions.md`（未決なし）、`independent-review-revise1.md`、本`revision-verification.md`。
- `openspec/changes/r-d29f1519-clarify-readme/proposal.md`、`design.md`、`tasks.md`。

## 結論

要求・仕様の整合更新を再承認へ渡す。READMEは英語の旧文のまま、実装・製品受入は未完了。新しい変更名、計画、実装、マージは行っていない。未決なしのためopen_questions=[]とし、未決事項添付は省略する（Gitには未決なしの現行原本を保存）。proposal/tasksに加えdesign・本検証・独立レビューもテキスト添付し、名前とsha256を照合する。
