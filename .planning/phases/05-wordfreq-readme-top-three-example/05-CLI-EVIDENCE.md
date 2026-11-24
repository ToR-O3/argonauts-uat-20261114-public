# Phase 5 — CLI 検証証拠

- 依頼 `r-864b299c`、PR ToR-O3/argonauts-uat-20261114-public#12。
- クリーンな実行対象 / 当カードの `start_sha`: `14e6df0700bb19a9e54a0d1b32e0f16f6eced634`。PR head・取得した依頼ブランチ・ローカル HEAD が一致。以下の正常系は文書だけを保存した後続コミットの結果ではない。
- PLAN の製品比較基点: `5528aa47cca27a93a6732e914710f2772118a572`。
- 画像確認0枚（画面変更なし）。受付カードに CI 失敗コメントなし。GitHub CI 自体は未確認。

## 受入条件

| 条件 | 判定・証拠 |
|---|---|
| 有効な上位3件の例が1つ | README 13行目、PLAN 指定の検証結果 `placement and scope: PASS`、実 CLI 終了0・JSON 3件。 |
| 既存例と同じ書式。既存例は保持 | `--top 2` JSON 例直後の既存 `sh` フェンス内。README 全バイトを基点への1行挿入として照合。 |
| 製品の差分は README だけ | `git diff --numstat origin/main...HEAD -- README.md` は `1  0  README.md`。製品 CLI・既存試験・CI ワークフローに差分なし。固定基点で許容する OpenSpec の差分は 1.1 のチェック欄のみ。 |

## 独立実行（クリーンな実装 head）

```text
$ python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py
base: 5528aa47cca27a93a6732e914710f2772118a572
HEAD: 14e6df0700bb19a9e54a0d1b32e0f16f6eced634
target: clean HEAD
untracked: []
placement and scope: PASS
published: python -m wordfreq input.txt --top 3 --format json
argv: ['python', '-m', 'wordfreq', '/home/Yuki/.hermes/profiles/argo-dev/cache/scratch/wordfreq-top-three-434r41l3/input.txt', '--top', '3', '--format', 'json']
input (UTF-8): delta gamma beta alpha beta gamma alpha beta alpha alpha
CLI: starting
CLI exit: 0
stdout: b'[{"word": "alpha", "count": 4}, {"word": "beta", "count": 3}, {"word": "gamma", "count": 2}]\n'
stderr: b''
verification: PASS (exit 0)
```

実行後、一時入力が残っていないことを `test ! -e`（終了0）で確認。既存の全回帰試験 `env -u GIT_INDEX_FILE /usr/bin/python3 -m pytest -q --tb=short` は終了0（`702 passed in 186.69s`）。`git diff --check origin/main...HEAD` は終了0。OpenSpec strict は終了0。

### 固定基点からの全変更パス

クリーン実行の worktree と index は同じ一覧。未追跡なし。

```text
M .planning/INGEST-CONFLICTS.md
M .planning/REQUIREMENTS.md
M .planning/ROADMAP.md
M .planning/STATE.md
A .planning/argonauts/r-864b299c-learnings.md
A .planning/argonauts/r-864b299c-manifest.yaml
A .planning/argonauts/r-864b299c-prd.md
M .planning/intel/SYNTHESIS.md
A .planning/intel/classifications/brief-wordfreq-top-three-3adfe49d.json
A .planning/intel/classifications/prd-wordfreq-top-three-73325b60.json
A .planning/intel/classifications/proposal-4146fcc0.json
A .planning/intel/classifications/spec-67452c5a.json
A .planning/intel/classifications/tasks-e477c401.json
M .planning/intel/constraints.md
M .planning/intel/context.md
M .planning/intel/decisions.md
M .planning/intel/requirements.md
A .planning/phases/05-wordfreq-readme-top-three-example/.gitkeep
A .planning/phases/05-wordfreq-readme-top-three-example/05-01-PLAN.md
A .planning/phases/05-wordfreq-readme-top-three-example/05-01-SUMMARY.md
A .planning/phases/05-wordfreq-readme-top-three-example/05-CONTEXT.md
A .planning/phases/05-wordfreq-readme-top-three-example/05-PATTERNS.md
A .planning/phases/05-wordfreq-readme-top-three-example/05-RESEARCH.md
A .planning/phases/05-wordfreq-readme-top-three-example/05-VALIDATION.md
A .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py
M .planning/state.json
M README.md
M openspec/changes/r-864b299c-readme-top-three/tasks.md
```

````diff
diff --git a/README.md b/README.md
index 486b319..1809202 100644
--- a/README.md
+++ b/README.md
@@ -10,6 +10,7 @@ Argonauts v1.10 acceptance test repository.
 python -m wordfreq input.txt
 python -m wordfreq input.txt --min-count 2 --top 1 --format json
 python -m wordfreq input.txt --top 2 --format json
+python -m wordfreq input.txt --top 3 --format json
 python -m wordfreq input.txt --format html
 python -m wordfreq input.txt --format html > result.html
 ```
````

## ギャップ再現（同じ HEAD 上の作業ツリー）

同じ検証コマンドを実行。製品は変更していない。

```text
未追跡のまま:
CLI: not run
verification: FAIL (exit 1): out-of-scope untracked paths: ['.planning/argonauts/t_40ba151e/openspec-verify.md', '.planning/phases/05-wordfreq-readme-top-three-example/05-SECURITY.md']

上の2ファイルを stage:
CLI: not run
verification: FAIL (exit 1): out-of-scope change: '.planning/argonauts/t_40ba151e/openspec-verify.md' (b'A')
```

`verify_readme_top_three.py:19–43,118–138` の完全一致リストに必須報告2件がないため。調査時の stage は解除済み。クリーンな実装 head での正常系は利用者の受入条件を満たすが、必須報告込みで同じ検証を再現できないため、GSD `gaps_found`。品質は検証器を修正していない。
