---
phase: "08"
slug: "wordfreq-exclude"
status: draft
shadcn_initialized: false
preset: none
created: "2026-11-29"
---

# Phase 8 — UI Design Contract

> 既存静的HTMLを維持する表示・CLI操作契約。公式UI-SPECテンプレートに基づくgsd-ui-researcher原本。checker承認、製品実装、試験・ブラウザ受入の完了を意味しない。

## Sources and Scope

- required_readingのSTATE/ROADMAP/REQUIREMENTS、08-CONTEXT/08-RESEARCH、承認済みPRD `_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md` を全文読了。REQ-28〜33、CONTEXT D-01〜11、FR-1〜7/RULE-1〜4を継承する。architecture/architecture.mdのAD-1〜4も直接全文読了した。
- `.planning/phases/03-wordfreq-html-output/03-UI-SPEC.md` と `.planning/phases/04-wordfreq-min-count/04-UI-SPEC.md` を全文読み、現行 `wordfreq/formatters.py`、`wordfreq/__main__.py`、README.md、pyproject.tomlへ照合した。既存CSS/DOM/文言/空状態/静的安全性を原本から引き継ぐ。Phase 2の残存成果は使わない。
- 公式launcherをsourceした同一terminalの `gsd_run query init.phase-op 8` はphase_found=true、phase_number=08、正しいphase_dir、has_context/has_research=true、has_plans=false、commit_docs=trueを返した。`gsd_run query config-get workflow.ui_phase --raw` はtrue。日付は `date +%F` による。
- 新しい製品判断は不要。Sketch findingsなし、AGENT_SKILLS_UI空は呼出し元の確定入力。HERMES.md、.hermes/HERMES.md、.hermes/skills、.agents/skills、components.jsonは存在確認で不在。
- 製品追加は任意の `--exclude FILE`、取得/行検証、共通ランキング選別、help/README説明と試験のみ。見た目・既存HTMLコピー・テーマ・依存を変えない。既存formatterの公開契約を維持し、除外FILEのI/Oを持ち込まない。
- この担当の変更は本書のみ。既存state.json、init/pre-hooks、.gitkeep、08-RESEARCH等の他者差分を保持する。commit_docs=trueだがcommit/push/Kanbanは親が担当する。STATEのPhase 7や過去の検証負債を変更しない。

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable |
| Component library | none — 既存semantic HTMLと内包CSSのみ |
| Icon library | none — アイコン・画像なし |
| Font | system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |
| Theme | light固定、color-scheme: light。dark分岐・切替なし |
| Output | UTF-8単一HTML、doctype、lang=ja、charset、viewport宣言を保持 |
| Runtime | script・外部参照・通信・対話操作・サーバーなし |

Python stdlib CLIでありReact/Next/Viteではない。shadcn初期化gateは対象外。Tool: noneのためComponent Inventory節は省略する。新パッケージ/registry/APIの調査・導入は不要。

### Existing Document and Layout — No Changes

根拠: `wordfreq/formatters.py:22–127` と03/04 UI-SPECの現在も有効な設計。

- 順序はmain → h1 → metadata（本文basename、元総出現回数）→ table（caption、thead、tbody）→ pairsが空の場合だけempty-message。値はラベルから独立したblockのtext nodeで、metadataは表より上。
- 3列は順位・単語・回数。thのscope=col、captionと空でも残るthead/tbodyを維持する。表示順位は除外/min-count/top後の1始まり欠番なし連番。除外語の元順位・欠番・同順位を表示しない。
- body margin 0。mainはwidth 100%、max-width 960px、border-box、左右auto margin、padding 32px。viewport 480px以下だけpadding 16px。
- tableはwidth 100%、table-layout fixed、border-collapse collapse。順位列56px、回数列64px、単語列は残り。全セルpadding 8px、vertical-align top、順位/回数は右寄せ・tabular-nums、単語は左寄せ。
- basename/単語はwhite-space: break-spaces、overflow-wrap: anywhere、word-break: normal、tab-size: 4。連続空白/LF/TAB/CRを削除・圧縮しない。h1、数値セル、空文言も現行折返し規則を保持する。
- 高さautoと自然なページ縦スクロールを保持。横スクロール依存、ellipsis、nowrap、行数制限、overflow hidden/clip、文字縮小、新min-widthは禁止。
- th背景と1px下罫線のみ。カード・影・角丸・新装飾・アニメーションなし。除外による行数と文書高さの変化は意図したデータ変化であり、CSS変更ではない。
- HTMLへ除外FILEのパス/内容/件数、フィルタchip、除外理由、生成日時、説明ラベル、フォーム、操作ボタンを追加しない。

---

## Spacing Scale

