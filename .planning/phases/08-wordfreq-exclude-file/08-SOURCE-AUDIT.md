# Phase08 Source Audit — 計画上の網羅、実装/品質合格ではない

## Authority / input / discovery

- 対象: 承認t_0d1aa16a、原本head `8a2c69b8332e9704377fe680af51767c74e4ab56`、OpenSpec r-6442a149-exclude-file。今回のcheckoutは指定worktree。公式`query init.phase-op 8`で08存在/context/researchあり/初回planなしを確認。
- 必読STATE/ROADMAP/REQUIREMENTS/CONTEXT/RESEARCH/PATTERNS/UI-SPEC/VALIDATION/結合PRD/learnings/plan-init/plan-pre-hooks/edge-probeと公式specless/prohibition referenceをread_fileで読了。pre-hooksのactive contribution into plannerのfragment.inlineはjq -rで全文抽出して適用。製品判断を追加しない。
- repo直下HERMES.mdと.hermes/HERMES.mdはread_fileでnot_found。追加AGENT_SKILLS_PLANNERは公式query空という呼出し元結果を採用。研究・patternのproject skillなしという確認を継承し、推測で追加しない。
- Discovery Level0: 既存標準ライブラリ/4+1モジュール内の実装。現在の__main__/sources/formatters/既存test_sources/test_cli/README/承認architectureを直接読み、研究と同じ境界・部品・pytest helperを確認した。新依存・新サービスを選ぶ調査は不要。`git ls-files -- wordfreq tests README.md pyproject.toml .github/workflows/pytest.yml _bmad-output/initiative-r-6442a149/architecture/architecture.md openspec/changes/r-6442a149-exclude-file`で使用既存pathの追跡を確認。
- 公式history-digestを取得し、現行部品/初出順/HTML/min-count/証拠原本の系譜を把握。現在の正本CONTEXTとコードを優先する。Phase7はdescriptionの説明メタデータであり、変更1行制限/専用検証2コマンド/unverifiedを今回へ流用しない。旧Phase1の語昇順は現在の初出順へ戻さない。旧phase検証の再開をしない。
- `query graphify status`はdisabled=true。設定を変更せずgraphなしで正本とコードを使用。
- estimate-calibration: factor1、sample_count0、confidence low。raw見積34000/30000をfactor1で適用し、それぞれPLANに記載。推定は実測コスト/所要時間ではない。
- 書込み許可: 新PLAN2件、本監査原本、VALIDATION正式task対応のみ。既存dirty文書を復元/上書きしない。ROADMAP/STATE/親metadata/tasksチェックは親に委ね、commit/push/Kanbanなし。

## Dependency / executable task graph

| Task | Needs | Produces / 利用者が得るもの | Wave / checkpoint |
|---|---|---|---|
| 08-01-01 | 既存CLI/source/formatter/pytest2モジュール/README | 正常除外の全形式実CLI/loader/help/README再現例 | 1 / なし（D-01/08人承認済み） |
| 08-01-02 | 08-01-01の実コードとassert | 行文法/Unicode/重複/最後FILE/未指定相当一覧の確定 | 1内直列 / なし |
| 08-01-03 | 先行2taskの実コードとassert | 閾値/top/全語除外/HTML総数と計数前spy | 1内直列 / なし（D-06/08人承認済み） |
| 08-02-01 | 08-01全成果 | 読込失敗と二入力優先の実CLI/直接spy/説明 | 2 / なし（D-04人承認済み） |
| 08-02-02 | 先行4taskの実assert | 全件/未指定互換/安全性/Builder原本と別主体品質handoff | 2内直列 / なし |

08-02 depends_on [08-01]。同じ依頼branch argonauts/r-6442a149へD.3順の直列積上げ。各task最大5変更ファイル、各PLAN最大3task。同README/CLI/testを同waveで別PLANへ割らない。新assertをtask内で先に実在ファイルへ書きRED→GREEN。先行で既にGREENならscratchコピーの最小変異で判別力REDを記録し、実worktreeへ故意の変異を注入しない。後続の未作成テストを試験前提にしない。

