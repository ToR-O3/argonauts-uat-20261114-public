---
phase: 07-wordfreq-max-count
plan: "02"
subsystem: testing
tags: [python, pytest, cli, max-count, readme]
requires:
  - phase: 07-01
    provides: Inclusive max-count implementation, sealed oracle and complete pre-feature RED
provides:
  - Four isolated exit-regression mutants and four unmodified controls
  - One executable README frequency-range example
  - Complete local regression evidence for this PLAN
affects: [07-03, phase-verification]
tech-stack:
  added: []
  patterns: [cold-copy mutation discrimination, literal README output oracle]
key-files:
  created: [.planning/argonauts/r-d4bcda40/builder/07-02/VERIFICATION.md]
  modified: [tests/test_cli.py, README.md, openspec/changes/r-d4bcda40-max-count/tasks.md]
key-decisions:
  - Preserve 07-01 sealed oracle and pre-feature RED without substitution
  - Follow human decision 2026-11-25 21:22 omitting browser images while retaining HTML content tests and independent quality
  - Mark OpenSpec1.3 only; keep aggregate2.1 and independent2.2 pending
requirements-completed: [REQ-23, REQ-24, REQ-25, REQ-26, REQ-27, REQ-28]
coverage:
  - id: D1
    description: Normal empty, input failure and pre-read usage remain distinguishable
    requirement: REQ-25
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_max_count_empty_exit_discrimination
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_max_count_input_failure
        status: pass
    human_judgment: false
  - id: D2
    description: README example is present once and reproducible with fixed JSON bytes
    requirement: REQ-28
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_max_count_readme_example
        status: pass
    human_judgment: false
  - id: D3
    description: Added tests and existing full suite pass without product changes
    requirement: REQ-27
    verification:
      - kind: other
        ref: .planning/argonauts/r-d4bcda40/builder/07-02/full/junit.xml
        status: pass
    human_judgment: false
plan_head_before: 0012db4060977bd5afeb07f12e36b857c1e6a882
commits: 3
duration: 639s
completed: 2026-11-25
status: complete
---

# Phase 7 Plan 02: 三出口とREADME例 Summary

**正常空exit0・入力失敗exit1・読取り前usage exit2の変異判別力を追加し、min2/max3のREADME例を固定JSONの実CLI試験で再現した。**

## Performance

- Started: 2026-11-25T13:05:19Z
- Task implementation and evidence committed: 2026-11-25T13:15:51Z
- Measured at closeout: 639秒（SUMMARY/状態の記録前）
- Tasks: 2
- Files changed before SUMMARY: 56（大半はstage別の原本）

## Accomplishments

- 先行oracle/REDの読取り照合2件と既存三出口129件を確認してから追加。製品ファイル編集なし。
- 独立coldコピーへmax正値制約・逆転エラー・空集合の入力取得短絡・usage後回しを各別に注入。狙ったassert失敗4件と未変異対照4件を保存。最終外側8件成功。
- README例欠落による1件の先行REDを保存し公式RED_EVIDENCE_OKを確認してから本文を編集。掲載command/input/JSON・旧7例・末尾検証B行を検査。実argvのinput.txtでbeta3/alpha2+LF、exit0・stderr空を再現しhelpも成功。
- 三出口追加込み137件、task1 CLI649件、README/help2件、全suite1008件成功。成功stageはfailures/errors/skipped0。

## Task Commits

1. 07-02-01: `da8916c` — test(07-02): discriminate normal-empty input and usage exits
2. 07-02-02 RED: `288e916` — test(07-02): pin README max-count example before documentation
3. 07-02-02 GREEN: `80d246b` — docs(07-02): document and reproduce inclusive frequency range（READMEとOpenSpec1.3チェックを同commitへ）

`git rev-list --count 0012db4..HEAD` はSUMMARY前に3。SUMMARYと公式STATE/ROADMAPの記録commitはこの後。

## Evidence and Verification

全原本: `.planning/argonauts/r-d4bcda40/builder/07-02/`。詳細は同rootのVERIFICATION.md。

| Stage | tests / exit | wall秒 |
|---|---|---|
| precondition | 129成功 / 0 | 5.521356699 |
| mutations-green | 8成功 / 0 | 8.889100510 |
| exits | 137成功 / 0 | 12.691700308 |
| cli-task1 | 649成功 / 0 | 57.488068019 |
| red | README掲載欠落1失敗 / 1 | 0.619013232 |
| green | README/help2成功 / 0 | 0.473428516 |
| full | 1008成功 / 0 | 217.374637236 |

正確なpytest argv/cwd/env/Python/実head・製品SHA・件数・exit・時間は各stage command.json/result.json、stdout/stderr/JUnitは同stage無加工原本。README実CLIの入力/argv/cwd/exit/stdout/stderrはgreen/stdout.txt。README先行REDのsemanticAssessmentはred-evidence.json、公式判定はred-classifier.json（passed=true / target_test_failed）。

fullは `288e9162d5c22d2d804623db7d3d1f59a3633f53` ＋README未commit差分で実行。現在の試験/製品はこのheadから不変、README SHA-256 `43f1a6a69cd3aa616bd715e513f4913875f5c2ba0ef85907c98769787c318d68` が検証後も一致。報告commitへ実行headを付け替えない。

## Decisions Made / Deviations from Plan

依頼者判断日時: 2026-11-25 21:22（JST、t_87068596の人defaultコメント1795609328）。原文:

> 依頼者の判断：この依頼の受入条件に、画面の画像の比較は入っていません。この試験環境ではブラウザーが起動できないため、変更前後の画像の取得と比較は省いてください。html の出力は、試験で中身（出す単語と回数）を確かめれば足ります。ほかの受入条件と品質の独立した確認はそのままにしてください。

前PLAN decision.md/受付引継ぎと一致。画像・browser測定を実施済みとせずHTML内容試験を維持。追加製品変更なし、新依存/CI/formatter/CSS/入力源変更なし。指定PLAN外への継続なし。

## Issues Encountered

- 初回変異fixtureの外側4件はpytest JUnit failure要素の省略可能なtype属性を必須としたため失敗。狙ったinner assertは既に失敗していたが、これを有効feature REDとせず初回原本を保持した。実failure本文のAssertionError/固有期待差と件数/errors/skipを照合するよう試験を修正し、8件成功を再実行した。
- CLIとfullは30秒を超え、高速検査としない。
- terminalへカードIDの環境変数が渡らずstage resultのtaskがnull。カード帰属はVERIFICATION.mdに記録し、実測原本は変えない。
- 新headのCIと独立品質はこの時点では未確認。ローカル1008成功をその代用にしない。

## User Setup Required

なし。

## Next Phase Readiness

07-03へ渡す。OpenSpec1.1/1.2の親チェックを保持し今回1.3を完了。2.1の今回全suiteは成功したが集約のscope/手順記録は07-03へ残す。独立品質2.2は未完了。REQのrequirements-completed欄は公式SUMMARY契約でPLANの全IDを転記しているが、共有REQのCompleteは公式ready-idsと後続の独立品質で別判断する。phase.completeを呼ばず、07-03を実行しない。

## Self-Check: PASSED

- 指定PLANのみ。試験102追加/削除0、READMEは1例と関連説明だけ、末尾検証B行と旧例保持。
- `git diff --exit-code 0012db4 -- wordfreq .github pyproject.toml` exit0。baseline/親RED原本不変。
- 先行README REDの公式判定、追加4変異と4対照、全1008件成功の実出力を確認。
- SUMMARY commit後に公式advance-plan/update-progress/roadmap.update-plan-progressを呼び、保存した位置を読み戻す。
