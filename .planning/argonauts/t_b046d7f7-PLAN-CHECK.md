# Phase8 計画検証・割振りへの引継ぎ

## 判定と対象
公式独立gsd-plan-checker第2回: **VERIFICATION PASSED**、BLOCKER0/WARNING0/INFO0。委任deleg_0c6850da、通常completed、truncated=false。これは計画の判定であり製品合格ではない。製品/pytest/ブラウザは未実施。

完了ガードがGSD REQUIREMENTSにBMAD要求の再記述ではなくID/path参照を要求したため、REQ-28〜33を同じ承認PRDのFR-1〜7/RULE-1〜4への直接参照に修正した。対応が複数のGSD IDは複数行でBMAD原本へ対応付け、CONTEXT/PLAN/承認原本の全文契約は変えていない。修正後の独立公式checker deleg_1605c371は通常completed/truncated=false、VERIFICATION PASSED、BLOCKER0/WARNING0/INFO0。3PLANのSHAは不変であり、親の2probeを同じSHAに対して再利用した。checkerは参照先実在・全範囲維持・全観点を再確認した。

受付判断: 2026-11-28T14:45:42.849521+00:00、原文「提案のまま進めてください（1〜5 すべて提案どおり）。」承認原本head17648fc、固定OpenSpec r-e0a2598f-wordfreq-exclude。PM t_9da1db1eの再開判断は設計の直接合成だけを外しplanner直接読取りへ移すこと。製品範囲/受入条件は縮小していない。

## 原本と最終SHA256
| PLAN | SHA256 | OpenSpec |
|---|---|---|
| 08-01 | 19b2b5003a278ee1db4408219f52117a7d97150c9915b2d1d636d9af4073d6c4 | 2.1 / 2.2 |
| 08-02 | d311bb387a9bca65406343a886d581926e843a80aea2a90539867032e640e293 | 2.1 / 2.2 |
| 08-03 | b563550445bbbe798e370895e218753a690208b3cef23b634c5dac437f854b7b | 3.1 / 3.2引渡し準備 |

全pathは `.planning/phases/08-wordfreq-exclude/<id>-PLAN.md`。各2task、同じ依頼branchで直列。phase8、ROADMAPにあるphase_count6（既存1/3/4/5/7＋今回8）。この依頼の計画対象は8だけ。

## 実測した公式検査
- 再分類6件: PRD2/SPEC1/DOC3、manifest_override=true、precedence=null、source_path/公式path hash一致。旧7件は停止済み履歴であり再利用なし。公式synthesizerが6原本から全intelを再生成しBLOCKERS0/WARNINGS0/INFO0、READY。設計原本は保持し研究/planner/checkerが直接読んだ。
- CE学習検索は同カード前runの保存原本を再利用。3関連学習。旧語昇順を現行初出順へ戻さない注意を保持。学習無しとはしていない。
- 親の最終 `gsd_run check verify-command-paths 8 --raw`: exit0、14件not_applicable、blocker0/warning0/readError:null。uvコマンドはパス検査対象外なので、独立checkerがtask内作成→実行順と前提を別途確認。コマンドが実行成功したという意味ではない。
- 親の最終 `gsd_run check verify-failure-directions 8 --raw`: exit0、14件ok、blocker0/warning0/readError:null。
- 完全JSON: `.planning/argonauts/t_b046d7f7-command-paths-v2.json` と `t_b046d7f7-failure-directions-v2.json`。checker前後SHA一致、sha256sum -c全3原本OK。
- 公式frontmatter/plan-structureは全PLAN valid、各2task。08-01 one-way warningは公式Already settled例外を独立checkerが根拠確認しissue0と判定。採用済みD01..07を再承認しない。
- UI契約: 独立gsd-ui-checker deleg_b2086421で7/7 VERIFIED、通常終了。親が承認後公式compiled probeを実行exit0、4要素/14項目、unclassified0。--autoで14explicit解決し原本へ記録。表示契約の定義であり製品描画確認ではない。
- edge compiled probe exit0、26項目。PLANに21explicit＋5backstopを保持。prohibition2件はdescriptor-less flagged-unverified。後続品質は個別dispositionを残し、未確認を合格にしない。中断/並列の新しい保証は発明しない。
- plan:pre: security/nyquist/plan_check/pattern_mapper開始trueを維持。公式研究/パターン調査を実施、AI/外部API/ORMは実scopeにない。drift照会はno-upstream-artifacts/no-structure-mdでadvisory skip、UI gate hasUiSpec=true/block=false。
- 公式decision coverage: passed=true、11/11、uncovered=[]。最初のCONTEXT bullet形式はcould-not-parseであったため `- **D-NN:**` へ書式だけ直した。内容/PLAN変更なし。再照会合格。初回の進捗更新をcoverage失敗と同じ呼出しで進めた手順順序の注意は保持し、再照会後に進捗を再確認した。
- plan:postの唯一のactive gate gap-analysis.plan-post: exit0、passed=true/block=false、6REQ＋11D=17/17 covered。
- state.planned-phaseの初回は更新phase8/plans3。再実行はupdated=[]で「Current Position has no recognized labels — transition was a no-op」のwarning。この応答だけを更新成功と扱わず、公式state-snapshotでcurrent_phase8/current_plan1/total_plans_in_phase3を読み戻し、STATE本文Phase8 READY TO EXECUTE/Current Plan1/Total Plans3を確認した。frontmatter status=executing・過去Phase7 activityは残存表示であり、製品実行開始や今回完了を示す証拠にはしない。

