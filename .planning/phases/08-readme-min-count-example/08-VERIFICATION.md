---
phase: 08-readme-min-count-example
verified: 2026-11-24T23:35:05Z
status: human_needed
score: 3/4 must-haves verified
covered_files:
  - .planning/phases/08-readme-min-count-example/08-01-PLAN.md
  - .planning/phases/08-readme-min-count-example/08-01-SUMMARY.md
  - .planning/phases/08-readme-min-count-example/08-BUILDER-CLI.md
  - .planning/phases/08-readme-min-count-example/08-QUALITY-CLI.md
  - README.md
covered_digest: "v4:sha256:fdef05c295b3afe83fa5a52c03d7fa0f43a3e4a4292c04cb41517d8d93dfdd6b"
behavior_unverified: 0
overrides_applied: 0
target:
  repository: ToR-O3/argonauts-uat-20261114-public
  base_branch: v112-a
  base: cf407aaa6babebc0a21cf6370530d321b8a615e1
  head: 882b4c60e36a4457c6d504cb07cccc69a03e7130
  merge_base: cf407aaa6babebc0a21cf6370530d321b8a615e1
  start_sha: 882b4c60e36a4457c6d504cb07cccc69a03e7130
  pr: "ToR-O3/argonauts-uat-20261114-public#19 (draft, changedFiles 61)"
  scope_kind: "D.5整備前の依頼branch比較（最終PR整備後ではない）"
requirements:
  REQ-28: satisfied
  REQ-29: "未達/暫定（整備前。最終判定はD.5後の独立品質再確認まで保留）"
flagged_prohibitions:
  - id: P1
    statement: "MUST NOT present the published README example as proof that the product CLI or three output formats were executed and accepted."
    llm_verdict: "not violated (non-authoritative)"
    flag: "unverified-prohibition — human review recommended"
  - id: P2
    statement: "MUST NOT present a filtered or intermediate change list or Builder self-review as independent approval of the final README-only PR."
    llm_verdict: "not violated (non-authoritative)"
    flag: "unverified-prohibition — human review recommended"
flagged_assumptions:
  - id: E1
    item: "REQ-28 boundary"
    status: unresolved
  - id: E2
    item: "REQ-28 precision"
    status: unresolved
  - id: E3
    item: "REQ-29 unclassified"
    status: unresolved
human_verification:
  - test: "D.5指定ファイル限定整備の後、独立品質が実PR（#19 又は後継）のbase branch・base/head完全SHA・PR識別子を読み直し、08-01-PLAN.md handoff 4のコマンド（name-status・name-only・README両原本・README patch・diff --check）を全件文字原本に保存して2条件を別々に判定する"
    expected: "path除外なしの非空全一覧が README.md のみ（M 1件）で、README patch は指定例1行の追加のみ・既存本文と最終行を保持。結果をVERIFICATION.md等の文字原本で標準添付し、PMがread_fileで読む"
    why_human: "最終PRは後続PM/最終化カードのD.5でのみ成立する。現時点（head 882b4c6）は工程文書60件が残る整備前状態で、REQ-29の最終達成はこのphaseのコードベースからは観測できない"
  - test: "prohibition P1（掲載例を製品CLI・3形式の実行受入の証拠として示さない）を人が確認する"
    expected: "QUALITY-CLI・BUILDER-CLI・SUMMARY・本報告のいずれも掲載例を実行証拠と称していない（LLM判定: 違反なし、非公式）"
    why_human: "judgment-tierかつdescriptorなしのunresolved prohibition。自律verifyでは非公式判定とflagのみで、解決には人の判断が要る"
  - test: "prohibition P2（途中/フィルタ済み一覧やBuilder自己確認を最終README限定PRの独立承認として示さない）を人が確認する"
    expected: "整備前一覧は61件全件を除外なしで記録し、REQ-29は未達/暫定のまま。Builder自己確認を独立承認と称していない（LLM判定: 違反なし、非公式）"
    why_human: "judgment-tierかつdescriptorなしのunresolved prohibition。人の解決なしにflagを消さない"
  - test: "spec-less fallbackのflagged assumption E1（REQ-28 boundary）・E2（REQ-28 precision）・E3（REQ-29 unclassified）の扱いを人が決める"
    expected: "E1/E2は製品実行対象外（依頼者判断2026-11-25T06:53+09:00）として受容するか明示判断、E3は最終PR全一覧の分類と併せて判断"
    why_human: "3件とも unresolved / verification=null。PLANがflagged assumptionとして後続へ引き継いでおり、自動解決扱いにできない"