現物 `wordfreq/formatters.py:56–102` を維持。4px単位であり、新適用はしない。

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | metadataラベル下 |
| sm | 8px | 全セルpadding、metadata-item間、caption下 |
| md | 16px | 狭幅main padding、h1下 |
| lg | 24px | metadata下、空文言上 |
| xl | 32px | 通常main padding |
| 2xl | 48px | 継承予約値、現物未使用・新適用禁止 |
| 3xl | 64px | 継承予約値、現物未使用・新適用禁止 |

Exceptions: marginリセット0。1px罫線はspacingではなく、56px/64px列幅・960px max-widthは幾何寸法。新たな余白例外なし。

---

## Typography

現物 `wordfreq/formatters.py:47–77` を継承。サイズ3種、weight2種のみ。

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Body | 16px | 400 | 1.5 |
| Label | 14px | 600 | 1.5 |
| Heading | 24px | 600 | 1.25 |

Bodyはbasename/総数値/全データセル/空文言。Labelはmetadataラベル/caption/th。Headingはh1。狭幅でも同じサイズを保持する。Display・外部フォント・別数値フォントは追加しない。

---

## Color

現物 `wordfreq/formatters.py:46–101` を継承。60/30/10は役割であり、画素面積を満たすための再配色はしない。

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | #FFFFFF | ページ・metadata・表本文背景 |
| Secondary (30%) | #F1F5F9 | th背景のみ |
| Accent (10%) | #1D4ED8 | h1と総出現回数の数値のみ |
| Primary text | #0F172A | basename、単語、順位、回数、本文、列見出し |
| Secondary text | #475569 | metadataラベル、caption、空文言 |
| Divider | #CBD5E1 | th/td下境界線 |
| Destructive | not applicable | 破壊的操作・HTMLエラー画面なし |

Accent reserved for: h1と元総出現回数の数値のみ。除外・閾値・ランキングの強調色は作らない。light固定を維持する。

---

## Copywriting Contract

現物 `wordfreq/formatters.py:34–44,107–124` のHTML文言は一字も変更しない。以下のコピー欄は既存値の継承であり、新コピー提案ではない。

| Element | Copy |
|---------|------|
| Primary CTA | not applicable — 静的閲覧結果。ボタン/リンク/適用/再試行操作なし |
| Document title / h1 | 単語の出現頻度 |
| Filename label | ファイル名 |
| Filename value | 本文のbasenameのみ。既存ファイルシステム復号/置換規則と全文・空白保持を継承 |
| Total label | 総出現回数 |
| Total value | 元countsの回数和を10進整数で表示。除外/min-count/topすべての適用前。除外語を引かず、表示行数・種類数・表示行の和にしない |
| Table caption | 集計結果 |
| Column headers | 順位 / 単語 / 回数 |
| Empty state heading | 新見出しなし。captionと3列見出しを保持 |
| Empty state body | 集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。 |
| Error state | HTMLなし。除外FILEの読込み/不正行はFILEと理由（不正行は元1始まり行番号）のstderr/exit2。既存引数/数値失敗もexit2、本文読込み失敗は既存exit1。いずれもstdout空、Tracebackなし。診断全文の新固定はしない |
| Destructive confirmation | not applicable — 書込み・削除操作なし。本文と除外FILEを変更しない |
| Loading / partial results | not applicable — 完成文書のみ。spinner/skeleton/部分結果/再試行UIなし |
| CLI help addition | --exclude FILEの目的と行形式を説明しexit0。既存helpの無関係な書換えなし。説明要件はFR-6を使用し、ここで新しい決め文句を発明しない |
| README addition | FR-6の実行例と行形式/Unicode/失敗/処理順/元HTML総数/未指定互換を最小追記。既存説明の更新も今回の意味変更に必要な箇所だけ |

全語除外でも既存空文言を置換しない。空理由ごとのコピー分岐やHTML内の閾値調整・除外解除案内は追加しない。README説明は次の確定仕様へ一致させる。

### CLI Interaction and Data Contract

