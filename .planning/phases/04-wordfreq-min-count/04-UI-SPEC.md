---
phase: "04"
slug: "wordfreq-min-count"
status: approved
reviewed_at: "2026-11-18T06:38:48+09:00"
shadcn_initialized: false
preset: none
created: "2026-11-18"
---

# Phase 4 — UI Design Contract

> 既存CLIに閾値だけを追加する表示・操作契約。既存HTMLの見た目は絶対不変。公式テンプレートに従った研究原本であり、checker承認・製品受入・baseline採取の完了を意味しない。

## Sources and Scope

- 承認済み r-e476c11d / t_a438e6b2 run140、`04-CONTEXT.md` D-01〜D-12、`04-RESEARCH.md`、`.planning/REQUIREMENTS.md` REQ-15〜21、ROADMAP Phase 4、`.planning/argonauts/r-e476c11d-prd.md` を読了。新しいユーザー判断は不要、確定事項を再質問しない。
- `.planning/phases/03-wordfreq-html-output/03-UI-SPEC.md` 全文と `wordfreq/formatters.py` 全文を現物照合した。以下のspacing/typography/color/copy/静的安全性はその継承であり、新デザインではない。Phase 2の残存成果は使わない。
- `wordfreq/__main__.py:12–47` と `pyproject.toml` を読了。現行はmin-count未実装、dependenciesは空。新しいUI要素・HTML構造・CSS・既存文言・formatter公開契約を追加変更しない。製品の変更対象は既存CLIの引数と共通選択だけ。
- 公式CLI `node /home/Yuki/workspace/argonauts-uat-20261116/home/.hermes/profiles/argonauts-uat-architect/gsd-core/bin/gsd-tools.cjs query init.phase-op 4` は phase_found=true、phase_number=04、has_context=true、has_research=true、has_plans=false、plan_count=0。STATE.mdのPhase 3完了表示はPhase 4の完了証明ではない。
- 調査時headは `1106acb0766fb7de446a1bce6382677f923879c7`。これは読取り時の識別子であり、baseline保存headを認定したものではない。既存 `.planning/state.json`、Phase 4 `.gitkeep` / RESEARCHの変更は触らない。
- root HERMES.md、project `.hermes/skills` / `.agents/skills` は不存在。ファイル探索でcomponents.json / package.json / SKILL.mdは検出なし。公式追加agent-skills・sketch findingsなしは呼出し元の確定入力。
- この工程はUI-SPEC原本のみ作成する。製品・検証コード、baseline、受入証拠、CI、依存は変更しない。commit/push/Kanbanは親の担当。

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable |
| Component library | none — 既存semantic HTMLと文書内CSSを無変更で使う |
| Icon library | none — アイコン・画像なし |
| Font | system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |
| Theme | light固定、`color-scheme: light`。dark分岐・切替なし |
| Output | UTF-8単一HTML、doctype、lang=ja、charset、viewport宣言を保持 |
| Runtime | 内包styleのみ。script・外部参照・通信・フォーム・対話操作なし |

Python CLIでありReact/Next/Viteではない。shadcn初期化・registry導入・package列挙は対象外。Tool: noneのためComponent Inventory節は設けない。

### Existing Document and Layout — No Changes

現物根拠: `wordfreq/formatters.py:22–127`、継承元 `03-UI-SPEC.md` Document Structure and Layout。

- 順序はmain → h1 → metadata（ファイル名、総出現回数）→ table（caption、thead、tbody）→ pairsが空の場合だけempty-message。basename値はラベルから独立したblockのtext node。totalも独立値で、両者は表より上。
- 列は順位・単語・回数の3列、`th scope="col"`を維持する。表示行は閾値とtop適用後の共通pairsで、順位は1始まりの欠番なし連番。元順位・同順位表示にしない。
- body margin 0。main width 100%、max-width 960px、border-box、左右auto margin、padding 32px。480px以下のみpadding 16px。今回の検証幅は1280pxと320px。
- tableはwidth 100%、fixed layout、collapse。順位列56px、回数列64px、単語列は残り。全セルpadding 8px、vertical-align top。順位/回数は右寄せ・tabular-nums、単語は左寄せ。固定高さなし。
- basename/単語は `white-space: break-spaces; overflow-wrap: anywhere; word-break: normal; tab-size: 4`。連続空白/LF/TAB/CRを削除・圧縮しない。h1、数値セル、空文言も折返し可能な現行規則を保持。
- ページの自然な縦スクロールだけで全文を読めること。横スクロール依存、ellipsis、nowrap、行数制限、overflow hidden/clip、文字縮小、新min-widthは禁止。
- 見出し背景と1px下境界線を維持。新カード、影、角丸、ランキング色、装飾、アニメーションなし。絞込みによる行数・文書高さの変化は意図したデータ変化であり、レイアウト変更ではない。

