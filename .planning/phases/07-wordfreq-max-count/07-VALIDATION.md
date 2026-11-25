---
phase: "07"
slug: "wordfreq-max-count"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-25"
---

# Phase 7 — Validation Strategy

## Test Infrastructure

| Property | Value |
|---|---|
| Framework | existing pytest 9.0.3 / CPython3.12.15 (research version probe only) |
| Config file | pyproject.toml; no dependency/CI update |
| Quick run command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -q -x` |
| Full suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/ -q` |
| Estimated runtime | 未測定。fast browser_free/read-onlyは30秒以内を目標とし初回実測で判定、超過はlatency gap。CLI matrix/full suiteも実測し30秒超は高速としない。両幅全E2Eは別の必須600秒有限gate |

## Sampling Rate
- After each task commit run focused tests relevant to that task, then full suite after each PLAN/wave.
- Before phase verify/UAT: full suite must be green.
- Every task has automated assertions; no three-task manual-only gap. Browser/visual verification supplements, never replaces pytest.
- Commands run from repo root; no outer cd/grep, watch, polling, or fabricated result.
- Check8bのtask automatedは標準pytestのbrowser_free/read-only原本validatorとfocused CLI。全case両幅E2E採取は下記precondition/phase gateに分離し、削除も免除もしていない。fast検査はbrowser/全suiteを内部起動せず、実gate原本の完備性/実exit/全case/hashを検証する。各commandの初回wall timeをstage result.jsonへ記録し、30秒超はlatency gapを報告する。未測定のため現時点で高速達成/8b合格を宣言しない。

## Mandatory finite high-latency gates (not task fast automated)

| Gate / owner | Exact execution after file exists | Timing / blocking evidence |
|---|---|---|
| 07-01-01 baseline precondition gate、製品編集前 | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_max_count.py --mode baseline --output-dir .planning/argonauts/r-d4bcda40/baseline` | browser_free成功後、全case両幅をfresh rootへ一度だけ採取。全体600秒timeout、初回wall time/段階時間/実case・view・画像数/exitを保存。非0/timeout/partial/不完全原本は停止、製品編集禁止。終端saved_baselineでread-only照合 |
| 07-03-01 Builder phase gate、driver/validator作成後 | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_max_count.py --mode capture --role builder --output-dir .planning/argonauts/r-d4bcda40/builder/07-03/capture --baseline-dir .planning/argonauts/r-d4bcda40/baseline` | browser_free成功後、全CLI/全HTML両幅/実canary/全suiteを一度だけ採取。全体600秒timeout、同じ実時間/件数/exit記録。非0/timeout/欠落/外部試行/帰属不明は停止。終端saved_builder_captureが全原本をread-only照合、pending-reviewのみ |

timeoutは同taskで作るdriverの有限deadlineとして実装し、成功までの反復や再採取で救済しない。partial rootを残してblockerを報告する。これらは「高速」扱いしない。独立品質2.2のCLI/全画像実閲覧/通信/PM文字証拠gateも別途必須のまま。

## Per-Task Verification Map

