# Phase 04 — PLAN mapping / source audit

Status: 計画作成済み、実装/試験/baseline/独立品質/配送は未実施。依頼 r-e476c11d、承認 t_a438e6b2 run140、OpenSpec r-e476c11d-wordfreq-min-count。判定の基準は今回AC1〜7/REQ15〜21であり旧phaseのACとは別。

## Serial execution / needs→creates

| Wave / PLAN | Tasks | Needs | Creates / end-of-task usable verification | Checkpoint |
|---|---|---|---|---|
| 1 / 04-01 | 01-01,01-02 | 現行製品と既存検証環境 | 01-01 baseline/validatorのbrowser-free実装検証・公式task commit→01-02 clean head一度採取/封印・read-only gate。後続mode不要 | なし。D-07承認済みone-way、公式警告は下記 |
| 2 / 04-02 | 02-01,02-02 | 不変baseline gate、同一branch | 1.2 RED/GREEN→1.3/1.4両群先行RED→共通実装/両群GREEN。既存pytestから検証可能 | なし |
| 3 / 04-03 | 03-01,03-02,03-03 | baseline+min-count製品 | capture/保存validator→review-session/finalize/実ownerをbrowser-free検証・各公式task commit→03-03 clean head一度実capture/read-only照合 | なし。costly共有CLIは固定 |
| 4 / 04-04 | 04-01,04-02 | 全先行成果と実driver4mode | 統合capture一度採取/read-only照合→実runbook/browser-free contract・公式commit→最終head品質へ | なし。品質gateは別主体の後工程 |

すべて `argonauts/r-e476c11d` へ順に積み上げる。依存は04-01→04-02→04-03→04-04であり独立PLANと偽らない。PLANごとのverifyはそのtask又は先行taskで実在化するfile/inputのみ。baseline indexは04-01保存後不変。後で旧headをcheckoutして採り直す代用は禁止。新driverは公開CLIを改名しない。

**Revision B1/B2:** 01-01実装/verify→公式task commit→01-02採取開始/完了封印→read-only確認→02-01初製品変更のtimelineを原本へ結ぶ。03-01/02も実装/verify→各正式commit後03-03採取。dirty実行面拒否を維持しverify内commitなし。baseline/captureの一度限り生成はaction、全反復automatedはtests/test_min_count_verifier.pyのsaved_baseline/saved_captureで実rootの全原本をread-only照合。pytest専用 WORDFREQ_MIN_COUNT_BASELINE_ROOT / WORDFREQ_MIN_COUNT_CAPTURE_ROOT を各PLANのexact commandで束縛、root欠落/改変/0 collected/未検査は失敗。未指定の通常full suiteは保存root不要のbrowser-free回帰で、原本合格ではない。採取driver内full suiteへopt-in環境を継承せず再帰を防ぐ。新driver mode/flag追加なし、上書き/再採取/無検査成功なし。artifact commitで現headが進んでも採取headのgit tree/blob/原本整合を再検査し付替えない。最終品質は全doc/tests確定後の対象headでfresh runする。

**Revision W1:** browser-free pytestは先行高速feedback。01-02/03-03/04-01と独立品質の全browser/全suite/実閲覧/finalizeは必須高遅延full E2E統合gate、実行担当が開始/終了/所要時間・件数/env/argv/exitを別記する。未測定を30秒内/超の実績にせず必須case/両幅/独立品質は省略しない。

**TDDの重要順序:** 02-01はOpenSpec1.2のRED→引数実装→GREEN。02-02はOpenSpec1.3群と1.4群を両方追加し、それぞれ独立にREDを保存してから共通選択を実装し、両群を別々にGREENへする。1.4の既存空file等が先にGREENなら既存GREENと表示し、全除外/正totalの新REDを実装前に確保する。後付けRED/故意の製品破壊なし。

## OpenSpec task → PLAN / outputs

