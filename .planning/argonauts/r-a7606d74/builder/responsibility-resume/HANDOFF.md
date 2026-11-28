# 責任分離後のBuilder検証と品質引継ぎ

PM判断 t_8b54614f コメント246・247に従い、同じQuickの担当責任だけを整合。製品要求・受入条件は変更しない。

- Quick: `.planning/quick/261128-vh0-wordfreq-min-length`
- 検証対象head: c7634579f9966f8718c16d9e88ffa5d47a9b7409。以降は工程文書と検証原本のみ。製品/試験/README/依存/CIは全suite成功1d3a99aから差分なし（git diff --exit-codeで確認）。
- 公式 `query verification.status` はpassed。新VERIFICATIONはBuilder担当範囲6/6のみ。旧human_neededは `261128-vh0-VERIFICATION.before-pm-responsibility-split.md` と添付168に保存。
- fresh対象実測: min-length.stdout/stderr/exit、263 passed、exit0。verifier fresh spotは同Quick verifier/responsibility-spot.*、54 passed、exit0。
- 全pytestは今回再実行していない。既存 resume-fixture/all.stdout/stderr/exit（1311 passed、exit0）と製品/試験不変を照合。独立品質はこの結果を流用せず実行する。
- PLAN公式構造3tasksとOpenSpec公式applyの3descriptionsは同順同名。3/3完了はBuilder実施項目のみ。品質側必須受入はPLAN quality_acceptanceとOpenSpec tasks末尾にpendingで保持。
- 公式quick-tasks-appendにより同Quickの再検証Verifiedを追記。旧Needs Review行は過去判定の履歴であり、Quickを新規作成・再実装したものではない。公式state getで両行を読み戻した。

## 品質側の必須未完条件

独立qualityの最終head/fresh rootによる対象・全pytest、HTMLの省略/明示1互換・絞込み・全除外・元総数の1280×900/320×900・DPR1・zoom100%の実閲覧。全画像/必要tileを開き、raw対応と可読性・行/順位・元総数・空状態・見出しを文字で記録する。これらは未実施・未合格であり、製品最終受入pending。Builderは品質印・自動マージ予約・自己completeを行わない。

実CLI全原本は既存添付171のtar.gz、追加原本は今回の責任分離添付と同worktreeを参照。README.md不変。
