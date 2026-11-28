# 品質担当への引渡し — 独立検証は未実施

Builder原本と対象の内容を検査した引渡しです。独立品質・フェーズ・PMの合格ではありません。OpenSpec3.2は未完です。

初期の製品内容対象: `526b89cec8d6b7c440b5716ee6319aec2f68f479`。依頼branch: `argonauts/r-e0a2598f`。固定過去版と依頼起点: `79d83ba14dd59d289d2ecd3e33c85e8de437972e`。
報告ファイルは自分自身のcommit hashを持てません。checkerは最新の製品/試験/README/pyproject変更commitをtargetとして固定し、その全Git bytesと現在のworktreeを照合します。報告だけの後続commitは許可しますが、品質のexact-head合格を引き継ぐものではありません。品質は報告時の実HEADを新しく解決し、必要な検査を独立再実行してください。

## 実行コマンド（repo直下）
```sh
uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude
uv run --extra dev python -m pytest -q
python3 -m unittest discover -s .planning/argonauts/r-e0a2598f -p test_quality_handoff.py -v
python3 .planning/argonauts/r-e0a2598f/check_quality_handoff.py --repo-root . --handoff .planning/argonauts/r-e0a2598f/quality-handoff.json
```

## 読む原本
- .planning/phases/08-wordfreq-exclude/08-01-PLAN.md
- .planning/phases/08-wordfreq-exclude/08-02-PLAN.md
- .planning/phases/08-wordfreq-exclude/08-03-PLAN.md
- .planning/phases/08-wordfreq-exclude/08-UI-SPEC.md
- .planning/argonauts/t_b046d7f7-edge-probe.json
- .planning/argonauts/t_b046d7f7-ui-probe.json
- _bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md
- _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md
- _bmad-output/initiative-r-e0a2598f/architecture/architecture.md
- openspec/changes/r-e0a2598f-wordfreq-exclude/{proposal.md,design.md,specs/wordfreq-cli/spec.md,tasks.md}

## Builder文字原本
- .planning/argonauts/r-e0a2598f/builder-evidence.md SHA-256 492758224c1cb88501c3e373436b2509382d0c9a14e6ae655bdefe3b73e45fe7
- .planning/argonauts/r-e0a2598f/baseline-captures.json SHA-256 13eb5869aae4e22afe71da6f1eef98b0fb6cf8c853593ba1657e53b57fb93682
- .planning/argonauts/r-e0a2598f/cli-captures.json SHA-256 7bf2cfa1980bb5fa0991a4d44b10c3a703c192c4c190b7a5d33328a697926b74
- .planning/argonauts/r-e0a2598f/baseline-controls.json SHA-256 80473813d75aab626250051193ea5e4ab7da8e4333e280b0e5330f8208c9a34a
- .planning/argonauts/r-e0a2598f/integration-green.xml SHA-256 905b596dbd3af217d6d7be71a3b93b2ceab25aaf2e760b122ec302327cd218fa
- .planning/argonauts/r-e0a2598f/suite-green.xml SHA-256 6ed2bd6ae8a0af8a7c61847134735e1000e6edc6adf1b15228671e91c75870a8
- .planning/argonauts/r-e0a2598f/checker-green.txt SHA-256 e83d7d9d1b7a92e5ef3d5345770afff08d5369d94583b8ac7ffd08d6ea568611
- .planning/argonauts/r-e0a2598f/regression-executions.json SHA-256 66949b64a29e7218690fdfe41ec2542ee015e7d8ede2ef40ffa9c87ec2433405
- .planning/argonauts/r-e0a2598f/exclude-final-stdout.txt SHA-256 89436c49e102a9e8d7ceaca5a03428a73a689e5eef8b2b7956dfc0e7715951e6
- .planning/argonauts/r-e0a2598f/exclude-final-stderr.txt SHA-256 2da222706982e0cf58345a76d311e577b29ca05cb0eaa8fa6807445f8c0feb60
- .planning/argonauts/r-e0a2598f/suite-final-stdout.txt SHA-256 a435184b3db74559f18ab06d99424b570e4abba7189808297b1a09fd2186db73
- .planning/argonauts/r-e0a2598f/suite-final-stderr.txt SHA-256 2da222706982e0cf58345a76d311e577b29ca05cb0eaa8fa6807445f8c0feb60

全6ACとREQ/FR/RULE/AD/EXへの根拠はbuilder-evidence.md。全26edge/14UI/2prohibitionと各predicate/source/dispositionはJSONに個別記録し、checkerがPLAN/raw probeから独立導出して比較します。5 concurrency backstopはhuman_needed/insufficient_spec、descriptor-less禁止2件はflagged-unverifiedを保持します。画像閲覧0枚、geometry/可読性/実通信は新規実測していません。未確認をgreenにしません。

