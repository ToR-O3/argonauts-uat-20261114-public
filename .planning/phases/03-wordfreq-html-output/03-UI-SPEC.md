---
phase: "03"
slug: "wordfreq-html-output"
status: approved
reviewed_at: "2026-11-17T21:08:43+09:00"
shadcn_initialized: false
preset: none
created: "2026-11-17"
---

# Phase 3 — UI Design Contract

> CLI が stdout に生成する静的 HTML の表示契約。公式 UI-SPEC テンプレートによる新規契約。gsd-ui-researcher 作成、gsd-ui-checker の承認は未実施。

## Sources and Scope

- 承認済み r-50053edc / t_13dfdc77 run83、03-CONTEXT.md D-01〜D-11、REQUIREMENTS.md REQ-09〜14、ROADMAP.md Phase 3、`.planning/argonauts/r-50053edc-prd.md`、`openspec/changes/r-50053edc-wordfreq-html/design.md` を使用する。
- 公式 CLI `query init.plan-phase 3` と `query roadmap.get-phase 3` で Phase 3 / wordfreq-html-output / CONTEXT あり / RESEARCH なし / PLAN なしを確認。`query config-get workflow.ui_phase --raw` は true。ROADMAP の `success_criteria` 配列は CLI 結果では空だが、返された section と読取り原本に AC1〜AC6 があるため、空配列を要件なしとは扱わない。
- 本依頼の既存 UI 契約はない。Phase 2 の残存成果は参照・継承しない。RESEARCH・sketch findings・agent-skills の追加入力なし。全決定は確定済みとして質問を行わない。
- 製品は Python 標準ライブラリのみ。既存 `wordfreq/tokenizer.py` の Unicode `\w+` 抽出と casefold、入力境界、既定 top10、正整数制約、exit/stderr 契約を継承。変更は HTML 形式追加と全形式共通の同数時初出順。text/json の構造・空出力は変更しない。
- `wordfreq/formatters.py` は現状 text/json の純粋整形のみ、`pyproject.toml` は dependencies = []。ファイル探索で HERMES.md、components.json、Tailwind/PostCSS 設定、CSS/TSX の既存デザインシステムは検出されない。React/Next/Vite ではないため shadcn 初期化・パッケージ列挙は対象外。
- 本書は設計のみ。製品実装・ブラウザ受入・CI 変更・依存追加・commit/push はしない。下記の表示・検証条件は後続 Builder/品質への義務であり、実行済みの証拠ではない。

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable |
| Component library | none — semantic HTML と文書内 CSS のみ |
| Icon library | none — アイコン・画像なし |
| Font | system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |
| Theme | light 固定、`color-scheme: light`。dark media query・テーマ切替なし |
| Output | UTF-8 の単一 HTML 文書、`<!doctype html>`、`lang="ja"`、先頭側の `meta charset="utf-8"` と `meta name="viewport" content="width=device-width, initial-scale=1"` |
| Runtime | 内包 style のみ。script・外部 CSS/フォント/画像・リンク・フォーム・通信要素なし |

Tool: none のため Component Inventory は設けない。以下は installed library の列挙ではなく、本フェーズで作る意味構造の契約。

### Document Structure and Layout

順序は `main` → `h1`「単語の出現頻度」→ 入力情報ブロック → 結果表 → 空の場合だけ補足文。

