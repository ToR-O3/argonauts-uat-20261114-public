---
phase: "08"
slug: "wordfreq-html-displayed-types"
status: approved
reviewed_at: "2026-11-26T05:15:10+09:00"
shadcn_initialized: false
preset: none
created: "2026-11-26"
---

# Phase 08 — UI Design Contract

> wordfreq HTML displayed types。既存の静的HTMLを継承する設計契約。公式UI checkerは7/7 APPROVED（2026-11-26T05:15:10+09:00）。実装・描画の受入は未実施。

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable |
| Component library | none — Python標準ライブラリで生成する静的HTML |
| Icon library | none |
| Font | system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |

既存の `wordfreq/formatters.py` の内包CSS・HTML構造が継承元である。`pyproject.toml` のruntime dependenciesは空。React/Next.js/Viteではなく、`components.json` もないためshadcn初期化・package inventory・registry vettingは適用外。新ライブラリ、依存、デザインシステム、アイコン、Web fontを導入しない。Component Inventory節はTool: noneのため省略する。

### Source and precedence

- `.planning/phases/08-wordfreq-html-displayed-types/08-CONTEXT.md` D-01〜D-06とspecifics：承認済みの表示意味、横配置、互換例外、独立品質検証を固定。
- `.planning/REQUIREMENTS.md` REQ-29〜REQ-31、`.planning/ROADMAP.md` Phase 8：現在の受入条件。
- `.planning/argonauts/r-6ae2cbf2-prd.md` と `openspec/changes/r-6ae2cbf2-html-displayed-types/design.md`：最終pairsを唯一の件数根拠とし、局所変更に限定。
- `wordfreq/formatters.py`：以下の実在する色・文字・余白・表・空状態の値の出典。
- Phase 8のRESEARCH/sketchは未作成。追加の製品判断は不要。AGENT_SKILLS_UIの公式skills-only queryは空。プロジェクト内HERMES.md、.hermes/skills、.agents/skillsは検出されなかった。

承認済みの表示追加と必要最小レイアウト以外は継承する。過去Phase 4/7のCONTEXT、封印baseline、完了履歴は変更しない。過去依頼の画像省略判断は今回に適用しない。

---

## Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | 既存label下余白 |
| sm | 8px | 既存metadata-item間、caption下、tableセルpadding。総数値と新文言の局所的な横gapにも使用 |
| md | 16px | 既存h1下余白、480px以下のmain padding |
| lg | 24px | 既存metadata下余白、空状態の上余白 |
| xl | 32px | 既存通常幅main padding |

48px/64pxの新規余白は必要ないため追加しない。Exceptions: 既存の1px table罫線はspacing tokenではなく維持する。0 marginも維持する。

### Layout contract

1. 既存mainのwidth:100%、max-width:960px、border-box、左右auto marginを維持。480px以下のみpadding:16px、それ以外32px。
2. 順序はh1 → metadata（ファイル名labelとbasename全文、総出現回数labelと値＋新文言）→ caption付き3列表 → 既存の空状態文言（空結果のみ）。
3. `総出現回数` labelは現状どおり値の上に置く。その値のすぐ右に8px gapで `表示 N 種類` を同じ論理行・同じ表示区画に置く。総数値が左、新文言が右。1280×900と320×900 DPR1の受入ケースの両方で横並びを維持する。新たな縦積みmetadata-item、表の追加列、badge/cardは作らない。
4. 最小実装は値と新文言だけを包む局所inline/flex行とする。既存`.total-value`の見た目を保ち、新文言はbody typographyを使う。新文言内のスペースを維持する。大きい内容で折返しが必要な場合も同じ論理区画内で全文を読めるようにし、固定高、切取り、ellipsis、文字縮小で逃げない。通常の受入ケースを縦積みにする根拠にはしない。
5. basenameは上の独立した既存filename区画で折返す。metadataの横gapのためにbasenameや表の幅を削らない。
6. tableはwidth:100%、table-layout:fixed、border-collapse:collapse。rank列56px、count列64px、残りword列、数値右寄せ・tabular-nums、セル上寄せを維持する。
7. 長語・長basenameは既存white-space:break-spaces、overflow-wrap:anywhere、word-break:normal、tab-size:4を継承し、全文を省略せず読む。ページ横overflow、重複、切取りを起こさず、長い内容の縦スクロールは許容する。

