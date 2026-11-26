# VERIFICATION — r-34320c15（確認・light）

- 確認カード: t_0d655351（品質）
- 対象: ToR-O3/argonauts-uat-20261114-public#31（OPEN・draft・同じrepo）
- 確認したhead: 9fd345838ea0553c1ad4de7be155288337adb905（= origin/argonauts/r-34320c15 = PRのheadRefOid）
- 基準: origin/v112-a（HEADの祖先。取込み不要）
- 依頼者の判断コメント: 受付に無し（受付の受入条件の原文で判定）

## 受入条件ごとの実行と結果

### 1. 「wordfreq の実行」のコード例に `python -m wordfreq input.txt --top 5` の1行を足す
- `git diff origin/v112-a...HEAD -- README.md`: `## wordfreq の実行` 直下の ```sh ブロック内、`python -m wordfreq input.txt` の次に `+python -m wordfreq input.txt --top 5` の1行追加のみ。削除行なし。
- `git show HEAD:README.md | rg -F -x -c -- 'python -m wordfreq input.txt --top 5'` → 1
- 同じ検査を origin/v112-a の README.md に → 0（今回追加された行）
- 例のとおり実行: `python3.12 -m wordfreq <一時の入力.txt> --top 5` → exit 0、5行（`4 apple`、`3 banana`、`2 cherry`、`2 egg`、`1 date`）。回数の多い順で上位5件。
- 結果: 合格

### 2. 変えるのは README.md だけ
- `git diff --name-status origin/v112-a...HEAD`:
  - `M README.md`
  - `A .planning/argonauts/r-34320c15/PLAN.md`
- 製品の変更：README.md のみ。工程の文書：1件（.planning/argonauts/r-34320c15/PLAN.md、判定の対象外）。本記録の追加で2件。
- 危険なパス：触れていない。`.github/workflows/` の変更なし。
- 結果: 合格

### 3. 未決事項は無い
- 受付・計画とも未決事項の記載なし。確認中にも新たな問いは無い。
- 結果: 合格

## 既存の試験とCI
- CIと同じ Python 3.12 + pytest（`uv run --no-project --python 3.12 --with pytest python -m pytest -q`）→ 702 passed（189.70s）。
- GitHub Actions（head 9fd3458）: pytest（push）success、pytest（pull_request）success。commit status は未報告（argonauts/quality は本工程では付けない）。

## 指摘
- 必須: 無し
- 提案: 無し

## 今回の学び
- 特になし

## 判定
- verdict: passed
