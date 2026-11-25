# VERIFICATION r-619abd39（light 確認）

- 確認カード: t_53748cce / 流れ: light / 品質: argonauts-uat-quality
- PR: ToR-O3/argonauts-uat-20261114-public#21（OPEN、draft、同じrepo）
- 確認対象の製品head: 4fba0a89a92b5f49cbe1149d24f2de5b9ea12fa0（= origin/argonauts/r-619abd39 = PR headRefOid）
- 比較起点: origin/v112-b 423e4bc6de73e7620e5541df71e8ec1387d36742（PR baseRefOid と同じ）
- 依頼者の判断: 受付 t_24354840 の「argonauts: 依頼者の判断」日時 2026-11-25T01:39:51.674303+00:00
  原文「wordfreq は、テキストに出てくる単語の回数を数えて一覧にする小さなコマンドです。」の1行にする。
  （これより新しい依頼者判断は無い）

## 受入条件1: 先頭の説明文が指定文と完全一致（引用括弧なし）
- `sed -n 3p README.md | grep -qxF 'wordfreq は、テキストに出てくる単語の回数を数えて一覧にする小さなコマンドです。'` → 終了コード 0
- PLANのコマンド `{ read title; read blank; read description; test "$description" = '<指定文>'; } < README.md` → 終了コード 0
- `grep -nvE '^(#|$)' README.md | head -1` → `3:wordfreq は、…コマンドです。`（見出しと空行の次の最初の本文行＝先頭の説明文）
- `cat -A` で行末は `$` のみ（末尾空白・CRなし）、「」の括弧なし
- 判定: 合格

## 受入条件2: README.mdの他の内容と他の製品ファイルを変えない
- `git diff --name-status -z --find-renames origin/v112-b...HEAD`（全件）:
  - `A .planning/argonauts/r-619abd39/PLAN.md`
  - `M README.md`
- `git diff --numstat`: README.md 1/1、PLAN.md 36/0
- README.mdの差分（-U0）は3行目だけ:
  - `-Argonauts v1.10 acceptance test repository.`
  - `+wordfreq は、テキストに出てくる単語の回数を数えて一覧にする小さなコマンドです。`
- `git diff --check origin/v112-b...HEAD` → 終了コード 0
- 製品の変更：README.md（3行目の1行置換）。工程の文書：1件（PLAN.md、判定の対象外）。この記録を加えると2件。
- 改名：無し
- 判定: 合格

## 既存試験
- `uv run --no-project --with pytest python -m pytest -q` → 702 passed in 184.07s（試験後 `git status --porcelain` は空）

## CI（1回だけ読取り、待たない）
- 必須一覧（rules/branches/v112-b、全ページ）: argonauts/quality、pytest → 品質を除くと pytest
- Actions（head 4fba0a8）: run 45529114693（pull_request）job pytest completed/success、run 45529073596（push）job pytest completed/success
- commit status: 4fba0a8 には無し
- 受付と本カードにCI失敗のコメントは無し

## 危険なパスと方針
- 全差分の旧・新パスを固定入力の危険なパスと照合: 該当無し（.github/、CODEOWNERS、依存・lock・pyproject.toml・Docker・infra・migrations・auth・security に触れていない）
- `.github/workflows/` の変更: 無し
- 数えるファイル数: 1（全体2、この記録の後3）。大きな変更の閾値100未満
- 方針 smart: 危険の印無し・危険なパス無し・小さい変更なので、最終確認で予約の対象になる見込み。
  PRはdraftで最終化前のため、この確認では自動マージを予約しない（予約は最終確認で決める）。autoMergeRequest: null
- rulesetの pull_request 規則は require_code_owner_review: false（GitHubの強制は効いていない。守りはガードのみ）

## 結論
- 判定: 合格（受入条件1・2とも満たす。既存試験・必須CIも成功）
- この記録だけを .planning/ に追加したcommitを依頼branchへpushし、そのheadに argonauts/quality を付ける。
  確認した製品のheadは 4fba0a8。記録のcommitの差分は .planning/ の下だけ。