- 入力情報は「ファイル名」と basename 値、「総出現回数」と整数値。両方とも表より上に置く。ファイル名は独立した block 要素としラベルと同じテキストノードへ連結しない。ラベル由来の空白を basename の検査に混ぜない。
- `title` は固定で「単語の出現頻度」。元のパスを body/title/属性/CSS/コメントのどこにも埋め込まない。basename もテキストノードだけへ安全に escape し、属性や URL へ転用しない。
- 表は `table` / `caption`「集計結果」/ `thead` / `tbody`、3 個の `th scope="col"`「順位」「単語」「回数」。列の順を変えない。空でも見出しは維持し、tbody 内のデータ行を 0 とする。空文言は tbody 外に置き、colspan の偽データ行を作らない。
- 正常時は 1 行につき順位・正規化語・整数回数。順位は top 適用後の表示行連番 1, 2, 3…であり、同数による同順位・欠番はない。
- body は margin 0。main は `width: 100%`、`max-width: 960px`、`box-sizing: border-box`、左右 auto margin。通常 padding は 32px、viewport 480px 以下は 16px。正常幅は 1280px、狭幅は 320px とする。
- 表は `width: 100%`、`table-layout: fixed`、`border-collapse: collapse`。順位列 56px、回数列 64px、単語列は残り。セル padding は上下左右 8px、垂直位置は top。順位・回数は右寄せ、`font-variant-numeric: tabular-nums`。単語は左寄せ。見出しも各列の寄せに合わせる。
- 数値に固定高さや桁省略を使わない。順位・回数セルも `overflow-wrap: anywhere` を許可し、さらに桁が増えても欠落させない。指定 fixture の 2 桁順位・3 桁回数はそれぞれ同一行で読めること。
- basename と単語値は `white-space: break-spaces; overflow-wrap: anywhere; word-break: normal; tab-size: 4`。連続スペース、改行、タブを保持しつつ長い非空白列も折返す。通常 `white-space: normal` に戻したり、strip/空白圧縮/タブの単一空白化をしない。
- 表・main・ファイル名ブロックは高さ auto。内部スクロール領域・横スクロールを前提にせず、ページの自然な縦スクロールだけで全文を読ませる。固定 min-width、行数制限、ellipsis、nowrap、overflow hidden/clip、文字縮小での回避は禁止。
- 境界線は 1px、角丸・影・カード枠・装飾アニメーションなし。表見出しだけ secondary 背景、データ行は白、行間は下境界線。複数行へ折れた行でも背景や罫線が文字を横切らない。

---

## Spacing Scale

宣言値は 4 の倍数のみ。未使用トークンを画面へ無理に適用しない。

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | 入力情報ラベルと値の間 |
| sm | 8px | 全表セルの padding、入力情報間の間隔 |
| md | 16px | 狭幅 main padding、h1 と入力情報の間 |
| lg | 24px | 入力情報と表の間、空補足文の上余白 |
| xl | 32px | 通常 main padding |
| 2xl | 48px | 予約、今回の表示では未使用 |
| 3xl | 64px | 予約、今回の表示では未使用 |

Exceptions: 1px の罫線は spacing ではない。列幅・max-width は幾何寸法。その他の余白例外なし。狭幅でもセル padding 8px と文字サイズを維持する。

---

## Typography

同一の system font stack を全要素で使用する。フォントサイズは 3 種、weight は 400 / 600 の 2 種のみ。外部フォント取得なし。

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Body | 16px | 400 | 1.5 |
| Label | 14px | 600 | 1.5 |
| Heading | 24px | 600 | 1.25 |

Body は basename、総数の値、表データ、空補足文。Label は入力情報ラベル、caption、列見出し。Heading は h1。caption は左寄せで表の上に 8px の間隔を置く。数値だけ別フォントや小さなサイズへ変更しない。ブラウザの既定 h1/th の weight を残さず明示する。

---

## Color

60/30/10 は役割の配分であり、画素面積を強制する比率ではない。データ量に応じて白面積が増えてよい。

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | #FFFFFF | ページ、入力情報、表本文の背景 |
| Secondary (30%) | #F1F5F9 | 表の列見出し背景のみ |
| Accent (10%) | #1D4ED8 | h1 と総出現回数の数値のみ |
| Primary text | #0F172A | basename、単語、順位、回数、本文、列見出し |
| Secondary text | #475569 | 入力情報ラベル、caption、空補足文 |
| Divider | #CBD5E1 | 表見出し/各データ行の下境界線 |
| Destructive | not applicable | 破壊的操作なし。HTML にエラー用カラーなし |

Accent reserved for: ページ見出し「単語の出現頻度」と総出現回数の数値。リンク風下線、行ごとの色ランキング、任意の語の強調には使わない。順位・情報は色だけで伝えず、ラベルと数値を使う。本文の背景を暗色にする分岐はない。

---

## Copywriting Contract

