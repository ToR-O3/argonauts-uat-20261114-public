# VERIFICATION r-f32a8f4a（light 確認）

- 確認カード: t_7594d2aa（品質）／実装 t_cc7a0bee のレビュー合格後の後続確認
- 対象: ToR-O3/argonauts-uat-20261114-public#25、branch argonauts/r-f32a8f4a
- 確認したhead: 936f605ee1e9cc1b76e12d8feabbeb87347f43e7（= origin の作業branch = PR headRefOid、PR OPEN・draft・同一repo・base v112-a）
- 基準: origin/v112-a b73d4b4（headに含まれる。baseのworkflow差分なし）
- 判断日時: 2026-11-25T18:41:27.520592+00:00
- 依頼者の判断（原文）: 既存の行はそのままにして、代わりに python -m wordfreq input.txt --top 3 --format json の1行を、同じコード例に足してください。変えるのは README.md だけです。
  （元の条件の --min-count 3 の行の追加は、この判断で対象外。PM判断 t_ec3bd9ca で採用）

## 条件ごとの実行と結果

1. 「wordfreq の実行」のコード例に `python -m wordfreq input.txt --top 3 --format json` を1行追加 — 合格
   - `git diff origin/v112-a...HEAD -- README.md`: `+python -m wordfreq input.txt --top 3 --format json` の追加1行のみ、削除0（numstat 1/0）
   - 追加位置: README.md 14行目、見出し「## wordfreq の実行」直下の ```sh ブロック（9〜17行）の中
   - 追加したコマンドを実行（scratch の UTF-8 の input.txt、PYTHONPATH=worktree）:
     `[{"word": "apple", "count": 4}, {"word": "banana", "count": 3}, {"word": "cherry", "count": 2}]` exit 0
2. 既存の行はそのまま — 合格
   - `python -m wordfreq input.txt --min-count 3` の行は base と head で各1行（11行目）。README の削除行は0
   - 同じコマンドを実行: `4 apple` / `3 banana`、exit 0
3. 変えるのは README.md だけ — 合格
   - `git diff --name-status origin/v112-a...HEAD`: `M README.md`、`A .planning/argonauts/r-f32a8f4a/PLAN.md`
   - 製品の変更：README.md の1行追加のみ。工程の文書：1件（.planning/ の PLAN.md、判定の対象外）。この記録を足すと2件
4. 既存の試験とCI — 合格
   - `uv run --no-project --with pytest python -m pytest -q`: 702 passed（187秒）
   - `git diff --check origin/v112-a...HEAD`: exit 0
   - head 936f605 の Actions: pytest run 45679410613 と 45679459838 はどちらも completed/success
   - 受付と確認カードに、CIの失敗コメントはない

## 危険なパス・安全

- 危険なパス（/.github/、CODEOWNERS、依存ファイル など）に触れていない。`.github/workflows/` の変更もない
- 秘密や個人情報は含まない

## 判定

passed。この記録を入れたcommit（.planning/ だけの変更、親は 936f605）に argonauts/quality=success を付ける。PR は draft のまま。最終化の後、品質がもう一度最終確認する

## 今回の学び

特になし
