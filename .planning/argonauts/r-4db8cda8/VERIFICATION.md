# 確認記録 — r-4db8cda8

- 対象: ToR-O3/argonauts-uat-20261114-public#41、`argonauts/r-4db8cda8`
- 検証した head: `5adc256358dda0653d2290a4220700892c60f23e`（PR・依頼branch・作業場所で一致）。この記録を追加するコミットとは区別する。
- 比較した `main`: `7b60e557975d8ffcb96aefcfa50205c4a35903be`
- 受付 t_43578b68 に追加の依頼者判断コメントなし。受付の受入条件を使用。PLAN と受入条件に判定上の差はない。

## 受入条件と結果

1. **README.md の使い方に `--top 4` の実行例を1件追加 — 合格。** `git diff origin/main...HEAD -- README.md` で「wordfreq の実行」の `--top 2` の直後に下記の1行だけを追加し、削除がないことを確認。完全一致は比較元で0件、対象で1件。
2. **製品の変更は README.md のみ — 合格。** `git diff --name-status -z --find-renames origin/main...HEAD` で全件を確認。改名なし。`git diff --check origin/main...HEAD` は終了コード0。

製品の変更：`README.md`（1行追加、削除なし）。工程の文書：1件（判定の対象外、`PLAN.md`。検証対象head時点、この記録の追加後は2件）。全差分に指定の危険なパスなし。

## 掲載コマンドの実行

`input.txt` に `kiwi pear banana apple melon kiwi pear banana apple kiwi pear banana kiwi pear kiwi` を1行入れ、リポジトリ直下で掲載例 `python -m wordfreq input.txt --top 4` を実行（Python 3.14.9）。終了コード0、標準出力は次の4行。上限なしの `python -m wordfreq input.txt` ではこれに続き `1<TAB>melon` が出た。検証用入力は削除済み。

```text
5	kiwi
4	pear
3	banana
2	apple
```

## 既存試験とCI

- CI指定と同じ Python 3.12 で `uv run --no-project --python 3.12 --with pytest python -m pytest tests/test_cli.py` は358件合格、同環境の `python -m pytest` は全387件合格。
- 検証対象headの必須 `pytest` は GitHub Actions の pull_request（45960077374）と push（45960035078）の両方で success。画面の変更なし。
- 学び：特になし。
