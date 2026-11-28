---
phase: "08"
slug: "wordfreq-exclude-file"
status: approved
shadcn_initialized: false
preset: none
created: "2026-11-28"
---

# Phase 8 — UI Design Contract

> 既存静的HTMLを継承する除外機能の表示契約。新デザインではない。独立checkerによる契約承認と公式状態probeの完了は末尾へ記録した。製品実装・試験合格・ブラウザ受入を意味しない。

## Sources and Scope

- 必読原本: `.planning/STATE.md`、`ROADMAP.md`、`REQUIREMENTS.md`、`08-CONTEXT.md`、`08-RESEARCH.md`、`.planning/argonauts/r-6442a149-prd.md` を全文読了。承認t_0d1aa16a、原本head `8a2c69b8332e9704377fe680af51767c74e4ab56` のREQ-28〜35、EX-1〜6、HTML-2とCONTEXT D-01〜08を採用し、決定済み内容を再質問しない。
- 継承元 `.planning/phases/03-wordfreq-html-output/03-UI-SPEC.md`、`.planning/phases/04-wordfreq-min-count/04-UI-SPEC.md`、現物 `wordfreq/formatters.py` を全文照合した。以下の寸法・色・字形・文言の具体値は現物の引用であり、一般的なデザイン推奨値への置換ではない。
- `wordfreq/__main__.py:13–54` は現在exclude未実装。総数はcountsの和をmin-count/top前に計算し、本文basenameとpairsとtotalだけをformatterへ渡す。今回の変更は共通計数の前に除外を反映する。formatterの公開契約・HTML構造・CSS・固定文言は変更しない。
- 公式runtime launcher経由 `gsd_run query init.phase-op 8` は `phase_found: true`、`phase_number: "08"`、`has_context: true`、`has_research: true`、`has_plans: false`。STATEのcurrent_phase 7と過去phaseの検証状態を今回の受入へ混ぜず、STATEを更新しない。
- AGENT_SKILLS_UIの公式query結果は空、sketch findingsなし（呼出し元確定入力）。root HERMES.mdはnot_found。ファイル探索でcomponents.json / package.json / Tailwind / PostCSS設定なし。`pyproject.toml:5–15` はwordfreq 0.1.0、dependencies空、devはpytestのみ。既存Python CLIでありReact/Next/Viteではない。
- この子の書込み対象は本書だけ。製品・試験・PLAN・設定・既存dirty文書を変更せず、commit/push/Kanbanを行わない。commit_docs=trueでもcommitは親に委ねる。
- 本工程では製品HTML生成、ブラウザ起動、画像生成・画像閲覧をしていない。画像は未閲覧。ソース照合を実描画の確認・合格とは呼ばない。

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable |
| Component library | none — 既存semantic HTMLと内包CSSのみ |
| Icon library | none — アイコン・画像追加なし |
| Font | system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |
| Theme | light固定、`color-scheme: light`。dark分岐・切替なし |
| Output | UTF-8単一静的HTML、doctype、lang=ja、charset、viewport宣言を維持 |
| Runtime | script・外部参照・外部通信・フォーム・対話操作・新サービスなし |

Tool: noneのためComponent Inventoryは省略する。shadcn初期化・library列挙・registry導入は非該当。新framework、library、設定、サービス、画像生成を追加しない。

### Existing Document and Layout — No Changes

現物根拠: `wordfreq/formatters.py:22–127`。Phase03/04の意味構造と見た目を継承する。

- 順序はmain → h1 → metadata（本文ファイル名、総出現回数）→ table（caption、thead、tbody）→ pairsが空の場合だけempty-message。basenameとtotalはラベルと独立したblock値で表より上に表示する。
- ファイル名は**本文**の実行環境のパス規則によるbasenameのみ。除外FILE名・パス・除外件数・chip・適用ラベルを追加しない。titleは固定。本文のディレクトリ情報をtitle・属性・コメントを含むHTMLへ埋め込まない。
- 表は順位・単語・回数の3列、`th scope="col"`。空でもcaptionとtheadを残し、tbodyのデータ行を0とする。空案内をtbody外に置き、colspanの疑似データ行は作らない。
- 各行は共通pairsの順。除外・min-count・top適用後の表示行に1始まりの欠番なし連番を付ける。回数降順・同数時正規化後の相対初出順を維持し、語昇順・同順位へ変えない。
- body margin 0。mainはwidth 100%、max-width 960px、border-box、左右auto margin、padding 32px。`@media (max-width: 480px)` でpadding 16pxだけにする（現物:47–62,102）。
- tableはwidth 100%、fixed layout、collapse。順位列56px、回数列64px、単語列は残り。全セルpadding 8px、vertical-align top。順位/回数は右寄せ・tabular-nums、単語は左寄せ（86–100）。
- basename/単語は `white-space: break-spaces; overflow-wrap: anywhere; word-break: normal; tab-size: 4`。空白・LF・TABを圧縮せず、CRは既存escape処理で保護する。h1、セル、空文言の折返しを維持（17–19,63–101）。
- 自然な縦スクロールで全文を読めること。固定高さ、新min-width、横スクロール依存、ellipsis、nowrap、行数制限、overflow hidden/clip、文字縮小を追加しない。
- 新カード・角丸・影・装飾・アニメーションなし。除外で行数・文書高さ・総数が変化することだけが意図した表示差分である。

