# 08-01 公式終了処理の記録

対象は `.planning/phases/08-wordfreq-exclude/08-01-PLAN.md` のみ。製品/試験原本は9498e0c、SUMMARY初回commit f5f0b4f。後続08-02/03は実行していない。

## 公式結果と保存原本の照合

- `state.begin-phase --phase 8 --name 'wordfreq exclude' --plans 3`: updatedあり。保存されたCurrent focusはPhase8、Current Plan1/Total3、本文状態Executing Phase8。
- SUMMARYをcommit後の `state.advance-plan`: advanced=true、previous_plan1/current_plan2/total_plans3。`state-snapshot`と保存されたCurrent Positionはphase8/plan2/total3、本文StatusはReady to execute。frontmatter executingはphase単位の進行状態。最終PLANではないためlast_plan/phase.completeは適用しない。
- `state.update-progress`: updated=false、reason=`phase scope is unscoped, not complete`。公式warningを成功扱いしない。既存Progress25%は更新されていない。`progress json`は6phase/20plan/18summary、Phase8は3plan/1summary/In Progress、percent=null/phase_scope=unscoped。`state.validate`はvalid=true/warnings=[]/scope=complete。スコープ未確定は全体パーセントの計算範囲であり、phase8/plan2の確定位置は保存原本と公式値で確認済み。過去phaseの書式/負債を書き換えてパーセントを発明しない。
- `roadmap.update-plan-progress 8`: updated=true/plan_count3/summary_count1/status In Progress/complete=false。保存ROADMAPは1/3 plans executed、08-01だけ[x]、08-02/03は[ ]。
- `state.record-metric --phase 08 --plan 01 --duration 11min --tasks 2 --files 13`: recorded=true。
- `state.record-session --stopped-at 'Completed 08-01-PLAN.md; same-card quality review pending' --resume-file None`: recorded=true。公式snapshotの停止場所も一致。
- `requirements.ready-ids <PLAN> REQ-28..33`: ready=[]、6IDすべてblocked。共有要件のためチェックを付けない。SUMMARYのrequirements-completedはPLANからの必須コピーであり全phase合格の宣言ではない。
- `init.execute-phase 8 --pick incomplete_plans`: 08-02-PLAN.md,08-03-PLAN.mdのみ。
- `verify-summary <SUMMARY>`: 最終応答passed=true、summary_exists=true、files_created checked2/found2/missing[]、commits_exist=true/self_check passed、errors=[]。

## 診断と書式補正

verify-summaryの初回は、inline codeにした「末尾が.xmlのコマンド全体」をパスと誤認し、`## Verification and TDD`以降の歴史的RED/blocked語を自己点検失敗と誤認した。公式verify.cjsの文字列ヒューリスティックを読み、コマンド内容・歴史的実測・未完事項は削除せず、表のコマンドを平文、見出しをExecuted Test Evidence、実在するCreated/Modifiedパスを独立列挙する書式だけに補正。最終Self-Check節を保持し公式再実行で上記合格を確認した。

公式evaluation-scopeはplan番号のsubject検索で過去の別08-01も返した。本件の起点2f6fa7dと4つの実作業commitはgitで直接確認し、過去commitを今回の試験証拠へ混ぜていない。

OpenSpec管理下CLI `instructions apply --change r-e0a2598f-wordfreq-exclude --json`: exit0/state ready、total5/complete1/remaining4。1.1だけdone、2.1/2.2/3.1/3.2は未完。08-01の実測を同tasksに追記したが、後続08-02/03・独立品質の所有分を先取りしていない。

## 実装と検証の範囲

追加71件成功、全suite773件成功（158.72s）。詳細の実コマンド/期待/実結果はSUMMARY、未編集JUnitと隔離13変異のconsole原本は同ディレクトリ。初回未指定baseline79d83ba比較・独立品質・画像閲覧は未実施で後続へ渡す。画像閲覧0枚。品質の印は付けない。

承認参照: 判断日時2026-11-28T14:45:42.849521+00:00、依頼者原文「提案のまま進めてください（1〜5 すべて提案どおり）。」。製品未決を追加していない。BMAD scripts=stale警告は継承、更新なし。
