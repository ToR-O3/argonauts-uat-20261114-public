# VERIFICATION — r-1633f4bd（light／確認）

- 確認カード: t_6fd54e26（品質）
- 対象: ToR-O3/argonauts-uat-20261114-public#38、作業branch `argonauts/r-1633f4bd`
- 確認したhead: e761f332a98b08f0c2cd02f9fa7b5bfd9aed64ed（ローカルHEAD・origin・PRのheadが一致、OPEN・draft・同じrepo）
- 基準: origin/v112-a（b723480、依頼branchに含まれ取込み不要）
- 依頼者判断: ［受付］t_eefd99c8 に「argonauts: 依頼者の判断」のコメントは無し（受付時の受入条件をそのまま使う）

## 受入条件ごとの実行と結果

### 1. README.md の「wordfreq の実行」のコード例に `python -m wordfreq input.txt --top 4 --format json` の1行を足す
- `git diff origin/v112-a...HEAD -- README.md` → `## wordfreq の実行` の ```sh ブロック内（16行目、`--top 3 --format json` の直後）に1行追加だけ。削除行なし。
- `rg -F -x -c -- 'python -m wordfreq input.txt --top 4 --format json' README.md` → 1
- 追加した行を実際に実行（scratchのUTF-8サンプル入力、Python 3.12、PYTHONPATH=worktree）:
  `python -m wordfreq input.txt --top 4 --format json` → exit 0、出力
  `[{"word": "elder", "count": 5}, {"word": "apple", "count": 4}, {"word": "banana", "count": 3}, {"word": "cherry", "count": 2}]`
  （5種類のうち上位4件、各要素は `word` と整数 `count`。READMEの説明どおり）
- 結果: 合格

### 2. 変えるのは README.md だけ
- `git diff --name-status -z --find-renames origin/v112-a...HEAD`:
  - `M README.md`
  - `A .planning/argonauts/r-1633f4bd/PLAN.md`
- 製品の変更：README.md（1行追加）。工程の文書：1件（PLAN.md。この確認でVERIFICATION.mdを追加し2件、判定の対象外）
- 結果: 合格

## 既存試験・CI
- `uv run --python 3.12 --no-project --with pytest python -m pytest -q` → 702 passed in 217.56s（リポジトリCI `.github/workflows/pytest.yml` と同じ Python 3.12・pytest）
- `git diff --check origin/v112-a...HEAD` → exit 0
- GitHub Actions（head e761f33）: pytest の run 2件とも completed/success

## 危険なパス
- 全差分で照合: 触れたパスは README.md と .planning/ 配下のみ。危険なパス（/.github/、CODEOWNERS、依存定義ファイルなど）には触れていない。`.github/workflows/` の変更なし。

## 画面
- 画面のある変更ではないため、画像の確認はしていない（0枚）。

## 判定
- verdict: passed（必須の指摘なし、提案なし）
- PLANとの差: PLANの回帰試験 `python3 -m unittest discover` はpytest関数を収集しないため、CIと同じpytestで確認した（受入条件への影響なし）。
- 合格の印（argonauts/quality）はこの工程では付けない（最終化の最終確認で付ける）。

## 今回の学び
- 特になし