---

# Phase 8: README min-count example 検証報告

**Phase Goal:** 承認済みr-d78495deの指定min-count例をREADME使い方へ1つ追加し、既存内容を保持し、最終PR全変更がREADME.mdのみであることを独立品質の文字証拠で確認する。
**Verified:** 2026-11-24T23:35:05Z
**Status:** human_needed
**Re-verification:** No — 初回の検証

**検証範囲（依頼者判断 2026-11-25T06:53+09:00 原文）:** 「検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。」
製品CLIの実行（3形式・入出力・終了コード）は対象外であり、gapにも人の確認項目にもしない。

**対象の身元（verifierが自分で再確認）:**

| 項目 | 値 | 確認コマンド |
|---|---|---|
| origin | https://github.com/ToR-O3/argonauts-uat-20261114-public.git | `git remote get-url origin` |
| BASE（fetch済み origin/v112-a） | cf407aaa6babebc0a21cf6370530d321b8a615e1 | `git rev-parse --verify 'origin/v112-a^{commit}'` |
| HEAD | 882b4c60e36a4457c6d504cb07cccc69a03e7130（= origin/argonauts/r-d78495de） | `git rev-parse HEAD`、`git rev-parse --verify 'origin/argonauts/r-d78495de^{commit}'` |
| MERGE_BASE | cf407aaa6babebc0a21cf6370530d321b8a615e1（= BASE） | `git merge-base BASE HEAD` |
| ローカル v112-a（参考、不使用） | c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 | `git rev-parse --verify 'v112-a^{commit}'` |

origin/main とローカル v112-a は基準に使っていない。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | （ROADMAP SC1 / PLAN truth1）README.mdの使い方へ `python -m wordfreq input.txt --min-count 3` が1例追加され、既存例・説明・末尾行が保持される | ✓ VERIFIED | `git --no-pager diff --no-ext-diff --no-textconv --unified=40 BASE...HEAD -- README.md` を全文直接読んだ。hunkは `@@ -1,35 +1,36 @@` の1つ、`+` 行は基本例直後の `python -m wordfreq input.txt --min-count 3` だけ、`-` 行0。既存4例・説明箇条・「部品の契約と検証状況」・最終行 `検証A: v1.12 の通しの確かめ（2026-11-22）` は文脈行として不変。`--numstat` = `1 0 README.md`、`diff --check` exit 0、作業README中の `--min-count 3` は1件、末尾改行あり |
| 2 | （ROADMAP SC2）D.5指定ファイル限定整備後の最終PR base...head全変更一覧がREADME.mdのみ。品質がbase/head・全一覧・2条件判定を文字原本でカード添付する | ? UNCERTAIN（整備前: 未達/暫定） | 現headの `--name-status BASE...HEAD`（path除外なし）は61件: README.md 1、`.planning/` 34、`_bmad-output/` 22、`openspec/` 4。README以外の製品ファイル変更は0。D.5はこのphaseではなく後続PM/最終化カードの工程で、最終PRはまだ存在しない。よって最終達成は観測不能で、合格とせず人の確認項目（human_verification 1）へ回す。path除外による合格化はしていない |
| 3 | （PLAN truth2）整備前の全変更一覧と作業ツリー残存パスを省略せず文字記録に残し、README以外があればREQ-29未達/暫定と記す | ✓ VERIFIED | 08-QUALITY-CLI.md 付録Aに61件全件（verifierの再取得と件数・分類が一致）、作業ツリー4種の別枠一覧、「判定（2）: 整備前は未達（暫定）」。08-BUILDER-CLI.md もTask2時点head fc3d736の全一覧と未達/暫定を記録 |
| 4 | （PLAN truth3）最終受入には後続D.5整備後の実PR base/headで独立品質が2条件を再確認した文字原本が必要であり、Builder自己確認をその代替にしない | ✓ VERIFIED | 08-01-SUMMARY.md `requirements-completed: [REQ-28]`・`requirements-pending: [REQ-29]`、REQUIREMENTS.md の REQ-29 は `[ ]`、openspec tasks.md 2.1 は未チェック。PLAN handoff 1-6・QUALITY-CLI §6・BUILDER-CLI §3 がD.5後の再取得手順を明記 |

