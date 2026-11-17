---
phase: "02"
slug: "wordfreq-html-output"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-17"
---

# Phase 02 — Validation Strategy

> 公式VALIDATION.mdテンプレートに基づく計画時の契約。未実装・未実行。最終task ID/wave/threatはplannerがPLANと同期する。

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | 既存pytest 9.2.0 / CPython3.12.15、Node24 native WebSocket / 既存Chromium156 |
| Config file | 既存pyproject.tomlは無変更。新tests/conftest.pyでbrowser opt-inを登録 |
| Quick run command | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest tests/test_aggregator.py tests/test_formatters.py tests/test_cli.py -q` |
| Full suite command | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest -q` |
| Estimated runtime | 未測定。quick目標30秒、browser matrixは別途上限付で実測 |

## Sampling Rate

- task毎: そのtask終了時に存在する試験ファイルのみ、該当quickコマンドを実行。
- PLAN毎: full default suite（browser skipを受入合格扱いにしない）。
- browser PLANと品質: `.../bin/python -m pytest tests/test_html_browser.py --real-browser --browser-evidence-dir=.planning/phases/02-wordfreq-html-output/evidence/builder -q`。品質はqualityサブディレクトリへ独立再生成。
- verify-work前: full suiteと明示browser matrixがgreenで画像・DOM/layout/network/version/headの実原本が揃う。
- Max feedback latency: quick目標30秒、browserは有限timeout。実測を記録し要件削減で短縮しない。

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| planner assigns | tracer | 1 | REQ-09, REQ-10, REQ-12, REQ-14 | planner assigns | 1回集計、既存境界と入力不変 | unit/CLI | 既存quick＋新HTML試験（作成後） | 既存＋W0 | pending |
| planner assigns | formatter | serial | REQ-11, REQ-13 | planner assigns | escape/CR保持/3列 | unit | pytest tests/test_html_output.py -q（作成後、上記既存interpreter） | W0 | pending |
| planner assigns | browser | serial | REQ-11, REQ-13, REQ-14 | planner assigns | 不実行・request0・layout/全文 | real browser | 上記--real-browserコマンド | W0 | pending |

## Wave 0 Requirements

- [ ] tests/test_html_output.py — HTMLと全形式CLI契約。対応task内で先に試験作成しtask終了時に実行。
- [ ] tests/conftest.py — --real-browser/--browser-evidence-dir/marker。default skipだがopt-in時の不足はfail。
- [ ] tests/test_html_browser.py — 実CLI生成fixture、正確oracle、証跡index確認。
- [ ] tests/browser/wordfreq_html_evidence.mjs — native WebSocket CDP、監視先行・実viewport・画像/DOM/network保存・終了処理。
- Framework install: なし。既存cacheが失われたら人へ回し、CI/依存追加で迂回しない。

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 画像から全内容と3列の可読性・日本語字形を独立確認 | REQ-11, REQ-14 | DOMだけで視認性は確定しない | 品質がCLI生成から独立再実行。320/375/1280px全caseの実PNGと測定/indexを照合。画像を開いて確認し、未読/未取得は未検証 |

## Validation Sign-Off

- [ ] All tasks have automated verify or earlier/same-task Wave0 file creation
- [ ] No 3 consecutive tasks without automated verify
- [ ] Wave0 covers missing references
- [ ] No watch mode / no inline shell snippets in automated commands
- [ ] Feedback latency measured
- [ ] nyquist_compliant true is reserved for real validation

**Approval:** pending execution. 計画の独立checker合格と製品検証は別。
