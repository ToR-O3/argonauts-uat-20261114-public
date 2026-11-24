# Builder scope / 原本索引

主体: argonauts-uat-builder、task t_5e02213b、run35。
cwd: /home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_5e02213b
依頼branch: argonauts/r-5f8197e8、local branch: wt/t_5e02213b。
開始head: fe080814752ef1cfe5f49d6aa39d6c1949bea064。
掲載確認head: 7aaca3077499ecf67b4eac6e0197ef1f4f2aadd6。
依頼基点、採取時origin/v112-a、merge-baseはいずれも2437aa3445ecdb87e7a11fe7a1c0e196726a5af4。
最終push headはカードのrequest_review metadataで固定する。下のtask1スナップショットは過去時点の原本であり、最終head原本と混同しない。

## 判断根拠

範囲判断日時: 2026-11-24T21:20+09:00
原文: 検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。

最新判断日時: 2026-11-24T13:09:04.816724+00:00
原文: Aに近いが、人の側では状態の修復をしない。進捗の照会が古い値を返すのは手続きの食い違いなので、保存済みの計画をそのまま使って、先（割振り・実装）へ進めてよい。

## 掲載の確認（Builderのみ）

- README全文を編集前に読み、指定例不在と通常例直後の位置を確認した。
- 同じtaskでREADME.before.mdをcp保存。依頼基点はgit showでREADME.request-base.mdへ保存。両者cmp exit0、先行README差分なし。
- README.expected.mdはbeforeをcpし、製品編集前に独立patchで指定行だけを追加。期待全文を読取り後、実READMEとのcmpはbyte348/line11でexit1（期待する不一致）。
- その後READMEだけへ同じ1行をpatch。期待cmp exit0、依頼基点からREADMEのgit diffは通常例直後の指定行1つだけ、numstatは1/0。git diff --check exit0。既存閾値2例、初出順の説明、検証A最終行、その他すべてのbyteを保持。
- tracerをcommit後にcmpとdiff --checkを再実行してexit0。task2も再確認。掲載確認はCLI動作・独立品質・PM受入の合格ではない。
- OpenSpec1.1だけチェック済み。1.2は依頼者判断により対象外で実行していない。2.1は品質本人の2条件文字判断がpendingのため未チェック。

## 文字原本（本書と同じディレクトリ）

| 原本 | 対象・内容 |
|---|---|
| README.before.md | fe08081の編集前byte原本 |
| README.request-base.md | 2437aa3のREADME原本、beforeと同一 |
| README.expected.md | 製品編集に先立ち準備した指定1行追加の期待原本 |
| HEAD.task1.txt | 掲載task commit 7aaca30 |
| name-status.task1.txt | 基点→7aaca30の全75path、分類は下表 |
| head.task1.patch | 基点→7aaca30の全patch。4452行を全区間読取り |
| tree.task2.patch | 同HEADでstate.begin-phaseの未commit更新を含む全tree差分。head.task1.patchとの全差分をgit diff --no-indexで確認し、差はSTATE.mdとstate.jsonのみ |
| index.task2.patch | 採取時index差分なし、0byte |
| status.task2.txt | 採取時のtracked/untracked全件。採取ファイル自身も含む |
| untracked.task2.txt | 同taskの全未追跡。すべて本taskが採取した文字原本。実行可能ツールなし |
| SCOPE.md | 本分類・判断境界・引継ぎ |

## 全path分類

下の表はname-status.task1.txt全件を1pathずつ分類したもの。README以外は内容を全patchで読んだ工程資料であり、製品コード・試験・設定・依存の変更はない。今回採取したpatch/status原本と本書は工程資料、後続SUMMARYと公式STATE/ROADMAP更新も工程資料。その他分類に該当するpathは検出なし。

**現時点の最終README-only条件は未達。工程資料を除外して数えるだけでは受入を満たさない。**

## 後工程への引継ぎ