- `--exclude FILE` は任意。UTF-8、LF/CRLF/最終改行なしを受け付ける。各行の両端空白除去後、空行と#開始行を無視する。残る元行全体を既存Unicode `\w+`で検証してからcasefoldする。lowerへの変更不可。
- 数字/underscore/非ASCII有効語は可。複数語、句読点、hyphen、単独結合文字、inline #注記、先頭BOMは不正。token分割、BOM/句読点除去で受理しない。重複・除外行順は結果へ影響しない。
- 既存引数構文・top/min-count数値検査 → 除外取得と全行検証 → 成功後だけ本文取得。途中有効語があっても後続不正行で本文未読。元の空行/コメントを数えた行番号を診断する。除外失敗が本文失敗より優先する。数値不正なら両ファイル未読。除外有効/未指定での本文失敗exit1は維持。
- 全文の既存抽出/casefold → 元counts/元total保持 → 指定語の全出現を表示候補から除外 → min-count → 回数降順・正規化後の同数初出順 → top → 全形式共通pairs。元Counterは破壊せず、除外語はtop枠を消費しない。
- `--top`既定10、`--min-count`既定1、既存正整数検査とformat既定textを維持。count_words/top_words/formattersの純粋な公開契約は変えない。
- textはcount/TAB/word/LF、JSONはword/count配列・ensure_ascii=True・末尾LF1つ。正常空結果はtext空、JSON `[]\n`、HTMLは既存metadata/見出し/0データ行/固定空文言、exit0。
- 空本文・抽出0語のtotalは0。語あり全除外（閾値との併用を含む）は0データ行でも元の正totalを保持する。空除外/コメントのみ/不一致語は既存結果を保持する。
- help/READMEは以上を説明する。README実行例は後工程が実ファイルで実行し期待結果を試験する。未作成試験はここで実行しない。

---

## UI Considerations

公式Step 9.5: 独立checkerが7/7 VERIFIED（deleg_b2086421、通常終了）後、親が公式compiled engineを実行しexit0。入力は `.planning/argonauts/t_b046d7f7-ui-elements.json`、未解決raw報告は `t_b046d7f7-ui-probe.json`。4要素のkindを--autoで再読確認しstatic-content、表のみlist-collection併有と明示した。14 applicable / unclassified0。以下の14状態を承認済み原本からexplicitに解決する（定義の解決であって製品実行合格ではない）。

- E1 overflow / long-text（2項目、resolved explicit）: h1は既存24px/600と自然折返しを保持し、横はみ出し/切取り/重複を生まない。
- E2 overflow / long-text（2項目、resolved explicit）: 長basename/空白/LF/TAB/CR/総数値は既存CSSで全文可読、metadataは表より上で省略・縮小・clipなし。
- E3 empty（1項目、resolved explicit）: 0データ行でもcaption/thead/tbodyとCopywriting Contractの固定空文言を保持。空本文total0、全語除外でも元の正total。
- E3 loading / partial（2項目、resolved explicit）: 完成文書のみ出力。取得中や部分HTMLを出さず、除外/min-count/topを不完全読込の表現と混同しない。
- E3 error（1項目、resolved explicit）: Copywriting Contractの役割別stderr/exit、stdout空でHTMLなし。新HTMLエラー画面/再試行UIは作らない。
- E3 populated / zero-one-many（2項目、resolved explicit）: 選別後共通pairsを既存3列/1始まり欠番なしで表示し、0/1/多数で同じラベル/構造/元総数を保持。
- E3 overflow / long-text（2項目、resolved explicit）: 長語/複数桁は既存CSSで自然折返し、横収まり/clipなし/非重複/全文可読。
- E4 overflow / long-text（2項目、resolved explicit）: 固定空文言を既存サイズのまま自然折返し、省略/縮小/置換なし。

Applicable state considerations resolved: 14/14 explicit, backstop0, unresolved0, dismissed0。raw probeのunresolvedは分類直後の出力として保持し、上記が親の--auto resolution。下表は同じ状態の原本参照をまとめる。

| Category | Element(s) | Status | Resolution / Reason |
|----------|------------|--------|---------------------|
| overflow / long-text | E1 heading (static-content) | resolved explicit | h1は既存文字サイズで自然折返し、横はみ出し/切取り/重複なし |
| overflow / long-text | E2 metadata (static-content) | resolved explicit | 長basenameと空白/LF/TAB/CR、元totalを保持し、省略せず読める。metadataは表より上 |
| empty | E3 table (list-collection + static-content) | resolved explicit | Copywriting Contractの空状態、0データ行、空本文total0/全除外元total正値を区別 |
| loading / partial | E3 table | resolved explicit | 完成HTMLのみ。除外/min-count/topは意図した選別であり、不完全データ・取得中UIなし |
| error | E3 table | resolved explicit | Copywriting Contractの役割別stderr/exitとstdout空。HTML/部分行/再試行UIなし |
| populated | E3 table | resolved explicit | 選別後共通pairsの3列と1始まり連番、元totalを表示 |
| zero-one-many | E3 table | resolved explicit | 0/1/多数行でも同じ構造/ラベル/metadataを保持し、欠番なし |
| overflow / long-text | E3 table | resolved explicit | 長語と複数桁数値は既存CSSで折返し、横収まり・clipなし・非重複・全文可読 |
| overflow / long-text | E4 empty message (static-content) | resolved explicit | Copywriting Contractの固定本文を自然折返し、省略/縮小/置換なし |

