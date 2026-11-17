---
phase: "04"
slug: "wordfreq-min-count"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-18"
---

# Phase 4 — Validation Strategy

> revision iteration 1/3のsampling契約。製品試験は未実行。採取actionと反復read-only verifyを分離済み。

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
- W1処置: browser-free pytestは先行高速feedback、全browser採取/全case/両幅/全suite/実閲覧/finalizeは省略不可の高遅延full E2E統合gateとして別枠で記録する。Builderは01-02/03-03/04-01、品質は最終independent_quality_gateで開始/終了/所要時間・件数/env/argv/exitを実測保存する。30秒超の実測指摘ではなく、未測定を30秒以内とみなさない。
- B1/B2処置: 実装→browser-free verify→公式task commit→次taskのclean head一度採取action→saved原本read-only automated。採取commandをautomatedに置かず、tracer commit後再verifyも原本再検証のみ。製品編集前baseline hard gate/dirty拒否/上書き禁止は維持。

## Per-Task Verification Map

全commandはrepo root、PLANの承認済み `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3` を前置する。下表は正規PLANの実task ID対応。未作成fileは当該taskで作成・read_file/収集確認してから実行し、計画中には試走しない。

| Task / Wave | Requirement | Threat Ref | Secure behavior / verification | File availability | Status |
|---|---|---|---|---|---|
| 04-01-01 / 1 | REQ-16/20/21 | T-04-01/02/SC | `-m pytest tests/test_min_count_verifier.py -k browser_free -x`。実CLI→scratch保存/validatorの縦slice、正常/拒否control→公式task commit | driver/tests/saved_baseline validatorをtask内作成、実baseline未要求/未採取 | pending |
| 04-01-02 / 1 | REQ-16/20 | T-04-01/02 | actionでclean正式headからbaselineを一度採取・封印。automatedはBASELINE_ROOT束縛 `-m pytest tests/test_min_count_verifier.py -k saved_baseline -x` + full suite | 01-01正式commit後、全形式/両幅実原本をread-only再検査。製品変更前timeline必須 | pending |
| 04-02-01 / 2 | REQ-17/21 | T-04-03/04 | `-m pytest tests/test_cli.py -x`。1.2のRED/GREEN、入力前spy/実permission/help/例 | 既存fileに今回試験追加、baseline gateが先行 | pending |
| 04-02-02 / 2 | REQ-15/16/18/19/20/21 | T-04-04/05 | `-m pytest tests/test_cli.py -x`、`-m pytest tests/test_aggregator.py -x`、`-m pytest tests/test_formatters.py -x`、full。1.3/1.4両群を共通実装前にRED | 既存file、追加試験実在後に収集/実行。後続mode不要 | pending |
| 04-03-01 / 3 | REQ-15/16/18/19/20/21 | T-04-09 | `-m pytest tests/test_min_count_verifier.py -k browser_free -x`。capture/比較/saved_capture validatorの実CLI縦slice→公式task commit | task内でcapture/validator作成。baseline/製品先行、実browser採取不要 | pending |
| 04-03-02 / 3 | REQ-16/20/21 | T-04-06/07/08 | 同browser_free + full。実owner lifecycle、全view/ledger/head/root/late通信/0件/AC7欠落拒否→公式task commit | review-session/finalizeをtask内作成、syntheticは実受入でない | pending |
| 04-03-03 / 3 | REQ-15/16/18/19/20/21 | T-04-09 | actionでclean headからcapture一度採取。automatedはBASELINE_ROOT/CAPTURE_ROOT束縛 `-m pytest tests/test_min_count_verifier.py -k saved_capture -x` | 全4mode正式commit後、builder/04-03-capture原本をread-only再検査 | pending |
| 04-04-01 / 4 | REQ-15〜21 | T-04-09/10 | actionで統合capture一度採取。automatedはfull + 同saved_capture（統合root束縛） | 全先行file実在、builder/04-04-integration原本を反復read-only検査 | pending |
| 04-04-02 / 4 | REQ-15〜21 | T-04-10/11/12 | browser_free driver/doc contract試験 + full。品質runbook/配送3gate | docsをtask内作成。公式commit後最終head品質は別主体 | pending |

BASELINE_ROOT/CAPTURE_ROOTの完全名は WORDFREQ_MIN_COUNT_BASELINE_ROOT / WORDFREQ_MIN_COUNT_CAPTURE_ROOT。各PLANのautomatedは実rootを明示する。これはpytest専用の保存原本束縛でdriverの公開mode/flag追加ではない。通常full suiteは未作成saved rootを要求しないbrowser-free回帰、明示saved群はroot未指定なら非0/0 collected、指定先欠落/改変は失敗。採取driver内full pytestへopt-in環境を継承せず再帰/未完成root検査を防ぐ。syntheticと実原本結果を混ぜず、saved群は採取/保存/再帰実行なしで全原本をread-only照合する。

品質のみ: 04-04-PLAN.md independent_quality_gateの実review-session→全画像/raw/baseline実閲覧→finalize→owner実終了/最終marker読取り→標準添付→PM原本読取り。Builder自己承認不可。全automated直後のfails_whenは各PLANに明記（非0/0 collected/欠落/未閲覧等）。各task終了時に使用可能なfile/inputだけをverifyする。連続sampling欠落なし、wave毎full。全先行成果がそろってからphase検証。feedback latency/件数は実測するまで未測定。

Edge30は29 explicit + 1 structured backstop（04-02 P6 REQ-17/concurrency）。未提示の中断/並列製品保証は創作しない。未実証backstopはhuman_needed/insufficient_spec。UI14全件は04-03 U01〜U14。全対応と根拠は .planning/argonauts/t_34cd1b56/PLAN-MAPPING.md。nyquist_compliant/wave_0_completeは実検証前のためfalseを維持する。

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