## Multi-source audit

COVEREDは計画の割当であって実装・試験合格ではない。

| SOURCE | ID | Feature / constraint | Plan/task | Status / notes |
|---|---|---|---|---|
| GOAL | Phase08 | 全形式除外/行/casefold/順序/失敗/総数/互換/説明/独立品質文字原本 | 08-01全task→08-02全task | COVERED |
| REQ | REQ-28 | 共通除外/重複/相対初出順/最後FILEのみ | 08-01-01/02/03,08-02-01 | COVERED |
| REQ | REQ-29 | BOM/strip/空/#/改行/非分割 | 08-01-02 | COVERED |
| REQ | REQ-30 | 本文維持/両側casefold/実Unicode | 08-01-02 | COVERED |
| REQ | REQ-31 | 引数→採用除外→本文/4原因/exit2/1 | 08-02-01 | COVERED |
| REQ | REQ-32 | help/README/再現例と対応試験 | 08-01-01,08-02-01 | COVERED |
| REQ | REQ-33 | 全語除外の既存形式/未指定互換/全件 | 08-01-03,08-02-02 | COVERED |
| REQ | REQ-34 | 依存/権限/送信不追加/独立品質文字原本/標準添付 | 08-02-02/handoff | COVERED、独立品質は後工程pending |
| REQ | REQ-35 | 除外→計数→min/top/除外後選択前total/未指定旧total | 08-01-01/03,08-02-02 | COVERED |
| CONTEXT | D-01 | 共通除外と最後FILE | 08-01-01/02,08-02-01 | COVERED |
| CONTEXT | D-02 | 専用行解釈 | 08-01-02 | COVERED |
| CONTEXT | D-03 | casefold | 08-01-02 | COVERED |
| CONTEXT | D-04 | 失敗と順序 | 08-02-01 | COVERED |
| CONTEXT | D-05 | 説明/試験、OpenSpec2.1/2.2/3.1 | 08-01全task,08-02全task | COVERED、1.1は再実行しない |
| CONTEXT | D-06 | 全語除外/未指定互換 | 08-01-03,08-02-02 | COVERED |
| CONTEXT | D-07 | 範囲と品質/文字証拠/画像実閲覧 | 08-02-02/handoff | COVERED |
| CONTEXT | D-08 | 処理順/total/HTML継承 | 08-01-01/03,08-02-02 | COVERED |
| RESEARCH | boundary / AD-1〜4 | CLI統括/source専用取得/本文変更なし/pairs共通/formatter純粋 | 08-01-01/02/03,08-02-01 | COVERED |
| RESEARCH | parser | parse中に開かず最後文字列値だけ取得 | 08-01-01/02,08-02-01 | COVERED |
| RESEARCH | codec | 除外だけstrict utf-8-sig、本文utf-8/原因連鎖維持 | 08-01-01/02,08-02-01 | COVERED |
| RESEARCH | probes | 直接集合/パス付きspy/count前token消費/実CLI全形式 | 08-01-02/03,08-02-01 | COVERED |
| RESEARCH | explicit oracle | 期待値を製品で再計算しない/総数3対5対2 | 08-01-01/03 | COVERED |
| RESEARCH | security | read-only/strict/失敗後I/Oなし/HTML path非露出/escape | 両PLAN threat_modelと08-02-02 | COVERED、ASVS1/high block |
| RESEARCH | regressions | hashseed0/1/42/両入力不変/全件/保存baseline不変 | 08-02-02 | COVERED |
| RESEARCH | env / Wave0 | 既定python pytestなし、既存代替、既存ファイルへassertを先に追加 | 全task | COVERED、新framework/conftest/driverなし |
| RESEARCH | documentation | 正常/異常help/READMEと実CLI例 | 08-01-01,08-02-01 | COVERED |
| RESEARCH | evidence | head/env/入力/argv/stdout/stderr/exit/条件別結果と独立品質 | 08-02-02 | COVERED、未実行/未配送はpending |
| RESEARCH | assumptions A1/A2 | 所要時間/品質環境未実測 | 08-02-02/handoff | COVERED、品質version再確認・欠測未検証 |
| RESEARCH | scope | 旧collector固定scope/旧phase未達を混ぜない/OQ7/8は背景 | 両PLAN/品質handoff | COVERED、追加条件なし |

