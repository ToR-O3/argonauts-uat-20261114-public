# VERIFICATION — r-c4f997f3（light／確認）

- 確認カード: t_ec4394e2（品質）
- 対象: ToR-O3/argonauts-uat-20261114-public#36、作業branch `argonauts/r-c4f997f3`
- 確認したhead: ea0e33e747527e1877b4ceaeffe16ad25b6d8338（ローカルHEAD・origin・PRのheadが一致、OPEN・draft・同じrepo）
- 基準: origin/v112-a
- 依頼者判断: ［受付］t_0236c4e3 に「argonauts: 依頼者の判断」のコメントは無し（受付時の受入条件をそのまま使う）

## 受入条件ごとの実行と結果

### 1. README.md の「wordfreq の実行」のコード例に `python -m wordfreq input.txt --top 3 --format text` の1行を足す
- `git diff origin/v112-a...HEAD -- README.md` → `## wordfreq の実行` の ```sh ブロック内（16行目、`--top 3 --format json` の直後）に1行追加だけ。削除行なし。
- `rg -F -x -c -- 'python -m wordfreq input.txt --top 3 --format text' README.md` → 1
- 追加した行を実際に実行（UTF-8のサンプル入力、Python 3.12）:
  `python -m wordfreq <sample>/input.txt --top 3 --format text` → exit 0、出力 `4\tapple\n3\tbanana\n2\tcherry\n`（READMEの「text は `<count>\t<word>\n`」の説明どおり、上位3件）
- 結果: 合格

### 2. 変えるのは README.md だけ
- `git diff --name-status -z --find-renames origin/v112-a...HEAD`:
  - `M README.md`
  - `A .planning/argonauts/r-c4f997f3/PLAN.md`
- 製品の変更：README.md（1行追加）。工程の文書：1件（PLAN.md。この確認でVERIFICATION.mdを追加し2件、判定の対象外）
- 結果: 合格

## 既存試験・CI
- `uv run --python 3.12 --no-project --with pytest python -m pytest -q` → 702 passed in 224.88s（リポジトリCI `.github/workflows/pytest.yml` と同じ Python 3.12・pytest）
- `git diff --check origin/v112-a...HEAD` → exit 0
- GitHub Actions（head ea0e33e）: pytest の run 2件とも completed/success

## 危険なパス
- 全差分で照合: 触れたパスは README.md と .planning/ 配下のみ。危険なパス（/.github/、CODEOWNERS、依存定義ファイルなど）には触れていない。`.github/workflows/` の変更なし。

## 画面
- 画面のある変更ではないため、画像の確認はしていない（0枚）。

## 判定
- verdict: passed（必須の指摘なし、提案なし）
- 合格の印（argonauts/quality）はこの工程では付けない（最終化のレビューで付ける）。

## 今回の学び
- 特になし（実装レビューの学び「回帰試験はCIのPython 3.12・pytestで、全702件に約4分かかる」を再確認）