---

## Spacing Scale

現物根拠: `wordfreq/formatters.py:56–102`。既存4px単位を保持する。

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | metadataラベル下 |
| sm | 8px | セルpadding、metadata-item間、caption下 |
| md | 16px | 狭幅main padding、h1下 |
| lg | 24px | metadata下、空案内上 |
| xl | 32px | 通常main padding |
| 2xl | 48px | Phase03/04の予約値。現物未使用、新適用なし |
| 3xl | 64px | Phase03/04の予約値。現物未使用、新適用なし |

Exceptions: 0はmarginリセット、1pxは罫線。56px/64px列幅・960px max-width・480px breakpointは幾何寸法であり余白tokenではない。新たな余白例外なし。

---

## Typography

現物根拠: `wordfreq/formatters.py:47–77`。サイズ3種、weight2種を継承し、狭幅でも変えない。

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Body | 16px | 400 | 1.5 |
| Label | 14px | 600 | 1.5 |
| Heading | 24px | 600 | 1.25 |

Bodyはbasename・総数値・全データセル・空案内。Labelはmetadataラベル・caption・th。Headingはh1。外部フォント・別数値フォント・Displayサイズを追加しない。

---

## Color

現物根拠: `wordfreq/formatters.py:46–101`。60/30/10は継承した役割配分であり、画素面積の強制比率ではない。

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | #FFFFFF | body・metadata・表本文の背景 |
| Secondary (30%) | #F1F5F9 | th背景のみ |
| Accent (10%) | #1D4ED8 | h1と総出現回数の数値のみ |
| Primary text | #0F172A | basename、単語、順位、回数、本文、列見出し |
| Secondary text | #475569 | metadataラベル、caption、空案内 |
| Divider | #CBD5E1 | th/td下の1px境界線 |
| Destructive | not applicable | 破壊的操作・HTMLエラー画面なし |

Accent reserved for: h1「単語の出現頻度」と総出現回数の数値のみ。除外・閾値・特定語・順位に新たな強調色を使わない。light固定、テーマ追加なし。

---

## Copywriting Contract

現物根拠: `wordfreq/formatters.py:34–44,107–124`。固定文言は一字も変更しない。総数の**値の意味だけ**を承認HTML-2へ拡張する。

<!-- DATA_04c8688f_START -->
| Element | Copy |
|---------|------|
| Primary CTA | not applicable — 静的結果。ボタン・リンク・除外入力・適用/再試行操作なし |
| Document title / h1 | 単語の出現頻度 |
| Filename label | ファイル名 |
| Filename value | 本文basenameのみ、全文と空白を保持。除外FILEへ置換しない |
| Total label | 総出現回数 |
| Total value | 除外後、min-count/top前のcountsの回数和を10進整数で表示。未指定時は従来総数。種類数・表示行数・表示回数和ではない |
| Table caption | 集計結果 |
| Column headers | 順位 / 単語 / 回数 |
| Empty state heading | 新見出しなし。captionと3列見出しを維持 |
| Empty state body | 集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。 |
| Error state | HTML内エラー画面なし。対象/原因をstderrへ通知。除外読込失敗exit2、本文のみ読込失敗exit1、既存引数不正exit2。全てstdout空。問題を確認しCLIを再実行する。エラー全文の厳密一致は新要求にしない |
| Destructive confirmation | not applicable — 書込み・削除・確認操作なし |
| Loading / partial results | not applicable — 完成文書のみ。spinner/skeleton/部分取得/再試行UIなし |
<!-- DATA_04c8688f_END -->