## Approved scenario audit

| Source scenario | Fixed expected value / assertion | Task |
|---|---|---|
| EX-1 全出現 | Zoo apple APPLE zoo banana/apple→zoo2,banana1,total3 | 08-01-01 |
| EX-1 top前 | 同本文/zoo/top1→apple2 | 08-01-03 |
| EX-1 重複/初出順 | beta apple alpha/重複apple→beta1,alpha1、単一一覧と同じ | 08-01-02 |
| EX-1 無一致 | 全形式stdout/exit/stderr未指定一致 | 08-01-02 |
| EX-1 最後FILE | missing→valid成功/逆順2/最後空は前一覧無効、前FILE未読spy | 08-01-02,08-02-01 |
| EX-2 空/コメント | apple marker banana/空,#marker,apple→marker1,banana1、集合に空/#なし | 08-01-02 |
| EX-2 有効項目なし | 空/空白コメント一覧=未指定 | 08-01-02 |
| EX-2 BOM/strip/改行 | 先頭BOM/空白/#marker/APPLEのLF・CRLF・終端なし→同上 | 08-01-02 |
| EX-2 行全体 | foo bar foo_bar 123 foo-bar apple note/指定5行→foo2,bar2,apple1,note1 | 08-01-02 |
| EX-3 ASCII | Apple APPLE apple banana/aPpLe→banana1 | 08-01-02 |
| EX-3 Unicode | STRASSE Straße banana/StraßeとSTRASSE各一覧→banana1 | 08-01-02 |
| EX-4 不存在 | 読める本文/missing除外→2/空stdout/対象原因stderr | 08-02-01 |
| EX-4 他原因 | permission/directory/decode全形式→同上、直接原因連鎖 | 08-02-01 |
| EX-4 複合 | 全無効引数は両FILE未読、両FILE失敗は除外のみ2、除外成功後/未指定本文4原因は1、help未読 | 08-02-01 |
| EX-6 全語除外 | Apple apple/apple→text空/json []+LF/HTML0行/既存案内/total0/exit0 | 08-01-03 |
| EX-5 案内 | help構文/全行規則/失敗/空、README json例zoo2とLF、HTMLtotal3 | 08-01-01,08-02-01 |
| EX-5 回帰 | 既存全件＋新assert、未指定全契約・入力不変・seed同一 | 08-02-02 |
| HTML-2 top可変 | zoo apple zoo banana apple cherry、top1:zoo2、2:zoo2/apple2、10:4行、全てtotal6 | 08-01-03 |
| HTML-2 別頻度 | beta beta beta alpha gamma alpha delta/top2→beta3,alpha2,total7 | 08-01-03 |
| HTML-2 既定/不正 | 11種類以上で既定10、top超過で残存全件、0/負/非整数は2/HTMLなし | 08-01-03,08-02-01 |
| HTML-2 min/top | 上記beta/min2/top1→beta3,total7、min4→0行,total7 | 08-01-03 |
| HTML-2 除外後 | Zoo apple APPLE zoo banana/apple/min2/top1→zoo2,total3 | 08-01-03 |

## Spec-less edge fallback: 25候補を全てexplicit truthへlift

