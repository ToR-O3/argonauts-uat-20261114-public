---
phase: 05-wordfreq-readme-top-three-example
plan: "02"
subsystem: testing
tags: [git, readme, wordfreq, verification]
requires:
  - phase: 05-wordfreq-readme-top-three-example
    provides: PLAN 05-01 の掲載例と CLI 検証
provides:
  - 報告のパスと Git 状態を限定する README 検証器
  - 独立 Git clone で動く差分判定の回帰ハーネス
affects: [独立フェーズ検証]
actuals:
  tokens: 5767
  tasks: 2
  commits: 2
tech-stack:
  added: []
  patterns: [全 Git 面の候補の和集合と通常ファイル型の照合]
key-files:
  created: [.planning/phases/05-wordfreq-readme-top-three-example/test_verify_readme_top_three_scope.py]
  modified: [.planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py]
key-decisions: []
requirements-completed: [REQ-22]
coverage:
  - id: D1
    description: "先行工程の報告を含むツリーの README 配置・製品差分と掲載 CLI"
    requirement: REQ-22
    verification:
      - kind: e2e
        ref: "python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "報告の三状態の受理と、範囲外・削除・型違いの拒否"
    requirement: REQ-22
    verification:
      - kind: integration
        ref: "python .planning/phases/05-wordfreq-readme-top-three-example/test_verify_readme_top_three_scope.py"
        status: pass
    human_judgment: false
duration: 418s
completed: 2026-11-24
status: complete
---

# Phase 5 Plan 02: README 検証器の報告パス誤判定を修正

**必須の品質報告と README の検証を両立させ、想定外の変更を CLI 実行前に拒否する。製品差分は先行 PLAN の README 1 行追加のまま。**

## Performance

- 開始 `2026-11-24T06:15:34Z`、実装検証終了 `2026-11-24T06:22:32Z`（418 秒）。タスク 2/2、実装ファイル 2。

## Accomplishments / Task Commits

1. `b3559b3699ba201c41c023db582c36f90f6d0356` — 05-02-01。旧検証器の実測 RED は verifier 終了1、`out-of-scope untracked paths` に既知2報告の両方、`CLI: not run`。独立 clone の HEAD/index に両方ともなく、status は `??`。修正後、同じケースと報告を含む依頼ツリーが verifier/CLI ともに終了0。
2. `ecb53ecc17195e913b698a89a5139e1bdd6ee87a` — 05-02-02。三状態と独立した負例を追加。初回行列は18件合格。親ディレクトリ symlink の追加試験では、初回は CLI 起動前に拒否したが親パスしか報告せず RED。報告候補の型検査を先に行い、対象報告パスと `symlink parent` を返すことを確認。拡張後は19件合格。

## 検証結果

比較基点 `5528aa47cca27a93a6732e914710f2772118a572`、隔離 clone の開始 `14e6df0700bb19a9e54a0d1b32e0f16f6eced634`、原本 `96c2df6c65af7060baca53fd80d573b3808d3728`、Builder 検証コードの最終コミット `ecb53ecc17195e913b698a89a5139e1bdd6ee87a`。この SUMMARY と GSD の後続コミットは工程記録のみ。行列で報告5件を追加する前に、既存の `05-VALIDATION.md` を `100644 → 100644` の追跡更新 `M` として別に準備した。追加 ID の報告内容はパス形状確認用のコピー。

| ケース | 観測された Git 状態・拒否理由 | verifier / CLI |
|---|---|---|
| untracked-previous | 既知2報告 `??`、HEAD/index なし | 0 / 0 |
| untracked | 報告5件 `??`、HEAD/index なし | 0 / 0 |
| staged | 報告5件 `A `、index 通常ファイル、HEAD なし | 0 / 0 |
| committed | 報告5件を基点から `A`、HEAD/index 通常ファイル、status 空 | 0 / 0 |
| tracked-change / tracked-fixture | `CONCEPTS.md` の worktree ` M` / 基点追跡 fixture の index `M ` | 各1 / 未実行 |
| unrelated-untracked | `.planning/unrelated.md` の `??` | 1 / 未実行 |
| wrong-id-length / wrong-id-case / extra-level / wrong-filename | 各 `??`、正規パスに完全一致しない | 各1 / 未実行 |
| report-in-base | 基点追跡済み OpenSpec 報告の `M ` | 1 / 未実行 |
| symlink-worktree / fixed-symlink | 新規の動的・固定報告パスを symlink に置換（`??`） | 各1 / 未実行 |
| symlink-index | `AT`、index 120000、worktree 通常ファイル | 1 / 未実行 |
| symlink-head | `T `、HEAD 120000、index/worktree 通常ファイル | 1 / 未実行 |
| fixed-mode-change | `05-VALIDATION.md` の ` M`、作業ツリー 100755 | 1 / 未実行 |
| symlink-parent | 追跡報告 ` D` と親 symlink `??`、リンク先には元報告が残る | 1 / 未実行 |
| staged-deletion | 正規報告 `D `、HEAD 100644・index/worktree なし。base→worktree・base→index・未追跡には不在。base→HEAD は A、HEAD→index は D | 1 / 未実行 |