全語除外でも既存空案内をそのまま使い、除外専用案内・理由分岐・閾値調整へのHTML文言置換をしない。生成日時・追加metadata・説明ログなし。help/READMEには承認済み構文・行規則・casefold・最後FILE・読込失敗exit2・空結果と再現例を最小追記するが、HTMLのcopy改善へ拡張しない。

### CLI Interaction and Total Contract

- 既存引数検証 → 最後の除外FILEだけ読込 → 本文取得 → 既存抽出/casefold → 一致語を除外 → 計数 → total保持 → min-count → 回数降順/同数初出順 → top → 既存formatter。除外FILEの前の指定は読まない。
- 除外一覧はUTF-8先頭BOM除去、strip後の空行/先頭#を無視、その他は行全体をcasefoldして比較する。分割・記号除去・途中#コメントを追加せず、本文抽出を変えない。
- 既存引数エラーはFILE読込前。除外の不存在/権限不足/ディレクトリ/不正UTF-8等は対象と原因のstderr・exit2・stdout空、本文未読。除外成功後または未指定の本文失敗は既存exit1。失敗を空結果へ変換しない。
- 全語除外はHTMLデータ0行・既存案内・total0、text空、JSON `[]`と末尾LF、全形式exit0。追加専用案内なし。
- min-countで表示だけ全除外した場合は、除外後countsの正のtotalを維持する。除外未指定でmin-countだけ使う従来の正totalも維持する。
- 未指定・空一覧・コメントのみ・該当語なしは既存出力と同じ。既定text/top10/min-count1、Unicode casefold、text/json構造・改行、HTML basename/escape/自己完結性を維持する。

---

## UI Considerations

親のStep9.5で公式probeを実行（`.planning/argonauts/r-6442a149-ui-probe.json`）。4要素・14 applicable・unclassified0を確認。--autoのkind確認は原文を再読し、E1/E2/E4=static-content、E3=list-collection+static-contentの明示overrideで実行。form/nav/media/interactive-controlは存在せず追加しない。下表の14項目は承認済み契約と既存表示を根拠に全てresolved/verification:explicitへ解決した。これは設計上の状態解決であり製品試験・画像閲覧の合格ではない。copyはCopywriting Contractを参照する。

Applicable state considerations: 14、explicit解決14、設計未解決0。

| Category | Element(s) | Status | Resolution / Reason |
|----------|------------|--------|---------------------|
| overflow | E1 | resolved (explicit) | 固定h1は現行CSSで自然折返し、省略・切取り・隣接重複をしない |
| long-text | E1 | resolved (explicit) | h1は24px/600のまま全文を表示し、文字縮小しない |
| overflow | E2 | resolved (explicit) | 本文basenameと除外後totalは表より上に保持し、横収まり・非重複・切取りなし |
| long-text | E2 | resolved (explicit) | 長basename・連続空白/LF/TAB/CR・数値の全文を現行規則で保持する |
| empty | E3 | resolved (explicit) | 全語除外は0データ行/total0/既存案内。min-countによる0行は除外後totalを保持する |
| loading | E3 | resolved (explicit) | 完成HTMLだけをstdoutへ出し、loading UIは生成しない |
| error | E3 | resolved (explicit) | Copywriting Contractのstderr/exit1または2、stdout空。エラーHTMLなし |
| populated | E3 | resolved (explicit) | 除外/min-count/top後のpairsを既存3列と1始まり連番で表示し、選択前totalを維持する |
| partial | E3 | resolved (explicit) | min-count/topは完成データの表示制限であり、部分取得状態や追加補足UIを生成しない |
| overflow | E3 | resolved (explicit) | 長語・数値は既存固定列幅/CSSで折返し、横はみ出し・clip・隣接重複をしない |
| zero-one-many | E3 | resolved (explicit) | 0/1/複数行で同じmetadata/caption/thead/列順を保持し、表示順位は欠番なし |
| long-text | E3 | resolved (explicit) | 長語・複数桁の数値を既存サイズで全文表示する。省略・文字縮小なし |
| overflow | E4 | resolved (explicit) | 固定空案内は自然折返し、横収まり・非重複・切取りなし |
| long-text | E4 | resolved (explicit) | Copywriting Contractの既存空案内を省略・置換・縮小せず全文表示する |

---

## Phase08 Verification Handoff

以下はBuilder/品質への条件であり、本工程の実行結果ではない。旧Phase03/04の固定scopeのcollector・baseline必須gate・全ブラウザ受入を今回の追加要件として再開しない。新規検証driverや未作成node-idを実在すると記さない。

