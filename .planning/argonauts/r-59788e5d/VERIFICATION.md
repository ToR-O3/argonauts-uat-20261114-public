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