---

## Spacing Scale

現物根拠: `wordfreq/formatters.py:56–102`。既存4px単位スケールを保持する。

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | 入力ラベルと値の間 |
| sm | 8px | 全セルpadding、metadata-item間、caption下 |
| md | 16px | 狭幅main padding、h1下 |
| lg | 24px | metadata下、空文言上 |
| xl | 32px | 通常main padding |
| 2xl | 48px | 継承予約値、現物では未使用・新適用禁止 |
| 3xl | 64px | 継承予約値、現物では未使用・新適用禁止 |

Exceptions: marginリセットの0、1px罫線はspacing tokenではない。56px/64px列幅と960px max-widthは幾何寸法。新たな余白例外なし。

---

## Typography

現物根拠: `wordfreq/formatters.py:47–77`。サイズ3種、weight2種を無変更で継承する。

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Body | 16px | 400 | 1.5 |
| Label | 14px | 600 | 1.5 |
| Heading | 24px | 600 | 1.25 |

Bodyはbasename/総数値/全データセル/空文言。Labelはmetadataラベル/caption/th。Headingはh1。外部フォント・別数値フォント・Displayサイズ追加なし。狭幅でもサイズを変えない。

---

## Color

現物根拠: `wordfreq/formatters.py:46–101`。60/30/10は既存役割配分で、画素面積の強制比率ではない。

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | #FFFFFF | ページ・入力情報・表本文 |
| Secondary (30%) | #F1F5F9 | th背景のみ |
| Accent (10%) | #1D4ED8 | h1と総出現回数の数値のみ |
| Primary text | #0F172A | basename、単語、順位、回数、本文、列見出し |
| Secondary text | #475569 | metadataラベル、caption、空文言 |
| Divider | #CBD5E1 | th/td下境界線 |
| Destructive | not applicable | 破壊的操作・HTMLエラー画面なし |

Accent reserved for: h1「単語の出現頻度」と総出現回数の数値のみ。閾値、除外、回数境界を色で強調しない。lightのみ、テーマ追加なし。

---

## Copywriting Contract

現物根拠: `wordfreq/formatters.py:34–44,107–124`。HTML文言は一字も変えない。

| Element | Copy |
|---------|------|
| Primary CTA | not applicable — ボタン・リンク・閾値入力・適用/再試行操作を追加しない |
| Document title / h1 | 単語の出現頻度 |
| Filename label | ファイル名 |
| Filename value | 実行環境のパス規則によるbasenameのみ、全文・空白を保持 |
| Total label | 総出現回数 |
| Total value | casefold後の元countsの回数和。min-countとtopの両適用前の10進整数。種類数・表示行数・表示行の和ではない |
| Table caption | 集計結果 |
| Column headers | 順位 / 単語 / 回数 |
| Empty state heading | 新見出しなし。captionと3列見出しを保持 |
| Empty state body | 集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。 |
| Error state | HTMLなし。使い方エラーはstderr/exit2、入力読込み・decode失敗はstderr/exit1、stdoutは空。既存argparse/int診断方式を保持し、Traceback/エラーHTMLは出さない |
| Destructive confirmation | not applicable — 書込み・削除操作なし |
| Loading / partial results | not applicable — 完成文書だけ。spinner/skeleton/部分取得/再試行UIなし |
| README-only recovery | 全除外時はmin-countを下げる案内を最小追記する。HTMLの既存空文言の改善・置換は禁止 |

新しい閾値表示ラベル、除外件数、フィルタchip、空理由分岐、生成日時をHTMLへ追加しない。正常stdoutに説明ログを混ぜない。

### CLI Interaction and Data Contract

- `--min-count N`は既定1、1以上の整数のみ。`--top`は独立した既定10の正整数。オプション指定順に意味差なし、大小の相互制約なし。
- 0/負数/非整数/非数値/値欠落は、入力取得より先にstderr/exit2・stdout空。有効N>1で不存在/ディレクトリ/開けない/不正UTF-8なら既存exit1を維持し、空結果へ変換しない。
- Unicode抽出 → casefold → 元counts → 元total保持 → N未満を除外 → 回数降順・同数時正規化後初出順 → top → 全形式共通pairs。元countsを破壊せず、旧語昇順へ戻さない。品質は出力だけでなくフィルタ→topのソース箇所を記録する。
- thresholdちょうどと超過は残す。textは既存count/TAB/word/LF、jsonは既存word/count配列・ensure_ascii=True・末尾LF1つ。空結果はtext空文字、json `[]` + LF、HTMLは既存メタ情報・見出し・tbodyデータ0行・固定空文言。全て正常exit0。
- 空/空白/句読点だけならHTML total0。語あり全除外ならデータ0行でも元の正totalを保持する。
- 未指定・明示1は変更前stdoutと全3形式でbytes一致。HTML原本・構造・CSS・copyも一致。既定text/top10・同数初出順を維持。

