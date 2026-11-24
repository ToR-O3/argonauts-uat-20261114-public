# 06-02 原本保全索引（未完・封印前）

## run45 最新判断による現状引継ぎ

判断日時: 2026-11-24T14:03:31.787198+00:00
判断原文: 今のまま合格にする
受付 t_dbab0a34 と本カード t_2b523d66 の default コメントを読んだ。直前の問いは正常な空原本の標準添付拒否と保全未完についてであり、現状の不足を残して品質レビューへ進める判断として扱う。空原本の実体添付成功、全payloadの保全完了、独立品質のpassed、README-only達成を意味する事実へ置き換えない。A/Bを選んだと偽記せず、空原本の内容も変更しない。以下はrun43停止時の記録であり、当時の未push/未実施表記を保持する。run45の結果は06-02-SUMMARY.mdと06-02-HANDOFF.mdを参照。追加の保全封印は行わず現状で引き継ぐ。

主体: builder t_2b523d66 run43。開始head 3a5857b98c7f43e3a2545f9fadbe9bf96d89311a、注記task1 commit 3ced8ae（ローカル、未push）。
判断日時: 2026-11-24T13:39:57.048159+00:00。
原文: Aを選ぶ。この依頼に限り、原本の保全→最終化→品質の最終確認→受入の判断、の順を許可する。
範囲判断2026-11-24T21:20+09:00を維持。工程差分があるため条件2未達、品質run37 gaps_foundの原本不変。補完は未完で、最終化による除外を許可する封印ではない。

## 実block

PLAN task2が保全対象に含める `index.task2.patch` は0 bytes。標準kanban_attachに原本tokenを渡すと「添付する原本は空にせず、Hermes標準の25MB以内にしてください。」で拒否された。添付一覧を再取得し、この原本のIDが作られていないことを確認した。原本を非空に書き換えたり、ガードを迂回したりしない。
原本path: `_bmad-output/initiative-r-5f8197e8/verification/builder/t_5e02213b-run35/index.task2.patch`。
sha256sum実測: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。
wc -c実測: 0。空である理由は先行実装のindex差分が無かったため（06-01-SUMMARY、標準添付45の品質レビュー42行でも0 bytesと記録）。これは正常な空原本であり製品出力欠落ではない。実体標準添付は未保全。
PLANは利用不能/不足をblockする指定なので、task2途中で停止。task3・SUMMARY・checksum・HANDOFF封印・公式close-outは未実施。次runはこの途中状態を完了とみなさない。

## 作成済み添付の実測対応（全保全の完了ではない）

保存root S = `/home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/kanban/boards/v112-a/attachments/t_2b523d66/`。
B = `_bmad-output/initiative-r-5f8197e8/`、P = `.planning/phases/06-readme-min-count-three-example/`、O = `openspec/changes/r-5f8197e8-readme-min-count-three/`。
下表のhashは原本とS+保存名の両実体をsha256sumで計算し文字照合した共通値。添付一覧のID/保存名/保存pathを再取得済み。「未読」は文字の版/主体読取り未完なのでhash一致だけで保全完了とはしない。