設定キー未指定defaultON。shared spec-sectionのedges/prohibitionsはともにsupplied=false、EDGE_ABSENT=1/PROHIB_ABSENT=1（親の公式判定を受領）。原本 `.planning/argonauts/r-6442a149-edge-probe.json` はapplicable25/unresolved25/unclassified0で保存済み。この原本は上書きしない。下表のresolved(explicit)は**設計上の受入条件の解決**であり、実装試験の合格ではない。各E-IDは対応PLAN frontmatter must_haves.truthsへそのまま載る。未分類/未定義を黙って落としたものはなく、backstopは不要。concurrencyは承認済み単発CLIの効果順序だけで解決し、並行/割込の新保証を発明しない。

| Edge | Requirement/category | Defensible resolution / source | Lift / task |
|---|---|---|---|
| E01 | REQ-28 adjacency | 正規化重複は無影響、EX-1重複/D-01 | 08-01 truth / 08-01-02 |
| E02 | REQ-28 empty | 空/コメント/無一致=未指定、最後空は前一覧無効、EX-1/2 | 08-01 / 08-01-02 |
| E03 | REQ-28 ordering | beta1,alpha1相対初出順、EX-1/D-01 | 08-01 / 08-01-02 |
| E04 | REQ-28 concurrency | 単発引数→最後除外→本文、前FILE未読、D-01/04/AD-4 | 08-01 / 08-01-02,08-02-01 |
| E05 | REQ-29 adjacency | foo bar/foo-bar/apple#noteは非分割、EX-2/D-02 | 08-01 / 08-01-02 |
| E06 | REQ-29 empty | strip空/#は集合不在、EX-2直接検査 | 08-01 / 08-01-02 |
| E07 | REQ-29 encoding | strict UTF-8-sig/先頭BOMのみ/3改行型/行casefold、D-02 | 08-01 / 08-01-02 |
| E08 | REQ-29 ordering | 一覧集合は所属判定のみ、本文相対順保持、D-01/02 | 08-01 / 08-01-02 |
| E09 | REQ-30 empty | 空一覧比較なし、全語除外exit0、EX-2/6 | 08-01 / 08-01-02/03 |
| E10 | REQ-30 encoding | 実Straße/STRASSE両側casefold、EX-3/D-03 | 08-01 / 08-01-02 |
| E11 | REQ-31 empty | 値欠落引数2・I/O0、空一覧成功→本文、D-04 | 08-02 / 08-02-01 |
| E12 | REQ-31 encoding | 除外decode2/本文decode1、EX-4/D-04 | 08-02 / 08-02-01 |
| E13 | REQ-31 concurrency | 単発の引数→除外→本文、失敗後後段0、EX-4/AD-4 | 08-02 / 08-02-01 |
| E14 | REQ-32 empty | help/READMEが既存空結果/exit0を説明、EX-5/6 | 08-01 / 08-01-01/03 |
| E15 | REQ-32 encoding | help/READMEが一覧UTF-8/BOM/行/casefoldを説明、EX-5 | 08-01 / 08-01-01/02 |
| E16 | REQ-33 adjacency | 閾値ちょうど残す/未満除外/残存全件top、旧契約維持D-06 | 08-01 / 08-01-03 |
| E17 | REQ-33 empty | 全語除外0/既存案内/各既存空形式、EX-6 | 08-01 / 08-01-03 |
| E18 | REQ-33 encoding | 本文Unicode抽出/casefoldと書式/escape/CR保持、D-06/08 | 08-01 / 08-01-03,08-02-02 |
| E19 | REQ-33 ordering | 回数降順/初出順→top維持、D-06 | 08-01 / 08-01-03,08-02-02 |
| E20 | REQ-34 concurrency | 単発CLIの無追加/対象headの別主体再実行、D-07/RULE-2 | 08-02 / 08-02-02 |
| E21 | REQ-35 boundary | apple除外min1/2/3でtotal3、min2/top1=zoo2、D-08 | 08-01 / 08-01-03 |
| E22 | REQ-35 adjacency | 正規化全出現の計数前除外→閾値→top、D-08/AD-1 | 08-01 / 08-01-03 |
| E23 | REQ-35 empty | 全語除外0と表示だけ空で正total保持を区別、EX-6/HTML-2 | 08-01 / 08-01-03 |
| E24 | REQ-35 ordering | count前tokens→min→top→共通formatterのspy、D-08/AD-1 | 08-01 / 08-01-03 |
| E25 | REQ-35 precision | counts整数和、3対5対2、未指定6/7、D-08/HTML-2 | 08-01 / 08-01-03 |