正例はすべて `placement and scope: PASS`、stderr 空、stdout は `[{"word": "alpha", "count": 4}, {"word": "beta", "count": 3}, {"word": "gamma", "count": 2}]` と末尾改行1つ。掲載 argv の `input.txt` のみを外部一時ファイルへ置き換え、入力 `delta gamma beta alpha beta gamma alpha beta alpha alpha` を使用した。負例はすべて対象パスと理由を報告し、`CLI: not run`、起動出力なし。ハーネス全体終了0。

- D-01 / D-02: 実依頼ツリーで README の配置、製品差分 `+1/-0`、OpenSpec task 1.1 が既存のチェックだけであることを確認。作業開始 `486ae2f` から README・製品 CLI・既存試験・OpenSpec に差分なし。
- D-03: 同じ verifier が報告込みの依頼ツリーで終了0、実 CLI 終了0、上記の完全な JSON と空 stderr を確認。
- 既存回帰 `env -u GIT_INDEX_FILE /usr/bin/python3 -m pytest -q --tb=short`: 702 passed。OpenSpec 厳格検証: 1件合格、指摘0。

## Deviations from Plan / Issues Encountered

契約の symlink 親拒否を個別に試験し、親パスだけでなく正規報告パスと理由を診断に出すようにした。製品スコープの変更なし。GitHub CI は未確認。公式 edge-probe fallback の未分類は解消扱いにしていない。

## Next Phase Readiness

PLAN 05-02 の実装完了。独立品質レビューの後、同じ HEAD を起点に新規の実報告を置いたフェーズ検証へ渡す。ここでは Phase 5 は閉じず、品質の報告は更新していない。

## レビュー差戻しの修正

コード `de5f7e8a41d105487368d0422a12eae355b07f09`。前回の確認対象 `35c20a9` から、検証器と専用ハーネスだけを変更した。README・製品 CLI・既存試験・OpenSpec は不変。

| ケース | RED：修正前 | GREEN：修正後 |
|---|---|---|
| `unchecked-task-worktree` | HEAD/index は `[x]`、worktree だけ基点の `[ ]`。base→worktree の一覧に出ず、誤って CLI と verifier が終了0 | 差分一覧に頼らず HEAD→index→worktree のバイト列を照合。チェックの後退を対象パス付きで終了1、CLI 未実行 |
| `nonempty-cli-stderr` | 実 CLI は終了0・期待 JSON・import profiler の stderr あり。verifier が誤って終了0 | 同じ CLI 出力で verifier は `published CLI wrote to stderr` を報告し終了1 |
| `duplicate-cli-key` | テスト用の子プロセスが `count:999` と `count:4` を同一オブジェクトに出力。終了0・stderr 空で verifier も誤って終了0 | JSON のオブジェクトを辞書に変換する前に重複を検出し、verifier は `duplicate JSON key: 'count'` を報告して終了1 |

全23ケース合格。先行 PLAN で使う初回チェック前の検証は引き続き成功し、実依頼ツリーの掲載 CLI は終了0・空 stderr・`alpha:4` → `beta:3` → `gamma:2`。既存 pytest 702件と OpenSpec 厳格検証（指摘0）も再実行して合格した。GSD CLI は Phase 5 / Current Plan 2 / `verifying`、未実施 PLAN なしと読み返せたため、計画位置は再更新していない。GitHub CI は未確認。

## 再レビュー差戻しの修正

コード `32638304c7e59f795b2786e6ad187f4fd72023e6`。対象は OpenSpec 1.1 の**コミット済み**のチェック後退。未チェックの HEAD が固定基点と同じ場合、対象パスについて基点から HEAD までの履歴を調べ、チェック済みの履歴がある場合は CLI 起動前に拒否する。基点や OpenSpec 原本は変更していない。

| ケース | 実測結果 |
|---|---|
| `unchecked-task-commit` | チェックを外したコミットの clean HEAD では、基点→HEAD の対象パス差分なし。RED は CLI 起動・終了0、verifier 終了0、負例ハーネス終了1。GREEN は `openspec/changes/r-864b299c-readme-top-three/tasks.md` と `task 1.1 reverted in HEAD` を示して verifier 終了1、CLI 未実行、ハーネス合格。 |
| `before-first-task-check` | 実チェックコミットの親から README の掲載行だけを再現。実チェックコミットは祖先になく、HEAD・index・worktree の 1.1 がすべて未チェック。verifier と CLI は終了0、stderr は空。 |

専用回帰は報告の三状態を含む全24件、既存 pytest は702件、OpenSpec 厳格検証は1件（指摘0）が合格。報告込みの依頼ツリーでは掲載 CLI が終了0、空 stderr、`alpha:4` → `beta:3` → `gamma:2`。GSD は Phase 5 / PLAN 2 / `verifying`、未実施 PLAN なし。計画位置は更新せず、独立検証に引き継ぐ。GitHub CI は未確認。

## Self-Check: PASSED

Builder が全24ケース、報告込みの依頼ツリー、既存回帰、OpenSpec 厳格検証を確認。独立品質は別工程。