| OpenSpec | PLAN task | Completion evidence | Owner |
|---|---|---|---|
| 1.1 | 04-01-01/02 | baseline/index.json、全形式stdout/HTML/画像/env/head/input/argv/SHA、事前採取と不変gate | Builder |
| 1.2 | 04-02-01 | usage/input spy・実CLI全形式・help/README例、独立RED/GREEN | Builder |
| 1.3 | 04-02-02 | 共通pairs/正規化/閾値/top/非破壊の先行RED/GREEN、実期待pairs、ソース箇所 | Builder、ソース独立確認は品質 |
| 1.4 | 04-02-02 | 空/空白/句読点/全除外の先行RED/GREEN、元total0/正数、固定空形式/README | Builder |
| 2.1 | 04-04-01（03-01/02/03が前提） | 全suite件数/env/実argv/exit、変更前比較、今回scope、AC索引、read-only再検証 | Builder |
| 2.2 | 04-04-02のrunbook + independent_quality_gate | 品質自身の対象head CLI/browser/全画像実閲覧/baseline比較/ソース順序、台帳/最終owner結果、原本配送 | **品質のみ**。Builderのtask doneは手順完成まで |

## AC / requirement / decision correspondence

| AC | Requirement | D | Implementation | Automated evidence | Independent / delivery evidence |
|---|---|---|---|---|---|
| AC1 | REQ-15 | D-03/04/06/08 | 02-02、P1/P2/P3/P7/P8 | tests/test_cli.py全形式境界/Unicode/空matrix | 03-01/02実装→03-03採取→04-04 qualityの既定/部分/全除外/空 |
| AC2 | REQ-16 | D-07/09/10 | 01-01/02、02-01/02、B1〜4/P4 | 01-02 baseline→03-03 capture→04-01統合の全形式bytes比較/read-only再検査 | 同環境変更前/後画像、quality自分の再生成、原本PM読取り |
| AC3 | REQ-17 | D-01/02/08 | 02-01、P5 | 不正0/-1/1.5/abc/欠落、read_text未呼出しspy、有効2の入力失敗exit1 | suite/実CLI原本をAC3へも索引化、P6の未提示保証はbackstop |
| AC4 | REQ-18 | D-03/04 | 02-02、P7/P8 | casefold/同数初出順/独立top/指定順/Counter値とitems順 | qualityがtarget headのfilter→topソース行/diffを別に読む |
| AC5 | REQ-19 | D-05/06 | 02-02、P9/P10 | beta N2/top1とN4でtotal7、Zoo全除外5、抽出0語0、既存formatter回帰 | quality全除外/空両幅、basename/static/raw/copy不変 |
| AC6 | REQ-20 | D-08/09/10 | 01-01〜04-02、V1/V2/F1〜4 | 実suite正件数/環境/exit、driver拒否control/実owner/全CLI | quality別profile/fresh root/全画像、保存→標準添付→PM原本読取り |
| AC7 | REQ-21 | D-02/06/11/12 | 02-01/02、03-01、04-01/02、P10/F4/F5 | 最小README/実例/help、既存suite、今回baseの保護path/scope | 品質diff確認、同head CI有限回確認は後工程、未報告成功扱い禁止 |

REQ-15〜21は04-02/04-04のrequirements全項目に記載し、各補助PLANも実際に扱うREQを非空で持つ。

| Decision | PLAN task | Explicit coverage |
|---|---|---|
| D-01 | 02-01 | 正整数/既定/入力前exit2、top相互制約なし |
| D-02 | 02-01/02、03-01 | 有効2入力失敗exit1、保護source/tokenizer/formatter |
| D-03 | 02-02 | 正規化counts→閾値→stable top→共通pairs |
| D-04 | 02-02、04-02品質gate | 閾値等値/Zoo/Straße literal、品質source位置 |
| D-05 | 02-02 | 元Counter値/順非破壊、元total7/5/0 |
| D-06 | 02-02、03-01/02 | 既存空出力/CSS/copy/basename/UTF-8/escape/安全性 |
| D-07 | 01-01/02、03-01/03、04-01 | 変更前hard gate・不変index・未指定/1比較 |
| D-08 | 02-01/02、04-01 | 1.2/1.3/1.4先行RED、全形式/全suite/件数/exit |
| D-09 | 03-02、04-02品質gate | 実品質profile/独立再生成/両幅全画像/ソース確認 |
| D-10 | 01-02、03-02、04-02 | scope/head不流用、保存/標準添付/PM原本読取り別gate |
| D-11 | 02-01/02、03-01、04-01/02 | README最小・保護差分・新依存/CI/見た目等対象外 |
| D-12 | 04-01/02 | CI等担当カードへ、有限回/未報告pending非成功、背景等非要件 |