No-silent-drop: probe25 = PLAN explicit truths25 + flagged assumptions0。機能検証は全25未実行、原本probeのunresolvedを実行合格へ改変しない。

## UI Considerations: 14 explicit状態を全てlift

UI原本のE1〜E4要素はedge E-IDとは別namespace。U01〜14は08-02 must_haves.truthsの各独立文字列。全状態の検査/品質表を08-02-02に割当て、機能上の空/順序/総数は先行08-01-03も検査する。CSS/DOM照合と実描画/実可読性は区別し、画像取得時は品質本人が全画像を閲覧して枚数/内容/結果を文字化する。旧phase全ブラウザ再検証/新デザインを追加条件にしない。

| Truth | UI category/element | Source / resolution | Task |
|---|---|---|---|
| U01 | overflow E1 | UI-SPEC150、h1自然折返し/省略clip重複なし | 08-02-02 |
| U02 | long-text E1 | 151、24px/600全文/縮小なし | 08-02-02 |
| U03 | overflow E2 | 152、本文basename/totalは表上、横収まり/非重複 | 08-02-02 |
| U04 | long-text E2 | 153、長basename/空白/LF/TAB/CR/数値全文 | 08-02-02 |
| U05 | empty E3 | 154、全語除外0、min表示0は除外後total保持 | 08-01-03,08-02-02 |
| U06 | loading E3 | 155、完成HTMLのみ/loadingなし | 08-02-01/02 |
| U07 | error E3 | 156、stdout空/stderr/除外2本文1/HTMLなし | 08-02-01 |
| U08 | populated E3 | 157、共通pairs3列/順位1始まり/total | 08-01-03,08-02-02 |
| U09 | partial E3 | 158、表示制限は完成データ/追加UIなし | 08-02-02 |
| U10 | overflow E3 | 159、既存列/CSS折返し/横収まり/clip重複なし | 08-02-02 |
| U11 | zero-one-many E3 | 160、0/1/複数のmetadata/caption/thead/列順/欠番なし | 08-01-03,08-02-02 |
| U12 | long-text E3 | 161、長語/複数桁数値の全文/既存サイズ | 08-02-02 |
| U13 | overflow E4 | 162、空案内折返し/横収まり/非重複/clipなし | 08-02-02 |
| U14 | long-text E4 | 163、既存案内全文/置換省略縮小なし | 08-01-03,08-02-02 |

UI probe14 = authored truths14、計画上explicit14。製品表示/画像閲覧合格を意味しない。

## Prohibition fallback — recall → precision → canon referral

公式prohibition-probe.md全文を読み、全REQに「作者が望まないものへ黙って変質し得るか」を適用した。下記は各REQのadversarial recall候補。列内の10候補はraw候補であり製品追加要件ではない。

