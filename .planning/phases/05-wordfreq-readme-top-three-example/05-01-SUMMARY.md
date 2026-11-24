---
phase: 05-wordfreq-readme-top-three-example
plan: "01"
subsystem: documentation
tags: [readme, wordfreq, cli, json, tdd]
requires: []
provides: [README top-three JSON example, executable acceptance check]
affects: [phase-verification]
actuals:
  tokens: 2530
  tasks: 1
  commits: 1
plan_head_before: c9b3f362fcc03d5efeddcda4e949623455cb5e5c
tech-stack:
  added: []
  patterns: [execute the published argv with an isolated UTF-8 input]
key-files:
  created:
    - .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py
  modified:
    - README.md
    - openspec/changes/r-864b299c-readme-top-three/tasks.md
key-decisions: []
requirements-completed: [REQ-22]
coverage:
  - id: readme-top-three
    description: 上位3語の JSON 実行例を既存例の直後に1行掲載する
    requirement: REQ-22
    verification:
      - kind: integration
        ref: python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py
        status: pass
    human_judgment: false
duration: 342s
completed: 2026-11-24
status: complete
---

# Phase 5 Plan 01: README の上位3語 JSON 実行例

**既存の上位2語 JSON 例の直後に `python -m wordfreq input.txt --top 3 --format json` を1行追加した。既存例・CLI・既存試験は変更なし。**

## Performance

- 開始: 2026-11-24T05:01:24Z、終了（実装検証）: 2026-11-24T05:07:06Z
- タスク: 1/1、タスクの変更ファイル: 3（製品1、検証1、OpenSpec 1）

## Accomplishments

- REQ-22 / OpenSpec 1.1: 配置、固定基点からの README 追加1・削除0、掲載行からの実 CLI の3件を確認した。
- 検証は `.planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py` に分離した。掲載行を固定 argv と照合し、入力の位置引数だけを一時 UTF-8 ファイルに差し替えてシェルなしで実行する。

## Task Commits

- `8df000ffbd4ef344e5063a21034cb612084ac35c`: 05-01-01。README・検証原本と OpenSpec 1.1 のチェックを同じコミットに収録。GSD の evaluation-scope はこのタスクコミットを解決した。

## 実測結果

実行コマンド: `python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py`。比較基点: `5528aa47cca27a93a6732e914710f2772118a572`。

| 段階 | 対象 | 実結果 |
|---|---|---|
| RED | `da342f12907c72dd3f2dba55326d8e4f45f86610` 上の作業ツリー、README 未編集 | 検証終了1。直後の掲載行がない (`top-three example missing immediately after the top-2 JSON example`)。CLI は未実行。 |
| GREEN | 同じ HEAD 上の README 編集済み作業ツリー | 検証終了0。配置・差分合格、CLI 終了0。 |
| チェック前 | ローカル仮コミット `737c0cc142d6b2176da09bc37c4a17d87f5744f1`、クリーン | 検証終了0、CLI 終了0。この後にだけ OpenSpec 1.1 をチェックした。 |
| チェック後 | `8df000ffbd4ef344e5063a21034cb612084ac35c`、クリーン | 検証終了0、CLI 終了0。未公開の仮コミットに OpenSpec のチェックだけを含め直した。 |

入力: `delta gamma beta alpha beta gamma alpha beta alpha alpha`。成功時の実 stdout は `[{"word": "alpha", "count": 4}, {"word": "beta", "count": 3}, {"word": "gamma", "count": 2}]` と末尾改行1つ、stderr は空。`openspec validate r-864b299c-readme-top-three --type change --strict --json` は `valid: true`、指摘0件。

## Decisions Made / Deviations from Plan

- 新しい設計判断や製品範囲の変更なし。作業ツリーの結果とクリーンなコミットの結果を分けて記録した。

## Issues Encountered / Next Phase Readiness

- 製品検証の未解決事項なし。既存の全回帰試験は初回180秒でタイムアウトし、再実行の結果はレビュー引継ぎに記録する。CI 未確認。
- Phase 5 の独立検証・PM 受入は未実施。REQ-22 の公式 edge-probe fallback の未分類は合格根拠にしない。Phase 5 の検証担当は最終 head で再実行し、平文証拠を保存する。

## Self-Check: PASSED

Builder の README 配置・固定基点との差分・実 CLI の検証は、OpenSpec のチェックを含むタスクコミットまで合格。品質担当の独立検証は別工程。