## UI14 → must_haves / task / evidence

すべて04-03のplain truth U01〜U14へlift。設計resolved/explicitと実受入は別。capture/validator実装03-01、live/ledger実装03-02、全実装正式commit後の実原本採取03-03、品質実閲覧04-04 independent_quality_gate。

| ID | Element/category | Truth | Evidence |
|---|---|---|---|
| UI01 | E1 overflow | U01 | 両幅h1 raw/clip/非重複+全画像 |
| UI02 | E1 long-text | U02 | 24px/600 computed/font+全文画像 |
| UI03 | E2 overflow | U03 | basename/total上配置/横収まり/clip/非重複 |
| UI04 | E2 long-text | U04 | 長basename/space/LF/TAB/CR/total raw+全画像 |
| UI05 | E3 empty | U05 | 空/抽出0/全除外0行と固定copy/元total |
| UI06 | E3 loading | U06 | 完成stdoutと静的Document/既存CSS差分 |
| UI07 | E3 error | U07 | 02-01実usage/input matrix、stdout空 |
| UI08 | E3 populated | U08 | 全形式pairs/3列/連番/元total、部分/top |
| UI09 | E3 partial | U09 | 表示制限だけ、静的Document/既存CSS/copy |
| UI10 | E3 overflow | U10 | 長語/数字の全Range/clip/列/非重複、raw無補正 |
| UI11 | E3 zero-one-many | U11 | 空/全除外/top1/複数/long12の3列と連番 |
| UI12 | E3 long-text | U12 | w256/順位10〜12/count123、全画像+raw |
| UI13 | E4 overflow | U13 | 両幅空文言raw/clip/非重複/全画像 |
| UI14 | E4 long-text | U14 | 固定空copy/既存サイズ/全文画像 |

UI原本の14 applicable = must_haves plain truths 14 + flagged 0。未分類0。画像の存在/DOM一致だけを閲覧証拠にしない。

## Edge30 — individual resolution (raw report preserved)

原本EDGE-PROBE.jsonは公式engineの生候補（unresolved）として変更しない。下表が今回の解決とmust_haves lift。E番号は原本items順。explicit truthは受入仕様として書けるという意味で、実試験PASSではない。

