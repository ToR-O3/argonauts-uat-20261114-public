---
phase: 06-readme-min-count-three-example
verified: 2026-11-24T13:31:27Z
status: gaps_found
score: 4/5 must-haves verified
covered_files: [".planning/phases/06-readme-min-count-three-example/06-01-PLAN.md", ".planning/phases/06-readme-min-count-three-example/06-01-SUMMARY.md", "README.md"]
covered_digest: "v4:sha256:b98379c03a761e2a4d23d692c6d89fbfbc3b088b848f181dc11afed8d75012ef"
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "最終PRの全差分がREADME.mdだけ（ROADMAP SC2 / PLAN truth3）。工程原本を添付保全し、最終化で工程文書の差分を外す。除外して数えるだけの判定は不可。"
    status: failed
    reason: "対象head 34eb0bb で依頼基点 2437aa3 からの全差分は84件。README.md 1件のほか、工程文書83件（.planning/ 49、_bmad-output/ 30、openspec/ 4）が残る。現時点では条件2は未達（工程差分83件が残る）。後続GSD phaseはなく、計画どおり非GSDの最終化工程の責務。"
    artifacts:
      - path: ".planning/, _bmad-output/initiative-r-5f8197e8/, openspec/changes/r-5f8197e8-readme-min-count-three/"
        issue: "この依頼で追加・変更された工程文書83件がPR差分に残っている"
    missing:
      - "必要な仕様・計画・検査・品質の原本を標準添付で保全する"
      - "最終化担当が、既存の工程文書を基準branchの内容へ戻し、今回新規の工程文書を最終treeから外す"
      - "最終化後、品質が最終確認で、実基準branch/merge-baseから最終PRの全差分（name-status）がREADME.md 1件だけかを再判定する"
---

# Phase 6: README min-count three example 検証報告

**Phase Goal:** 最新依頼者判断2026-11-24T21:20+09:00に従いREADMEの閾値3例1つとREADMEだけの全PR差分の2点を確認できる。3形式実行・実行証拠は対象外。
**Verified:** 2026-11-24T13:31:27Z
**Status:** gaps_found
**Re-verification:** No — 初回の検証
**対象:** worktree `t_de9630c7`、HEAD `34eb0bb03d285843561faf567fa6cef4a4cd141c`（branch `argonauts/r-5f8197e8`）、依頼基点 `2437aa3445ecdb87e7a11fe7a1c0e196726a5af4`（merge-baseと一致）
**主体:** 品質（argonauts-uat-quality, gsd-verifier）。Builder（t_5e02213b run35）とは別の主体として、下のコマンドを自分で再実行した。