## 独立checker全観点と差戻し
第1回deleg_efac2620は2BLOCKER: Builder計画内の後続品質実行taskが循環、研究Open QuestionsのRESOLVED記録不足。plannerとresearcherへ各所有原本を戻して修正。第2回は全観点合格:
- REQ28〜33、FR1〜7/AD1〜4/EX1〜5/D01〜11の具体task対応。
- task完全性、01→02→03依存/共有ファイル、成果物/データ契約/責任階層、task時点の検証ファイル作成順、Nyquist/失敗方向、予算内、security/pattern/UI/fallback、対象SHAを確認。
- HERMES/追加project skills/REVIEWS等は不在・非該当。追加agent-skills照会は空。
- 最終08-03-02はBuilderが実在handoff資料/target原本をfail-closed検査して完了可能。実品質実行・VERIFICATION/quality-evidence生成・標準配送・OpenSpec3.2完了は後続独立品質カードに残す。品質をBuilderが代理実行しない。

## 後続への注意
1. PMは3PLANを直列予約し、その後に通常の独立品質フェーズ検証/フェーズ判断を予約する。08-03-02から品質をdispatchしない。3.2は引渡し準備だけでチェック不可。
2. pytest環境は未構築/未実行。Builderは既存dev extraを利用可能にし版を記録してから意味あるREDへ。環境失敗をRED/GREENにしない。新依存/CI/uv.lock commitなし。
3. 固定版79d83ba14dd59d289d2ecd3e33c85e8de437972eの未指定stdoutを同条件でバイト比較。入力両役不変、全行検証後casefold、zero body reads、HTML元総数/全空状態/全形式を試験する。
4. 品質がhead/command/exit/expected-actual/AC対応をVERIFICATIONとCLI文字原本へ保存添付。画像があれば実閲覧枚数/内容/結果を文字へ。PMが画像/圧縮を開く前提なし。
5. BMAD scripts=stale警告は継承、本家更新なし。別途doctorで道具を確認。前run synthesizerのgsd-tools.cjs直接照会逸脱は成功根拠にしない。再開後親/委任は公式launcher使用を明示し、確認したtraceでは直接呼出しなし（compiled独立probeは公式手順通り）。
6. 過去phaseのstale/Phase7未解決は保持。今回の成功と混同せず、範囲を勝手に追加しない。OpenSpec checkboxは1.1だけdoneを維持、2.1/2.2/3.1/3.2未完了。
