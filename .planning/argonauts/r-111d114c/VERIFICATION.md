# VERIFICATION — r-111d114c（light 確認）

- カード: t_3f60f097（品質）／流れ: light
- PR: ToR-O3/argonauts-uat-20261114-public#16（OPEN, draft, 同一repo）
- 確認した対象head: 6aacf1e4aa0bc820e7e8cdbe30865c10a2927c9b
  （HEAD = origin/argonauts/r-111d114c = PR headRefOid）
- base: v112-b（baseRefOid c0a53a73011e377c611d96e03e6bf5897cae64de）
- 依頼者の判断コメント（argonauts: 依頼者の判断）: 受付 t_07ca7f9a に無し
- 本記録だけを保存するcommitは、確認対象headとは別（下記の後に作るcommit）

## 範囲
製品の変更：README.md（+1行）。工程の文書：1件（.planning/argonauts/r-111d114c/PLAN.md。判定の対象外）
- 全差分 `git diff --name-status -z --find-renames origin/v112-b...HEAD`: `A .planning/argonauts/r-111d114c/PLAN.md`, `M README.md`
- 危険なパス：触れていない（README.md・.planning/ のみ）
- `.github/workflows/` の変更：無し。baseに未取込みの差分：無し

## 受入条件ごとの実行と結果

| # | 条件（原文） | 実行 | 結果 |
|---|---|---|---|
| 1 | README.md の使い方の説明に、--top 3 を指定した実行例を1つ足す | `git diff origin/v112-b...HEAD -- README.md` と README.md 9-17行の読取り | 「wordfreq の実行」の使い方コードブロックに `python -m wordfreq README.md --top 3` が1行だけ追加。合格 |
| 1' | 例が実際に動く | `python3 -m wordfreq README.md --top 3` | exit 0、出力3行（`13 html` / `9 wordfreq` / `9 top`）。合格 |
| 2 | 変えるのは README.md だけ | 上記の全差分 | 製品ファイルは README.md のみ。合格 |
| 3 | 未決事項は無い | 受付のコメント・本文の確認 | 未決事項の記載なし。合格 |

## 既存の試験・CI
- `uv run --with pytest python -m pytest -q`: 702 passed（169.21s）
- 必須チェック（rules/branches/v112-b 全ページ）: `pytest`, `argonauts/quality`
- `pytest`（Actions job, head 6aacf1e）: run 45477267478 / 45477209113 とも completed/success
- commit status: 無し（argonauts/quality は本確認の合格後に付ける）

## 判定
passed（必須の指摘なし。提案なし）
