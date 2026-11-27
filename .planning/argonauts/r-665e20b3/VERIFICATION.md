# 確認結果 — README.md の `--top 6` 実行例

- 判定：合格（受付 r-665e20b3、light）
- 対象：ToR-O3/argonauts-uat-20261114-public#48、`argonauts/r-665e20b3` → `main`
- 実行確認した head：`d1d2e741e9fd288a756cc7a9400328cda35e14e1`（確認記録を追加するコミットの親）
- 比較元：`9bd1c0f79dfba4048fcb2876c3924b81b7d54e0e`
- 受付の依頼者判断：追加コメントなし。受付の受入条件を適用し、PR の掲載範囲に別の指定はないため工程文書を同じ PR に含める。

## 受入条件ごとの結果

1. **使い方に実行例を1件追加 — 合格。** README.md の「wordfreq の実行」のコードブロックで `--top 4` の直後に `python -m wordfreq input.txt --top 6` が1行だけ追加された。`git show HEAD:README.md | rg -F -x -c -- 'python -m wordfreq input.txt --top 6'` は `1`。README.md の既存行の変更・削除なし。
2. **製品の変更は README.md のみ — 合格。** `git diff --name-status --find-renames <比較元>...HEAD` の全件は `M README.md` と `A .planning/argonauts/r-665e20b3/PLAN.md`。改名なし、`git diff --check` は終了 0。製品の変更：README.md のみ。工程の文書：1件（判定の対象外）。この確認記録を収録した PR では工程の文書は2件。全差分で危険なパスへの変更なし。
3. **掲載例が動き、出力は最大6件 — 合格。** Python 3.12 の環境で、7種類の語を含む UTF-8 の一時入力 `input.txt` を使った。掲載例 `python -m wordfreq input.txt --top 6` は終了 0、下記6行。同じ入力で `python -m wordfreq input.txt --top 7` は終了 0、7行目に `1<TAB>melon` が加わった。確認専用の入力は削除済み。

入力：`kiwi pear banana apple grape mango melon kiwi pear banana kiwi pear kiwi`

```text
4	kiwi
3	pear
2	banana
1	apple
1	grape
1	mango
```

## 既存試験と引継ぎ

- `uv run --no-project --python 3.12 --with pytest python -m pytest tests/test_cli.py`：358件合格（Python 3.12.15）。
- 実行確認した同じ head の GitHub Actions `pull_request` run `46019229468`：`pytest` job は `success`。
- CLI の文書変更のみ。画面検証は対象外。
- PR は下書き。マージ可否の判断と予約は後続の最終確認で行う。
- 学び：特になし。
