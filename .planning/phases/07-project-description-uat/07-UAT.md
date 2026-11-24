---
status: partial
phase: 07-project-description-uat
source: [07-VERIFICATION.md]
started: 2026-11-24T20:52:00Z
updated: 2026-11-24T20:52:00Z
---

## Current Test

number: 2
name: PMが文字原本をread_fileで開き、AC別に判定する
expected: |
  PMが条件別に判定でき、受入/差戻しを決める
awaiting: 後工程のPM（フェーズ判断 t_f322fb6b）

## Tests

受入条件はどれも人の目による確認を明示していないため、品質（argonauts-uat-quality、カード t_9dff5b92）が自分で試せる項目は試した。対象head c5d0eb136bf92d6f00c3fc807346e55103917504。

### 1. 品質担当が .planning/argonauts/r-cf2eeaab/VERIFICATION.md を自分の対象head c5d0eb1 での独立実行から作成し、quality-cli-evidence.txt と共に Kanban カードへ標準添付する
expected: 両ファイルが保存（commit）・標準添付され、AC-1/AC-2/AC-3 別判定、起点 c572613・対象head c5d0eb1・報告head、実コマンド・exit・原本pathを含む
result: pass
source: 品質がC1〜C7を実行して両ファイルを作成。カード t_9dff5b92 に添付85（VERIFICATION.md）・86（quality-cli-evidence.txt）。保存先と原本のSHA-256は一致。保存のcommitは .planning だけのcommit（報告head）

### 2. PM が read_file で .planning/argonauts/r-cf2eeaab/VERIFICATION.md と CLI 文字原本（quality-cli-evidence.txt、builder-red-cli.txt、builder-green-cli.txt）を開き、AC別に判定する
expected: PM が条件別に判定でき、受入/差戻しを決める
result: blocked
reason: PMの読取りはPMの行為で、品質は代わりに行えない。後工程のフェーズ判断 t_f322fb6b が行う

### 3. prohibition P1（judgment-tier, status unresolved, descriptor-less flagged-unverified）: 'MUST NOT present the UAT label as certification that end-to-end testing or independent acceptance has passed.' を人がレビューする
expected: description 値「(UAT)」や各報告が通し検証・独立受入の合格認定として提示されていないと人が判断する
result: skipped
reason: 品質の確認（非権威的）では違反を見つけなかった。説明文の値は依頼者が指定したもので、品質の文書は受入を済みとしていない。カードの指示により flagged を保持し、解消済みにしない（PM・人の判断）

### 4. prohibition P2（judgment-tier, status unresolved, descriptor-less flagged-unverified）: 'MUST NOT present Builder self-verification, stored evidence, or an evidence-only report head as independently executed quality acceptance or PM original-reading.' を人がレビューする
expected: Builder自己検証・保存済み証拠・報告head が独立品質受入やPM読取りとして提示されていないと人が判断する
result: skipped
reason: 品質の確認（非権威的）では、品質の文書は Builder 実行と品質実行、対象headと報告head、保存・添付・PM読取りを分けて書いている。SUMMARY の requirements-completed と REQUIREMENTS.md の REQ-27 [x] は独立品質の前に付いている（本文には pending とある）。カードの指示により flagged を保持し、解消済みにしない（PM・人の判断）

### 5. PLAN の flagged-assumption 表（spec-less fallback）の probe 未分類3件 REQ-25/REQ-26/REQ-27（category unclassified, status unresolved, probe 'unclassified — review manually'）を人が手動レビューする
expected: 各行を人が分類・判断する。本検証は自動で resolved/dismiss しない
result: skipped
reason: カードの指示により flagged を保持する。品質は分類を書き換えていない（PM・人の判断）

## Summary

total: 5
passed: 1
issues: 0
pending: 0
skipped: 3
blocked: 1

## Gaps