---

## UI Considerations

公式Step 9.5 probeを親が実行し、適用14・未分類0を確認（原本: `.planning/argonauts/t_34cd1b56/UI-ELEMENTS.json` と `UI-PROBE.json`）。`--auto`のkind-confirmationで4要素のkindを原文へ再照合し、E3はlist-collectionとstatic-contentの両方、他はstatic-contentとした。以下14項目は設計上のresolved/explicitであり、製品・ブラウザ試験合格ではない。COPYは上のCopywriting Contractを参照する。

| ID | Category | Status | Verification | Truth |
|----|----------|--------|--------------|-------|
| E1 | overflow | resolved | explicit | h1は両幅で折返し横収まりし、省略・切取り・隣接重複なし。 |
| E1 | long-text | resolved | explicit | h1は既存24px/600のまま全文表示し、文字縮小しない。 |
| E2 | overflow | resolved | explicit | metadataのbasename/元totalは表より上、両幅で横収まり・非重複・切取りなし。 |
| E2 | long-text | resolved | explicit | 長basenameと連続空白/LF/TAB/CR・元totalを保持しraw Rangeと全画像で全文可読を検証する。 |
| E3 | empty | resolved | explicit | 空/抽出0語/全除外は既存0データ行とCopywriting Contractの空表示。元totalは前二者0、全除外は正の元値。 |
| E3 | loading | resolved | explicit | CLIは完成HTMLだけをstdoutへ出す。loading/部分取得UIを生成しない。 |
| E3 | error | resolved | explicit | 入力/使い方失敗はCopywriting Contractのexit1/2とstderr、stdout空。エラーHTMLなし。 |
| E3 | populated | resolved | explicit | 閾値後top後の共通pairsを既存3列と1始まり連番に表示し、元totalを維持する。 |
| E3 | partial | resolved | explicit | min-count/topは完成データの意図した表示制限であり、不完全データ・追加補足UIを生成しない。 |
| E3 | overflow | resolved | explicit | 表は既存幅/列/CSSで長語・数値を折返し、横はみ出し・clip・隣接重複なし。rawを補正しない。 |
| E3 | zero-one-many | resolved | explicit | 0/1/複数行でも同じ3列・copy・metadata・見出しを保持し、表示順位に欠番なし。 |
| E3 | long-text | resolved | explicit | 長語・複数桁数値を既存字形/サイズで全文表示し、全画像閲覧とraw Rangeで裏付ける。 |
| E4 | overflow | resolved | explicit | 空文言は両幅で自然折返し、横収まり・非重複・切取りなし。 |
| E4 | long-text | resolved | explicit | Copywriting Contractの固定空文言を省略・置換・縮小せず全文表示する。 |

---

## Baseline and Independent Browser Acceptance

この節は後工程への義務。現在baseline採取、pytest、ブラウザ起動/撮影/実閲覧、画像比較、配送は未実施。未実施を合格にしない。

### Before the First Product Change — Hard Gate (AC2 / REQ-16)

1. Builderは最初の製品変更より先に、実装着手前head・git status/製品差分・cwd・環境・入力原本・正確なargv・exit/stdout/stderrを保存する。同数語と10種類超を含む同一入力を全3形式に使い、既定text/top10も固定する。basename/入力バイト列を後比較で変えない。
2. 変更前CLIのtext/json/html stdout、生HTML原本、1280×900と320×900 CSS px・DPR1の画像を保存する。baseline取得時はまだ存在しないmin-countを渡さない。保存原本・索引が読めることを確認してから製品編集へ進む。失敗なら停止する。
3. ブラウザは既存Chromium/既存検証環境、ズーム100%、fresh context、file URLの実CLI生成HTML。browser版/executable/OS/実フォント/viewport/DPR/描画条件を記録する。新依存・新CI・新サービスは作らない。
4. 変更後の未指定と明示1を変更前の全形式stdoutとbytes比較し、同環境・同条件画像で見た目を比較する。変更後同士だけの比較、後から旧headを取り直すことを事前保存の代用にしない。

### Required States and Literal Expectations

以下は仕様由来の期待値であり、実行結果ではない。Builderが実在する入力/検証ファイルへ固定し、その後にだけ実行する。