| Element | Copy |
|---------|------|
| Primary CTA | not applicable — 静的な閲覧結果。ボタンやリンクを作らない |
| Document title / h1 | 単語の出現頻度 |
| Filename label | ファイル名 |
| Filename value | 実行環境のパス規則による basename を一字も省略せず表示。空白を含む元値を保持 |
| Total label | 総出現回数 |
| Total value | top 適用前の総出現回数を 10 進整数で表示。種類数・表示行数・表示行の和にしない |
| Table caption | 集計結果 |
| Column headers | 順位 / 単語 / 回数 |
| Empty state heading | 追加の見出しなし。「集計結果」と 3 列見出しを維持 |
| Empty state body | 集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。 |
| Error state | HTML 内のエラー画面なし。既存 CLI の stderr 診断を維持。読込み/開けない/UTF-8 decode 失敗は exit 1、不正 top/format/引数個数は exit 2、いずれも stdout は空。確認後に CLI を再実行する |
| Destructive confirmation | not applicable — 書込み・削除・確認操作を HTML に持たない |
| Loading / partial results | not applicable — 完成した静的文書のみ。spinner、skeleton、部分行、retry ボタンなし |

空入力は総数 0 / データ行 0 / exit 0。正常 HTML の stdout に説明ログを混ぜない。生成日時や top の説明ラベル等の追加メタ情報は作らない。保存方法は利用説明で示すが、HTML 自体は対話操作を持たない。

---

## Acceptance Fixtures and Browser Contract

以下は後続検証ファイルに固定する入力の定義であり、ここでは生成・実行しない。反復表記は fixture の構成規則であり、製品コマンドに渡すインラインコードではない。Builder は実在する fixture 作成/検証ファイルを用意し、その完了以降にのみ PLAN の検証コマンドで実行する。

### Browser and Viewports

- 対象は Chromium、実行候補は `/usr/bin/chromium-browser`。このパスと `/home/Yuki/.local/bin/playwright` のコマンド解決を確認済み。起動可否・版・製品表示の合格は未確認。
- 既存 Playwright ローカルツールから system Chromium を利用する。インストールが不足する場合は環境側の Chromium/ブラウザツールを利用・整備するが、プロジェクトの依存宣言・lockfile・CI を追加変更しない。ブラウザが使えなければ未検証として止める。
- 通常 viewport は **1280 × 900 CSS px**、狭幅は **320 × 900 CSS px**。deviceScaleFactor 1、ブラウザ既定ズーム 100%。headless Chromium、毎回新しい context、実行時に browser version / executable / OS / 実 font-family と利用フォント情報 / viewport / DPR を保存する。
- 実 CLI stdout の UTF-8 バイト列を HTML として保存し、`file://` で開く。HTML の貼付け、手修正した DOM、テンプレートだけのプレビュー、開発サーバーを受入の代用にしない。
- 両幅で空・通常・top・長文・注入候補を観察する。スクリーンショットは full-page とし、長くて画像全体を一度に読めない場合は全域を覆う重なり付き分割画像も保存・全て閲覧する。

### Fixed Input Matrix

| Fixture | Input / options | Locked expectations |
|---------|-----------------|---------------------|
| empty | `empty.txt`、0 bytes、html | basename 表示、総数0、見出し3列、データ行0、空補足文、exit0 |
| normal/top | 下位ディレクトリの `通常.txt`、UTF-8 `zoo apple zoo banana apple cherry`、top 1 / 2 / 10 | 総数は全て6。行は順に zoo2 のみ / zoo2, apple2 / zoo2, apple2, banana1, cherry1。順位は連番。ディレクトリ情報は全 HTML で不在 |
| frequency | `frequency.txt`、`beta beta beta alpha gamma alpha delta`、top2 | 総数7、beta3 / alpha2。表示行の和5を総数にしない |
| normalized tie | `tie.txt`、`Zoo apple APPLE zoo banana`、top1 / top2、text/json/html | zoo2 のみ / zoo2, apple2。同数を語昇順に戻さない。後の出現で初出位置を変えない |
| long / multi-digit | 下記固定 basename と本文、top12 | 12行、順位1〜12、先頭回数123、末尾回数2、総数200。長語・basename が両幅で実際に複数行になる |
| default / oversized top | long fixture の本文、top省略 / top99 | 省略は10行、top99は全12行。どちらも総数200 |
| injection / UTF-8 | 下記有効 basename、本文 `Café CAFÉ Straße STRASSE 日本語`、html | café2, strasse2, 日本語1、総数5。名前の特殊文字はテキストのまま。追加タグ/属性/通信なし |
| formatter-only escaping | 整形部品へ語値 `& < > " '` と `<img src=x onerror=alert(1)>` を直接渡す | 元の語文字列と表示テキストが一致し、要素・イベント・URL を生成しない。CLI tokenizer は緩めない |

**固定長文 fixture の厳密な構成:**