## 後続品質の全義務（原本をそのまま転記、すべてpending）
1. A different quality actor reads approved PRD/Brief/architecture/OpenSpec originals, all PLANs and handoff materials, current sources/full request diff, all26 edge predicates including five backstops, fourteen UI states and both prohibitions. Builder originals are leads, not independent results.
2. Re-resolve and record exact target head before and after execution/reporting, verify content manifest and repeat relevant checks on changed target content. Independently run `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude` and `uv run --extra dev python -m pytest -q` plus real CLI cases covering AC1..6. Nonzero/zero-selected, stale-head or reused Builder execution is not independent success. Capture literal commands/argv, fixture bytes, interpreter/environment, stdout/stderr/exit and expected-vs-actual; retain full baseline provenance and both input-role immutability.
3. Execute the real official GSD phase-verification and OpenSpec verify workflows, preserving genuine results. Independently inspect source order/pure interfaces/full diff, unchanged formatter/CSS/basename/static safety and no new dependency/network/CI/new source/input rewrite. Write `.planning/phases/08-wordfreq-exclude/08-VERIFICATION.md` and `.planning/argonauts/r-e0a2598f/quality-evidence.md` plus readable text originals with per-AC/REQ/FR/RULE/EX/AD trace and pass/failure/unverified dispositions. These paths are later quality outputs, not Builder files_modified/must-have artifacts.
4. Give every UI state an evidence disposition. Source/fixed-baseline bytes support preservation, not measured geometry. If render inspection is needed, use actual saved CLI UTF8 HTML with inherited1280x900/320x900 DPR1; text records actual image viewing count/content/result and raw Range/clip/non-overlap checks without adjustment. If none inspected, record zero and actual evidence used. For browser/network observations if performed, record versions/conditions and failed/blocked attempts; unperformed observations remain unverified. PM need not inspect images/archives.
5. Preserve both descriptor-less prohibitions as flagged-unverified. Backstops without explicit evidence yield human_needed/insufficient_spec, not invented interruption/parallel guarantees, false feature failure or silent pass. All26 edges/14 UI/2 prohibitions need dispositions, not merely aggregate counts.
6. Standard-deliver VERIFICATION and CLI/quality readable text originals through parent with exact paths and delivery index, so PM can read_file each condition. Quality owns actual verification, these outputs and delivery; OpenSpec3.2 remains pending until genuine independent verification/delivery, and Builder never checks it. Archive/PR/finalization and PM acceptance remain with later owners. No independent actor/evidence means quality card pending, not Builder PLAN blocked.

## 実在する公式手順（参照のみ、Builderは実行しない）
- gsd: /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/gsd-core/workflows/execute-phase/steps/verify-phase-goal.md (SHA-256 97bea7d8154f2fc31fca29cf13668386060ea9bc4f0d8819ed306f4f2b7df94e)
- openspec: /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/plugin-data/agent-plugin-argonauts-55aeafc7/openspec/.agents/skills/openspec-verify-change/SKILL.md (SHA-256 3b86fbb9734fdb6b942dd12d0afa4247457aa7f212bb48832eae133f5e66880a)
GSDは公式execute-phaseの検証経路（verify:post/security→code-review→regression→verifier→fingerprint→verification.status）を品質が実行。OpenSpecはstatus/instructions applyから完全性・正確性・整合性を品質が確認。公式ランチャーは同じ端末内のgsd_run関数からshで起動し、gsd-tools.cjs直実行はしません。
後続成果物: .planning/phases/08-wordfreq-exclude/08-VERIFICATION.md、.planning/argonauts/r-e0a2598f/quality-evidence.md と読みやすい文字原本。品質は標準添付とSHA-256照合で配送し、PMが条件ごとにread_fileできる索引を渡します。後続品質をこのBuilderから起動/予約しません。archive/最終化/PR ready/マージは対象外。

## 品質差戻し後の浅い取得への対応

現在の内容対象は上のtarget。修正前の実測原本は履歴として保持。最新の全件確認はoriginを切断したdepth1 checkoutで1159件成功、固定commit欠落は実行前後とも確認。基準のGit object chainを同梱原本で認証するためfetch/skip/自己goldenを使わない。
必須のCI不具合だけ修正。記録のみのWR-01/WR-02/IN-01〜05は未変更。独立品質・OpenSpec3.2はpending。
- .planning/argonauts/t_354e296c/CI-REPAIR.md SHA-256 74150fa23977a0fbb672110779a627f7adbba5f69f61cb696f9d19bed7d40882
- .planning/argonauts/t_354e296c/shallow-red.txt SHA-256 f4da3e699ed15a0105c6e668da98ea461c46d4afe63a38b705ee0bb3a39ef9f3
- .planning/argonauts/t_354e296c/shallow-green-final.txt SHA-256 8bf11c06f3a455f39e509c40b744c781f6196b5b12c911b750b07a4b425f0bab
- .planning/argonauts/t_354e296c/shallow-suite.json SHA-256 2b6e186dd48a7d25d9ca637ef96314948370d4ce60893a599130065085905436
- .planning/argonauts/t_354e296c/shallow-suite-stdout.txt SHA-256 10af6daccc15c833bbd18dac2bef8f842de354d53747a2bbb06c9d2bfa1fc9d7
- .planning/argonauts/t_354e296c/shallow-suite-stderr.txt SHA-256 1429f52773992e8aaa5645993703a024707382db2c1a276c2debb8e005446a09
- .planning/argonauts/t_354e296c/exclude-repair-green.txt SHA-256 462faccee3766c02ce9e4917d02491af20031b56df09949a6f246b2495ee0907
- .planning/argonauts/t_354e296c/handoff-tests-repair.txt SHA-256 dcd0df7b87be057ea0a9767037dffd6e7c3a3ba2d45ffac3bced281867eb7164
- .planning/argonauts/t_354e296c/verification-status-repair.json SHA-256 1768fe9c86ba3cfcb7a5bf3fcab7ef746630f432285ddc20d0582ee5bd0c4b4a
- .planning/argonauts/t_354e296c/state-repair.json SHA-256 6ddbc3681ebc29bcd5d2a42162fdcbd8b6e238548b3eb262b053e135fdea2dc5