| Input / state | Options | Expected rows / HTML total |
|---------------|---------|----------------------------|
| 同数語＋10種類超のbaseline入力 | min未指定 / 明示1、既存引数を固定 | 変更前と全形式bytes一致、既定top10・初出順・画像不変 |
| `beta beta beta alpha gamma alpha delta` | min2 / top10 | beta3、alpha2 / total7 |
| 同上 | min2 / top1 | beta3 / total7 |
| 同上 | min4 | データ0行、既存空文言 / total7 |
| `Zoo apple APPLE zoo banana` | min2 / top10、min2 / top1、指定順逆転 | zoo2・apple2、またはzoo2 / total5、語昇順禁止 |
| 同上 | min3 | データ0行、既存空文言 / total5 |
| `Straße STRASSE` | min2 | strasse2 / total2 |
| 空ファイル・空白のみ・句読点のみ | 有効N | データ0行、既存空文言 / total0 |
| Phase 3固定長語/長basename/複数桁・注入候補 | 既存条件＋閾値条件 | 既存全文・空白保持・折返し・安全性を維持、期待pairsと元totalを独立固定 |

Phase 3の固定長文/特殊basenameの定義は `03-UI-SPEC.md` Fixed Input Matrixを継承し、字数・文字列を再設計しない。

### Quality-Owned Verification and Evidence (AC1 / 2 / 4 / 5 / 6 / 7)

- 品質自身が対象head・入力原本からCLIを独立再実行し、既定/閾値部分表示/top併用/全除外/空を両viewportで開く。BuilderのHTML/画像、自動capture成功、過去Phaseの合格だけで独立閲覧を代用しない。
- 同環境のbaselineと比較する。未指定/1はそのまま一致、N>1では対象行・連番・元total・既存空状態だけが意図した変化。環境差を見た目不変の証拠に使わない。
- full-pageと必要な全域分割画像を保存し、品質が全画像を実閲覧する。DOM文言一致、画像の存在、scrollWidth単独では可読性PASSにしない。
- Phase 3のraw geometry契約を継承する。basename/語/順位/回数/総数の全文・文字単位Range、空白/制御文字位置、全祖先の矩形とcomputed overflow、隣接列/前後行/metadataの非重複を保存。丸め/clamp/都合のよい除外でraw値を修正しない。
- 横方向viewport/列内収まり、clipによる欠けなし、隣接重複なし、全画像全文可読を判定する。自身の要素矩形への厳格な縦包含は必須にしない。自然な縦スクロール領域はfull-page/全tileで確認。
- 静的安全性は `wordfreq/formatters.py:17–19,39–127` を継承。escape(quote=True)とCR保護、UTF-8、basename限定を維持。title/属性/コメントを含む全HTMLへdirectoryを埋め込まない。script/イベント属性/CSS url/@import/meta refresh/外部resource/リンク/フォーム/埋込みなし。
- 通信観測はpageを開く前から画像/閲覧完了まで。要求/failed request/navigation/popupとframe/initiator/url/outcomeを保存。最初のfile文書読込みと外部通信は区別。失敗・遮断でも文書起因の外部試行は不合格、背景通信の除外には帰属根拠が必要。不明なら未検証。
- 各ケースにhead/run/actor/root/path/SHA、入力、exact argv、cwd、exit/stdout/stderr、期待pairs/元total、生HTML、browser環境、raw、全画像、閲覧結果、比較結果、ソース順序箇所を結び付け、今回AC1〜7/REQ-15〜21の索引を作る。保存→標準添付→PM原本読取りは別gate。拒否・不能は迂回せず停止して理由を報告する。
- Phase 3 verifierは固定scope/head/AC1〜6を持つため、無変更の旧判定を今回合格装置として使わない。今回専用の実ファイルを後工程で用意し、既存汎用採取部品を使う。新driverの実在・CLIを本書では捏造しない。
- PLAN検証はBuilder/品質がそのtaskで実在化・確認した試験/検証ファイルから実行する。計画中の未作成コマンド試走、インラインコード、ヒアドキュメント、無検査no-opは禁止。
- 全pytestの収集件数/実コマンド/環境/exitを保存。0件収集・skipでの穴・未閲覧・観測漏れ・配送不能はgaps。既存CIのpending/未報告を成功と呼ばず、CI追加変更・待機ループを作らない。

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable — shadcn・第三者registry・外部packageを導入しない |

依存/CI/新デザイン/新入力元/抽出変更/全体リファクタは禁止。検証のためにも製品CSS/DOM/文言を手修正しない。

---

## Checker Sign-Off

- [x] Dimension 1 Copywriting: PASS
- [x] Dimension 2 Visuals: PASS
- [x] Dimension 3 Color: PASS
- [x] Dimension 4 Typography: PASS
- [x] Dimension 5 Spacing: PASS
- [x] Dimension 6 Registry Safety: PASS
- [x] Dimension 7 Inventory Provenance: PASS

**Approval:** approved — 独立gsd-ui-checker sa-0-2e004355 は7/7 PASS、BLOCK/FLAGなし、通常終了。Step9.5 probeは親が原本保存して設計truthへ解決。製品受入・baseline採取・試験は後工程であり未実施。
