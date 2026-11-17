---
phase: "04"
slug: "wordfreq-min-count"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-18"
---

# Phase 4 — Validation Strategy

> 計画時のsampling契約。製品試験は未実行。PLAN保存後に実タスク対応を補完する。

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | pytest 9.0.3（既存Python3.12環境、04-RESEARCH参照） |
| Config file | pyproject.toml（依存変更しない） |
| Quick run command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py tests/test_aggregator.py tests/test_formatters.py -q` |
| Full suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` |
| Estimated runtime | 未測定、実行担当が記録する。未測定を合格としない |

## Sampling Rate
- task毎に対応pytestのRED→GREENとquick run。追加した実在file/nodeを収集してから使う。
- wave毎とphase検証前にfull suite。0件収集・未実施・skipの穴を成功扱いしない。
- 既存の承認済みfull commandはそのまま使う。新driver/試験はtaskの作成順と実在をPLANで固定する。
- feedback latencyは未測定。watch-mode・承認待ち対話・待機ループなし。

## Per-Task Verification Map

| Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| REQ-15, REQ-17, REQ-18 | 各PLANの一意T-04-NNへ対応 | 入力前検証、元counts保持、全形式共通対象 | unit/integration | quick run command | 既存fileあり、今回試験はW0追加 | pending |
| REQ-16, REQ-19 | 各PLANの一意T-04-NNへ対応 | 変更前baseline不変、元total、空出力 | integration + comparison | quick run command + 作成task後のbaseline照合 | baseline/driver未作成 | pending |
| REQ-20, REQ-21 | 各PLANの一意T-04-NNへ対応 | 静的安全性・差分範囲維持・品質の独立性 | regression + evidence | full suite command | 既存suiteあり、今回証拠は後工程 | pending |

PLANごとのtask ID/wave/実コマンドを最終PLANから追記する。合否を先取りしない。

## Wave 0 Requirements
- [ ] 最初の製品変更前baseline保存用の実入力/argv/env/head/stdout/stderr/exit/HTML/画像と索引を最初のPLANで作成する。
- [ ] min-count新規pytest/入力境界spyを追加しRED→GREEN。空結果試験を後付けREDにしない。
- [ ] 今回専用検証driverと試験、独立品質runbookを必要最小限で作成する。旧scope/head/AC1〜6の合格を流用しない。
- [ ] 検証ファイル・入力・command availabilityを各task完了時点で成立させる。
- 新install/依存/CI変更は不要かつ禁止。基盤は既存環境を使う。

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 独立品質の全画像実閲覧/比較 | REQ-16, REQ-20 | capture/DOM一致では可読性を代用できない | 対象headで品質自身のCLI生成HTMLを1280×900/320×900 DPR1で開きbaselineと同環境比較。raw Range/通信試行/画像/閲覧結果を保存 |
| フィルタ→topの実ソース順序 | REQ-18 | 出力だけでは順序を識別できない | 対象headのファイル・行/diffを品質が記録 |
| 保存・標準添付・PM原本読取り | REQ-20 | profileごとの可読性を試験成功から推測できない | AC別索引にhead/root/run/path/SHAを付けて正規配送。拒否/読取り不能はgaps |
| 既存CI状態と禁止差分 | REQ-21 | CI未報告は成功でない | 有限回確認、追加変更・待機なし。CI/依存/CSS/文言不変を今回base差分で照合 |

## Validation Sign-Off
- [ ] 全taskにautomated verifyまたはW0依存
- [ ] 連続3taskのsampling欠落なし
- [ ] W0が未作成参照を網羅
- [ ] watch-modeなし
- [ ] feedback latencyを実測
- [ ] 公式validate-phaseが判定するまでnyquist_compliantをtrueにしない

**Approval:** pending — 実装・独立品質未実施。
