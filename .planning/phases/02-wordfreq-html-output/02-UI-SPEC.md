---
phase: "02"
slug: "wordfreq-html-output"
status: draft
shadcn_initialized: false
preset: none
created: "2026-11-17"
---

# Phase 02 — UI Design Contract

> 静的ローカルHTMLレポートの視覚・表示契約。gsd-ui-researcher作成。製品実装・ブラウザ検証・checker承認は未実施。

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable |
| Component library | none — Python標準ライブラリが生成する意味的HTMLとinline CSSのみ |
| Icon library | none |
| Font | system-ui, sans-serif（OS標準フォントのみ、取得しない） |

根拠: `02-CONTEXT.md` D-01〜D-09、REQ-09〜14、承認済み `.planning/argonauts/r-5c041156-prd.md`。解決済み回答を再質問しない。以下の具体的なトークン・配置・日本語固定文言は、承認範囲内の研究者デフォルトとして定める。未回答のユーザー判断はない。

既存調査: `pyproject.toml` はPythonパッケージ、runtime dependenciesは空。`wordfreq/formatters.py` は純粋text/json整形のみ、`wordfreq/__main__.py` はargparse CLI。既存UI・継承すべきデザイントークンはない。ファイル検索 `*HERMES*`、`*SKILL.md`、`*components.json`、`*.css` は該当なし。React/Next/Viteではないためshadcn初期化・package inventory・registry列挙は適用外。フレームワーク・外部画像・フォント導入で補わない。公式CLIの `query agent-skills gsd-ui-researcher --skills-only` は空。RESEARCH/sketch findingsなし。

## Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | メタデータラベルと値の間 |
| sm | 8px | メタデータ行間、セルの全方向padding |
| md | 16px | ページ左右余白、見出し下余白 |
| lg | 24px | ページ上下余白、メタデータと表の間 |
| xl | 32px | 予約値、このphaseでは未使用 |
| 2xl | 48px | 予約値、このphaseでは未使用 |
| 3xl | 64px | 予約値、このphaseでは未使用 |

Exceptions: 余白の例外なし。境界線の1pxはspacing tokenではない。装飾的カード・影・角丸は不要。ブラウザ既定の見出し/段落marginはリセットし、この表の値を使用する。

## Typography

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Body / data cells / metadata values | 16px | 400 | 1.5 |
| Label / metadata labels / column headers | 14px | 600 | 1.5 |
| Heading / single h1 | 24px | 600 | 1.2 |

サイズは14/16/24pxの3種のみ、weightは400/600の2種のみ。Displayロールなし。メタデータ値の総数も16px/400。列の対応を保つため数値セルは右寄せ、語セルは左寄せ、全セルは上端揃え。数字はtabular-numsを指定できる。狭幅でフォントを縮小しない。

## Color

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | #FFFFFF | ページ・表bodyの明るい基調面 |
| Secondary (30%) | #F1F5F9 | 表のthead背景 |
| Accent (10%) | #1E40AF | h1文字色のみ |
| Text | #0F172A | 通常本文、メタデータ値、表セル、列見出し |
| Muted text | #475569 | メタデータラベルのみ |
| Border | #CBD5E1 | 表の外周と行の水平区切り（1px） |
| Destructive | not applicable | 破壊操作なし |

Accent reserved for: 固定h1のみ。順位・回数に意味的な色やヒートマップを付けない。60/30/10は配色の役割比率であり、空表や可変行数で面積の厳密比率を強制しない。単純なデータレポートを埋める目的の装飾は追加しない。本文/ラベル/見出しの各前景背景組合せは通常文字4.5:1以上を受入時に確認する。ダークテーマ・prefers-color-scheme切替なし。

## Copywriting Contract

| Element | Copy |
|---------|------|
| Document title / h1 | `wordfreq 集計結果` |
| Input metadata label | `入力ファイル:` の後にbasenameを独立したテキスト要素で表示 |
| Total metadata label | `総出現数:` の後にtop前総数の10進整数を表示 |
| Column headers | 左から正確に `順位`、`単語`、`回数` |
| Primary CTA | not applicable — 閲覧専用、ボタンやリンクを作らない |
| Empty state heading | 追加しない。通常h1・メタデータ・3列見出しをそのまま保持 |
| Empty state body | 追加しない。総出現数の値 `0` と空のtbodyで表現。ダミー行・colspan説明行・順位セルなし |
| Error state | HTML上はnot applicable。CLIエラーは既存stderr/exit規約を維持しstdoutは空。失敗をHTMLの成功レポートへ変換しない |
| Destructive confirmation | not applicable — HTML内に操作はない |

