# r-6442a149 計画検証・割振りへの引継ぎ

## 結果と範囲

Phase 8「wordfreq exclude-file」を公式GSDで追加し、2 PLAN・5 taskを直列に計画した。計画の独立検査は `## VERIFICATION PASSED`、BLOCKER/WARNING/INFO各0。これは計画の合格だけであり、製品実装・新試験・既存全件回帰・ブラウザ・独立品質・受入は未実施。

| PLAN | 原本 | 順序/task | OpenSpec tasks |
|---|---|---|---|
| 08-01 | .planning/phases/08-wordfreq-exclude-file/08-01-PLAN.md | Wave1、3 task、正常系tracer/行文法/Unicode/最後FILE/空結果/総数 | 2.1 |
| 08-02 | .planning/phases/08-wordfreq-exclude-file/08-02-PLAN.md | Wave2、08-01依存、2 task、失敗/順序→全件回帰/独立品質文字原本 | 2.2, 3.1 |

同じ依頼branch `argonauts/r-6442a149` へ順に積み上げる。共有README/CLI/testsを並列変更しない。各taskが新assertを実在する既存試験ファイルへ先に追加し、RED→GREENを確認する。先行実装ですでにGREENなら、その事実と使い捨てscratch変異による判別力を記録する。未実施のREDを創作しない。

## 承認入力と取込み

- 要求・仕様 t_c6600988 のcompleted/done run、仕様承認t_0d1aa16aのapproved、承認head `8a2c69b8332e9704377fe680af51767c74e4ab56`、同じOpenSpec変更 `r-6442a149-exclude-file` を照合した。
- 判断日時: 2026-11-28T06:59:36.405633+00:00
- 受付の依頼者原文: 提案のまま進めてください（1〜6のとおり。既存の集計に合わせ、追加の文法は設けない）。
- CE公式learnings-researcher: docs/solutions/の6文書を検索、関連4件。旧語昇順の学習例は現行初出順と違うため流用しない。原本 `.planning/argonauts/r-6442a149-learnings.md`。
- 開始時init.progressのPROJECT/REQUIREMENTS/ROADMAP/STATEは全てtrue。既存phaseは1/3/4/5/7。古い検証staleは今回へ混ぜない。
- 公式分類・合成を実施。初回Brief/PRD参照循環は、原本を変えず背景Briefをmanifestから外し、正本PRD/設計/proposal/spec/tasksの5件へ絞って再合成した。今回集合の循環なし。分類はmanifest_override=true・precedence=null、原本パス/型/出力名を照合。
- 公式合成は旧locked HTML総数契約と今回の除外指定時の総数変更をBLOCKER1件として記録した。E.7の「今回承認済み変更」分岐を採り、標準mergeは行わず公式phase.addで8を追加。旧履歴を消さず08-CONTEXTへ指定時だけの承認済み拡張を記録し、REQ-28〜35を追加した。報告は `.planning/INGEST-CONFLICTS.md`、添付195、SHA-256 `d1b3cd26c9095fdc2898c8833162752dc99f2631709da904334bf2f0f170ae16`。
- OpenSpec tasks1.1は完了を保持。2.1/2.2/3.1のチェックを完了にせず、GSD対応だけ追加した。

## 公式計画・独立検査