> **要点:** 条件1（README に `--min-count 3` 例が1つ）は達成。**現時点では条件2は未達（工程差分83件が残る）。最終化後に品質の最終確認で再判定する。** 工程文書を除外して数え、READMEだけと判定することはしていない。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | (ROADMAP SC1 / PLAN truth1) 使い方に指定コマンド例1つだけを追加し、既存の説明・例・検証A行・LFを保持する。0回または2回以上の追加は不合格 | ✓ VERIFIED | `git diff --no-ext-diff --no-color 2437aa3 HEAD -- README.md` は `python -m wordfreq input.txt` の直後に `+python -m wordfreq input.txt --min-count 3` を1行足すだけ（numstat 1/0）。`grep -c -- '--min-count 3' README.md` = 1。`git diff --check` exit0。最終行 `検証A: v1.12 の通しの確かめ（2026-11-22）` が残り、末尾は `\n`（od で確認）。README全文（36行）を read_file で読んだ |
| 2 | (PLAN truth2, REQ-25 precision) 掲載は指定コマンドと完全一致し、同数時の初出順の説明を語の昇順へ書き換えない | ✓ VERIFIED | 追加行は `python -m wordfreq input.txt --min-count 3` と完全に一致。削除行は0なので、24行目の「同数時は**正規化後の初出順**」の説明は基点から変わっていない。独立した期待との比較 `cmp …/t_5e02213b-run35/README.expected.md README.md` は exit0。基点のREADMEと Builder の原本 `README.request-base.md` も cmp で exit0 |
| 3 | (ROADMAP SC2 / PLAN truth3) 最終PRの全差分がREADME.mdだけ。工程原本を添付保全し、最終化で工程文書の差分を外す。除外して数えるだけの判定は不可 | ✗ FAILED | `git diff --name-status 2437aa3 HEAD` は84行。内訳は README.md 1件、`.planning/` 49件、`_bmad-output/` 30件、`openspec/` 4件。工程文書以外にREADME以外の変更はない。禁止範囲の確認 `git diff --exit-code 2437aa3 HEAD -- wordfreq tests tools pyproject.toml .github` は exit0。それでも**全差分はREADMEだけではないので未達**。最終化（非GSD）の後に品質の最終確認で再判定する |
| 4 | (ROADMAP SC3) 3形式の実行・pytest・入力/出力/実行ログは依頼者の判断により対象外。独立品質の確認は上の2点の文字判断だけ | ✓ VERIFIED | 全84 pathを列挙して確認した。input.txt・出力の期待値・実行ログ・新しい試験・script・runbookは無い。製品CLIとpytestは、依頼者の判断に従いこの検証で実行していない。それを欠落とは扱わない |
| 5 | (PLAN truth4) 独立品質は例1つと全差分の2条件だけを文字で確認し、原本の添付とPMのread_file判断を別主体の未完了gateとして残す | ✓ VERIFIED | この報告が2条件だけを文字で判定している。SUMMARY の「Next Phase Readiness / 未完了gate」と 06-VALIDATION の Sign-Off には、添付保全・最終化・PMのread_file判断が pending と書かれている。Builder は品質判定を代わりに書いていない（OpenSpec 2.1 は未チェック） |

**Score:** 4/5 truths verified（behavior-unverified 0）

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `README.md` | 使い方の閾値3の例1行だけの製品差分 | ✓ VERIFIED | `verify.artifacts`: exists/passed。内容があり、差分は+1/-0 |
| `_bmad-output/initiative-r-5f8197e8/verification/builder/` | README変更前/依頼基点/独立期待の文字原本、全差分、SCOPE.md、後工程への引継ぎ（最終PRからは外す） | ✓ VERIFIED (手動) | `verify.artifacts` はディレクトリを入力に取れず「Not a file: path is a directory」を返した。これは STUB 判定（Only N lines / Missing pattern）ではなく、ツールの入力の形の問題。`ls` で `t_5e02213b-run35/` 配下に README.before/request-base/expected、SCOPE.md（15995B）、head.task1.patch、tree.task2.patch、index.task2.patch（空）、status/untracked/name-status/HEAD の11ファイルがあることを確認した |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| README.md | 06-CONTEXT.md (D-01) | 完全一致1行追加を独立期待とのcmpと全文/patchで確認 | ✓ WIRED (手動) | `verify.key-links` は README の中に CONTEXT パスへの参照を探すため「Target not referenced」を返した。この link は文字比較による対応付けなので、参照が無いのは当然。cmp exit0、diff は D-01 の1行・位置と一致 |
| builder/ | 06-01-SUMMARY.md | 全差分分類・原本保全・最終化・最終確認の引継ぎ | ✓ WIRED (手動) | ツールはディレクトリを読めず EISDIR。SUMMARY は `t_5e02213b-run35` を3回参照し、原本の索引と未完了gateを書いている |

### Data-Flow Trace (Level 4)

N/A。README 1行の文書変更で、動的なデータを描画するコードは無い。

### Behavioral Spot-Checks

Step 7b: SKIPPED。文書だけの phase で、製品CLIとpytestは依頼者の判断により対象外。参考情報として、`gh run view` で対象 head 34eb0bb の GitHub Actions run 45402522159 と 45402462563 が completed/success であることは確認した。これは2条件の判定には使っていない。

