---
phase: "02"
slug: "wordfreq-html-output"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-17"
---

# Phase 02 — Validation Strategy

> 公式VALIDATION.mdテンプレートに基づく計画時の契約。未実装・未実行。task ID/wave/threatとAC/OpenSpec/edge/UIの対応を02-01〜03-PLAN.mdと同期済み。

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | 既存pytest 9.2.0 / CPython3.12.15、Node24 native WebSocket / 既存Chromium156 |
| Config file | 既存pyproject.tomlは無変更。新tests/conftest.pyでbrowser opt-inを登録 |
| Quick run command | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest tests/test_aggregator.py tests/test_formatters.py tests/test_cli.py -q` |
| Browser harness quick command | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest tests/test_browser_harness.py -m 'not real_browser' -q` — 02-03-02内で作成後、02-03-02/03で全量E2Eとは別に実行 |
| Full suite command | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest -q` |
| Estimated runtime | 未測定。quick目標30秒、browser matrixは別途上限付で実測 |

## Sampling Rate

- task毎: そのtask終了時に存在する試験ファイルのみ、該当quickコマンドを実行。
- 02-03-02/03の早期検知: 上記browser harness quickを先に実行。oracle/request分類/indexの3系統すべて非0件・skip0、正常対照と独立変異の期待診断を確認し、各系統件数/時間/exitを記録する。browser/Node/font/CDPの起動・探索、実CLI生成、全matrix fixtureに依存させない。30秒未満は未実測の目標であり、超過はfindingとして残す。
- PLAN毎: full default suite（browser skipを受入合格扱いにしない）。
- browser PLANと品質: `.../bin/python -m pytest tests/test_html_browser.py --real-browser --browser-evidence-dir=.planning/phases/02-wordfreq-html-output/evidence/builder -q`。品質はqualityサブディレクトリへ独立再生成。
- verify-work前: full suiteと明示browser matrixがgreenで画像・DOM/layout/network/version/headの実原本が揃う。
- Max feedback latency: quick目標30秒、browserは有限timeout。実測を記録し要件削減で短縮しない。

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 02-01 | 1 | REQ-09/10/11/13/14 | T-02-01/02 | 一度escape/CR参照、basename、実CLI別ファイル保存 | unit/CLI | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest tests/test_html_output.py tests/test_cli.py tests/test_formatters.py -q` | HTML試験は同task先頭で新設、他既存 | pending |
| 02-01-02 | 02-01 | 1 | REQ-10/12/14 | T-02-02 | 共通初出順、casefold、top前total、seed bytes | full | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest -q` | 既存＋先行task作成済み | pending |
| 02-02-01 | 02-02 | 2 | REQ-09/10/11/12/14 | T-02-03 | 全形式エラー/once-only/cold input-worktree不変/並行別出力 | CLI/boundary | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest tests/test_cli.py tests/test_sources_boundary.py tests/test_aggregator.py tests/test_sources.py tests/test_tokenizer.py -q` | 既存を同task拡張 | pending |
| 02-02-02 | 02-02 | 2 | REQ-09/13 | T-02-05 | 全文直接payload/純粋性、browser前の部品境界 | unit | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest tests/test_html_output.py tests/test_formatters.py -q` | 先行PLANで存在、同task拡張 | pending |
| 02-02-03 | 02-02 | 2 | REQ-14 | T-02-03/04 | UTF-8別パス実例、共有露出/切詰め注意 | full/docs example | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest -q` | 既存を同task拡張 | pending |
| 02-03-01 | 02-03 | 3 | REQ-09/10/11/13/14 | T-02-06/07/08 | 全target監視先行/positive main file/不実行/外部0 | real browser normal | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest tests/test_html_browser.py --real-browser --browser-evidence-dir=.planning/phases/02-wordfreq-html-output/evidence/builder -q` | conftest/HTML browser/mjsを同taskで新設 | pending |
| 02-03-02 | 02-03 | 3 | REQ-11/12/13/14 | T-02-06/07/08 | oracle/request分類/index純粋負例＋全case×全幅、全文/rect/不実行、known-bad実browser負例 | pure unit quick + mandatory real browser matrix/harness | 上記Browser harness quick command、次に `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest tests/test_browser_harness.py tests/test_html_browser.py --real-browser --browser-evidence-dir=.planning/phases/02-wordfreq-html-output/evidence/builder -q`（個別時間/件数/exitを記録） | browserは先行task、self-test/純粋判定は同taskで先に作成 | pending |
| 02-03-03 | 02-03 | 3 | REQ-09/10/11/12/13/14 | T-02-09 | 純粋3系統再検証、実index/head帰属、独立品質handoff | pure unit quick + full + mandatory real browser | 上記Browser harness quick command、次に `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest -q`、次に02-03-01と同じ明示opt-inコマンド（個別時間/件数/exitを記録） | 全file/optionが先行taskで存在 | pending |

高速subsetは実証跡にも使うassert_evidence_index→validate_recorded_evidence/classify_recorded_requestの純粋判定経路を直接検査する。oracleのfilename/total/headers/rows、raw requestの追加local/HTTP(S)/WS(S)/その他外部scheme、indexのcase/幅/必須原本path/main file完了欠落を独立変異させる。fixtureは検証器のunit入力であり実browser受入証跡ではない。全量E2Eと全幅の受入gateは削らない。

各PLANにT-02-SC（予約された共通ID）を保持する。それ以外T-02-01〜09はphase内一意。全taskにread_first/acceptance_criteria/automated直後fails_whenを設けた。非0・0 tests・collection errorは失敗、明示browserでskipは失敗。課題別の誤動作は各PLANのfails_whenを参照する。独立PLANは02-01のみで、02-02/03は先行成果が必須。検証ファイルの存在を前提とするコマンドは作成taskの完了時まで実行しない。

## AC / OpenSpec対応表

| AC | Requirement | PLAN/task | OpenSpec tasks | 証拠 |
|---|---|---|---|---|
| AC1 | REQ-09 | 02-01-01、02-02-01、02-03-01/03 | 2.1, 2.2, 3.2 | 完全文書/UTF8保存・既存形/exit回帰 |
| AC2 | REQ-10 | 02-01-01/02、02-02-01、02-03-02 | 2.1, 2.2, 3.1 | basenameのみ、top1 total5/1,zoo,2、空total0 |
| AC3 | REQ-11 | 02-01-01、02-03-01/02/03 | 2.1, 3.1 | 明るい3列/連番/scoped headers、全幅実画像/rect |
| AC4 | REQ-12 | 02-01-02、02-02-01、02-03-02 | 1.1, 2.2, 3.2 | first-seen/casefold/頻度/top/seed形式内byte一致 |
| AC5 | REQ-13 | 02-01-01、02-02-02、02-03-01/02 | 2.1, 3.1 | 一度escape、CR/CRLF/空白忠実性、不実行・全target通信0 |
| AC6 | REQ-14 | 02-02-01/03、02-03-03＋独立品質 | 2.2, 3.1, 3.2 | full回帰・入力不変・利用例・品質再生成・CI依存無変更 |

OpenSpec→PLAN集合: 1.1→02-01/02、2.1→02-01/02/03、2.2→02-01/02、3.1→02-03、3.2→02-02/03。OpenSpecチェック更新/sync/archiveは本計画作成では行わない。

## Edge fallback no-silent-drop監査

公式edge engine原本 `.planning/argonauts/r-5c041156-edge-probe.json` の10itemをすべて維持する。原本は未編集。公式spec-sectionのedges/prohibitionsはともにsupplied:false。toggle未定義はdefault ON。--autoの解決は下表で行い、explicitは各PLAN frontmatterのmust_haves.truthsへ投影した。今回はbackstop適用なし（曖昧な任意入力への保証を追加せず既存scopeの検査可能なassertionを選んだ）。unclassified3件を自動resolveしない。

| 原本item | 判定 | 投影先/根拠 |
|---|---|---|
| REQ-09 empty | resolved/explicit | 02-01 truths REQ-09 empty、02-01-01/02-02-01の空/1/多数 |
| REQ-09 encoding | resolved/explicit | 02-01 truths REQ-09 encoding、UTF8と全文一致 |
| REQ-10 unclassified | unresolved/flagged assumption A-E10 | metadata既知契約は別に計画済みだが分類missは消さない |
| REQ-11 concurrency | resolved/explicit | 02-02 truths REQ-11 concurrency、02-02-01別出力並行/input不変。途中stdoutのatomic保存保証は追加しない |
| REQ-12 adjacency | resolved/explicit | 02-01 truths REQ-12 adjacency、casefold統合と同数別語の区別 |
| REQ-12 empty | resolved/explicit | 02-01 truths REQ-12 empty、空pairs/top後連番 |
| REQ-12 encoding | resolved/explicit | 02-01 truths REQ-12 encoding、Unicode/casefold初出 |
| REQ-12 ordering | resolved/explicit | 02-01 truths REQ-12 ordering、sort後top/seed |
| REQ-13 unclassified | unresolved/flagged assumption A-E13 | escape/browser契約は別に計画済み、分類missは残す |
| REQ-14 unclassified | unresolved/flagged assumption A-E14 | 回帰/説明/品質契約は別に計画済み、分類missは残す |

原本10item = truthsへ7item + flagged3item。分類3件は不足情報があるという新しい製品設計質問ではなく、公式分類の未解決レビューsignalである。判定根拠を独立checker/品質に引き継ぎ、証拠がなければhuman_needed。既知のstdin/URL/DB/サーバ等scope外を未決設計に昇格させない。

## UI Considerations lift監査

承認済みUI11itemはすべてexplicit。各々must_haves.truthsへliftし、実画像/測定が揃うまで充足はpending。

| UI item | PLAN truth/task |
|---|---|
| E1 empty | 02-01 UI E1 empty/populated/partial/zero-one-many、02-01-01/03-02 |
| E1 loading | 02-01 UI E1 loading/error、02-01-01 |
| E1 error | 02-01 UI E1 loading/error、02-02-01 |
| E1 populated | 02-01 UI E1 empty/populated/partial/zero-one-many、02-01-01/02 |
| E1 partial | 同truth、02-01-02/03-02 top1 |
| E1 overflow | 02-01 UI E1 overflow、02-03同overflow truth、02-03-02 |
| E1 zero-one-many | 02-01同名truth、02-01-01/03-02 |
| E2 overflow | 02-01 UI E2 overflow/long-text、02-03同overflow truth、02-03-02 |
| E2 long-text | 同truth/task、全空白/CR保持 |
| E3 overflow | 02-01 UI E3 overflow/long-text、02-03同overflow truth、02-03-02 |
| E3 long-text | 同truth/task、固定h1の自然折返し |

## Prohibition fallbackとflag

02-02の2段階recall→precisionを適用。routine engineeringはDROPしedge/回帰へ。注入/path privacy/外部通信などcanonical securityは /gsd-secure-phase + 各PLANのASVS1 threat_modelへのbreadcrumbにしてDROP、prohibitionを重複作成しない。bespokeな2件のみ02-02 must_haves.prohibitionsへprojectProhibitionsのflat scalar statement/status契約でdescriptor-lessに投影する。

- P-02-01: HTMLを匿名化済み/内容非露出と誤案内しない（共有時語/名前残存）。unresolved、flagged-unverified。
- P-02-02: 途中stdout/未取得browser証跡を完成/受入済みと案内しない。unresolved、flagged-unverified。

check_* descriptorは捏造せず、verification:test/judgmentを無根拠に付けない。機械的greenにせず人/品質のレビューへ。既知scopeの禁止を再質問するという意味ではない。

## Multi-Source Coverage Audit

| SOURCE | ID | Feature/Requirement | Plan/task | Status |
|---|---|---|---|---|
| GOAL | Phase2 | 保存可能な安全HTML/モバイル3列表/初出順/独立証跡 | 02-01/02/03 | COVERED |
| REQ | REQ-09 | 単一HTML、既存形式/exit | 02-01-01、02-02-01、02-03-03 | COVERED |
| REQ | REQ-10 | basename/top前total | 02-01-01/02、02-03-02 | COVERED |
| REQ | REQ-11 | 3列/全幅/画像/全文layout | 02-01-01、02-03-01/02/03 | COVERED |
| REQ | REQ-12 | 全形式初出/casefold/seed | 02-01-02、02-02-01 | COVERED |
| REQ | REQ-13 | escape/CR/不実行/通信0 | 02-01-01、02-02-02、02-03-01/02 | COVERED |
| REQ | REQ-14 | 全回帰/説明/独立品質/手段不足 | 02-02-01/03、02-03-03 | COVERED |
| RESEARCH | pipeline | Counter保持/純粋formatter/一度取得・集計・選択 | 02-01-01/02、02-02-01 | COVERED |
| RESEARCH | compatibility | 旧期待/CONCEPTS置換・text/json不変 | 02-01-02、02-02-01/03 | COVERED |
| RESEARCH | serialization | escape後CR参照、直接payloadと実名両経路 | 02-01-01、02-02-02、02-03-02 | COVERED |
| RESEARCH | tooling | cached pytest絶対path、install/CI変更なし | 全task、02-03-03 | COVERED |
| RESEARCH | evidence | Node24 native WS/Chromium156・短TMPDIR・loopback/全target監視・PNG/rect/network/index | 02-03-01/02 | COVERED |
| RESEARCH | integrity | cold copy/add済み基底/全untracked/input bytes、許可失敗 | 02-02-01 | COVERED |
| RESEARCH | handoff | builder/quality別root・head再照合/無害fixture/未検証人へ | 02-03-03 | COVERED |
| CONTEXT | D-01 | 同数初出順と既存構造 | 02-01-02、02-02-01 | COVERED |
| CONTEXT | D-02 | 明るい3列/連番/空 | 02-01-01、02-03-02 | COVERED |
| CONTEXT | D-03 | basename/top前total | 02-01-01/02、02-03-02 | COVERED |
| CONTEXT | D-04 | 純粋formatter/一度集計/既存境界 | 02-01-01、02-02-01/02 | COVERED |
| CONTEXT | D-05 | 単一文書/escape/CR/空白 | 02-01-01、02-02-02、02-03-02 | COVERED |
| CONTEXT | D-06 | 全幅/長語名/不実行 | 02-03-01/02 | COVERED |
| CONTEXT | D-07 | 独立品質原本/不足人へ | 02-03-03 | COVERED |
| CONTEXT | D-08 | 回帰/安全保存/入力不変説明 | 02-02-01/03 | COVERED |
| CONTEXT | D-09 | 範囲外/CI依存設定不変 | 全PLAN scope/T-02-SC、02-03-03 | COVERED |
| CONTEXT | D-10 | 同branch直列/各task試験存在/fails_when | 全PLAN dependencies/task contracts | COVERED |
| CONTEXT | D-11 | 全matrix/exit/seed/既存形 | 02-01-02、02-02-01、02-03-03 | COVERED |

COVEREDは計画上の対応であり製品合格ではない。Deferred Ideas/Phase1出荷履歴は今回の欠落と数えない。AI製品、DB/schema push、APIサービス統合は適用外（native CDPは試験のみ）。

## Reversibility / quality handoff

02-01-02はone-way（公開同数順/top選択の変更）だがD-01の承認済み正確な選択なので公式Already settled例外により再checkpoint無し。構造CLIが出す警告はこの根拠で処理し、ratingを下げて隠さない。02-03-01はcostly（CDP証跡schemaの共有）。その他はreversible。

品質の独立コマンド（ファイルは02-03-01/02完了後に実在）:
`/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python -m pytest tests/test_html_browser.py --real-browser --browser-evidence-dir=.planning/phases/02-wordfreq-html-output/evidence/quality -q`

独立品質は全PNGを実際に開き可読性・字形を判断する。Builderは品質用原本を代作しない。未取得/未読画像、font/browser/CDP不足、全target監視/positive main file証拠不足、head不整合、prohibition/assumptionの未検証はhuman_needed。実装/ブラウザ製品受入は現時点未実施。

## Wave 0 Requirements

- [ ] tests/test_html_output.py — HTMLと全形式CLI契約。対応task内で先に試験作成しtask終了時に実行。
- [ ] tests/conftest.py — --real-browser/--browser-evidence-dir/marker。default skipだがopt-in時の不足はfail。
- [ ] tests/test_html_browser.py — 実CLI生成fixture、正確oracle、証跡index確認。
- [ ] tests/browser/wordfreq_html_evidence.mjs — native WebSocket CDP、監視先行・実viewport・画像/DOM/network保存・終了処理。
- [ ] tests/test_browser_harness.py — 02-03-02で先に作成するfail-closed負例。実browserを使う負例だけreal_browser markerでopt-inにし、純粋oracle/request分類/indexの3系統はdefaultと独立quickで非0件・skip0実行する。共有純粋判定はtests/test_html_browser.pyに同taskで作り、import/fixtureでbrowserを起動しない。
- Framework install: なし。既存cacheが失われたら人へ回し、CI/依存追加で迂回しない。

## 計画自己検査の実結果

- 公式runtime identity: @opengsd/gsd-core 1.21.0。init.plan-phase 2はPlanned/plan_count=3、threat_id_duplicate_count=0。
- 3 PLANともfrontmatter.validate --schema planとverify.plan-structureがvalid:true。task_countは順に2/3/3。
- verify-command-pathsはnot_applicable、blocker0/warning0（pytest形式はこの版の対象外）。よってファイル作成順は上のPer-Task表と各taskのactionで別途保証する。
- revision1保存後に公式 `check verify-failure-directions 2 --raw` を再実行しstatus:ok、8task内の10 automatedすべてnearest fails_whenに結合、blocker0/warning0を確認。`check verify-command-paths 2 --raw` は10 automatedともnot_applicable、blocker0/warning0（pytest形式は対象外）。3 PLANのverify.plan-structureはvalid:true、task_countは2/3/3、変更した02-03のfrontmatter.validate --schema planもvalid:true。
- API coverageの公式detectorにPhase2 sectionと3 PLAN全文を与えdetected:false（exit1は正式なnegative）。COVERAGE.md不要。CDPは試験ローカルinstrumentationで製品サービス統合ではない。
- assumption-delta scan 2はdetected:false。DB/schemaパスも対象になくschema push不要。AI-SPEC/API_SURFACE等を新設しない。
- estimate-calibrationはfactor1/sample_count0/confidence low。各PLANのtokens=raw_tokens、tasksは2/3/3。
- one-way警告はD-01のAlready settled例外として記録済み。独立checkerの合否とは別の自己検査である。
- 製品pytest/新browser harness/受入証跡は計画中に未実行。nyquist_compliant/wave_0_complete/statusは実検証前のfalse/false/draftを維持する。
- revision1: check8bの警告は高速unit/smoke経路の未明示であり、所要時間超過の実測指摘ではない。02-03-02/03に独立quick automatedと直後のfails_whenを追加し、全量E2E必須gateを維持した。時間目標の達成と独立checker再判定は未確認。

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