| State / source | Input and options | Locked expected display |
|----------------|-------------------|-------------------------|
| 指定除外 / EX-1 | 本文 `Zoo apple APPLE zoo banana`、一覧apple | zoo2、banana1。total3、appleなし |
| top前除外 / EX-1 | 同本文、一覧zoo、top1 | apple2、順位1。先top後削除の空表示にしない |
| 同数/重複 / EX-1 | 本文 `beta apple alpha`、一覧apple/APPLE/aPpLe | beta1、alpha1の初出順。単一apple一覧と同じ |
| 除外＋min/top / HTML-2 | 本文 `Zoo apple APPLE zoo banana`、一覧apple、min2/top1 | zoo2だけ、順位1、total3。除外前5・表示和2ではない |
| 表示だけ空 / REQ-35 | 同本文/一覧apple、min-countを残存最大回数より大きくする | 既存空表/案内、除外後total3を保持 |
| 全語除外 / EX-6 | 本文 `Apple apple`、一覧apple | 0データ行、既存案内、total0、exit0、専用案内なし |
| 旧min-only空 / HTML-2 | 本文 `beta beta beta alpha gamma alpha delta`、除外なし、min4 | 0データ行、既存案内、total7 |
| 未指定互換 / HTML-2 | 本文 `zoo apple zoo banana apple cherry`、除外なし、top1/2/10 | 総数は全て6、既存pairs/順位を維持 |
| 入力・抽出0語 | 空/空白/句読点のみ、有効引数 | 0データ行、既存案内、total0、exit0 |
| 無効除外FILE / EX-4 | 不存在/権限不足/ディレクトリ/不正UTF-8 | HTMLなし、stdout空、対象/原因stderr、exit2 |

- 上表に加えREQ-28〜35/EX-1〜6/HTML-2の全scenarioは `08-RESEARCH.md` Scenario Coverage Matrixと原本に従う。行文法・Unicode・最後FILE・順序は直接試験と実CLIで確認し、表示契約だけで機能全体の網羅を主張しない。
- Builder/品質は、その時点で実在する試験/検証ファイルからコマンドを実行する。計画中の未作成コマンド試走、インラインPython/Node/shell実行、ヒアドキュメントは禁止。既存試験全件と除外未指定互換を確認する。
- 安全性は現物 `formatters.py:17–19,39–127` を維持する。escape(quote=True)とCR保護、strict UTF-8、basename限定。除外一覧やパスをHTMLへ流さない。script/イベント属性/外部resource/CSS urlや@import/meta refresh/リンク/フォーム/外部通信を追加しない。
- 見た目は既存1280×900/320×900 CSS px・DPR1のレイアウト規則を継承する。実画像を取得した場合は品質が全画像を実閲覧し、枚数・対象内容・結果を文字原本に残す。画像存在やDOM一致だけを可読性合格にしない。長語/basename/数値は折返し・横収まり・clip/非重複・全文可読性を確認し、生矩形を補正して合格にしない。自身の要素への厳格な縦包含は新必須条件にしない。
- 品質が対象headでCLIを独立再実行し、環境・cwd・入力原本・exact argv・stdout/stderr・exit・期待pairs/total・条件別判定・処理順のソース箇所をVERIFICATION.md等の文字原本へ保存し標準添付する。PMへ画像/圧縮ファイルを開かせず、文字で判断可能にする。
- 未実行・未閲覧・欠測・配送未確認は未検証とする。過去phaseの未達を今回の実装範囲へ混ぜず、今回の試験成功も過去phaseの完了証明にはしない。

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable — shadcn/第三者registry/外部packageの導入なし |

新しいlibrary/framework/設定/サービス/画像生成、依存追加・権限変更・外部送信なし。検証の都合でも製品CSS/DOM/文言を手修正しない。

---

## Checker Sign-Off

- [x] Dimension 1 Copywriting: PASS
- [x] Dimension 2 Visuals: PASS
- [x] Dimension 3 Color: PASS
- [x] Dimension 4 Typography: PASS
- [x] Dimension 5 Spacing: PASS
- [x] Dimension 6 Registry Safety: PASS
- [x] Dimension 7 Inventory Provenance: PASS

**Approval:** approved 2026-11-28 — 独立gsd-ui-checker sa-0-a954a989 が ## UI-SPEC VERIFIED、全7次元PASS（InventoryはN/A根拠確認）を返した。親の公式Step9.5で14状態を照合しexplicit解決を記録。製品試験・ブラウザ確認・画像閲覧は未実施。