- 公式phase-researcher sa-0-03b28049: `## RESEARCH COMPLETE`。原本08-RESEARCH.md、実コード/実在test/公式Python資料を照合。既定Pythonのpytest欠落と既存代替環境を区別。機能試験は実行していない。
- UI researcher sa-0-0d15fb8bと独立UI checker sa-0-a954a989: `## UI-SPEC VERIFIED`、7次元PASS（registry/inventoryはN/A根拠あり）。既存formatter/CSS/文言を継承し再設計なし。親が公式ui-consideration-probeを実行し4要素/14候補/unclassified0を確認、承認済み設計truthでexplicit解決14をUI-SPECへ記録した。製品表示の合格ではない。
- 公式pattern-mapper sa-0-dd7d1f90: `## PATTERN MAPPING COMPLETE`、既存analog/責務/配線/試験を08-PATTERNS.mdへ保存。
- 公式planner sa-0-b700beb1: `## PLANNING COMPLETE`、2 PLAN。VALIDATIONは正式task/wave/threat対応を記録しdraft/nyquist_compliant:falseを維持。ASVS1/security high、pattern_mapper/nyquist/plan_check等の開始設定を無効化していない。
- 独立plan-checker sa-0-7a488c35: `## VERIFICATION PASSED`、BLOCKER0/WARNING0/INFO0。全公式観点でREQ-28〜35、決定D-01〜08、承認scenario、edge25件、UI状態14件を確認。全5taskのファイル作成順と実在するtests/test_sources.py/test_cli.pyを読取り確認。one-wayの3警告は承認済み判断の公式Already settled例外として未解決指摘に残さない。
- checker結果は通常終了、truncated:false、exit_reason:completed。PLAN SHAを前後照合して一致した。

## 親の実行結果と制約

公式CLIは同じシェルでruntime launcherをsourceして `gsd_run` から実行した。初回合成子の直接node照会を発見し、再合成は公式ランチャーの取得済み原本を使うよう訂正した。

| 確認 | 実際の結果/原本 |
|---|---|
| verify-command-paths 8 --raw | 親がexit0。7 commands、status:not_applicable、blocker0/warning0/readError:null。pytest/env形式が解析対象外であり、パス解決済み/試験成功とは呼ばない。checkerがファイル実在と作成順を別途確認。argonauts/r-6442a149-command-paths.json |
| verify-failure-directions 8 --raw | 親がexit0、7件ok、blocker0/warning0/readError:null。argonauts/r-6442a149-failure-directions.json |
| decision-coverage | 最初の見出し形式はcould-not-parse。親がCONTEXTの8 ID見出しだけを公式bullet書式へ直し、内容は不変。原本に対する再実行exit0、passed:true/total8/covered8/uncovered[]。argonauts/r-6442a149-decision-coverage.json。補助projectionは初回履歴にすぎない |
| UI plan gate | hasUiSpec:true/frontend:true/block:false |
| context drift | block:false/stale_artifacts:[] |
| codebase drift | skipped:true/reason:no-structure-md、非blocking |
| post-planning gate | exit0、passed:true/block:false、REQ8+D8=16/16 covered/uncovered0。argonauts/r-6442a149-plan-post.json |
| state.planned-phase | exit0、phase8/plan_count2、Current Position/Current Phase/Total Plans更新を公式出力と原本で読戻し。bodyはPhase8 READY TO EXECUTE、Current Plan1、Total Plans2。公式正規化frontmatter statusはexecutingだが製品実行は未開始 |
| roadmap.analyze | phase_count6、番号1/3/4/5/7/8、08はplan_count2/disk_status planned。番号8と全体件数6を混同しない |
| OpenSpec strict | 管理CLIのvalidate、exit0、valid:true/issues:[]。tasksチェック不変 |
| git diff --check | exit0。製品/README/tests/依存/CIは承認headとの差分なし |

## 固定したPLAN原本

- 08-01: `b2648ab2d52e255e75a08e909c0ea85fc692efab83a47f377a38fe98561fb3d0`
- 08-02: `525026af0bb3d8df09ad69aebbe6db9c7de19b66f33b752572c3077029022f88`

`.planning/argonauts/r-6442a149-plan-hashes.txt` と `sha256sum -c` で前後一致。後続でPLANを変える場合は親の2 probeと独立checkerを再実行する。

## 実装・品質へ

- pytest実行系は研究でversion確認済みの `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest ...`。利用可能性は実装/品質でも再確認し、無断依存追加をしない。
- 品質は対象headで独立再実行しVERIFICATION/QUALITY-CLI等の文字原本を保存・標準添付する。画像取得時は品質自身が全画像を実閲覧し枚数/内容/結果を文字化。PMへ画像/圧縮閲覧を求めない。
- 新機能/全件回帰/画像確認の合格は本工程に含まない。次の割振りPMが08-01→08-02→フェーズ検証を予約する。
