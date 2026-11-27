# VERIFICATION — r-59788e5d（light・確認）

- カード: t_c6ea5c37（品質）／入力: t_34e2b00c（PLANレビュー合格）、t_d508c8e7（PLAN.md）、t_9e115029（受付）
- 対象: ToR-O3/argonauts-uat-20261114-public#46（OPEN・draft・同じrepo、base v112-a）
- 確認したhead: 4c6eb68ce03ef57fb18aef0c9ebaa128354ef200（origin/argonauts/r-59788e5d・PRのheadRefOid・手元HEADが一致）
- 依頼者の判断: 受付に `argonauts: 依頼者の判断` のコメントは無い（受入条件は受付の原文どおり）

## 範囲

製品の変更：README.md（+1/-0）。工程の文書：1件（.planning/argonauts/r-59788e5d/PLAN.md、判定の対象外）。本記録の追加で2件になる。
危険なパス：触れていない（`git diff --name-status -z --find-renames origin/v112-a...HEAD` の全件は `A .planning/argonauts/r-59788e5d/PLAN.md`、`M README.md` のみ）。`.github/workflows/` の変更無し。

## 受入条件ごとの実行と結果

### 1. README.md の「wordfreq の実行」のコード例に `python -m wordfreq input.txt --top 8` の1行を足す

- `rg -n '^#' README.md` → 5行目 `## wordfreq の実行`、次の見出しは36行目。
- `rg -n -C4 'wordfreq input.txt' README.md` → 9〜23行目の ```sh ブロック内、14行目に `python -m wordfreq input.txt --top 8`（`--top 7` の直後）。
- `rg -F -x -c -- 'python -m wordfreq input.txt --top 8' README.md` → `1`（完全一致1件、重複無し）。
- `git diff origin/v112-a...HEAD -- README.md` → 追加1行だけ。既存の例は削除・変更無し。
- 実行：`python3 -m wordfreq <scratchの10行のUTF-8入力> --top 8` → 8行（apple 10 … honeydew 3）を出力、exit 0。
- 判定：合格

### 2. 変えるのは README.md だけ

- 全件差分で、工程文書の場所（.planning, openspec, _bmad-output, .compound-engineering, docs/solutions）以外の変更は README.md のみ。
- 判定：合格

## CI（同じheadを1回読取り、待たない）

- Actions `pytest`（pull_request, run 45990673341）: completed / success
- Actions `pytest`（push, run 45990622867）: completed / success
- commit status: 無し（argonauts/quality は最終確認で付ける）
- 試験の全件は本確認では再実行していない。親のPLANレビュー（t_34e2b00c）で Python 3.12＋pytest 702件合格の記録があり、同じheadのCIも成功。

## 結論

verdict: passed（受入条件2件とも直接実行で満たした）。
今回の学び：特になし。

## 最終化の再検証（t_16580b70）

- 検証記録commit a32a74757fa9f10c071b2e687fa547669d5e7f38 のREADMEを再確認。READMEの内容は確認時の製品head 4c6eb68ce03ef57fb18aef0c9ebaa128354ef200 と同一。
- `git merge --no-edit origin/v112-a` → Already up to date. baseのworkflow差分無し。
- `rg -F -x -c -- 'python -m wordfreq input.txt --top 8' README.md` → 1。節内の既存top7の直後、README全差分は指定の1行追加のみ。
- NUL区切りの全件差分 → README.md、今回のPLAN.md、VERIFICATION.mdのみ。危険なパスの変更無し。
- `git diff --check` → exit 0。
- `uv run --python 3.12 --with pytest python -m pytest tests/test_cli.py` → Python 3.12.15、358 passed in 14.98s、exit 0（CLI回帰を選択して再実行）。生成されたuv.lockとegg-infoは削除し、製品差分に含めない。
- 実CLI: `python3 -m wordfreq <scratch>/r-59788e5d-final-input.txt --top 8` → exit 0。入力は apple×10、banana×9、cherry×8、date×7、elderberry×6、fig×5、grape×4、honeydew×3、kiwi×2、lemon×1。出力は順に `10\tapple`、`9\tbanana`、`8\tcherry`、`7\tdate`、`6\telderberry`、`5\tfig`、`4\tgrape`、`3\thoneydew` の8行で期待値どおり。
- `gh pr ready argonauts/r-59788e5d` → 成功。読み戻しで同じPR #46がOPEN・isDraft=falseであることを確認してから、本記録をcommit・pushする。
- OpenSpec同期・archiveおよび新規の工程文書生成は行わない。今回の学びは空のまま引き継ぐ。最終headの品質判定と予約判断は同じカードの品質レビューへ渡す。
