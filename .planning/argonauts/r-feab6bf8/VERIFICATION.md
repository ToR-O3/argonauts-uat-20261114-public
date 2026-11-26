# 確認の記録 r-feab6bf8（light）

- 対象head: `f6cabb10e30acd4765ee0db8fb25f076891e901f`（origin/argonauts/r-feab6bf8 = PR headRefOid）
- PR: ToR-O3/argonauts-uat-20261114-public#37（OPEN, draft, 同じrepo）
- 比較の起点: `origin/v112-b` = merge-base `d2ee48b6c827628d937b0d6dfd14d26f43b86f39`
- 参照した依頼者の判断: 2026-11-26T18:11:30.266319+00:00（検査道具のREADME承認ハッシュも追従。検査の省略・無効化は不可）、
  2026-11-26T17:50:57.454849+00:00（READMEのコード例の完全一致の試験を追従）
- 確認者: 品質（argonauts-uat-quality）。結果: **合格**

## 製品の範囲
製品の変更：README.md（+1/-0）、tests/test_cli.py（+1/-0）、tools/verify_wordfreq_max_count.py（+1/-1）。
工程の文書：1件（.planning/argonauts/r-feab6bf8/PLAN.md。判定の対象外。本書を加えて2件）。
tests/test_cli.py と tools/… の変更は、上の依頼者の判断で許された追従だけ。危険なパスには触れていない。

## 条件ごとの実行と結果
1. 「wordfreq の実行」のコード例に指定の1行を足す — 合格
   - `sed -n 1,25p README.md`：見出し `## wordfreq の実行` 直後の `sh` フェンス（9〜18行目）の15行目に
     `python -m wordfreq input.txt --min-count 3 --format json` がある。直前は既存の `--top 2 --format json`、直後は `--format html`。
   - `git show HEAD:README.md | rg -F -x -c -- '<指定行>'` → 1。基準では0件。アンカー行は基準で1件。
   - `git diff -U0 origin/v112-b...HEAD -- README.md` の追加・削除行は指定行の追加1行だけ（既存内容は保持）。
   - 実際に動かした: `uv run --no-project --python 3.12 python -m wordfreq <一時の入力> --min-count 3 --format json`
     → `[{"word": "a", "count": 4}, {"word": "c", "count": 3}]`、exit 0（3回以上の語だけがJSONで出る）。
2. 変えるのは README.md だけ（依頼者の判断による追従を除く） — 合格
   - `git diff --name-status origin/v112-b...HEAD`：A PLAN.md、M README.md、M tests/test_cli.py、M tools/verify_wordfreq_max_count.py。
   - tests/test_cli.py：`test_max_count_readme_example` の期待行に同じ1行を追加しただけ。
   - tools/verify_wordfreq_max_count.py：README.md の承認ハッシュ1行だけを `e8c2babf…9696` に差し替え。
     `sha256sum README.md` = `e8c2babfe5371cd4cbce3fe5f67d7e5887a236fd59eedb91b3c77d696ccb9696` と一致。検査処理そのものは不変。
   - `git ls-files --others --exclude-standard` → 0件。`git diff --check` → exit 0。
3. 未決事項は無い — 合格（受付・本カードの最新の依頼者判断を再読。新しい判断の要求は無い）

## 試験
- `uv run --no-project --python 3.12 --with pytest python -m pytest -q tests/test_cli.py::test_max_count_readme_example tests/test_max_count_verifier.py` → 55 passed
- `uv run --no-project --python 3.12 --with pytest python -m pytest -q`（CIと同じ全件、Python 3.12）→ 1048 passed in 295.92s
- CI（Actions, head f6cabb1）: pytest run 45875597234・45875591140 ともに completed/success

## PLANとの差
- PLANは一時の試験スクリプトでのRED/GREENを求めるが、品質の手順は新しい試験道具を作らないため、同じ点を git・rg・既存試験で直接確かめた（受入条件の確認には影響なし。提案扱い）。
- 画面の変更は無いので画像の証拠は無し。

## 学び
特になし