---

## Typography

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Body / basename / table data / total value / displayed count | 16px | 400 | 1.5 |
| Label / caption / table headers | 14px | 600 | 1.5 |
| Heading h1 | 24px | 600 | 1.25 |

サイズは既存3種、weightは400/600の2種のみ。独立したDisplay roleは設けない。新文言を見出し化・太字化・小文字化しない。見出しのline-heightをテンプレート推奨値へ変更しない。

---

## Color

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60% role) | #FFFFFF | ページ背景・table dataセル |
| Secondary (30% role) | #F1F5F9 | 既存table header背景のみ |
| Accent (10% role) | #1D4ED8 | 既存h1と総出現回数の値のみ |
| Body ink | #0F172A | 既存本文・basename・table data、新しい表示N文言 |
| Muted ink | #475569 | 既存label、caption、空状態文言 |
| Border | #CBD5E1 | 既存tableの下罫線1px |
| Destructive | not applicable | 破壊操作なし。新しいsemantic colorなし |

Accent reserved for: h1、既存`.total-value`。新文言・表の行・数字を新たにaccentで強調しない。60/30/10は役割分類であり、既存の白基調ページを面積比へ塗り直す指示ではない。ライトのみ、`color-scheme: light`を維持し、テーマ切替・dark variantは追加しない。

---

## Copywriting Contract

| Element | Copy |
|---------|------|
| Page title / h1 | 単語の出現頻度 |
| Basename label | ファイル名 |
| Total label | 総出現回数 |
| Total value | 既存のtotalを10進文字列で表示。min/max/top前のcounts和 |
| Displayed count | `表示 N 種類` — Nを最終pairsのlenの10進文字列で置換。例：表示 0 種類、表示 1 種類、表示 3 種類、表示 10 種類。空白は各1個、括弧や追加句読点なし |
| Table caption | 集計結果 |
| Table headings | 順位 / 単語 / 回数 |
| Primary CTA | not applicable — 出力専用の静的HTMLに操作なし |
| Empty state heading | not applicable — 新しい見出しは作らない |
| Empty state body | 集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。 |
| Error state | not applicable in HTML — 既存CLIのstderr/exitを維持し、エラーHTMLやretry UIを作らない |
| Destructive confirmation | not applicable — 破壊操作なし |
| README追加1行 | HTMLでは総出現回数の横に「表示 N 種類」を示し、Nは絞込み・top適用後の表示語種類数で、空結果は0です。 |

Nはtop引数値、表示回数の和、元の全種類数ではない。`format_html(pairs, basename, total)`の公開引数は変更しない。追加の入力読込み・集計・選択処理を作らず、既存pairsから求める。順位は残った行に1から連番、回数降順・同数初出順は不変。

READMEは既存HTML説明へ上の1行だけを追加する。上限・下限の説明や既存JSON例、無関係な本文は変更しない。

---

## UI Considerations

公式post-verification probeをchecker後に実行し、exit0とJSON形を確認。E1 metadata、E2 read-only results table、E3 empty result surfaceを入力し、22 applicable / 0 unclassified。`--auto`のkind確認として全文を再読し、いずれも静的データ表示でありform/action/media等の欠落なしと判断。下表は全E1/E2/E3に共通のカテゴリをまとめたexplicit解決であり、描画合格を意味しない。empty/populated/partial/zero-one-manyは現行ケース試験、overflow/long-textは実ブラウザで後続検証する。loading/errorは理由付きdismissed（非同期なし、エラー時HTMLなし）。未解決の製品判断なし。