生成日時、期間、top件数の追加表示、著作権footer、並べ替え案内、再試行/共有/ダウンロード操作を追加しない。ファイル名や語をtitle・属性・CSSへ埋め込まない。

## Layout and Semantic Contract

1. UTF-8の単一完結文書: doctype、html（`lang="ja"`）、head、固定title、`meta charset="utf-8"`、`meta name="viewport" content="width=device-width, initial-scale=1"`、inline style、body/mainを持つ。script、外部CSS/font/image、ネットワークURLを持たない。
2. DOM/視覚順序は、h1 → 入力basenameメタデータ → top前総数メタデータ → table。basenameはリンクにせず、ディレクトリを含めない。ラベルと値は別要素にし、値だけのtextContentを元文字列と照合できるようにする。
3. 全要素はborder-box。body marginは0。mainは幅100%、max-width 960px、左右auto margin、paddingは上下24px・左右16px。固定heightは置かず縦スクロールを許す。h1の下16px、メタデータ行間8px、メタデータから表まで24px。
4. tableはwidth 100%、table-layout fixed、border-collapse collapse。colgroupで順位20%・単語60%・回数20%を指定する。tableのthead/tbodyを必須とし、列見出しは3つのthすべて `scope="col"`。各データ行は対応する3個のtdのみ。必要な表名は固定のaria-label `単語の出現頻度` で付け、見える追加列は作らない。
5. セルpaddingは8px。順位/回数は右寄せ、単語は左寄せ、列見出しも同じ配置。罫線は外周と行区切りのみ。ゼブラ、hover、選択、sort indicatorなし。表の役割を壊すdisplay:blockによるカード化をしない。
6. basename値と語値には `white-space: pre-wrap; overflow-wrap: anywhere; word-break: normal` を指定する。basenameのラベルと値は別ブロックとし、値にはwidth 100%/min-width 0を適用する。セル全体にもoverflow-wrap:anywhereを指定し、長い整数も列外へ流さない。値要素の開始/終了タグとデータの間へ整形用空白を挿入しない。
7. 320/375/1280 CSS pxで同一3列表を保つ。200文字連続語・長い日本語basenameは行数を増やして全文表示する。固定行高、max-height、ellipsis、nowrap、clip、hiddenによる見せかけのoverflow抑制、横スクロールcontainerは禁止。改行/折返しは許すがデータ自体へのゼロ幅文字や改行追加はしない。
8. sourceの語はUnicode抽出+casefold後の値、sortは回数降順・正規化初出順、その後top。formatterは選択済みpairs/basename/totalを受け取り、入力読取り・再sort・再集計をしない。順位は渡された表示行の順に1からの連番。同数も連番。text/jsonにこのレイアウトやmetadataを追加しない。

## Text Fidelity and Safety Contract

- 語・basenameはHTMLのテキストノードとして一度だけescapeする。元の `&amp;` 相当の文字列も、ブラウザtextContentがその元文字列と一致しなければ失敗。タグ/イベント/属性として解釈させない。
- HTML parserは生のCR/CRLFを正規化するため、通常のHTML escapeだけでは不十分。escape済みテキスト内のCRを数値文字参照 `&#13;` に置換してシリアライズする。LFは保持する。CRLFはCR参照とLFの組として保持し、参照を後から再escapeしない。これによりDOM textContentのCR・LF・CRLF一致を要求する。入力読取り層のuniversal newline規約は変えない。
- 連続スペース・tab・LF・CR/CRLFは値のDOM文字列を変更せず保持し、pre-wrapで表示する。文字列一致はformatter直接入力でも試験する（通常tokenizerが語に含めない文字も境界試験では渡す）。CSSだけの確認や正規化後比較で代用しない。
- 悪意ある実basenameのCLI出力でも、入力由来の追加要素・script・イベント実行がなく、外部requestが0であることをブラウザで確認する。

## UI Considerations

Applicable state considerations resolved: 4 covered, 2 backstop, 0 unresolved。coveredは仕様で解決済みの意味であり、実装合格を意味しない。backstopは実ブラウザ証跡がない限り未検証。