**Score:** 3/4 truths verified（0 present, behavior-unverified）。残る1件（SC2）は最終PRが後続工程で成立するまで観測できないため UNCERTAIN とし、passed に吸収していない。

### Prohibitions（must_haves.prohibitions、judgment-tier・unresolved）

| ID | Statement | 非公式LLM判定 | Flag |
|---|---|---|---|
| P1 | MUST NOT present the published README example as proof that the product CLI or three output formats were executed and accepted. | 違反なし（QUALITY-CLI §2「掲載したコマンドは実行していない」、SUMMARY「product execution is excluded」） | unverified-prohibition — human review recommended |
| P2 | MUST NOT present a filtered or intermediate change list or Builder self-review as independent approval of the final README-only PR. | 違反なし（全61件を除外なしで記録、REQ-29未達/暫定、SUMMARYはBuilder自己確認を独立承認と称していない） | unverified-prohibition — human review recommended |

### Flagged assumptions（spec-less fallback E1-E3）

| ID | 内容 | 状態 |
|---|---|---|
| E1 | REQ-28 boundary | unresolved / verification=null（指定行の完全一致1件は確認したが、probeの解決とはしない） |
| E2 | REQ-28 precision | unresolved / verification=null（製品精度保証は本phaseの要件外。未解決を維持） |
| E3 | REQ-29 unclassified | unresolved / verification=null（全一覧は確認済みだが分類済み扱いにしない） |

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `README.md` | 指定min-count例1つと保持された既存本文（contains `python -m wordfreq input.txt --min-count 3`） | ✓ VERIFIED | `verify.artifacts` passed、内容はTruth 1の直接読取りで確認 |
| `.planning/phases/08-readme-min-count-example/08-BUILDER-CLI.md` | 編集前/後の文字判定、全一覧、暫定範囲、引継ぎ | ✓ VERIFIED | 369行。EDIT_BASE=e18a818…、編集前FAIL/編集後GREEN、全patch、全一覧、D.5後handoff |
| `.planning/phases/08-readme-min-count-example/08-01-SUMMARY.md` | 実施範囲と未実施の独立品質/最終PR条件の区別 | ✓ VERIFIED | REQ-28 completed / REQ-29 pending を分離 |

`gsd_run query verify.artifacts` → all_passed true、3/3、exit 0。

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| README.md | 08-BUILDER-CLI.md | EDIT_BASE原本と編集後原本・全patchの直接読取りでREQ-28判定 | ✓ WIRED（手動、逆方向） | `verify.key-links` は「Target not referenced in source」（exit 1）。README（製品文書）が工程文書を参照しないのは正しく、参照を足せばREQ-29に反する。証拠の流れは逆方向で、BUILDER-CLI 26-72行に `git diff ... e18a818… -- README.md` の全patch（42行に指定行）と numstat/check、224・262行に両README原本がある。意図した結合は成立 |
| 08-BUILDER-CLI.md | .planning/argonauts/r-d78495de-prd.md | OpenSpec1.1/2.1、整備前暫定と最終判定の分離 | ✓ WIRED | `verify.key-links` verified true |

### Data-Flow Trace (Level 4)

対象外。動的データを描画する成果物はない（静的README文書のみ）。

### Behavioral Spot-Checks

Step 7b: SKIPPED（文書のみのphase。依頼者判断により製品CLIの実行は対象外）。

回帰の確認として、品質担当がhead 882b4c6で既存の全試験を1回実行済み: `uv run --with pytest python -m pytest -q` → 702 passed（exit 0、08-QUALITY-CLI.md §4）。本verifierは再実行していない。受入条件の証拠には使わない。