| Edge | requirement/category | Resolution | Canonical source / concrete acceptance | PLAN truth / task |
|---|---|---|---|---|
| E01 | REQ-15/boundary | resolved/explicit | D-04 beta N2/N3/N4、未満/ちょうど/超 | 02 P1 / 02-02 |
| E02 | REQ-15/adjacency | resolved/explicit | D-03/04 count=Nを残す、tie初出順 | 02 P1 / 02-02 |
| E03 | REQ-15/empty | resolved/explicit | D-06 空/空白/句読点/全除外の全形式exit0 | 02 P2 / 02-02 |
| E04 | REQ-15/ordering | resolved/explicit | D-03 初出順・共通pairs | 02 P2 / 02-02 |
| E05 | REQ-15/precision | resolved/explicit | D-01/04 既存intの整数比較、丸めなし、大きい有効Nは全除外 | 02 P3 / 02-02 |
| E06 | REQ-16/adjacency | resolved/explicit | D-07 未指定=1=変更前bytes、同数等値 | 02 P4 + 01 B1/B2 / 03-01実装,03-03採取,04-01統合 |
| E07 | REQ-16/empty | resolved/explicit | D-06/07 変更前空原本も既存空形式 | 02 P4 + 01 B3 / 01-02,03-03 |
| E08 | REQ-16/encoding | resolved/explicit | D-02/06/07 同入力UTF-8/正規化/全bytes互換 | 02 P4 / 03-01実装,03-03採取 |
| E09 | REQ-16/ordering | resolved/explicit | D-07 同数+10種類超、既定top10/初出順 | 02 P4 + 01 B3 / 01-02,03-03 |
| E10 | REQ-17/boundary | resolved/explicit | D-01 0/-1/1.5/abc/欠落前exit2、1有効 | 02 P5 / 02-01 |
| E11 | REQ-17/precision | resolved/explicit | D-01 argparse/int維持、非整数丸め受理なし | 02 P5 / 02-01 |
| E12 | REQ-17/concurrency | resolved/backstop | 中断/並列の新たな製品保証はCONTEXT/PRDになく創作不可 | 02 P6（flat statement/verification） |
| E13 | REQ-18/boundary | resolved/explicit | D-03/04 Nちょうど、top1/10と独立値 | 02 P7/P8 / 02-02 |
| E14 | REQ-18/adjacency | resolved/explicit | D-03/04 casefold合算後の等値保持 | 02 P7 / 02-02 |
| E15 | REQ-18/empty | resolved/explicit | D-06 閾値後0件でも共通pairs空 | 02 P8/P2 / 02-02 |
| E16 | REQ-18/encoding | resolved/explicit | D-04 Straße STRASSE→strasse2 | 02 P7 / 02-02 |
| E17 | REQ-18/ordering | resolved/explicit | D-03/04 Zoo初出順とfilter→top source記録 | 02 P8 / 02-02,04-02品質 |
| E18 | REQ-18/precision | resolved/explicit | D-01/03 整数N/top独立、大小/同値/指定順不変 | 02 P8 / 02-02 |
| E19 | REQ-19/boundary | resolved/explicit | D-05 beta N2/top1とN4でもtotal7 | 02 P9 / 02-02 |
| E20 | REQ-19/adjacency | resolved/explicit | D-05 元total≠表示和/種類数、N等値も元回数和 | 02 P9 / 02-02 |
| E21 | REQ-19/empty | resolved/explicit | D-05/06 全除外total正、抽出0語total0 | 02 P9 / 02-02 |
| E22 | REQ-19/ordering | resolved/explicit | D-05/06 totalは選択前、表上配置/表示連番 | 02 P9 + 03 U03/U08 / 02-02,03-01実装,03-03採取 |
| E23 | REQ-19/precision | resolved/explicit | D-05 回数和の整数、丸め/表示和への置換なし | 02 P9 / 02-02 |
| E24 | REQ-20/adjacency | resolved/explicit | D-09/10 exact image/raw/path/hash/台帳1対1 | 03 V1 / 03-02,04-02品質 |
| E25 | REQ-20/empty | resolved/explicit | D-08/09 0件suite/空台帳/未閲覧非成功 | 03 V2 / 03-01/02実装,03-03採取 |
| E26 | REQ-20/encoding | resolved/explicit | D-09/10 入力/argv/bytes/strictUTF8/raw/SHAの原本対応 | 03 V1 / 03-01/02実装,03-03採取 |
| E27 | REQ-20/ordering | resolved/explicit | D-07/09/10 baseline先行、live→実閲覧→flush/final→保存/添付/読取り | 03 V1/V2 + 04 F2/F3 / 04-02 |
| E28 | REQ-20/concurrency | resolved/explicit | D-09/10 別run/root/head混在や中断を未検証にする証拠契約（製品並列保証ではない） | 03 V2 / 03-02 |
| E29 | REQ-21/empty | resolved/explicit | D-06/11 既存空copyを変えずREADME閾値案内だけ | 02 P10 / 02-02 |
| E30 | REQ-21/encoding | resolved/explicit | D-02/06/11 既存UTF8/casefold/escape/formatter/source不変 | 02 P10 / 02-01/02,03-01 |

**No-silent-drop arithmetic (jqで原本件数確認):** 30 applicable = 29 explicit + 1 structured backstop + 0 unresolved/unclassified flagged。REQ別件数は15:5、16:4、17:3、18:6、19:5、20:5、21:2。UIは別集合14、混算しない。

**残留P6:** backstopを実証できなければverify-phaseはhuman_needed / insufficient_specへabstainする。新しい中断時atomic stdout/並列性能・順序の保証は作らない。PRDの単発CLI/証拠run分離の具体要件は他truthで完全に扱う。E12を黙ってexplicit/passへ変換しない。

## Prohibition recall — §B/§C precision audit

