---
status: partial
phase: 08-wordfreq-exclude
source: [08-VERIFICATION.md]
started: 2026-11-28T18:55:41Z
updated: 2026-11-28T18:55:41Z
---

## Current Test

number: 1
name: 並行・中断の backstop 5件（REQ-28/30/31/32/33 concurrency）
expected: |
  保証を追加しない方針が承認される。保証が必要なら別の要求として起票される
awaiting: PM decision (insufficient_spec; not an explicit human-eye acceptance criterion)

## Tests

### 1. 5件の並行・中断 backstop（REQ-28/30/31/32/33 concurrency）について、単発ローカルCLIに新しい中断・並列・原子的出力の保証を求めないことをPMが確認する（必要なら held-out 試験を追加）
expected: 保証を追加しない方針が承認される。保証が必要なら別の要求として起票される
result: skipped
reason: 品質が受入条件に照らして確認した。受付の6条件と承認済み仕様に中断・並列の保証は無く、README.md 39行が「中断や並列実行について新しい保証は追加しません」と明記している（実ファイルで確認）。保証そのものは仕様に定義が無いため検証できず、insufficient_spec のまま残す。合格にも製品の失敗にもしない。依頼者が人の目を明示した項目ではない。

### 2. P-08-01（自動ストップワード・推定除外の禁止）を人が確認する
expected: --exclude FILE に書いた語だけが除外され、他の語は暗黙に除外されない
result: skipped
reason: 品質の非権威の観測では違反なし。未指定時の出力は固定過去版 79d83ba と3形式でバイト一致、空・コメントのみ・不一致語のFILEは未指定とバイト一致（quality/cli/cli-log.txt の AC6-*、E-*）。descriptor-less の禁止事項のため flagged-unverified を保持する。

### 3. P-08-02（Builder結果・履歴・未実行probe・未閲覧画像を独立受入として示すことの禁止）を人が確認する
expected: 受入の根拠が品質の対象head f3747b7 での独立実行原本と本 VERIFICATION.md に限られる
result: skipped
reason: 品質の判定は f3747b7 で品質が実行した pytest（457 / 1159 passed）、regression gate、実CLI 237出力と追加観測だけに基づく（.planning/argonauts/r-e0a2598f/quality-evidence.md）。画像は ui-review 委任が閲覧した2枚だけを数え、親は0枚。descriptor-less のため flagged-unverified を保持する。

### 4. 日本語フォントのある環境で --format html の出力（通常・全件除外）をブラウザで開く
expected: 見出し・ラベル・caption・列見出し・空文言の日本語が読める。はみ出し・重なりがない
result: skipped
reason: この検証ホストには日本語フォントが無く（fc-list :lang=ja → 0）、日本語の描画は確認できない。受入条件に照らすと、HTMLの見た目を変えないこと（formatter 差分なし、未指定時のHTMLが過去版とバイト一致）は確認済みで、日本語の表示は今回の変更の範囲外。依頼者が人の目を明示した項目ではない。

### 5. SC4: 親が本 VERIFICATION.md と .planning/argonauts/r-e0a2598f/quality/ のCLI文字原本を、PMが read_file できるパスで標準配布したことを確認する
expected: PMは画像や圧縮ファイルを開かずに、各条件の文字原本を読める
result: pass
reason: 品質カード t_d369e688 が 08-VERIFICATION.md・quality-evidence.md・openspec-verify.md・cli-log.txt ほかの文字原本を標準添付し、保存先と原本の SHA-256 を照合する（添付IDは完了の要約）。原本は依頼branchにもcommitされ、PMは read_file で読める。

## Summary

total: 5
passed: 1
issues: 0
pending: 0
skipped: 4
blocked: 0

## Gaps