保存PLANは07-01→07-02→07-03の同一依頼branch直列。以下の新selector/driverは計画時には未実装であり、同taskまたは先行taskで作成後だけBuilder/品質が実行する。工程文書の保存を実装成功としない。全commandはrepo rootで実行する。

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| 07-01-01a | 07-01 | 1 | REQ-26,REQ-27 | T-07-01,T-07-03 | oracle破損/偽head/synthetic/再採取拒否 | validator | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_max_count_verifier.py -k browser_free -q -x` | 同task新規作成 | pending |
| 07-01-01c | 07-01 | 1 | REQ-26,REQ-27 | T-07-01 | 封印原本のread-only照合 | regression | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_max_count_verifier.py -k saved_baseline -q -x` | 同task新規作成、baseline後 | pending |
| 07-01-01e | 07-01 | 1 | REQ-23..REQ-27 | T-07-01,T-07-02,T-07-04,T-07-05 | 全1.1先行実行/未実装時RED/未変更製品blobのread-only照合 | evidence validator | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_max_count_verifier.py -k saved_preimplementation_red -q -x` | 同task新規作成 | pending |
| 07-01-01f | 07-01 | 1 | REQ-23..REQ-27 | T-07-01,T-07-02,T-07-04,T-07-05 | 本体変更前に作った1.1全追加群が実装後GREEN | CLI+spy | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k max_count -q -x` | file既存、同taskで全1.1群作成 | pending |
| 07-01-01d | 07-01 | 1 | REQ-23,REQ-24,REQ-26,REQ-27 | T-07-02,T-07-03 | 全3形式の実max path RED/GREEN | CLI E2E | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k max_count_tracer -q -x` | file既存、同task群追加 | pending |
| 07-01-02 | 07-01 | 1 | REQ-23,REQ-24,REQ-26,REQ-27 | T-07-01,T-07-02,T-07-03 | 先行群の包含/AND/top前/Counter不変/shared pairs/保存bytesと追加判別力 | CLI+spy+discrimination | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k max_count -q -x` | 07-01-01で全群作成済み、同task変異fixture追加 | pending |
| 07-02-01 | 07-02 | 2 | REQ-23,REQ-24,REQ-25,REQ-26,REQ-27 | T-07-04,T-07-05 | 先行群の正常空/usage前readなし/実入力失敗/書込みなしと追加判別力 | CLI+spy | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k "max_count_empty or max_count_invalid_before_read or max_count_input_failure or max_count_read_only" -q -x` | 07-01-01で全群作成済み、同task変異fixture追加 | pending |
| 07-02-02 | 07-02 | 2 | REQ-27,REQ-28 | T-07-06 | 指定README1例を実CLIで再現 | doc+CLI | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k max_count_readme_example -q -x` | file既存、同task群追加 | pending |
| 07-03-01a | 07-03 | 3 | REQ-26,REQ-27 | T-07-07,T-07-08 | actor/head/全画像/raw/late-network欠落を拒否 | validator | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_max_count_verifier.py -k browser_free -q -x` | 07-01作成file、同task拡張 | pending |
| 07-03-01b | 07-03 | 3 | REQ-23..REQ-28 | T-07-07,T-07-08 | 必須captureの全原本/全case/view/canary/suite/実成功とpending-reviewをread-only照合 | evidence validator | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_max_count_verifier.py -k saved_builder_capture -q -x` | 07-01作成file、同task試験追加 | pending |
| 07-03-02 | 07-03 | 3 | REQ-23..REQ-28 | T-07-09,T-07-10 | scope限定/既存試験維持/全AC文字証拠の独立handoff | contract+git diff | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_max_count_verifier.py -k "evidence_contract or scope_contract" -q -x` | 同task群とrunbook作成 | pending |

**全command共通の失敗方向:** 非0/ERROR/0 collected/必須case skipは失敗。REDは対象assertの失敗を保存し、pytest欠落/import失敗/未作成selectorはREDにしない。GREENで同失敗が残る、対象case未実施、入力/期待値不一致、原本改変/欠落、対象head/環境/件数/exitの記録欠落も失敗。PLANの各automatedの直後に個別fails_whenを記した。baseline commandは製品編集前の一度限りで、以後はsaved_baselineのread-only検証を使う。

**既存標準command（正確な形を維持）:**
- task終端CLI回帰: `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -q -x`
- 各PLAN/wave終端とphase gate: `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/ -q`
- 両者とも非0/ERROR/0 collected/必須skipで失敗。実件数・環境・argv・head・exit/stdout/stderrをstage別保存する。旧min専用受入driverをmax成功commandとしない。

## Acceptance / OpenSpec / scenario traceability

AC1..6はBriefのB1..6を指す。ROADMAPの5項目へ圧縮して6ACを失わない。

| AC | Requirement | Execution / acceptance |
|---|---|---|
| AC1/B1 整数/省略互換 | REQ-23,REQ-26 | 07-01-01/02 parser/help/固定bytes、品質独立省略CLI |
| AC2/B2 包含上限 | REQ-24,REQ-25 | 07-01-02境界/全形式、07-02-01正常空、品質境界 |
| AC3/B3 min併用 | REQ-24,REQ-25,REQ-26 | 07-01-02 AND/指定順/元12、07-02-01逆転、品質独立再現 |
| AC4/B4 追加と全既存試験 | REQ-27 | 全task RED/GREEN/実数、07-03全suite、品質対象headで再実行 |
| AC5/B5 README1例 | REQ-28 | 07-02-02掲載/実CLI、品質再現 |
| AC6/B6 scope限定 | REQ-26,REQ-27 | 07-03-02 diff/blob、品質両幅/全画像/通信/ソース確認 |

| OpenSpec task | PLAN / responsibility | Completion boundary |
|---|---|---|
| 1.1 | 07-01-01 baselineと全追加pytestの先行作成・実行/未実装時RED | 本体変更前に整数/境界/Unicode/top/空/入力失敗を含む全件を-xなしで実行し、狙ったassert失敗と自然GREENを区別して保存。後続変異REDは代用不可、旧oracle上書きなし |
| 1.2 | 07-01-01登録/AND局所実装、07-01-02内部spy/GREEN | type=int/defaultNone/Counter不変/共有pairs |
| 1.3 | 07-02-02 | 指定例1つ・入力/期待JSON/実CLI |
| 2.1 | 各PLAN全suite、07-03-02 scope/実数 | Builder実行分のみ |
| 2.2 | 07-03で検証手段/runbookを準備、実施はphase verificationの独立品質 | Builder completionに含めない。VERIFICATION.md/文字証拠添付/PM読取りまで別gate |

| Spec requirement / scenario (原識別子を保持) | Task / assertion |
|---|---|
| MAX-1 上限未満と境界値と超過 | 07-01-01/02 max2全形式alpha2,gamma1,delta1 |
| MAX-1 上下限の包含と指定順 | 07-01-02 min2max2/3、順交換 |
| MAX-1 最小の有用な正の上限 | 07-01-02 max1 gamma1,delta1 |
| MAX-1 整数の表記とヘルプ | 07-01-02 None/0/負数/+2/02/大整数/equals/help |
| MAX-1 上限の引数エラーは入力取得より先 | 07-02-01 abc/1.5/欠落、全形式read spy/実CLI |
| MAX-2 全除外と不一致区間 | 07-02-01 max0/-1/min3max2、空形式と元7 |
| MAX-2 空または抽出0語 | 07-02-01 空/空白/記号、元0 |
| MAX-2 有効な上限でも入力失敗は失敗 | 07-02-01 missing/directory/permission/decode、exit1 |
| MAX-2 空集合でも既存引数の検証は必要 | 07-02-01 max0/負数+min0/top0、pre-I/O exit2 |
| MAX-2 省略互換と大きな上限 | 07-01-01変更前封印、07-01-02固定bytes比較 |
| MAX-3 使用例を再現できる | 07-02-02指定1例、入力/JSON/exit/stderr |
| MAX-3 試験と独立した結果の記録 | 07-03準備、phase verification品質実施 |
| FR-2 既定は10件 | 07-01-02 選択後12種類→既定10 |
| FR-2 件数指定と全件出力 | 07-01-02 top3/残り3未満/99 |
| FR-2 不正な件数 | 07-02-01 +既存top0/abc試験維持 |
| FR-2 上限を適用してから件数を制限 | 07-01-02 max2top1→alpha2、12種類/既定10/99 |
| FR-4 同回数ワードは単語の昇順 (旧識別子) | 07-01-02 zoo/apple各5回、期待はzoo→apple初出順 |
| FR-4 正規化とtop境界 | 07-01-02 上限省略Zoo apple APPLE zoo banana、top1/2 |
| FR-4 上限判定も正規化後の回数 | 07-01-02 Straße/STRASSE/日本語、max1/min2max2 |
| FR-4 上下限と同数初出順 | 07-01-02 min2max2 top1/2 zoo→apple |
| HTML-2 topを変えても総数は一定 | 07-01-02保存bytes/既存matrix維持、top1/2/10、元6 |
| HTML-2 異なる頻度の入力とtop | 07-01-02保存bytes/既存matrix、top2元7 |
| HTML-2 top既定と不正値 | 07-01-02 12種類/大top、07-02-01不正topとHTMLなし |
| HTML-2 閾値とtopの両方で表示を絞る | 07-01-01 baseline/07-01-02固定比較、min2top1/min4元7、既存試験維持 |
| HTML-2 三条件の除外でも元総数を保つ | 07-01-02 beta4/zoo3/apple2/pear2/single1→zoo3/元12/順位1 |
| MC-1 下限未満と境界値と超過 | 07-01-02 max省略min2top10→beta3,alpha2、既存試験維持 |
| MC-1 topとの順序と独立値 | 07-01-02 max省略min2top1/top10順交換、既存試験維持 |
| MC-1 Unicode正規化してから閾値を判定 | 07-01-02 max省略Straße STRASSE min2→strasse2、既存試験維持 |
| MC-1 引数エラーは形式と入力読込みに優先 | 07-02-01 min0/-1/1.5/abc/欠落、spy/実CLI、既存試験維持 |
| MC-1 有効な閾値でも入力失敗は失敗 | 07-02-01 +既存min2×4入力失敗を維持 |
| MC-2 未指定と1と従来の出力 | 07-01-01固定oracle、07-01-02省略/明示min1/大max比較 |
| MC-2 語のある入力で全件除外 | 07-01-01既存min全除外baseline、07-02-01 min3 zoo入力元5/既存試験 |
| MC-2 抽出語0件 | 07-02-01空/空白/句読点、有効min/max、元0 |

上記scenario表の07-01-02/07-02-01は実装後の再確認・追加判別力の担当を表す。そこに列挙した1.1対象pytestは例外なく07-01-01で本体変更前に作成・実行する。先行REDは同taskの `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k max_count -q`（全件実行のため-xなし）で保存し、JUnitとcase→scenario対応/未変更製品blobをsaved_preimplementation_redで照合してから本体編集する。未実装でも成功するusage/省略既存caseを偽ってREDとは呼ばない。

## Probe resolutions / threat verification

| Edge row | Requirement/category | must_haves location | Explicit evidence |
|---|---|---|---|
| E01 | REQ-23 boundary | 07-01 | parser/help整数matrix |
| E02 | REQ-23 precision | 07-01 | exact int正負10**100、+2/02、float不使用 |
| E03 | REQ-24 boundary | 07-01 | min/max両端/include/AND/順交換 |
| E04 | REQ-24 empty | 07-02 | 空/空白/記号/単語1つ、0/1行 |
| E05 | REQ-24 encoding | 07-01 | Unicode casefold合算 |
| E06 | REQ-24 precision | 07-01 | exact count/同数初出/top境界 |
| E07 | REQ-25 boundary | 07-02 | max0/-1/逆転/正常空と元total |
| E08 | REQ-25 precision | 07-02 | 整数全域と三出口/usage優先 |
| E09 | REQ-26 boundary | 07-02 | 元12/0/正totalと固定bytes |
| E10 | REQ-26 precision | 07-02 | 元整数和/UTF8/escape/末尾LF/API |
| E11 | REQ-26 concurrency | 07-02 | 既存read-only単発CLI、cold-copy書込みなし、新daemon/保証なし |
| E12 | REQ-27 boundary | 07-03 | 非0/0collected/ERROR/必須skip/未実施を拒否 |
| E13 | REQ-27 precision | 07-03 | exact head/argv/原本/件数/閲覧台帳 |
| E14 | REQ-28 boundary | 07-02 | 指定1例と正負/包含/空/省略説明 |
| E15 | REQ-28 precision | 07-02 | 固定JSON+LF/exit/stderrの実CLI |

原probe15行=上表15行、unclassified0。全explicit、backstop0。UIの14問は07-03 must_haves UI01..UI14へ全件lift、実施は品質両幅/全画像/rawのgate。prohibition recall/precision/canon referralの全文とDROP根拠は07-03、kept0で架空wired-checkなし。

| Threat Ref | Test / secure behavior | Acceptance evidence |
|---|---|---|
| T-07-01 | 07-01 browser_free/saved_baseline/max_count_saved_bytes | immutable原本/改変拒否/固定bytes比較 |
| T-07-02 | 07-01 max_count_internal_order/selection/discrimination | 別Counter/順序不変/共有pairs/元12 |
| T-07-03 | 07-01/02全CLI回帰 + 07-03/品質HTML | hostile/CR/UTF8/basename/静的安全性 |
| T-07-04 | 07-02 invalid_before_read/input_failure/empty | spy未呼出し・exit0/1/2区別 |
| T-07-05 | 07-02実permission/全HTML回帰 | native拒否・stdout空・path非露出 |
| T-07-06 | 07-02 readme_example | 指定1例実exit/stdout/stderr |
| T-07-07 | 07-03 browser_free/品質owner/ledger | 実actor/head/全画像・全view最終照合 |
| T-07-08 | 07-03実canary/通信原本 + 品質確認 | pre-open→実閲覧終了/failed含む全外部試行 |
| T-07-09 | 07-03 scope_contract/全suite | 基底blob/試験維持/実件数・exit |
| T-07-10 | 07-03 evidence_contract + 品質標準添付/PM | 文字原本hash/添付readback/PM read_file |
| T-07-SC | 全PLAN installなし/既存環境のみ | 依存/CI/設定不変、不足ならscope停止 |

ASVS1/high blockのまま。high mitigation未確認をpassedにせず、認証/DB/AI/外部APIは非該当。公式API/assumption negativeは07-01に記録、最終probes/独立checkerは親が実施する。

## Wave 0 Requirements
- [ ] Before production edits, inspect existing saved output and freeze any missing omission oracle/input/argv/cwd/env/exit/stderr. Never regenerate expected values from new implementation.
- [ ] 07-01-01で1.1全追加pytestを本体変更前に作成・実行し、未実装時の狙ったRED/自然GREENを保存・検証してから最小実装GREEN。README先行試験だけ1.3として07-02-02。後続単一変異は追加判別力であり先行REDの代替不可。
- [ ] If new baseline fixture or verifier/test driver is needed, PLAN explicitly creates it in same/earlier task, with nonzero failure assertions and standard Python/pytest execution. No no-op or synthetic evidence.
- [ ] Existing CPython3.12 pytest environment suffices; do not add dependencies/CI. PATH Python3.14 has no pytest; use recorded explicit environment.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|---|---|---|---|
| Actual HTML readability and image inspection | REQ-26,REQ-27 | DOM/pytest cannot substitute actual visual review | Quality independently generates HTML from target head; 1280x900 and 320x900 CSS px DPR1; compare same-condition pre-change states; inspect all images/tiles, raw Range, clipping, overlap, whitespace and injection candidates; track all document-caused request/failed-request/navigation/popup attempts. |
| Ownership/head and delivery | REQ-27 | evidence attribution not inferred from file presence | Quality records fresh head, source, actor, argv/input/exit/stdout/stderr, HTML/raw/image/network files; attaches VERIFICATION.md plus CLI/CI text proof and states viewed image count/content/result per AC. PM reads text only; no archive/image requirement. OpenSpec2.2 execution belongs to phase verification. |

## Validation Sign-Off
- [x] All final task IDs/commands mapped to saved 07-01..03 PLANs; command execution remains pending
- [ ] No missing command inputs at task completion
- [ ] Sampling continuity and no watch flags
- [ ] RED/GREEN and all existing suite results measured, not inferred
- [ ] Quality independent CLI/browser/image/network evidence and text attachment complete
- [ ] nyquist_compliant true only after official validate-phase verifies actual implementation

**Approval:** executable planning map saved. Official PLAN frontmatter/structure checks are separate from execution. Implementation, Nyquist completion, independent quality OpenSpec2.2, text-original delivery and phase acceptance remain pending.