### Probe Execution

対象外。PLAN/SUMMARYに `probe-*.sh` の宣言はない（E1-E3はspec-less edge probeのflagで、実行可能probeではない）。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| REQ-28 | 08-01 | README.mdの使い方へ `--min-count 3` の例を1つ追加、既存例・説明・末尾行保持、原本と文字差分で確認 | ✓ SATISFIED | Truth 1。独立に再取得したBASE...HEAD README patchと全文 |
| REQ-29 | 08-01 | 最終PR base...headの全変更ファイルがREADME.mdだけ（path除外なし、D.5後に品質が再確認） | ? NEEDS HUMAN（整備前: 未達/暫定） | 現在61件中60件が工程文書。最終判定はD.5後の独立品質再確認まで保留（human_verification 1）。最終合格とは主張しない |

孤立要件: REQUIREMENTS.md でPhase 8に対応する要件は REQ-28・REQ-29 のみで、どちらもPLANが宣言している。ORPHANEDなし。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| — | — | README.md と openspec tasks.md に TBD/FIXME/XXX/TODO/HACK/PLACEHOLDER なし | — | なし |

コード審査 08-REVIEW.md は status clean（0 findings）。08-SECURITY.md は threats_open 0。08-VALIDATION.md は status validated、nyquist_compliant false（REQ-29がD.5後の手動確認のみでpendingのため）。

画面: 画像0枚。READMEの文字だけの変更で、UI変更なし。

### Human Verification Required

### 1. D.5後の最終PR再確認（REQ-29 / ROADMAP SC2）

**Test:** 後続PM/最終化がfull工程原本の保存・push・標準添付を確かめてからD.5で整備した後、独立品質が実PRのbase branch（期待 v112-a）・base/head完全SHA・PR識別子を読み直し、08-01-PLAN.md handoff 4のコマンドを全件文字原本に保存する。
**Expected:** path除外なしの非空全一覧が README.md のみ。README patch は指定例1行の追加のみで既存本文・最終行を保持。結果を標準添付し、PMがread_fileで読む。
**Why human:** 最終PRは後続工程でのみ成立し、現headは工程文書60件が残る整備前状態。

### 2. Prohibition P1

**Test:** 掲載例が製品CLI・3形式の実行受入の証拠として扱われていないかを人が確認する。
**Expected:** どの記録も実行証拠と称していない（非公式LLM判定: 違反なし）。
**Why human:** judgment-tierかつdescriptorなしのunresolved prohibition。

### 3. Prohibition P2

**Test:** 途中/フィルタ済み一覧やBuilder自己確認が最終README限定PRの独立承認として扱われていないかを人が確認する。
**Expected:** 整備前の全一覧は除外なしで、REQ-29は未達/暫定のまま（非公式LLM判定: 違反なし）。
**Why human:** judgment-tierかつdescriptorなしのunresolved prohibition。

### 4. Flagged assumptions E1-E3

**Test:** E1（REQ-28 boundary）・E2（REQ-28 precision）・E3（REQ-29 unclassified）の扱いを人が決める。
**Expected:** E1/E2は依頼者判断による製品実行対象外として明示的に受容するか判断。E3は最終PR全一覧と併せて判断。
**Why human:** 3件とも unresolved / verification=null で、自動解決扱いにできない。

### Gaps Summary

このphaseの実行範囲で直せるgapはない。REQ-28（指定例1行の追加と既存内容の保持）は、独立に再取得したGitの原本と文字差分で確認した。REQ-29は、最終PR整備（D.5）が後続PM/最終化カードの担当であり、現時点の head 882b4c6 では README.md 以外に工程文書60件（`.planning/` 34、`_bmad-output/` 22、`openspec/` 4）が残る。このため **未達/暫定** と記録し、最終合格とは主張しない。後続phaseはROADMAPにない（Phase 8が最後）ので deferred にはできず、D.5後の独立品質再確認・P1/P2・E1-E3を人の確認項目として残した。status は human_needed。

---

_Verified: 2026-11-24T23:35:05Z_
_Verifier: Claude (gsd-verifier)_