- 語 L は ASCII 小文字 `w` を **256 個**連続させた 1 語。
- basename B は `集計  ` + ASCII 小文字 `n` を **176 個** + 実 LF + `続き` + 実 TAB + `終わり  &<>"'.txt` の連結。`集計` の直後と `終わり` の直後はそれぞれ ASCII space 2 個。LF/TAB はバックスラッシュ記法の文字列ではなく実際の文字。スラッシュ・NUL は含まない、有効な Linux basename とする。生成場所は検証用の下位ディレクトリ、表示は B だけ。
- 本文は L を123回、`row01` を12回、`row02` を11回、`row03` を10回、`row04` を9回、`row05` を8回、`row06` を7回、`row07` を6回、`row08` を5回、`row09` を4回、`row10` を3回、`row11` を2回の順で並べ、全トークン間を ASCII space 1 個で連結し末尾 LF 1 個。UTF-8 保存。top12 とする。
- L と B 内の長い n 連続部分の双方について、1280/320 の各 viewport で character Range の y 座標が異なる複数行を記録する。LF による改行だけを長い非空白部分の wrapping の代用にしない。
- B は DOM textContent の文字列一致だけでなく、computed `white-space: break-spaces` / `tab-size: 4`、連続空白・LF・TAB のコードポイント位置、各範囲の raw 矩形と画像で空白保持を確認する。空白の不可視性を理由に改行やタブを消さない。
- injection fixture の basename は `検査  &<>"'` + 実 LF + `次` + 実 TAB + `終.txt`。Linux で有効な名前を実ファイルとして実 CLI に渡す。`<script>` 等に似た語は tokenizer の通常抽出結果を維持し、任意記号入りの語の escape は部品試験で補う。
- 保存 HTML のバイト列を strict UTF-8 として復号でき、宣言と実際の保存エンコーディングが一致すること、日本語・é・ß の入力と casefold 後の表示を検証する。`meta charset` の有無だけで合格にしない。

### Geometry and Readability — Raw Evidence Required

1. viewport、document scroll 寸法、main、h1、入力ラベル/値、caption、全 th/td/tr、各データテキストの element `getBoundingClientRect()` と `getClientRects()` を保存する。
2. basename/単語/順位/回数/総数について、全文 Range の行断片および文字単位 Range の `getClientRects()` を原本のまま JSON 化する。テキスト、文字位置、改行・タブ・スペース位置を対応付け、空矩形の文字も省かず記録する。数値は複数桁の全文と各桁を含む。
3. 各対象の全祖先について矩形と computed overflow-x/y を保存し、hidden/clip/scroll/auto 等で切取りを起こす祖先を特定する。隣接セル、前後行、入力情報と表の位置関係も保存する。
4. **合格条件:** ページに横はみ出しがなく、全可視文字の横方向が viewport と該当列内に収まり、切取り祖先の clip 範囲により欠けず、隣接列・前後行・メタ情報と表の表示内容が重ならず、全画像で全文が読めること。正常な縦スクロールによる画面外部分は full-page/分割画像で確認する。
5. own element の厳格な縦包含は必須にしない。文字 Range が自身の要素矩形を縦に越えても、clip・重なり・画像可読性で判断する。画像で読めない文字、罫線への重なり、切取りは不合格。
6. clamp、丸め、座標の差替え、都合のよい矩形の除外をして合格にしない。浮動小数の raw 値を保存し、判定用の比較や説明は別フィールドとする。scrollWidth だけ、DOM 文言だけ、スクリーンショット存在だけでは合格にしない。

### Independence, Network and Acceptance Record

