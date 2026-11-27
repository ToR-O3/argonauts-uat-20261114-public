# 確認の記録 r-9c690425（流れ: light）

- 確認カード: t_b246587a（品質）
- 対象: ToR-O3/argonauts-uat-20261114-public#42（OPEN・draft・同じrepo、base v112-a）
- 確認したhead: 6d9026367c74a2a3886fb5838a289b1cb1a54bfe（ローカルHEAD = origin/argonauts/r-9c690425 = PRのheadRefOid）
- 依頼者の判断コメント（argonauts: 依頼者の判断）: 無し

## 受入条件ごとの実行と結果

### 1. README.md の「wordfreq の実行」のコード例に `python -m wordfreq input.txt --top 6` の1行を足す
- `git show HEAD:README.md | rg -F -x -c -- 'python -m wordfreq input.txt --top 6'` → `1`（完全一致1件）
- 基準 `git show origin/v112-a:README.md | rg -F -x -c -- (同じ行)` → 一致なし（0件。今回の追加）
- 位置: README.md 5行目の見出し「## wordfreq の実行」直下、9〜21行目の ```sh コード例の12行目（`--top 5` の直後）
- 既存例の保持: `git diff --numstat origin/v112-a...HEAD -- README.md` → `1 0`（追加1行・削除0行）。既存の例10行はすべて残る
- 実コマンド: 一時の入力ファイル（UTF-8、18語）で `python3 -m wordfreq <input.txt> --top 6` → exit 0、6行出力
  ```
  4	apple
  3	banana
  3	fig
  2	cherry
  2	date
  2	egg
  ```
- 判定: 合格

### 2. 変えるのは README.md だけ
- `git diff --name-status origin/v112-a...HEAD`
  - `M README.md`
  - `A .planning/argonauts/r-9c690425/PLAN.md`
- 製品の変更：README.md だけ。工程の文書：1件（PLAN.md、判定の対象外。本記録の追加で2件）
- 危険なパス（/.github/、CODEOWNERS、依存定義、Dockerfile 等）: 触れていない。`.github/workflows/` の変更なし
- 判定: 合格

## 既存の試験とCI
- `uv run --no-project --python 3.12 --with pytest python -m pytest -q` → 702 passed（CIの pytest.yml と同じ Python 3.12）
- head 6d90263 の Actions: pytest run 45968830474・45968785313 とも completed / success（1回読み取り、待たない）
- 受付カードに CI 失敗コメント無し

## 結論
- verdict: passed（必須の指摘なし、提案なし）
- 品質の印（argonauts/quality）は付けていない。最終head への印は後続の最終確認で付ける
- 今回の学び: 特になし
