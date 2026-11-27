# VERIFICATION — r-14f949ea（light の確認）

- 確認カード: t_6268d693（品質）
- 対象: ToR-O3/argonauts-uat-20261114-public#44（OPEN・draft・同じrepo、base v112-a）
- 確認対象head: 0571631c6a2352f4cdd7559c63e6aba09e08ecf7（HEAD＝origin/argonauts/r-14f949ea＝PRのheadRefOid）
- baseとの差: origin/v112-a に未取込みのcommitは0件。baseのworkflow変更なし。
- 依頼者の判断コメント: 受付（t_df84827b）に無し。

## 範囲

製品の変更：README.md（+1/-0）。工程の文書：1件（.planning/argonauts/r-14f949ea/PLAN.md、判定の対象外）。
危険なパス：触れていない（全差分 `git diff --numstat origin/v112-a...HEAD` は上記2件だけ）。

## 受入条件ごとの実行と結果

1. 「wordfreq の実行」のコード例に `python -m wordfreq input.txt --top 7` を1行足す — **合格**
   - `rg -F -x -c -- 'python -m wordfreq input.txt --top 7' README.md` → 1
   - 位置: 見出し「## wordfreq の実行」直下の ```sh ブロック内、`--top 6` の直後。
   - 既存例の保持: README.md の差分は追加1行・削除0行。既存の11行はそのまま。
   - 実CLI: 8種類の語を回数8〜1で並べた一時ファイル input.txt を作り、
     `uv run --no-project --python 3.12 python -m wordfreq input.txt --top 7`
     → 7行（8 alpha … 2 eta）、exit 0。上位7件で8件目（theta）は出ない。一時ファイルは確認後に削除。
2. 変えるのは README.md だけ — **合格**（範囲の節のとおり、製品ファイルは README.md のみ）
3. 未決事項は無い — **合格**（受付・計画とも未決事項なし。追加の判断は不要）

## 既存の試験とCI

- `uv run --no-project --python 3.12 --with pytest python -m pytest -q` → 702 passed（155s、CIと同じPython 3.12）
- Actions（head 0571631）: pytest run 45985091971・45985046045 とも completed/success

## 判定

passed。必須の指摘なし、提案なし。最終の品質の印はこの工程では付けない（最終化で付ける）。

## 今回の学び

特になし。
