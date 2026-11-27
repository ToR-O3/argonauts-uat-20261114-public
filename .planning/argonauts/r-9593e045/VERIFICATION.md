# r-9593e045 確認（light）

- 確認カード: t_f96d93f1（品質）／実装 t_8c8a718f（品質レビュー完了済み）
- 対象: ToR-O3/argonauts-uat-20261114-public#43（OPEN・draft・同一repo）、base v112-b
- 確認したhead: 29fb681043be91b32573bd8403772084000ad526（= origin/argonauts/r-9593e045 = PR headRefOid）
- base: 142f336aa8b2dbc7212261bb868b24cd0762c838（取込み不要。base側の新しいcommitなし）
- 依頼者の判断（最新）: 2026-11-27T08:55:36.137717+00:00
  「①でお願いします。検証ツールの README の承認済みの値だけを新しい README.md に合わせて更新してください。検査を省いたり無効にしたりはしないでください。ほかのファイルは変えないでください。」
- 先の判断: 2026-11-27T08:44:38.046740+00:00（①の文言と位置を確定）

## 範囲
製品の変更：README.md（+1/-0）、tools/verify_wordfreq_max_count.py（承認ハッシュ1値の置換 +1/-1。最新の依頼者判断で許可）。
工程の文書：1件（.planning/argonauts/r-9593e045/PLAN.md。判定の対象外）＋本書。
危険なパス：触れていない（.github/・CODEOWNERS・依存ファイル等の変更なし）。workflowの変更なし。

## 受入条件ごとの実行と結果
1. 「wordfreq の実行」の節の最後に指定文を1行追加 — 合格
   - `git diff origin/v112-b...HEAD -- README.md`：追加1行「入力ファイルは UTF-8 で保存してください。」、削除0。
   - `git show HEAD:README.md | rg -F -x -c -- '<指定文>'` → 1。base側は0（exit1）。
   - read_file：README 52行目に追加。直前は節の下位節「### 出現回数の範囲を指定する」の末尾、直後53行目が次の同レベル見出し「## 部品の契約と検証状況」。節の最後に当たる。
2. それ以外のREADMEの内容とほかの製品ファイルは変更しない — 合格（最新判断の例外を含む）
   - `git diff --numstat origin/v112-b...HEAD`：README.md 1/0、tools/verify_wordfreq_max_count.py 1/1、PLAN.md 43/0 のみ。
   - ツール差分は approved 辞書の README.md の SHA-256 文字列1値だけ（e8c2bab… → 5a0ca56…）。検査の分岐・比較は不変。
   - `sha256sum README.md` → 5a0ca56634033c569765f1c3002962b15357b45821cbfd1245b86862a54aeb3a（承認値と一致）。
   - `git diff --check origin/v112-b...HEAD` → exit0。
3. ②は追加しない — 合格
   - `git show HEAD:README.md | rg -F -c -- '大きなファイルでは結果が出るまで時間がかかります'` → 0件（exit1）。

## 試験（CIと同じ Python 3.12 + pytest、uv）
- `PYTHONDONTWRITEBYTECODE=1 uv run --no-project --python 3.12 --with pytest python -m pytest -q -p no:cacheprovider tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only tests/test_max_count_verifier.py::test_scope_contract_cold_damage_rejected` → 8 passed、exit0（承認ハッシュ検査が有効なまま通る）。
- 全件 `... python -m pytest -q -p no:cacheprovider` → 1048 passed（275.95s）、exit0。実行後 `git status --porcelain` は空。

## CI（1回読取り、head 29fb681）
- Actions「pytest」push run 45971322468：completed/success。pull_request run 45971379310：completed/success。
- commit status：なし（argonauts/quality は最終確認で付ける。本工程では付けない）。

## 画面
画面の変更なし。画像の撮影・添付なし。

## 判定
verdict: passed（全受入条件を満たす）。
提案（記録のみ）：追加行と次の見出しの間に空行が無い。Markdownの表示上は段落として分かれ、問題なし。
今回の学び：特になし。