| Category | Element(s) | Status | Resolution / Reason |
|----------|------------|--------|---------------------|
| empty | frequency-table (list-collection) | ✅ covered | Copywriting ContractのEmpty state行を適用。空入力/記号のみは総数0、3見出し、tbodyデータ0行 |
| populated | frequency-table (list-collection) | ✅ covered | 通常例one one one two two threeは1/one/3、2/two/2、3/three/1。同数例は1/zoo/2、2/apple/2、3/beta/1 |
| partial | frequency-table (list-collection) | ✅ covered | topは表示行のみを制限する意図的な部分表示。top1でもZoo例の総数は5、1/zoo/2。語種数より大きいtopは全件。欠落セルや途中までのエラー文書は出さない |
| zero-one-many | frequency-table (list-collection) | ✅ covered | 0行は空tbody、1行は順位1、複数行は欠番なし。総数や列見出しの単複で文言/配置を変えない |
| overflow | frequency-table (list-collection), input-metadata (static-content) | 🧪 backstop | 320/375/1280pxでpage/tableの横overflowなし、列重なりなし、縦スクロールで全内容を読めることを画像とDOM/layoutで実測 |
| long-text | input-metadata, word-values (static-content) | 🧪 backstop | 200文字連続語と長い日本語名の全文・空白保持をtextContentで照合し、各viewportの画像で折返しと欠落/重複/切捨てなしを確認 |

適用除外（理由付き）: loadingはローカル生成済み文書のため非同期取得・pending stateなし。errorはCopywriting ContractのCLI境界へ帰属しHTMLのエラーUIなし。form/nav/media/interactive-control自体が存在しない。ライブ更新、オフライン切替、animation/focus管理は追加しない。

## Real-Browser Evidence Contract

この節はBuilder/品質への検証要求であり、実行結果ではない。計画段階では未作成の検証コマンドを試さない。

- 提供済み発見情報では `/usr/bin/chromium-browser` と `/home/Yuki/.local/bin/playwright` が候補。起動・版・自動化APIの利用可否は未検証。phase research/PLANで既存環境の経路を確定し、実在する検証ファイルを作成した後にBuilder・独立品質が実行する。依存/ブラウザdownload/CI追加やWebサーバ導入で迂回しない。
- 実CLIで入力とは別のUTF-8 HTMLへ保存し、file URLとして既存の実ブラウザで開く。200文字語+長い日本語名、通常行、同数行、top1、空入力、悪意ある実basenameを対象とする。全幅320/375/1280 CSS pxで長文ケースと空表を必ず確認し、画像・DOMの記録から他ケースの確認幅も明示する。viewport高さ・device scale factorも記録する。
- 証跡の予定保管先は `.planning/phases/02-wordfreq-html-output/evidence/`。このディレクトリ/検証コードはまだ作らない。実施時は実HTML、入力fixture/生成条件、対象git head、CLI引数とexit/stdout/stderr、ブラウザ名/版、viewport、画像、DOM/text/layout、network logを保存する。生成コマンドと独立再実行手順を記録する。
- DOM/layout測定は3つのscope=col、thead/tbodyと各行3セル、順位/語/回数/metadataの期待値、各値textContent一致、document/tableのscrollWidthとclientWidth、セル境界の列重なり/画面外はみ出し、実測rectを含む。画像と併用し、overflowを隠すCSSで合格にしない。
- networkはナビゲーション前から採取し、ローカルfile文書の読込みと外部requestを区別して記録する。外部request 0を実測し、空ログだけを根拠に監視成功と見なさない。悪意ある名前について追加DOM要素、script/event実行、dialog等の副作用がないことも記録する。検証ハーネスが観測に使うスクリプトと製品HTMLのJS禁止を混同しない。
- ブラウザが起動しない、既存ツールだけで観測できない、証跡が欠ける場合はその条件を未検証として人へ返す。静的HTML解析・スクリーンショット予定・作り物の測定値で合格にしない。品質はBuilderの画像を流用するだけでなく、実CLI生成から独立再実行する。
- 利用説明は入力と別パスへのUTF-8保存、保存HTMLに語/名前が残る共有リスク、同じパスへのシェルリダイレクトがCLI起動前に入力を切り詰める危険を明記する。無害なデータで例を実行し入力バイト不変を検証する。既存pytest・入力境界・exit0/1/2・text/json構造を維持する。

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable — Tool:none、第三者コード/registry/assets導入なし |

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS
- [ ] Dimension 2 Visuals: PASS
- [ ] Dimension 3 Color: PASS
- [ ] Dimension 4 Typography: PASS
- [ ] Dimension 5 Spacing: PASS
- [ ] Dimension 6 Registry Safety: PASS
- [ ] Dimension 7 Inventory Provenance: PASS

**Approval:** pending — 公式gsd-ui-checkerが検証する。Tool:noneのためComponent Inventoryは公式指示に従い省略。ブラウザ受入は実装後の別工程であり本draftの作成では承認しない。
