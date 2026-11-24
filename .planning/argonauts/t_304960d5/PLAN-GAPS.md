# phase 6 補完計画の未決判断：最終化への到達条件

何が起きたか：READMEの例は追加済みだが、工程差分が残り条件2は未達。条件2の解消を担う最終化は、通常の工程順では受入合格後にしか始まらない。
決めてほしいこと：条件2を未達のまま正しく記録し、原本保全後の最終化と独立品質の最終確認へ到達する工程順序を、PMの権限で決めてほしい。
選択肢：A＝受入合格を偽記せず、この依頼に限り原本保全→最終化→品質最終確認→受入判断の順をPMが許可する（推奨、最終化担当の責務を維持）。B＝工程差分の復元・除外を補完実装へ移すことをPMが明示承認する（担当時点の変更が必要）。どちらも2条件・独立品質・マージ禁止は維持する。

## 対象と最新判断
- 依頼 r-5f8197e8、計画カード t_304960d5、親フェーズ判断 t_c7b65335、後続割振り t_0ac7e6e2。
- repo ToR-O3/argonauts-uat-20261114-public、基準branch v112-a、作業branch argonauts/r-5f8197e8。
- 判断日時: 2026-11-24T13:09:04.816724+00:00
- 最新原文：「Aに近いが、人の側では状態の修復をしない。進捗の照会が古い値を返すのは手続きの食い違いなので、保存済みの計画をそのまま使って、先（割振り・実装）へ進めてよい。」
- 範囲判断日時: 2026-11-24T21:20+09:00
- 範囲原文：「検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。」

## 実際に確認したこと
- GH_CONFIG_DIR の存在確認 exit0。origin一致、fetch成功。依頼branchの起点に合わせ、base取込みは Already up to date。
- 確認HEAD f21dda5226c12e42f3d09a86019ccb412c4ed8df。
- 基準branchのHEAD 2437aa3445ecdb87e7a11fe7a1c0e196726a5af4。
- `git diff --name-status origin/v112-a...HEAD` を全件読んだ。全88件、README.md 1件と工程文書87件。報告前の品質確認head34eb0bbの84件とは対象headが違う。件数はfilterしてREADMEだけと判定していない。
- README差分は `python -m wordfreq input.txt` 直後への `python -m wordfreq input.txt --min-count 3` 1行追加、numstat 1/0。
- 公式ランチャーを同じシェルで読込み、`gsd_run query init.progress`、`roadmap.analyze`、`init.plan-phase 6` を実行。
- init.plan-phase 6 は phase_found=true、phase_status=Executed、phase_number=06、既存phase_dir、verification_pathを返した。新たなComplete判定ではない。同じphaseの --gaps が該当する。phase_count=5を維持。
- current_phase=01/1、旧phaseのstale表示は既知の手続き例外。これを停止理由にしていない。状態修復・新phase追加・過去phase再検証は求めない。
- planner.stall_detection_enabled=false。設定は変更していない。
- 保存済み06-01-PLAN.md、06-VERIFICATION.md、06-CONTEXT.md、OpenSpec tasks.mdを読んだ。既存PLANとREADMEは変更していない。
- 品質カード添付46〜50と計画カードの最新PLAN添付30が存在することを標準ツールで確認。添付30/46/49/50は現worktree原本とSHA-256が一致（順に c069f22c28c02875e0fe828499266e31134818ec19c1cf5d1e83c78b2366bc9e / e201fb9aee0e60c18fc45eb5daa66957c409faa007e3e5ea6e281fb2bf81956a / 1482c3c7a4b3a7f674b53e67651e569d8df665bf68efa9f078e0d184511fa3c9 / 0f5b7716b02775d6395ddc87144149b03a3cd994315584eab2328b5994741266）。これだけで全必要原本の保全完了とは認定しない。

## なぜ補完PLANだけでは閉じないか
1. 品質の06-VERIFICATION.mdは status=gaps_found、最終README-onlyを明示的FAILEDとしている。現在も全差分88件なので、この未達は継続する。
2. 現行PLAN/CONTEXT D-04とこのカードは、原本保全後の工程差分除外を「最終化担当の後工程責務」と固定する。
3. チーム通常順はフェーズ合格→受入合格→最終化。未達ならgaps計画へ戻る。
4. したがって、注記と引継ぎだけの補完実装→品質再検証では工程差分が残り、同じgapsへ戻る。最終化へ到達せず循環する。
5. architectには受入基準の変更・未達をpassedへ変換・最終化の前倒し予約・Builderへの責務移動の権限がない。最新の進捗例外承認も、受入未達で最終化へ進む承認ではない。

## PM決定後に作る限定補完の内容（未作成・未検査）
- 06-01と合格済みREADME1行を保持し、別の補完PLANに残件のみを書く。GSD状態修復・全面再計画はしない。
- OpenSpec1.2に「依頼者の判断により対象外（2026-11-24T21:20+09:00）」を明記し、proposal/design/tasksの旧範囲にも縮小判断を注記する。2.1は独立品質の2条件文字判断だけにし、条件2未達中はチェックしない。
- 必要な仕様・計画・検査・品質文字原本の標準添付ID/保存名/SHA-256の索引を確定し、全必要原本を照合してから除外する。
- PMが承認した時点・担当で、この依頼の変更済み工程ファイルを基準branch内容へ戻し、新規工程ファイルを最終treeから外す。過去の原本を無差別削除しない。sync/archiveで新たに生じる工程差分も同じ原本保全・最終全差分確認の対象。
- 最終化中のarchiveより前に、1.2対象外・2.1未完・未完taskの扱いと原本保全を最終化担当へ渡す。CLIの未完警告を実行成功やtask完了の証拠に変えない。
- 品質は最終head/実PR base/merge-baseを固定し、工程資料を除外しない全name-statusとREADME patchを文字で判定・添付する。全差分がREADME.md 1件でない間は条件2未達。品質が書く最終証拠もPRの追加差分にしない形で標準添付保全する。
- PMは文字添付をread_fileで読み、両条件達成後に初めて受入を判断する。品質の代筆や先行合格はしない。
- 3形式実行・pytest・実入力/出力/ログ・新試験・quality runbookは対象外。画像0枚、理由はREADMEの文字1行変更でUI/製品実行検証が対象外のため。画像/zip不要。

これは補完PLANの完成や品質合格ではない。PM決定前に実行可能と偽って割振りを解放せず、同一範囲の再計画を繰り返さないための未決判断の文字原本である。