- Builder は実在する検証ファイルと fixture から試験する。品質は対象 head の製品コードで入力原本から CLI を**独立再実行**し、自分の HTML・矩形・画像・通信記録を作る。Builder の HTML/画像の流用だけでは品質合格にしない。
- 開始時の head、git status、製品差分を保存し実行コードと対応付ける。未コミットの製品差分がある状態を対象 head の結果と偽らない。
- ケースごとに入力原本（basename は制御文字が分かる形でも併記）、exact argv、実行 cwd、exit、stdout 生バイト/保存 HTML、stderr、期待順・回数・総数、browser/version/viewport、raw geometry、全画像、画像の閲覧と可読性判定、通信記録を結び付ける。証拠索引を AC1〜AC6 に対応付ける。
- 通信観測は page を開く前に開始し、画像・表示確認終了まで継続。要求、failed request、document/navigation、popup 等の文書由来の遷移、initiator/frame/url/outcome を観測できる既存ブラウザ手段を使い、試行そのものを記録する。`file://` の最初のローカル文書読込みは外部通信と区別して残す。
- 外部要求・外部遷移は成功/失敗/遮断に関係なく文書起因なら不合格。ネットワークを遮断したことや成功要求が0であることだけでは無通信の証拠にならない。ブラウザ背景通信を除外する場合は、ページ frame/initiator、別の空 context の記録等の区別根拠を残す。文書起因か判定できない通信は未検証とする。
- HTML の静的解析でも script、外部 resource 属性、CSS url/@import、イベント属性、meta refresh、リンク/フォーム/埋込み等の通信・実行経路の不存在を確認し、ブラウザ観測と併用する。
- 読込み/開けない/decode 失敗、引数個数、不正 top 0/負数/非整数、不正 format の回帰も実 CLI で確認。既存 text/json の空出力と構造、入力取得境界、抽出/casefold は同数順以外を変えない。
- 未実行・環境不足・未閲覧画像・測定漏れ・通信観測漏れは合格にしない。PLAN の後続検証コマンドは、その task 完了時に実在する試験/検証ファイルを repo root から起動する。インラインコード・ヒアドキュメント・外側 cd/grep・無検査で成功する no-op は使わない。計画作成中に未作成コマンドを試さない。

---

## UI Considerations

公式 ui-phase Step 9.5 のprobeを実行。入力/出力原本: `.planning/argonauts/t_bd1bf85e/ui-probe-{elements,report}.json`。検出kindを再確認しE1/E2/E4はstatic-content、E3はlist-collection+static-contentを明示した。applicable14、unclassified0。以下は--autoで既存契約から全14項目をexplicit解決した設計上の真実であり、製品検証の実施結果ではない。

Applicable state considerations resolved: 14/14 (explicit); unresolved 0.

| Element(s) | Category | Resolved truth (verification: explicit) |
|------------|----------|-----------------------------------------|
| E1 heading | overflow, long-text | 固定h1は自然に折返し、1280/320 CSS pxのviewportから横にはみ出さない。省略・切取りなし。 |
| E2 metadata | overflow, long-text | basenameは固定長文fixtureの連続文字/空白/LF/TABを保持し折返す。総数は省略せず表示。両幅でraw文字Range・clip・非重複・全画像可読性を満たす。 |
| E3 table | empty | Copywriting Contractの空表示を使用し、見出し3列・tbody0データ行・総数0を維持する。 |
| E3 table | loading | 完成した静的文書だけを生成し、取得中のHTML・spinner・skeletonは生成しない。 |
| E3 table | error | エラー時はstdout空、既存stderr/exit1または2。エラーHTMLやretry操作は追加しない。 |
| E3 table | populated | normal/top fixtureの固定語順・回数・順位と総数を表示する。 |
| E3 table | partial | 完成文書のみ。topは意図した表示制限であり欠損ではなく、総数は全入力。部分データ状態は生成しない。 |
| E3 table | overflow, long-text | 長文fixtureは両幅で非空白列も折返し、横はみ出し・clip・隣接重複なし、全画像で全文可読。生矩形を補正しない。 |
| E3 table | zero-one-many | empty/top1/top2/top12の0/1/多数行を同じ3列で表示し、順位は連番、複数桁数値も欠けない。 |
| E4 empty message | overflow, long-text | Copywriting Contractの固定本文を自然に折返し、両幅で横収まり・非重複・画像可読性を満たす。 |

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable — shadcn も第三者 registry も使わない |

外部パッケージ・デザインシステムの導入、Web フォント・CDN・JS の追加で表示や検証を解決しない。検証用ブラウザは環境側のツールであり、製品依存ではない。

---

## Checker Sign-Off

- [x] Dimension 1 Copywriting: PASS
- [x] Dimension 2 Visuals: PASS
- [x] Dimension 3 Color: PASS
- [x] Dimension 4 Typography: PASS
- [x] Dimension 5 Spacing: PASS
- [x] Dimension 6 Registry Safety: PASS
- [x] Dimension 7 Inventory Provenance: PASS

**Approval:** approved — independent gsd-ui-checker sa-0-3e89e909, ## UI-SPEC VERIFIED, no recommendations。親がpost-verification probeを実行し設計条件をexplicit解決。製品のブラウザ受入は未実施。