公式specless-probe-fallback.md §B/§Cとprohibition-probe.mdを適用。以下はStage1候補を省略せず分類したbreadcrumb。列の10候補は新しい禁止仕様ではなく、routine engineering/既存契約/canonへの帰属確認。

| Requirement | Stage1 recall candidates | Precision disposition |
|---|---|---|
| REQ-15 | 閾値誤差、等値除外、丸め、空例外、形式差、sort不安定、Counter破壊、Unicode分割、top順序逆転、partial stdout | routine工程をdrop→P1/2/3/7/8とpytest。partialの新atomic保証はE12 backstopへ |
| REQ-16 | 後撮りbaseline、変更後同士比較、input改変、basename変更、argv差、環境差、幅欠落、SHA不一致、default変更、tie変更 | 既存D-07/09契約B1〜4/P4/driverで保持。新bespoke prohibitionとしてmintしない |
| REQ-17 | 入力先読、0受理、負数受理、小数丸め、欠落受理、stderr消失、stdout混入、read失敗を空化、桁数独自制限、top相互制約 | routine工程drop→P5/usage/input/spy試験。int境界はD-01既存規則 |
| REQ-18 | lexical復帰、set順、casefold後回し、Counter破壊、filter後回し、top依存、引数順依存、同数再配置、形式別経路、source未確認 | routine工程drop→P7/P8と品質ソース確認 |
| REQ-19 | 表示和total、種類数total、全除外0、空total正、copy変更、CSS変更、path漏洩、語注入、外部resource、UTF8破壊 | 前6/UTF8は既存D-05/06/11→P9/P10。path/注入/外部経路はcanon securityへbreadcrumb |
| REQ-20 | Builder自己承認、未閲覧readable、head流用、root混在、0件suite成功、観測unknown無視、原本欠落、添付だけでPM可読、遅い通信無視、部分marker成功 | すべて既存D-08/09/10の証拠契約V1/V2/F1〜4で保持。新mustNOTを創作しない |
| REQ-21 | 依存追加、CI追加、テーマ追加、入力元追加、抽出変更、全体refactor、権限変更、外部送信、課金、削除 | D-11の既存明示範囲禁止を保持。新しい禁止への格上げではない |

Canon breadcrumb: HTML injection / path disclosure / unauthorized external transmissionはcanon security — `/gsd-secure-phase`の監査領域と各PLANのASVS1 threat_model・既存静的監査/pytest/browser observerで扱う。prohibitionとして新規mintしない。dropはsecurity義務の除去ではない。

Stage2後に新しく残るbespoke mustNOTは0（新must_haves.prohibitionsは空、descriptor発明なし）。もし後工程で新bespoke prohibitionが出たらdescriptor-less flagged-unverifiedとして親へ返す。既存明示禁止D-11/12を破ってよいという意味ではない。

## Multi-source coverage audit (GOAL / REQ / RESEARCH / CONTEXT)

| SOURCE | ID / content | PLAN | Status |
|---|---|---|---|
| GOAL | 全形式min-count/閾値→top/元total/既定互換/見た目安全性/独立可読証拠 | 01〜04 | COVERED |
| REQ | REQ-15 | 02,03,04（上表AC1） | COVERED |
| REQ | REQ-16 | 01〜04（上表AC2） | COVERED |
| REQ | REQ-17 | 02,04（上表AC3、P6明示backstop） | COVERED |
| REQ | REQ-18 | 02〜04（上表AC4） | COVERED |
| REQ | REQ-19 | 02〜04（上表AC5） | COVERED |
| REQ | REQ-20 | 01〜04（上表AC6） | COVERED |
| REQ | REQ-21 | 01〜04（上表AC7） | COVERED |
| RESEARCH | 最小CLI合成/元Counter別mapping/安定sort/純formatter | 02 | COVERED |
| RESEARCH | argparse/int/入力優先度/permission実EACCES/独立literal oracle | 02 | COVERED |
| RESEARCH | 製品編集前baseline・全形式bytes/同環境画像・不変索引 | 01,03,04 | COVERED |
| RESEARCH | 旧scope/head/AC固定部を使わず汎用部品だけ再利用 | 01,03 | COVERED |
| RESEARCH | 空結果RED先行、既存GREENを捏造REDにしない | 02 | COVERED |
| RESEARCH | raw/実font/全画像/通信canary/live/late flush | 01,03,04 | COVERED |
| RESEARCH | 0件suite/actor/dirty実行面/scope ref欠落のfail-closed | 01,03,04 | COVERED |
| RESEARCH | 新installなし、既存Python3.12+承認env利用、管理scratch短pathのみ | 01〜04 | COVERED |
| RESEARCH | 独立品質能力/PM原本読取り、head変更は全面再実行 | 04 | COVERED |
| RESEARCH | LOW confidenceの未実行browser/suite/CIを実測する | 01,03,04と後続CI担当 | COVERED |
| CONTEXT | D-01〜D-12 | 上のdecision全件対応表 | COVERED |

