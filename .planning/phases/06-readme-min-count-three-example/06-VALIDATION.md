---
phase: "06"
slug: "readme-min-count-three-example"
status: validated
nyquist_compliant: false
wave_0_complete: true
created: "2026-11-24"
---

# Phase 06 — Validation Strategy

> 計画時の契約。実行未実施。後続の正式validate-phaseがvalidatedを設定するまでdraft。

## Test Infrastructure

| Property | Value |
|---|---|
| Framework | 新試験なし。既存cmp/gitの文字比較とread_file判定のみ |
| Config file | .planning/config.json（変更しない。security/nyquist/plan_check/pattern_mapper開始値維持） |
| Quick run command | `cmp "$E/README.expected.md" README.md`（後続task1で変更前byte原本から独立期待を準備後） |
| Full scope command | `git diff --no-ext-diff --no-textconv --no-color 2437aa3445ecdb87e7a11fe7a1c0e196726a5af4 --`（工程資料込み。PLANのHEAD/index/status/untrackedと併用） |
| Product execution / pytest | 依頼者の判断により対象外。実入力・出力期待・実行ログ・quality runbook作成なし |
| Estimated runtime | 未測定。計画時は未作成verifyを試さない |

## Sampling Rate

- task1終了時: 同taskで準備したREADME.before/request-base/expectedと編集後READMEのcmp、全文/patch読取り。
- task2終了時: task1全成果と工程文書を含む全git差分、index、status、untrackedを読み、SCOPE/SUMMARYへ分類/未達を記録。
- phase検証前: 全先行成果あり。独立品質は指定例1つと全差分README1ファイルのみの2条件を文字判定する。工程差分ありの現段階では条件2未達。
- 最終化: 必要原本の標準添付保全後、既存工程資料を基準branch内容へ復元し今回新規資料を最終treeから外す。品質本人が最終PRの実基準branch/merge-baseから全差分を再確認する。工程資料を除いて数えるだけの判定は禁止。
- Max feedback latency: 未測定（watch-modeなし、有限コマンド）。

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| 06-01-01 | 01 | 1 | REQ-25 | T-06-01 | README byte保持・独立期待・例1つ | documentation tracer | `cmp "$E/README.expected.md" README.md` とREADME patch/check | README実在。before/request-base/expected文字原本は同taskで準備してからverify | green（品質t_de9630c7がhead 34eb0bbで再実行: cmp exit0、README diff +1/-0、diff --check exit0） |
| 06-01-02 | 01 | 1 | 縮小後REQ-27 | T-06-02, T-06-03 | 主体分離・工程含む全差分・保全前に消さない | scope/evidence | PLANの全git差分/HEAD/index/status/untracked、task1期待cmp | git追跡資料実在。SCOPE/SUMMARY/差分原本は同taskで準備 | partial（name-status全84件を品質が再採取: README以外83件は工程資料、禁止path diff exit0。最終PRのREADME-onlyは最終化後のmanual-only確認でpending） |

両taskの全automated直後にfails_whenを置く。コマンドexit0だけでは2条件の合格としない。README全文/patchと全pathのread_file確認で具体的不一致/欠落を判定する。最終PRのREADME-onlyは後工程pendingでありBuilder taskの完了と別。

## Wave 0 Requirements

新規test/script/validator/fixture/設定/依存を追加しない。実入力input.txtは不要。cmp用の変更前/独立期待README文字原本だけをtask1内で準備し、task2はその全成果を利用する。旧pytest環境と旧3形式の入力/期待出力準備は最新CONTEXT D-02により対象外でありWave0要件にしない。

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|---|---|---|---|
| 指定例1つ・既存例/説明/検証A/改行保持 | REQ-25/OpenSpec1.1 | 文字cmpの期待自体の独立性と位置も確認する | read_fileでREADME前/期待/後と全patchを読み指定1行以外不変を確認 |
| READMEのみの全PR差分 | REQ-25/縮小後REQ-27 | git表示成功はscope合格ではない | HEAD/tree/index/status/untracked全件を工程資料込みで分類。最終化後の実基準branchから全PR差分がREADME1件のみか独立品質が確認 |
| 原本保全・独立品質/PM判断 | 縮小後REQ-27/OpenSpec2.1 | 別主体の判断/既読をBuilderは認定できない | 品質は2条件の文字VERIFICATIONと原本を標準添付し、PM本人がread_file判断。添付保全後に工程差分を最終化で復元/除外 |

最新依頼者判断2026-11-24T21:20+09:00が旧PRD/RESEARCH/PATTERNSの検証要求に優先する。REQ-26/OpenSpec1.2、旧boundary/empty/encoding/precisionの実行項目、3形式/pytest/ブラウザとその実行証拠は「依頼者の判断により対象外」。情報透明性prohibitionsは未解決のまま引継ぐ。画像0枚、理由はREADME1行の文字変更でUI/製品実行の検証は対象外のため。zip不要。

## Validation Sign-Off

- [x] 最終PLANの全taskに標準automatedと直後fails_when、task末入力実在
- [x] 2tasks番号順直列、同branch argonauts/r-5f8197e8、先行全成果あり
- [x] 新規試験/補助script/入力/実行ログ/quality runbook作成なし
- [x] 工程資料込み全差分と現時点のREADME-only未達を明記
- [ ] 原本添付保全後の工程差分復元/除外と独立品質の最終全差分確認（最終化・最終確認でpending）
- [x] 独立品質2条件の文字判定（t_de9630c7）。PM read_file判断は後工程pending
- [x] 公式validate-phaseがnyquist_compliantを判定。開始設定は維持

**Nyquist audit (gsd-validate-phase 6, 品質 t_de9630c7, head 34eb0bb):** REQ-25 COVERED（cmp/git diff/diff --check再実行green）。REQ-27の「最終PR全差分README.mdだけ」は最終化後にしか観測できないためmanual-onlyへescalate（新試験は依頼者判断で作らない）。よって nyquist_compliant: false（PARTIAL: automated 1 / manual-only 1）。監査失敗ではない。

**Approval (計画段階の記録):** pending（計画段階）。計画検査の合格、実装/品質/最終化の完了、既存GSD state-snapshotのplan/status不一致は別々に扱い、状態を勝手に修復しない。

## Validation Audit 2026-11-24

| Metric | Count |
|---|---|
| Gaps found | 1 |
| Resolved | 0 |
| Escalated | 1 |
