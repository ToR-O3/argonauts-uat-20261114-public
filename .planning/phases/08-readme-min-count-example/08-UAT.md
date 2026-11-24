---
status: testing
phase: 08-readme-min-count-example
source: [08-VERIFICATION.md]
started: 2026-11-25T08:45:00+09:00
updated: 2026-11-25T08:45:00+09:00
---

## Current Test

number: 1
name: D.5整備後の最終PR再確認（REQ-29 / ROADMAP SC2）
expected: |
  path除外なしの非空全一覧が README.md のみ（M 1件）で、README patch は指定例1行の追加のみ・既存本文と最終行を保持。結果をVERIFICATION.md等の文字原本で標準添付し、PMがread_fileで読む
awaiting: D.5 整備（後続PM・最終化）の後の品質の最終確認

## Tests

### 1. D.5整備後の最終PR再確認（REQ-29 / ROADMAP SC2）
expected: path除外なしの非空全一覧が README.md のみ（M 1件）で、README patch は指定例1行の追加のみ・既存本文と最終行を保持。結果をVERIFICATION.md等の文字原本で標準添付し、PMがread_fileで読む
result: blocked
blocked_by: D.5 整備がまだ（後続PM・最終化の工程）。この時点（head 882b4c6）は工程文書60件が残る整備前の状態
quality_observation: 品質 t_5c607fb0 が整備前の全一覧を除外なしで取得（61件。08-QUALITY-CLI.md §3・付録A）。受入条件は人の目を明示していないため、人への質問はしない。最終確認（最終化のレビューrun）で品質が実PRを読み直して判定する

### 2. prohibition P1（掲載例を製品CLI・3形式の実行受入の証拠として示さない）
expected: QUALITY-CLI・BUILDER-CLI・SUMMARY・VERIFICATION のいずれも掲載例を実行証拠と称していない
result: [pending]
quality_observation: 品質が 08-QUALITY-CLI.md・08-VERIFICATION.md を読み、掲載例を実行証拠と称する記述は無いことを確認（QUALITY-CLI §2 は「掲載したコマンドは実行していない」と明記）。prohibition は unresolved のまま残す（人の解決なしにflagを消さない：PLAN・受付の方針）

### 3. prohibition P2（途中/フィルタ済み一覧やBuilder自己確認を最終README限定PRの独立承認として示さない）
expected: 整備前一覧は61件全件を除外なしで記録し、REQ-29は未達/暫定のまま。Builder自己確認を独立承認と称していない
result: [pending]
quality_observation: 品質の記録は61件全件・除外なしで、REQ-29 を「整備前は未達（暫定）」としている。Builder の記録は転載せず、品質が自分で取り直した。prohibition は unresolved のまま残す

### 4. flagged assumption E1（REQ-28 boundary）・E2（REQ-28 precision）・E3（REQ-29 unclassified）の扱い
expected: E1/E2は製品実行対象外（依頼者判断2026-11-25T06:53+09:00）として受容するか明示判断、E3は最終PR全一覧の分類と併せて判断
result: [pending]
quality_observation: 3件とも unresolved / verification=null のまま。依頼者判断で製品実行は対象外のため、品質は E1/E2 の製品実行試験を追加していない。E3 は最終PRの全一覧と併せて扱う

## Summary

total: 4
passed: 0
issues: 0
pending: 3
skipped: 0
blocked: 1

## Gaps