Deferred/Q-01/Q-02/A-01〜04/新依存/CI編集/新UI/入力源/形態素解析/全体refactor/旧phase修復は計画から除外（MISSINGではない）。学習原本の注意はRESEARCH/PATTERNSの具体ルールとして反映し、過去合格の流用はしない。

## Official discovery / capability / verification status

- 公式役割全文とrequired_reading全件、追加reference読了。Level0: 新外部依存なし、現行コード/承認design/既存pytest・verifierに沿う。HERMES.mdは不存在。追加agent-skillsは呼出し元で空、project skill不存在はRESEARCH/PATTERNSの調査入力。勝手に追加しない。
- PLAN-PRE-CONTRIBUTIONS.jsonのinto=planner fragment.inlineはjqで全文抽出して適用。security ASVS1/block_on high、各PLANにT-04-01〜12と予約T-04-SC。API detector false（exit1は正常negative）、assumption-delta false、schema-relevant fileなし、AI統合なしは親の確定結果。active driftはcontext skipped no-upstream-artifacts / codebase skipped no-structure-md。UI frontend=true/hasUiSpec=true/block=false。監査設定は変更なし。
- 公式estimate-calibration: factor1/applied=false/sample_count0/confidence low。各estimateはrawと同値、予測であり実績ではない。
- 公式history-digestを読み、Phase3の実CLI/bytes/初出順/全view lifecycle/actor/原本証拠を継承。旧scope/ACと合格結果は継承しない。公式graphify statusはdisabled=true、graphを有効化しない。
- 初版の公式frontmatter/structureは4PLAN valid:trueだった。revisionでは04-03を3taskへ分離、ほかは2taskを維持。修正版の公式structural query結果は本revisionの実出力を根拠に親へ返し、初版結果を再検査済みと流用しない。04-01の承認済みD-07 one-way警告は保持、追加checkpoint不要の既決境界を変えない。
- Git branch変更/commit/push/Kanban/実装/pytest/browser実行/未作成driver試走/補助script作成は計画工程で行わない。親が別checkerを呼ぶためここではcheckerを呼ばない。
- PATTERNSのtracked analog所属は計画中未確認。01-01でprovenance記録を実装し、01-02の正式head/baseline採取で実確認する。未確認を完了扱いしない。

**Revision B3:** 04-RESEARCH Open Questions全5件にRESOLVEDを追記。driver path/固定CLIと各作成/正式commit/採取task、環境・件数/時間・品質能力/配送・現head CIの未実施gate/担当、Q-01/Q-02の承認済み非blocker非要件処置を確定。RESOLVEDは処置先の確定であり、製品/pytest/browser/CIの実行合格を意味しない。

## Residual gates / assumptions

1. P6 REQ-17/concurrencyはstructured backstop。新仕様を作らず、必要ならhuman_neededとして残す。
2. baseline保存/実browser起動/字体/全pytest件数・時間/品質閲覧能力/PM配送可読性/現head CIは実行担当が確認する未実施事項。未達なら停止/gaps。
3. 2.2品質受入はrunbookができただけでは完了しない。品質実行・標準添付・受取PM読取りが必要。既存CIは該当担当カードで有限回確認、未報告成功扱いなし。
4. 文書のみでもheadが動けば品質はfresh rootで全面再実行。旧phase1/3 staleを今回範囲へ混ぜない。
5. 公式structure照会は計画構造だけの確認。実装正しさ・全AC受入・独立checker PASSは未主張。