1. Builder原本を標準添付してSHA-256を読み戻す。添付IDはカードのmetadataで引き継ぐ。保存済みとPM既読は別であり、PM本人のread_file判断はpending。
2. 品質本人が指定例1つと工程資料を含む全差分の2条件を独立に文字判断し、対象headと根拠原本をVERIFICATION.md等へ記録・標準添付する。Builderはこれを代筆・署名しない。OpenSpec2.1は未完了。
3. 最終化担当は必要な仕様・計画・検査・品質原本の添付保全を確認してから、この依頼の工程差分を実基準branch相当へ復元・除外する。元からある工程資料は基準branchの内容へ復元、新規工程資料は最終treeに残さない。無差別削除、添付前の原本消失は禁止。
4. 最終化で実PRのbase/merge-base/headと全patch/name-statusを記録。基点と異なる場合は両方の全差分を確認する。品質本人が最終PR全差分がREADME.mdだけと確認するまで条件2・最終受入はpending。
5. 製品CLI実行、3形式、pytest、実入力、出力期待・実行ログ、追加試験、検証script、quality runbookは依頼者の判断により対象外。旧資料の記述で復活させない。画像0枚: READMEの文字1行のみでUI/製品実行の確認が対象外のため。zip不要。
6. REQ-27のunclassified assumptionとdescriptor-less transparency prohibitions2件は未解決/flagged-unverified。品質/PM本人の原本読取り前に自動解消しない。GSD状態の古い値も未修復の手続き上の例外。phase6/phase_count5を親から引継ぎ、phase.completeやarchiveは実行しない。

| status | path | 分類 |
|---|---|---|
| M | `.planning/INGEST-CONFLICTS.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `.planning/PROJECT.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `.planning/REQUIREMENTS.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `.planning/ROADMAP.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `.planning/STATE.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-STATE-BLOCKER.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-checker-attempt1.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-checker-final.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-checker-revised.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-command-paths.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-config-start.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-edge-coverage.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-edge-reqs.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-estimate-check.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-failure-directions.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-find-phase.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-gap-analysis.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-init-plan.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-init-plan.stderr` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-learnings.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-manifest.yaml` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-merge-preview.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-phase-op.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-plan-post.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-plan-pre.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-plan-structure.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-plan.sha256` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-planner-contributions.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-prd.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-roadmap-final.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-state-planned-result.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/argonauts/r-5f8197e8-state-snapshot.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `.planning/intel/SYNTHESIS.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/intel/classifications/brief-readme-min-count-3-f56bedfc.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/intel/classifications/prd-readme-min-count-3-befb04a5.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/intel/classifications/proposal-d97b8bcf.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/intel/classifications/tasks-94eddf6b.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `.planning/intel/constraints.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `.planning/intel/context.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `.planning/intel/decisions.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `.planning/intel/requirements.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/phases/06-readme-min-count-three-example/.gitkeep` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/phases/06-readme-min-count-three-example/06-01-PLAN.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/phases/06-readme-min-count-three-example/06-CONTEXT.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/phases/06-readme-min-count-three-example/06-PATTERNS.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/phases/06-readme-min-count-three-example/06-RESEARCH.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `.planning/phases/06-readme-min-count-three-example/06-VALIDATION.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `.planning/state.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| M | `README.md` | README（指定1行追加） |
| A | `_bmad-output/initiative-r-5f8197e8/brief/.memlog.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/brief/.template.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/brief/brief-readme-min-count-3.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/brief/review-fresh-reader.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/brief/review-prose.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/brief/review-reconciliation.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/brief/review-rubric.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/brief/review-structure.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/initiative-r-5f8197e8.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/openspec-status.json` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/prd/.memlog.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/prd/.template.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/prd/review-fresh-reader.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/prd/review-prose.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/prd/review-reconciliation-brief.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/prd/review-reconciliation-request.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/prd/review-rubric.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/prd/review-structure.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/verification/builder/t_5e02213b-run35/README.before.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/verification/builder/t_5e02213b-run35/README.expected.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `_bmad-output/initiative-r-5f8197e8/verification/builder/t_5e02213b-run35/README.request-base.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `openspec/changes/r-5f8197e8-readme-min-count-three/.openspec.yaml` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `openspec/changes/r-5f8197e8-readme-min-count-three/design.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
| A | `openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md` | 工程資料（全patch内容確認済み、最終化で復元/除外） |