| REQ | Stage1 raw recall（10候補） | Stage2 / canon referral |
|---|---|---|
| 28 | 前FILE読込、一覧合併、重複増幅、同数語昇順化、形式別除外、top後削除、全出現未除外、集合出力順、無一致で変化、遠隔一覧収集 | 前9は通常正確性/edge E01〜04、DROP。遠隔一覧収集は安全性/プライバシーcanon、ASVS/gsd-secure-phaseへreferral、T-08-01/08で既存ローカル範囲を検査 |
| 29 | BOM残留、全行BOM除去、strip欠落、コメント残留、空文字残留、CR残留、終端行欠落、行分割、途中#除去、不正bytes黙認 | 全て通常入力正確性/edge E05〜08とstrict decode制御、DROP。不正入力検証canonはASVS/gsd-secure-phase、T-08-01/05へreferral |
| 30 | lower化、ASCIIのみ、ß不一致、本文正規化変更、本文抽出変更、追加NFKC、一覧casefold欠落、重複キー誤処理、空項目一致、元表記推測復元 | 全て既存正規化/等値の通常正確性、E09/10と承認D-03のassertへ、DROP。独自の価値/公平性制約はこの単語utilityに根拠なし |
| 31 | 本文先読、引数前I/O、exit1誤用、exit2誤用、stdout部分漏れ、対象なし診断、原因なし診断、decode握潰し、権限昇格、shellパス評価 | 前8は正確性/失敗順序E11〜13、DROP。権限昇格/shell injectionはcanon、ASVS/gsd-secure-phaseへreferral、T-08-04/05/08 |
| 32 | 構文省略、行規則誤記、casefold誤記、最後FILE誤記、失敗コード誤記、空結果誤記、再現不能例、本文と一覧混同、HTML copy変更、案内に外部追跡URL追加 | 前9は文書と仕様の通常一致検査E14/15/D-05、DROP。外部追跡はprivacy canon、ASVS/gsd-secure-phaseへreferral、T-08-06/08。新しい文言価値制約は発明しない |
| 33 | 空結果専用化、JSON LF欠落、text空でない、空HTML表消失、旧案内消失、Unicode退行、同数順退行、min/top退行、入力書換え、HTML注入 | 前9は通常互換/edge E16〜19/既存回帰、DROP。HTML injectionはcanon、ASVS/gsd-secure-phaseへreferral、T-08-02/06 |
| 34 | 新依存導入、製品chmod、遠隔送信、旧head転記、実行者混同、環境欠落、入力原本欠落、exit欠落、未実施を成功記録、圧縮だけ配送 | 依存と最後7は今回明示D-07の工程正確性/証拠契約で既にQ02/E20・handoffに直接検査割当、追加の推論禁止条件に重複mintしない。chmod/遠隔送信はcanon、ASVS/gsd-secure-phaseへreferral、T-08-07/08 |
| 35 | 元total使用、種類数total、表示和total、min後total、top後total、計数後削除、top先行、順位欠番、未指定total変更、除外パスmetadata | 前9は通常データフロー正確性/edge E21〜25、DROP。パス露出はprivacy canon、ASVS/gsd-secure-phaseへreferral、T-08-02/06 |

Stage2結果: utilityの正確性/明示済み工程契約/canon以外のbespokeなvalues/safety/ethics候補は0。新製品条件を発明しないためkept prohibitionsは空（自動dismissで解決した項目はない）。projectProhibitionsへ渡すkept itemsが空なのでPLANに非空prohibitionを手書きしない。未検証禁止事項をresolved扱いしていない。将来keptを足す必要が生じたら公式projectProhibitionsの投影契約でdescriptorless・flagged-unverifiedを維持し、check_*を捏造せず親へ差分を返す。今回の実装安全性と証拠契約は通常truth/threat modelで引き続き必須。

## Active planner contributions disposition