### Probe Execution

N/A。PLAN/SUMMARY に probe の宣言は無い。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| REQ-25 | 06-01 | README「wordfreq の実行」に `--min-count 3` の例を1つ追加し、既存を保持する。利用者向けの変更はREADME.mdだけ | ✓ SATISFIED（例の掲載部分）/ 最終PRのREADME-only部分は SC2 と同じく未達 | Truth 1・2・4。コード・設定・依存・試験の差分は0（禁止範囲 diff exit0） |
| REQ-27（縮小後） | 06-01 | 独立品質による例1つと全差分の文字判断、添付、PMのread_file判断 | ✗ BLOCKED（部分） | 品質の独立した文字判定はこの報告で実施した。全差分の scope は、工程差分83件のため未達（Truth 3）。原本の標準添付とPMのread_file判断は後工程で pending |
| REQ-26 | — | 3形式の実行 | 依頼者の判断により対象外 (2026-11-24T21:20+09:00) | REQUIREMENTS.md の表に記載あり。orphan ではない |

REQUIREMENTS.md で Phase 6 に割り当てられた ID は REQ-25/26/27。PLAN が宣言しているのは REQ-25/27。REQ-26 は明示的に対象外とされているので、ORPHANED の要件は無い。

### Decision Coverage

`check.decision-coverage-verify`: total 7 / honored 7 / not_honored []。「All trackable CONTEXT.md decisions are honored by shipped artifacts.」（警告だけの gate で、status には影響しない）

### Test Quality Audit

N/A。要件に結びついた試験ファイルは無い。新しい試験は依頼者の判断により対象外。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| README.md | — | TBD/FIXME/XXX/TODO/HACK/PLACEHOLDER | なし | grep の結果は0件（exit1） |

### Prohibitions（descriptor-less、flagged-unverified）

| # | Prohibition | 判定（LLM判断、非権威） | Flag |
|---|-------------|------------------------|------|
| P1 | README掲載やBuilderの自己検証を、独立品質・PM受入・通し検証全体の合格認定に変えない（REQ-27） | 違反は見つからなかった。SUMMARY は「Builder task scope only」と書いている。この報告も条件2を未達とし、PM受入を pending としている | unverified-prohibition — 人のレビューを推奨 |
| P2 | 欠落・失敗した証拠を、捏造した結果・他主体の判断・成功の主張で置き換えない（REQ-27） | 違反は見つからなかった。品質が主要コマンドを自分で再実行し、結果は一致した | unverified-prohibition — 人のレビューを推奨 |

### Human Verification Required

なし（文書だけの phase）。上の P1・P2 は PM 本人が read_file で判断する対象として引き継ぐ。

### 手続き上の例外（gap ではない）

GSD の state-snapshot が古い値（current_plan: Not started）を返す既知の問題は、依頼者判断 2026-11-24T13:09:04.816724+00:00 で承認された手続き上の例外。gap として扱わず、STATE も修復していない。

### Gaps Summary

Gap は1件で、根本原因も1つ。依頼基点から HEAD までの PR 差分に、この依頼の工程文書83件（`.planning/` 49、`_bmad-output/` 30、`openspec/` 4）がまだ残っている。製品の差分は README.md の1行追加だけで、条件1は満たしている。工程差分を外す作業は、CONTEXT D-04 と PLAN の実行契約により、原本を添付保全した後の非GSD最終化工程の責務。ROADMAP に後続の GSD phase は無いので、deferred にはせず gap のまま記録する。

**現時点では条件2は未達（工程差分83件が残る）。最終化後に品質の最終確認で再判定する。** 再判定では、最終PRの実基準branch/merge-base から `git diff --name-status` を取り直し、README.md 1件だけであることと、README の差分が上と同じ+1/-0であることを確認する。

---

_Verified: 2026-11-24T13:31:27Z_
_Verifier: Claude (gsd-verifier)_
