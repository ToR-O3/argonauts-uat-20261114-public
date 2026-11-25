# Phase 7 計画検査・引継ぎ

依頼: r-d4bcda40 / カード: t_67272f01 / 工程: 計画 / 流れ: full
承認元: t_ef216d95、t_fa8e2c5f completed run119、OpenSpec r-d4bcda40-max-count。
成果は計画のみ。製品コード/README/試験実装は未変更、製品pytest/CLI/HTML画像閲覧/通信検証/CI確認は未実施。

## 公式取込みと対象
- 開始時init.progressはPROJECT/REQUIREMENTS/ROADMAP/STATEすべてtrue。既存要求を変えないmergeを選択。
- 承認BMAD/OpenSpec5文書を公式classifierへ1文書ずつ委任し、source_path/type/manifest_override/precedenceと出力名を照合。
- 公式synthesizerのSTATUS READY。INGEST-CONFLICTS: BLOCKERS0 / WARNINGS0 / INFO0。今回分類専用ディレクトリで旧分類を混ぜない。
- 公式phase.addは7を返した。REQ-23..28を追加、過去phaseや残存ディレクトリを再利用しない。
- 過去phaseのstale検証は今回の達成とせず、その履歴を保持。

## 独立検査
- UI researcher sa-0-9a35ac69、独立checker sa-0-4a6d9cf9：全7観点PASS。表示を変更しない契約。
- 公式UI probe14適用・unclassified0、autoのkind確認と具体契約によるexplicit解決を書戻し。
- 公式researcher sa-1-257928ef、pattern mapper sa-0-1a9b5e43が原本を保存。
- 公式planner sa-0-c47b6d9aが3PLANを保存、checker sa-0-20dfbf48で2blocker+1warning。
- 指摘: OpenSpec1.1全ケースの未実装時REDの配置、ResearchのRESOLVED表記、task feedbackと高遅延E2E gateの区別。
- revision planner sa-0-2d8c7510が全1.1先行REDを本体変更前へ集約、未決なしと実行gate委譲を正式化、必須E2Eは有限600秒gateとして維持し終端をread-only検証へ分離。
- 最終checker sa-0-01343a59は通常終了/非truncated、`## VERIFICATION PASSED`。未解決BLOCKER/WARNING/INFOなし。全6task・REQ-23..28・D-01..08・edge15/UI14・脅威・依存/作成順・独立品質配送を検査。
- checker前後のPLAN SHA-256一致を親のsha256sum -cで確認。最終検査後PLAN変更なし。

## 最終版のSHA-256
| PLAN | SHA-256 |
|---|---|
|07-01|6320b2ec98800e2e5e21122a4a705336fc88aa0d7ae66c3e630ba093b81d1dd3|
|07-02|f3b83de3d43a128bb08497a329f8a0fe2b51cf0924bb40fe6badbb561d427dd3|
|07-03|9decf06663507346a47246c68ccd27d337d939c32898508fd2575439861ceeb5|

## 親が実施した公式照会
- verify-command-paths exit0: not_applicable、17commands、blocker0/warning0/readError null。対応外を実在証明とせずcheckerが同/先行task作成順を確認。
- verify-failure-directions exit0: ok、17commands、blocker0/warning0/readError null。
- verify.plan-structure: 全3PLAN valid:true、各2task。
- check.decision-coverage-plan: passed true、8/8、uncoveredなし。
- gap-analysis-plan-post: exit0、passed true、block false、要求6+決定8=14/14 covered。
- 最終PLAN集合+ROADMAPでAPI coverage実行：exit1は正常negative、detected false/signalsなし。AI/schema対象なし。
- security_enforcement/nyquist_validation/plan_check/pattern_mapperは開始値trueを維持。config.jsonは承認headから差分なし。
- state.planned-phaseをphase7/name/plans3で実行しStatus更新を確認。Current PositionはCurrent Plan:1 / Total Plans in Phase:3 / Status:Ready to execute。
- 状態注意: 旧完了値の保存規則で初回planned-phaseがStatus/Last activityを保持したため、公式テンプレートのPlanningラベルへ整合後に公式state.update/planned-phaseを再適用。Current Planは公式state.updateのbody source経由で1に同期。state-snapshotはphase7/current_plan1/total3。snapshotのstatusはReady to executeをexecutingへ正規化するが実装済みではない。
- CONTEXTのD-ID箇条書きを公式の `- **D-NN:**` へ表記修正。決定内容とPLANは変えず、公式網羅検査を再実行。

## 実装と品質への割振り情報
| PLAN / wave | OpenSpec tasks | 内容 |
|---|---|---|
|07-01 / 1|1.1,1.2,2.1|変更前oracle封印、全1.1先行RED、全形式の局所max実装と内部spy・互換比較|
|07-02 / 2（07-01依存）|1.1,1.3,2.1|先行群の空/入力/usage再確認、README例1つの先行試験と説明|
|07-03 / 3（07-02依存）|2.1,2.2（引継ぎのみ）|max専用検証経路、全pytest/scope記録、品質の独立実行手順と証拠配送|

3PLANを同じ依頼branchへ直列で積む。taskの検証ファイル/入力は同taskまたは先行taskで作る。旧min-count専用合格や人の例外を流用しない。
OpenSpec2.2の実施は品質のフェーズ検証へ必ず渡す。品質本人が対象headで独立CLI/1280x900と320x900 DPR1/全画像実閲覧/raw/通信を確認し、VERIFICATION.mdとCLI/CI文字証拠を標準添付。AC別の閲覧画像枚数/内容/結果を記録し、PMに画像や圧縮物の閲覧を求めない。未報告CI・未実施を成功扱いしない。

製品の受入合格ではなく、実装へ渡せる計画の合格である。
