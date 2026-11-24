# 計画引継ぎ保留 — GSD状態の公式照会不一致

## 現象

Phase 6のPLANは独立公式checker合格、同じSHAを保持している。しかしSTATE.md本文のCurrent Positionが `Current Plan: 1` / `Total Plans in Phase: 1` / `Status: Ready to execute` でも、公式state-snapshotが `current_plan: Not started` / `status: completed` を返す。frontmatterに古い値が残る。

## 保存済み成果

- Phase 6は公式phase.add結果。全3要件REQ-25/26/27とOpenSpec1.1/1.2/2.1を06-01-PLAN.mdの2tasksへ対応。
- 独立checker2回目: VERIFICATION PASSED、blocker/warning/info各0。初回見積証拠欠落だけを公式estimate-check exit0で解消。
- 2つの公式probe: exit0、command paths not_applicable（実在保証とはしない）、failure directions ok、全29commands severity none。
- decision-coverage-plan: 8/8、plan:post gap-analysis: 11/11。設定開始値と一致。
- README/製品CLI/試験は変更も実行もしていない。入力と期待値は計画値であり実測ではない。
- PLAN SHA-256: 45a984e6144e5e654e30ff80e41b24519fd2e165cba9b6e818d2605659055106。

## 試みた公式操作と結果

1. 公式launcherを同じシェルでsourceし、`gsd_run query state.planned-phase --phase 6 --name 'README min-count three example' --plans 1`。初回はphase位置等を更新したが、plan/statusの旧値が残った。
2. 導入版stateテンプレートとチーム指定のCurrent Plan/Total Plans in Phase書式を確認し、既存STATE本文だけを実際の位置へ合わせた。phase6/plans1は実在PLANと一致。
3. 公式 `state.update 'Current Plan' '1'` / `state.update 'Status' 'Ready to execute'` はupdated:trueでもsnapshotの旧値は維持。
4. CLIが案内する直接field更新も試した。current_planはbody-derivedとして拒否。statusはupdated:trueでもsnapshotはcompleted。last_activity_descだけは公式更新が反映した。
5. planned-phase再実行はexit0でもupdated:[]、`Current Position has no recognized labels — transition was a no-op`警告。snapshotは依然として旧plan/status。

最終の生JSON: `.planning/argonauts/r-5f8197e8-state-planned-result.json`、`r-5f8197e8-state-snapshot.json`。本文・frontmatter・公式照会の一致を確認できないので、役割の計画完了条件に従い割振りを解放せず保留する。GSD本体・Hermes・設定を改変する迂回はしていない。

## 再開時

同じカード・同じ依頼の保存済みPLANと今回の取込み結果を再利用できる。新phaseを重複追加しない。作業開始手順で依頼branch最新へ合わせ、公式ランチャーで状態を再確認する。GSD状態修復後、公式state.planned-phaseとstate-snapshotでphase6/current_plan1/total1/実装待ちが一致することを確かめる。PLANを変更する場合はSHA取得→両公式probe→独立checkerをやり直す。製品の実装・CLI検証は後続工程のまま。