|用途・原本の主体/版|原本path|標準ID|保存名（実体はS+保存名）|原本SHA-256 = 保存実体SHA-256|文字読取り結果 / 状態|
|---|---|---|---|---|---|
|例外判断・計画担当/run41|.planning/argonauts/r-5f8197e8-fix-1.md|55|scope-fix-1.md|98ee90c5636930f5e40ae46b9158d621649a81b29654f10a62192e007ff4fc71|原本全文読取、保存先文字再読はpending|
|縮小判断・計画担当/current|P/06-CONTEXT.md|56|scope-context.md|8e294869155ac48791de75964aa6cd08d41c238f27139af2d9ab7bf2b05448d4|原本全文読取、保存先文字再読pending|
|BMAD Brief・architect/run27 final|B/brief/brief-readme-min-count-3.md|57|brief.md|3acfd2118b18be2945956d3f819c262aa6ce49b15ff1b3150ac588951e67de12|原本全文読取、旧3形式要求は対象外。保存先文字再読pending|
|BMAD PRD・architect/run27 final|B/prd/prd-readme-min-count-3.md|58|prd.md|c5910c008a50afa18852f905f7a0366c71aee298cc0d1277f0d65c9661e9f423|原本全文読取、旧3形式要求は対象外。保存先文字再読pending|
|変更後提案・builder/3ced8ae|O/proposal.md|59|proposal-current.md|d8bf43935ffc42c994169835a5f61184e3395bfa1d8cb17d9c9a7fa865007c3a|原本patch全文読取、最新2条件/例外順序に整合。保存先文字再読pending|
|変更後設計・builder/3ced8ae|O/design.md|60|design-current.md|ac14ca77e81411f5e6f2740d00844be4327e75d74738febcde4c7a8af3ccc524|原本patch全文読取、保存先文字再読pending|
|変更後tasks・builder/3ced8ae|O/tasks.md|61|tasks-current.md|68c528a0b97ff59ab25f3107fed6d72df0cd10ed06a7ceb5226636ae0c287125|1.1チェック保持/1.2対象外/2.1未チェック。保存先文字再読pending|
|skip_specs設定・architect/current|O/.openspec.yaml|62|openspec.yaml|c1c8053f8a2e226033e3a4a616a653dfae3595387bd8f893e8360ba3e2d006f4|原本全文読取、true保持。保存先文字再読pending|
|調査原本・planner/current|P/06-RESEARCH.md|63|06-RESEARCH.md|f00f74f329caae1b872c7fe683b44f8ad360bafec16273de85da220b8abb7866|文字未読、hash一致のみ。旧実行要求は復活させない|
|パターン原本・planner/current|P/06-PATTERNS.md|64|06-PATTERNS.md|a4b5ec0da8a97d149eab4992c1262192909a1eb23c025aebfe522d3fceed8f86|文字未読、hash一致のみ|
|README・builder06-01/current不変|README.md|65|README.md|61e6dcd61f4296b9447ce800ff74923ac29b28b6d510795247355aecb428aec8|原本全文読取、独立期待cmp exit0。保存先文字再読pending|
|先行task1 head・builder/run35|B/verification/builder/t_5e02213b-run35/HEAD.task1.txt|66|HEAD.task1.txt|c659d556238f54bd032063ba614ed83eaee48b9535884a79b8f65510129ef17e|文字未読、hash一致のみ|
|先行全path・builder/run35|B/verification/builder/t_5e02213b-run35/name-status.task1.txt|67|name-status.task1.txt|c93494e6b43463abccac6c1c125e7df50fef9b8e55b65510683e4f59d98c3690|文字未読、hash一致のみ|

## 既存標準添付の実一覧取得済み候補（このrunの保全照合は未完）

- t_38b60b51: 24 proposal、25 tasks（旧仕様）。t_9c048e29 done/completed run28のreview_basisがこの2原本を承認根拠として指定。旧実行要件は後日の縮小判断により対象外であり、現在義務ではない。
- t_07d1d2d7: 30 `06-01-PLAN (1).md` が現在版候補、31 `PLAN-CHECK (1).md`、32 `STATE-BLOCKER (1).md`。26/28/29は旧版であり要求復活の根拠にしない。
- t_5e02213b: 33 before/34 request-base/35 expected/36 SCOPE/37 SUMMARY/38 head.task1.patch/39 tree.task2.patch/40 head.final.patch/41 name-status.final/42 status.task2/43 untracked.task2/44 FINAL-HANDOFF/45 06-REVIEW。45の保存実体全文はread_fileで読んだ。builder原本と品質の主体は分離する。空indexは添付されていない。
- t_de9630c7: 46 VERIFICATION/47 VALIDATION/48 SECURITY/49 openspec-verify/50 cli-evidence。原本VERIFICATION/openspec-verifyは全文読取済、run37のgaps判定を変更しない。
- t_304960d5: 52 06-02-PLAN/53 06-02-CHECKER/54 06-02-VERIFICATION-RECORD。ローカル原本はP/06-02-PLAN.md、.planning/argonauts/t_304960d5/CHECKER.mdとVERIFICATION-RECORD.md。3原本全文を読取済、保存実体の再読/hash照合は未完。

## 残件（停止したtask2以降）

上の空原本の保存方式の決定後、BMAD各レビュー原本、承認根拠、先行原本群、現行全差分/実装検査、SUMMARY等を列挙し全payloadの標準添付と全文/版/主体/hash照合を完成する。必要な未取得原本を架空IDで埋めない。hash一覧だけで完全性を認定しない。
索引/checksum/HANDOFFはpayload checksumから除外し、索引/checksumの配送receiptをHANDOFFへ、HANDOFF自身は標準添付metadataへ記録する。後発品質レビュー/検証は最終化開始前の追補gate。
原本保全→最終化担当だけの復元/除外→品質の最終実PR全差分/2条件文字原本の非commit標準添付→PM本人read_file後の受入。受入前自動マージ予約禁止、手動待ち。これは後工程契約であり現時点では未実施。
画像0枚（文字のみ）、zip不要。製品CLI/3形式/pytest/新試験/quality runbookは実行・作成しない。
