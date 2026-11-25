# 確認の記録（light）r-2a4d03c5

- 確認カード: t_45f31ef8（品質）／流れ: light
- 対象: ToR-O3/argonauts-uat-20261114-public#27（OPEN・draft・同じrepo・base v112-a）
- 確認したhead: 96a106f9fcf110f65ec3266b00e358c13b6b1f03（= origin/argonauts/r-2a4d03c5 = PR headRefOid）
- 基準: origin/v112-a 3a34709bc8dcbd3edcc92fe92e807e5bfba37943
- 判断日時: 2026-11-25T19:37:56.185995+00:00（受付の最新の「argonauts: 依頼者の判断」。原文は置換文の全文）

## 受入条件ごとの実行と結果

### 1. README.md の1行目の見出しの次の段落が確定文と完全一致する
- `sed -n '1,5p' README.md | cat -A`：1行目 `# argonauts-uat public`、2行目 空行、3行目 確定文、4行目 空行。段落は3行目の1行だけ。
- `grep -Fxc 'テキストファイルの単語の出現回数を数えて、text・json・html の形式で出力する小さなコマンドラインツールです。' README.md` → `1`
- 行末の余分な空白や改行コードの違いなし（cat -A で `$` のみ）。
- 結果: 合格

### 2. README.md の他の箇所と他の製品ファイルは変更しない
- `git diff --name-status origin/v112-a...HEAD` → `M README.md`、`A .planning/argonauts/r-2a4d03c5/PLAN.md`
- `git diff origin/v112-a...HEAD -- README.md`：3行目の1行置換（旧「Argonauts v1.10 acceptance test repository.」）だけ。
- 製品の変更：README.md の冒頭説明段落1行のみ。工程の文書：1件（.planning/argonauts/r-2a4d03c5/PLAN.md、判定の対象外）。本記録の追加で2件になる。
- 危険なパスへの変更：無し（全差分で確認）。
- 結果: 合格

## 既存の試験とCI
- `git diff --check origin/v112-a...HEAD` → 終了コード0
- `uv run --no-project --with pytest python -m pytest -q` → 702 passed
- Actions（head 96a106f）: pytest 2件とも completed/success。commit status は無し。
- 受付とこのカードに CI 失敗のコメント無し。

## 判定
- verdict: passed（受入条件2件とも直接実行で満たす。必須の指摘なし）
- 新しい試験道具は作っていない。画面の変更は無いためブラウザー確認は対象外。
- 今回の学び: 特になし
