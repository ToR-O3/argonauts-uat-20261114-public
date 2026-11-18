# 配送索引 — r-e476c11d / t_e22f75a9 run154

保存gate: Builder統合原本の保存とread-only再検証済み。標準添付gate: この索引・archive・manifest・SUMMARY・runbookを標準添付し、親workerが保存先SHAを照合してhandoffに添付IDを記録する。PM原本読取りgate: **未実施**。添付成功はPM読取り済みではない。

## 原本identity

- request:r-e476c11d; actor:argonauts-uat-builder; task:t_e22f75a9; run154。
- 成功capture root:.planning/argonauts/r-e476c11d/builder/04-04-integration-retry-run154/。
- 原本head:904e95b8b1e9910f95d5832cfe9620370feb5ff9。manifest SHA:81b87ca76d2ac2573167281f44a8cf13a9f7d2448a1244f1b3da93a358542871。
- baseline root:.planning/argonauts/r-e476c11d/baseline/。head789cc17267fb4cfeea24111797c3d934c542ce6a、run143、index SHA:d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089。
- 失敗run153は添付179/180、元root builder/04-04-integration/を不変保持。失敗manifest SHA:0d07f3e1e305554ea053fb472654b77d5cab4f74687dad12bf1952f1d8bf49a3。
- archiveはrepo root相対pathを保持。manifest/index内の絶対pathは採取worktreeの履歴。展開後はroot_relativeを使って対応付ける。検査のため原本を編集せずvalidatorはメモリ内path写像だけ。

## 読む順番と全AC原本

1. 04-04-SUMMARY.md: command/件数/exit/時間/環境/未実施gate。
2. run154/capture.stdoutとcapture root/suite.json、suite.xml、suite.stdout、suite.stderr: 685全試験の実結果。
3. capture root/manifest.json: 62 casesのinput/body/argv/cwd/env/exit/stdout/stderr/HTML、68 viewsのraw/network/全110画像/derived、artifacts全path→SHA、ac_index全AC対応、24 baseline comparisons、scope/provenance。
4. baseline/index.jsonと全32画像/入力/bytes/HTML/raw: 元head比較原本。元rootを後headへ付替えない。
5. t_ff71cb87/EVIDENCE.mdとred/green原本: OpenSpec1.2/1.3/1.4の先行TDD実行。04-02-SUMMARYが対応箇所を説明。
6. PLAN-MAPPING・UI-SPEC・docs/wordfreq-min-count-verification.md: AC1=REQ15..AC7=REQ21、14UI truth、source34〜38/44の確認先、品質専用実行/台帳/final owner/3配送gate。
7. run154/runbook-red.txt、runbook-green.txt、browser-free.txt、full-suite.txt、saved-capture*.txt: doc absent RED1 failure、正常/8mutation GREEN9、browser-free75/full694/保存原本27×2、各exitはSUMMARY/実terminal結果。

## 未実施（合格として配送しない）

品質独立CLI/全pytest/両幅全画像実閲覧/同環境baseline比較/source-order署名/canary/final owner終了・全view照合、品質ledger、OpenSpec2.2、PM本人の原本読取り、現head CI、公式phase検証/OpenSpec verify/PM受入。品質の対象は後続push済み最終headでfresh rootから全面実行する。Builder captureはpending-review/independent_acceptance=false。
