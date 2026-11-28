---
phase: "08"
slug: wordfreq-exclude-file
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-28"
---

# Phase 08 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | 既存pytest 9.0.3 / CPython 3.12.15（研究のversion probe） |
| Config file | 既存tests検出、追加設定なし |
| Quick run command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_sources.py tests/test_cli.py -q -x` |
| Full suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest -q` |
| Estimated runtime | 未測定。Builderが実測し、長い場合も省略して合格としない |

## Sampling Rate

- After every task commit: 対応単体RED/GREEN後Quickを実行。
- After every plan wave: Full suiteを実行。
- Before verify-work: 対象headの全件GREENを品質が独立確認。
- Max feedback latency: 未測定、実測で記録。watchなし。

## Per-Task Verification Map

正式PLANのtask IDとwaveを以下へ対応付けた。計画段階であり新assert・機能・回帰・独立品質の実行結果ではない。各automatedの観測可能なfails_whenはPLAN内で直後に記載する。

| Task ID / Wave / scope | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|------------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 08-01-01 / 1 / 正常系全形式tracer・説明 | REQ-28,32,35 | T-08-01,02,03,SC | read-only・strict UTF-8-sig・共通計数・escape維持 | unit/CLI | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_sources.py tests/test_cli.py -q -x` | ファイルあり、新assertを同taskで先に追加 | pending |
| 08-01-02 / 1内直列 / 行境界・Unicode・最後FILE | REQ-28,29,30 | T-08-01,03 | 直接集合・前FILE未読・本文抽出/casefold保持 | unit/CLI spy | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_sources.py tests/test_cli.py -q -x` | ファイルあり、新assertを同taskで先に追加 | pending |
| 08-01-03 / 1内直列 / 空・閾値/top・total | REQ-28,32,33,35 | T-08-02,03 | 計数前tokens spy・選択前整数total・既存空HTML維持 | unit composition/CLI | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_sources.py tests/test_cli.py -q -x` | ファイルあり、新assertを同taskで先に追加 | pending |
| 08-02-01 / 2（depends 08-01）/ 失敗tracer・順序・説明 | REQ-28,31,32 | T-08-04,05,08 | 引数→除外→本文、失敗後本文/計数/formatterなし・stdout空 | unit spy/CLI | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_sources.py tests/test_cli.py -q -x` | ファイルあり、新assertを同taskで先に追加 | pending |
| 08-02-02 / 2内直列 / 安全性・未指定互換・統合 | REQ-33,34,35 | T-08-06,07,08,SC | 全件回帰・両入力不変・HTMLパス非露出/escape・独立品質文字原本 | full pytest/品質handoff | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest -q` | 既存tests、新assertを同taskまでに先に追加 | pending |

## Wave 0 Requirements

- 新framework/依存/conftest不要。既存test_sources.py/test_cli.pyに新ケースを実装担当が先に書く。未作成node-idや検証driverを実在扱いしない。
- 既定python3.14のpytestは欠落。既存代替Python系を使用し、品質もversion/importを独立確認する。
- 研究のScenario Coverage Matrixと結合PRDの全scenarioを正式PLANで網羅する。

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| HTML既存表示継承 | REQ-33,35 | 自動DOM一致と実可読性は別 | 品質は生成HTMLを確認し、画像を得た場合は全画像実閲覧・枚数/内容/結果を文字原本へ残す |
| 証拠の配送 | REQ-34 | pytestだけでは標準添付を証明できない | VERIFICATION.md/実CLI証拠を標準添付、原本とSHA-256照合。PMは文字原本で判断 |

## Validation Sign-Off

- [ ] All tasks have automated verify or explicit preceding file creation
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] All missing assertions covered by execution tasks
- [ ] No watch-mode flags
- [ ] Feedback latency measured
- [ ] nyquist_compliant only after actual validation

**Approval:** pending。計画段階のdraft、機能試験は未実施。