---

## Compatibility, Safety and Verification Handoff

後工程への義務であり、以下はこの担当の実行結果ではない。

### Accepted Scenarios

| Source input / exclusion | Options | Expected rows / original HTML total |
|--------------------------|---------|------------------------------------|
| Zoo apple APPLE zoo banana / apple | existing defaults, each format | zoo2, banana1 / total5 |
| 同本文 / zoo | min-count2, top1 | apple2のみ、順位1 / total5 |
| 同本文 / 全語除外、または除外+閾値で全件消失 | valid options | 0データ行、既存空文言 / total5 |
| 空本文・抽出0語 / valid exclusions | valid options | 0データ行 / total0 |
| 同本文 / 空・コメントのみ・不一致語 | identical existing argv | 元の語/回数/順序/totalを保持 |
| Straße STRASSE hello / STRASSE | each format | hello1のみ / total3 |
| blank・comment・valid・invalidの元4行 | each format | FILE/元line4のstderr、exit2、stdout空、本文取得0回 |
| 同数逆語順・Unicode・10種類超・空本文 / exclude未指定 | identical inputs/argv/environment | 固定既存版との全形式stdoutバイト一致 |

- 未指定互換の唯一の指定比較元は `79d83ba14dd59d289d2ecd3e33c85e8de437972e`。同じ入力パス/バイト・argv・環境で実行、または同版から出所付きで保存した期待バイトを使う。候補自身を期待値にしない。Phase 4固有の「最初の製品変更前baseline採取」gateを今回の追加要件として移植しない。
- 既存formatter/CSS/HTMLコピー不変をソース差分と既存回帰で確認する。変更後未指定同士だけの比較では不十分。正常stdoutに説明ログを混ぜない。
- escape(quote=True)とCRの文字参照保護、本文basenameのみ・独立text node、UTF-8出力を維持。ディレクトリ情報をtitle/属性/コメント等にも出さない。除外FILEのmetadataもHTMLに追加しない。
- script、イベント属性、CSS url/@import、meta refresh、外部resource、リンク/フォーム/埋込みを導入しない。外部通信・依存・CI変更・新入力元・全体リファクタなし。
- 03/04から通常1280×900と狭幅320×900 CSS px・DPR1、同じ描画条件、自然な縦スクロール、長語/長basename/空白保持/複数桁/注入候補の表示契約を継承する。03のFixed Input Matrixの長文/有効特殊basename定義を再設計しない。
- 表示確認を行う場合は実CLIの保存UTF-8 HTMLを使い、browser/version/executable/viewport/DPR/フォント条件を記録する。全画像を実閲覧し、全文と文字単位raw Range、空白位置、祖先overflow/clip、隣接列/行/metadata非重複を確認する。raw値のclamp/丸め/差替えで合格にしない。自身の矩形への厳格な縦包含は必須ではなく、横収まり・clipなし・非重複・全文可読で判断する。
- 通信確認を行う場合は文書読込み前から観測し、要求/failed request/navigation/popupと帰属根拠を残す。最初のローカルfile読込みを区別し、外部試行は失敗/遮断でも安全性合格にしない。不明は未検証。
- Phase 8のREQ-32に従い、品質は対象headで独立実行し、VERIFICATION.mdとCLI文字原本にhead/commands/exit/expected-vs-actual/AC対応を保存する。画像確認があれば枚数/内容/結果を文字化し、PMに画像/圧縮ファイル閲覧を求めない。旧phaseの証拠・固定scope verifierを今回合格の代用にしない。
- このUI契約は過去のブラウザdriverや画像配送・Phase 4固有gateの新規構築を要求しない。実際の検証面はplannerがREQ-28〜33の範囲で実在化する。未作成コマンド/試験を実行せず、未検証・未閲覧・収集0件を合格にしない。
- 新製品判断が必要になったら推測で契約を拡張せずUI-SPEC BLOCKEDとして親/PMへ返す。現時点の未決製品事項はない。

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable — shadcn/第三者registry/外部packageを導入しない |

見た目の維持や検証のためにも新テーマ・依存・Webフォント・CDN・JSを追加しない。

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS
- [ ] Dimension 2 Visuals: PASS
- [ ] Dimension 3 Color: PASS
- [ ] Dimension 4 Typography: PASS
- [ ] Dimension 5 Spacing: PASS
- [ ] Dimension 6 Registry Safety: PASS
- [ ] Dimension 7 Inventory Provenance: PASS

**Approval:** independent gsd-ui-checker VERIFIED 7/7 (deleg_b2086421), parent official probe exit0 and 14 explicit resolutions. 製品試験・互換バイト比較・ブラウザ確認は未実施。