| Category | Element(s) | Status | Resolution / Reason |
|----------|------------|--------|---------------------|
| empty | Results table / metadata | 契約明示・検証待ち | 空・空白・記号のみは総数0、N0、theadと0データ行、Copywriting Contractの既存空状態bodyを保持。全除外は元総数を保ちN0 |
| populated | Results table / metadata | 契約明示・検証待ち | max2の承認入力はalpha2/gamma1/delta1、総数7、N3。総数とNを表より上の同じ行に置く |
| zero-one-many | Results table / metadata | 契約明示・検証待ち | 0/1/3/10/12種類を扱い、1でも文言は種類。候補12で既定topはN10、top99はN12。見出しをNに含めない |
| partial | Filtered results table | 契約明示・検証待ち | min/max/topで絞った完成済み結果を表示し、欠損やロード途中のplaceholderを追加しない。beta4/zoo3/apple2/pear2/single1、min2/max3/top1ではzoo3の1行、総数12、N1 |
| overflow | Metadata / results table | 契約明示・実描画待ち | 両viewportで数値・新文言・表の横overflow、重複、切取りなし。縦スクロール可。raw文字Rangeを補正せず保存し、厳格な自己縦包含だけを合否にしない |
| long-text | Basename / word cells | 契約明示・実描画待ち | 既存wrapを継承し、長basename・長語を全文可読にする。省略やパス露出なし |
| loading | Results table | 適用外・理由明示 | CLIが完成した自己完結HTMLを出すため非同期取得・ロード状態なし |
| error | Results table | 適用外・理由明示 | 入力失敗・usage失敗は既存CLI stderr/exitで処理しHTMLを出さない。HTML内error UIは対象外 |

### Verification handoff

- OpenSpec tasks 1.1：`tests/test_formatters.py`、`tests/test_cli.py`に先行REDを追加。文言・元総数・最終行数・表より前の構造を検証し、構造だけで「横」を証明したとは扱わない。
- OpenSpec tasks 1.2：局所実装GREEN、全pytest、README差分1行。通常、top1/top99、12候補の既定top10、min/max境界・併用・矛盾範囲、空/語なし/全除外、Unicode `Straße STRASSE`の合算を含む。
- OpenSpec tasks 2.1：品質が対象headで実CLI生成と全pytestを独立実行。1280×900、320×900、DPR1で通常・絞込み/top・空・長basename/長語・escape候補を描画し、総数横の配置と全内容の可読性を確認する。
- 変更前同条件の原本と比較し、許すのは新文言とその必要最小レイアウトのみ。封印済み過去baselineは上書きせず、今回用期待値または狭く明示した変換を使用する。text/jsonは全バイト・末尾改行を含め旧固定期待値を維持する。過去snapshot専用scope gateは今回の合否と区別する。
- basenameと単語のescape、HTML全体にdirectory情報なし、内包CSSのみ、script/外部参照/外部通信試行なしを維持。新しいデータ属性・リンク・tooltip・通信・interactionは追加しない。
- 品質は入力/argv/exit/stdout/stderr/検証head/HTML原本/browser/viewport/raw Range/通信試行（失敗も含む）/全画像の実閲覧を追跡可能にし、AC別結果と実際の画像閲覧枚数・内容・結果をVERIFICATION.mdとCLI/CI文字証拠へ記録し標準添付する。PMはread_fileで判断でき、画像やarchiveの閲覧を要求されない。未実施・未報告CIを成功扱いしない。
- 本契約の作成時に未作成の検証コマンドを試行しない。PLANは実在する検証ファイルを根拠に実行コマンドを定め、Builder・品質が実行する。新サービスや新依存は必要ない。

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable — shadcn未使用、第三者registry/外部component/assetなし |

---

## Checker Sign-Off

- [x] Dimension 1 Copywriting: PASS
- [x] Dimension 2 Visuals: PASS
- [x] Dimension 3 Color: PASS
- [x] Dimension 4 Typography: PASS
- [x] Dimension 5 Spacing: PASS
- [x] Dimension 6 Registry Safety: PASS
- [x] Dimension 7 Inventory Provenance: PASS

**Approval:** approved — independent gsd-ui-checker sa-0-e69bfede、7/7、通常終了・truncated:false。post-verification probe exit0。実装・ブラウザ受入の合格とは別。