| Contribution | Actual disposition |
|---|---|
| ai-integration / API coverage | 公式`query check api-coverage-verify-pre .planning/phases/08-wordfreq-exclude-file`でdetected=false/passed=true/block=false、matrix不要。ローカルCLIのみで外部API/SDK/serviceなし。skippedを偽のnegativeへ変換していない |
| assumption-delta | 公式`query assumption-delta scan 8 --json`でdetected=false/signals空。checkpoint非該当、identity一般化を新設しない |
| schema-gate | CONTEXT/RESEARCH/PLANの対象はPython/README/pytest/工程文字原本。Payload/Prisma/Drizzle/Supabase/TypeORMのschema pathなし。DB/ORM/移行なし、push taskは非該当 |
| security | 両PLANにASVS1/high blockのthreat_model。T-08-01〜08はphase内重複なし、T-08-SCのみ予約共有。READ-only/strict/失敗後I/Oなし/HTMLパス非露出/escapeを新assertへ紐付け。AI/model integrationなしでAI-SPEC不要。設定変更でgate回避しない |

## 親による最終gate追記

上記のcould-not-parseと補助投影はplanner実行時の履歴。親は製品判断を変えず、08-CONTEXTのD-01〜08見出しだけを公式の `- **D-01:**` bullet書式へ直した。原本に対する公式decision-coverageを再実行しexit0・passed:true・total8/covered8/uncovered[]を確認した（`.planning/argonauts/r-6442a149-decision-coverage.json`）。独立checkerは同じ最終PLANの内容と原本8判断を照合しVERIFICATION PASSED/全指摘0。親のpost-planning公式gateもREQ8+D8=16/16 covered。PLANのSHAは不変。詳細と独立委任IDは `.planning/argonauts/r-6442a149-PLAN-VERIFICATION.md` を参照する。

## Verification status at planning

- 機能/回帰pytest、README CLI例、ブラウザ/画像、独立品質は現工程で**未実行**。ここに実装件数/成功値を記入しない。
- PLANのautomatedは全て既存tests/test_sources.py/test_cli.pyまたは既存tests全件。新assertが先に追加されてからBuilder/品質が実行する。pytest実行系は研究実測代替 `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` を完全形で記載。今回に無関係なdescription専用prior_verify_commandsは不採用。
- 公式frontmatter.validate/verify.plan-structureは両PLAN valid=true。one-way checkpoint警告は3taskに出るがD-01/D-04/D-06/D-08の人承認済み例外を各reversibilityに明記し、役割公式規則Already settledに従う。新しい一方通行判断は追加していない。
- 公式verify-failure-directionsは7commands全てok、blocker0/warning0。verify-command-pathsは7commands not_applicable、blocker0/warning0（この環境付pytest形式をCLIが解析対象にしていないため、path実在はgit ls-files/read_fileと研究のversion実測で別に根拠化、CLIがpytestを実行/検証したとは呼ばない）。
- decision-coverage-plan初回はcontext引数不足、次はphase番号でなくdirectory指定が必要という呼出し誤りを訂正した。最終の正しい公式呼出しは `query check decision-coverage-plan .planning/phases/08-wordfreq-exclude-file --context .planning/phases/08-wordfreq-exclude-file/08-CONTEXT.md`。原本の`### D-NN:`見出しを公式parserが抽出できず、could-not-parseのまま。原本を改変しない。同じ8判断をbullet形式へ投影した計画監査原本08-DECISIONS-PROJECTION.mdに対して同gateを再実行しpassed=true/total8/covered8を確認した。これは計画の引用網羅の補助証拠であり、元CONTEXTのparse障害を修正済み/原本gate合格と呼ばない。親のcheckerへこの制約を渡す。
- ui-plan-gateはhasUiSpec=true/block=false。公式frontmatter getのmust_haves出力をjqで抽出しE01〜E25各1件/edge_count25、ui_count14を確認した（08-PLAN-CHECK-lift-counts.json）。公式init.plan-phaseの最終返値はplan_count2/phase_status Planned、threat_id_duplicate_count0。
- 最終構造/決定対応等の公式返値は `08-PLAN-CHECK-*.json` に保存し、親のplan checkerへ渡す。実装と品質の未検証状態は変更しない。製品/試験/README/pyproject/既存CIのgit diff --statは空。新規PLAN2件・監査/公式返値・VALIDATION正式対応だけを今回保存した。
