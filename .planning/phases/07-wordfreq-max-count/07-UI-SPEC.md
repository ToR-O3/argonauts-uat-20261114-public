---
phase: "07"
slug: "wordfreq-max-count"
status: approved
shadcn_initialized: false
preset: none
created: "2026-11-25"
---

# Phase 7 — UI Design Contract

> 既存HTMLの表示を保持する契約。新しいUIを設計しない。変更は共通選択に上限を加えることで生じる表示行だけであり、HTML構造・CSS・ラベル・空文言・レイアウトは変更しない。checker承認と製品受入は別工程。

## Sources and Scope

- 承認原本: `.planning/argonauts/r-d4bcda40-prd.md`（proposal、全spec scenario、tasksの結合）、`07-CONTEXT.md` D-01〜D-08、`.planning/REQUIREMENTS.md` REQ-23〜REQ-28、ROADMAP Phase 7。未決事項なし。`--auto`の無人実行として確定事項を再質問せず採用する。
- 現物: `wordfreq/formatters.py:1–127`、`wordfreq/__main__.py:13–54`、`pyproject.toml`。既存デザインの継承元は `.planning/phases/04-wordfreq-min-count/04-UI-SPEC.md`。Phase 4のデザイントークンと現行formatterを照合し、以下に具体値を固定する。旧承認・画像・head・独立品質合格はPhase 7の証拠に流用しない。
- 公式CLI `gsd-tools.cjs query init.plan-phase 7` はphase_found=true、phase_number=07、has_context=true、has_research=false、has_plans=falseを返した。`query roadmap.get-phase 7`はfound=true、`query config-get workflow.ui_phase --raw`はtrue。STATEのPhase 5完了表示を今回の完了としない。
- RESEARCH.md、sketch findings、公式追加UI agent-skillsはなし。ファイル探索でHERMES.md、SKILL.md、components.json、package.json、Tailwind設定は検出なし。Python stdlib-only CLIでありReact/Next/Viteではない。
- 基本の製品差分は `wordfreq/__main__.py`、関連CLI試験、README。formatter API、formatter実装、CSS、依存、CI、サービス、入力元、抽出、全体リファクタを変更しない。本工程は本書だけを作成し、commitは親が担当する。

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable |
| Component library | none — 既存semantic HTMLと内包CSSを無変更で使用 |
| Icon library | none |
| Font | system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |
| Theme | light固定、`color-scheme: light`、切替なし |
| Output | UTF-8の自己完結静的HTML1枚。doctype、lang=ja、charset、viewportを保持 |
| Interaction | なし。ボタン、フォーム、リンク、フィルタ入力、再試行UIを追加しない |

shadcn初期化・registry導入は非該当。Tool: noneのためテンプレートのComponent Inventoryは省略する。外部ライブラリの列挙・導入・フォント取得はしない。

### Existing Document and Layout — No Changes

現物根拠: `wordfreq/formatters.py:22–127`。以下は既存値の記録であり変更指示ではない。

- 順序: main → h1 → metadata（ファイル名、総出現回数）→ table（caption、thead、tbody）→ pairsが空の場合のみempty-message。basenameとtotalはそれぞれラベルとは別のblock text nodeで表より上に置く。
- 順位・単語・回数の3列と `th scope="col"` を維持。選択後top後の共通pairsに対し1始まり・欠番なしの表示順位を付ける。元順位・同順位表記は追加しない。
- body margin 0。main width 100%、max-width 960px、border-box、左右auto margin、padding 32px。480px以下のみpadding 16px。通常幅1280pxと狭幅320pxを検証する。
- table width 100%、table-layout fixed、border-collapse collapse。順位列56px、回数列64px、単語列は残り。全セルpadding 8px、vertical-align top。順位・回数は右寄せ、tabular-nums。単語は左寄せ。固定高さなし。
- basename/単語は `white-space: break-spaces; overflow-wrap: anywhere; word-break: normal; tab-size: 4`。空白/LF/TAB/CRを削除・圧縮しない。h1、セル、空文言の既存折返し規則を保持する。
- 自然な縦スクロールで全文可読。横スクロール依存、ellipsis、nowrap、行数制限、overflow hidden/clip、文字縮小、新min-width、カード、影、角丸、装飾、アニメーションを追加しない。
- 上下限とtopによる行数・文書高さ・表示行内容の変化だけを許容する。新しい閾値ラベル、除外件数、chip、空理由分岐、生成日時を追加しない。

---

## Spacing Scale

現物根拠: `wordfreq/formatters.py:56–102`、Phase 4継承。既存4px単位を保持する。

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | metadataラベル下 |
| sm | 8px | セルpadding、metadata-item間、caption下 |
| md | 16px | 狭幅main padding、h1下 |
| lg | 24px | metadata下、空文言上 |
| xl | 32px | 通常main padding |
| 2xl | 48px | 継承予約値、現物未使用・新適用禁止 |
| 3xl | 64px | 継承予約値、現物未使用・新適用禁止 |

Exceptions: marginリセット0、罫線1pxはspacing tokenではない。56px/64px列幅と960px max-widthは既存幾何寸法。新例外なし。

---

## Typography

現物根拠: `wordfreq/formatters.py:47–77`。サイズ3種・weight2種を維持する。

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Body | 16px | 400 | 1.5 |
| Label | 14px | 600 | 1.5 |
| Heading | 24px | 600 | 1.25 |

Bodyはbasename/総数値/データセル/空文言、Labelはmetadataラベル/caption/th、Headingはh1。Display役割・別数値フォント・外部フォントを追加しない。狭幅でもサイズ変更なし。

---

## Color

現物根拠: `wordfreq/formatters.py:46–101`。60/30/10は既存役割の分類であり、画素面積を比率へ合わせる再配置・再着色はしない。

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | #FFFFFF | ページ、metadata、表本文 |
| Secondary (30%) | #F1F5F9 | th背景のみ |
| Accent (10%) | #1D4ED8 | h1と総出現回数の数値のみ |
| Primary text | #0F172A | basename、単語、順位、回数、本文、列見出し |
| Secondary text | #475569 | metadataラベル、caption、空文言 |
| Divider | #CBD5E1 | th/tdの1px下境界線 |
| Destructive | not applicable | 破壊的操作・HTMLエラー画面なし |

Accent reserved for: h1「単語の出現頻度」と総出現回数の数値のみ。閾値境界・除外・順位を色で強調しない。light以外のテーマなし。

---

## Copywriting Contract

現物根拠: `wordfreq/formatters.py:34–44,107–124`。既存HTML文言は一字も変えない。

| Element | Copy |
|---------|------|
| Primary CTA | not applicable — 対話操作なし |
| Document title / h1 | 単語の出現頻度 |
| Filename label | ファイル名 |
| Filename value | 実行環境のパス規則によるbasenameだけ。全文・空白を保持し、title/属性を含む全HTMLにdirectory情報を埋め込まない |
| Total label | 総出現回数 |
| Total value | 正規化後の元Counterの回数和。min-count・max-count・topより前の10進整数。種類数・表示行数・表示回数の和ではない |
| Table caption | 集計結果 |
| Column headers | 順位 / 単語 / 回数 |
| Empty state heading | 新見出しなし。既存captionと3列見出しを保持 |
| Empty state body | 集計対象の単語はありません。単語を含む UTF-8 ファイルで再実行してください。 |
| Error state | HTMLを出さない。使い方はstderr/exit2、入力取得・decode失敗はstderr/exit1、stdout空。既存argparse/int診断方式を保持しTracebackを出さない |
| Destructive confirmation | not applicable — 書込み・削除操作なし |
| Loading / partial results | not applicable — 完成文書のみ。spinner/skeleton/部分取得UIなし |
| CLI help addition | `--max-count MAX_COUNT`。ファイルなしのhelpはexit0、stderr空 |
| README-only recovery | 上限による全除外はmaxを上げるか省略する案内。HTML空文言へ追記・置換しない |

READMEには承認済み例を1つだけ追加する。コマンドは `python -m wordfreq input.txt --min-count 2 --max-count 3 --format json`、入力は `beta beta beta alpha gamma alpha delta`、期待stdoutは `[{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]` と末尾改行1つ、exit0・stderr空。整数全域、上限省略、両端包含、min併用、逆転等の正常空結果、max前の元総数を直接関連説明として記す。正常stdoutへ説明ログを混ぜない。

### CLI Interaction and Data Contract

- `--max-count N` はtype=int相当、default=None。0、負整数、+2、02、大整数、`--max-count=-1`を受理する。max正値制約・min/max関係エラーを追加しない。min既定1とtop既定10の既存正整数制約は維持する。
- 抽出 → casefold → 元Counter → 元total保持 → `count >= min_count AND (max_count is None OR count <= max_count)` の共通選択 → 回数降順・同数時正規化後初出順 → top → 共通pairsを全formatterへ渡す。選択は両端包含、指定順独立、topとは独立。元Counterを破壊せず、語昇順へ戻さない。top入力spy・Counter不変・shared pairsで順序も検証する。
- max欠落/abc/1.5と既存不正min/topは入力取得前exit2・stdout空・stderr通知。max0/負数/min>maxでも入力取得を省略せず、有効引数で不存在/ディレクトリ/読込拒否/不正UTF-8ならexit1。
- 正常に読めたmax0/負数/min>max/全除外/空/抽出0語はexit0・stderr空。textは空、jsonは `[]` + LF1つ、HTMLは既存メタ情報・3列見出し・0データ行・固定空文言。語あり全除外の元totalは正値、空/抽出0語は0。
- 未指定・十分大きいmax・明示min1を変更前に固定された期待バイト列/exit/stderrへ照合する。変更後の2呼出し同士だけの比較では不可。既存期待値を新コードで作り直さない。UTF-8、escape(quote=True)とCR保護、basename、公開formatter API、text/json構造、既定top10を維持する。

---

## UI Considerations

独立gsd-ui-checkerは全7観点PASS（sa-0-4a6d9cf9、2026-11-25）。その後、公式ui-consideration-probe.cjsを `.planning/argonauts/r-d4bcda40-ui-elements.json` で実行し、原出力を同ディレクトリの `r-d4bcda40-ui-probe.json` に保存。適用14件、unclassified0件。--autoとして各要素の実体を再確認し、E3のlist-collectionとstatic-contentの両kindを明示した。14件のprobe問いすべてを下表の具体的な承認契約でexplicit解決（E1/E2/E4各2件、E3は8件）。原JSONのunresolvedは未解決の設計判断ではなく解決前のprobe原本であり、次表が書戻した解決結果。製品試験・画像閲覧は後工程であり未実施。

要素定義: E1=h1（static-content）、E2=basename/元total metadata（static-content）、E3=結果表（list-collection + static-content）、E4=空文言（static-content）。`--auto`ではこの実体に基づいてkindを確認し、操作部品のkindを追加しない。COPYは上表参照。

Applicable state considerations resolved: 設計上は以下すべてexplicit、backstopなし、未決なし。製品検証は後工程。

| Category | Element(s) | Status | Resolution / Reason |
|----------|------------|--------|---------------------|
| empty | E3 | ✅ covered | 空/抽出0語/上下限全除外は既存0データ行とCopywriting Contractの空表示。元totalは空で0、語あり全除外で元の正値 |
| loading | E3 | ✅ covered | 完成済み静的HTMLだけを生成し、ロード中・部分取得UIを設けない |
| error | E3 | ✅ covered | Copywriting Contractのstderr/exit1・2とstdout空。max0/負数でも入力失敗を隠さない |
| populated | E3 | ✅ covered | min/max選択後top後の共通pairsを既存3列・1始まり連番で表示し、元totalを保持 |
| partial | E3 | ✅ covered | 行の選択は完成データの意図した表示制限。不完全データや追加入力・補足UIではない |
| overflow | E1, E2, E3, E4 | ✅ covered | 両幅で既存折返し・全文保持。横はみ出し、clip、隣接列/行/metadataの重複なし。自然な縦スクロールは許容 |
| zero-one-many | E3 | ✅ covered | 0/1/複数行で同じ3列見出し・metadata・copyを保持。表示順位は常に欠番なし |
| long-text | E1, E2, E3, E4 | ✅ covered | 長basename/長語/複数桁数値/固定空文言を既存サイズで全文表示。連続空白/LF/TAB/CRを保持し省略・縮小しない |

---

## Baseline and Independent Browser Acceptance

後工程への義務。ここでは製品変更・baseline採取・pytest・ブラウザ実行・画像閲覧・通信観測を実施しておらず、合格扱いしない。

### Fixed Expected States

次表は仕様由来の期待値であり実測ではない。全3形式の対応とHTMLの元総数を試験へ固定する。

| Input / state | Options | Expected rows / HTML total |
|---------------|---------|----------------------------|
| `beta beta beta alpha gamma alpha delta` | max2 / max1 | alpha2,gamma1,delta1 / gamma1,delta1。ともに元7 |
| 同上 | min2/max2 / min2/max3、指定順交換 | alpha2 / beta3,alpha2。ともに元7、指定順不変 |
| 同上 | max2/top1 | alpha2だけ、順位1 / 元7 |
| 同上 | max0 / max-1 / min3/max2 | 0データ行と既存空文言 / 元7 |
| beta4,zoo3,apple2,pear2,single1 | min2/max3/top1 | zoo3だけ、順位1 / 元12 |
| `Zoo apple APPLE zoo banana` | min2/max2/top1 / top2 | zoo2 / zoo2,apple2、元5。初出順維持 |
| `Straße STRASSE 日本語 日本語` | max1 / min2/max2 | 空 / strasse2,日本語2。ともに元4 |
| 空・空白のみ・記号のみ | 有効max | 0データ行と既存空文言 / 元0 |
| 上下限選択後11種類以上残る入力 | top省略 / 十分大きいtop | 10行 / 残った全種類。元total不変 |
| 同数・10種類超を含む既存固定入力 | max未指定 / 十分大きいmax / 明示min1 | 変更前固定bytes/exit/stderrと一致。既定text/top10・画像・安全性を保持 |
| 既存の長語/長basename/空白・制御文字/注入候補 | 既存条件と上下限条件 | 既存全文・escape・折返し・元totalを維持。期待pairsは入力から独立固定 |

### Evidence and Ownership

- Builderは最初の製品変更前に省略互換の保存済み期待出力を確認し、不足分は変更前に入力/argv/環境/bytes/exit/stderrとともに固定する。旧Phase 4のbaseline headや受入を今回の変更前headへ付け替えない。
- 品質自身が対象headから実CLIを独立実行し、上限省略互換・包含・min併用・top・全除外・元総数を確認する。Builder生成HTMLや旧phaseの合格だけでは代用しない。
- HTMLは1280×900と320×900 CSS px、DPR1、zoom100%、fresh contextで確認する。browser版/executable/OS/実フォント/描画条件を記録し、同条件の変更前表示と比較する。新依存・新サービス・CI変更を導入しない。
- 全full-page/必要な全域tile画像を実際に閲覧する。縮小画像だけで全文可読とせず実寸以上または全域panを使う。DOM一致、画像存在、scrollWidth単独でPASSにしない。
- basename/語/順位/回数/総数の文字Range原本、空白/制御文字位置、祖先box/computed overflow、列/行/metadata非重複を保存する。rawのclamp/丸め/都合のよい除外は禁止。横収まり・clipなし・全文可読を判定し、自身の要素矩形への厳格な縦包含は必須にしない。
- pageを開く前から閲覧終了まで要求/失敗要求/navigation/popupとframe/initiator/url/outcomeを観測する。初回file読込みと外部通信を区別する。文書起因の外部試行は失敗・遮断でも不合格、帰属不明は未検証。script/イベント属性/CSS url/@import/meta refresh/外部resource/埋込みを追加しない。
- 品質は現headのソースを読み、元Counter/元total→min/max共通選択→top→同一pairsの各formatterという順序を記録する。出力一致だけで内部順序を証明しない。
- 各受入条件とREQ-23〜28にhead/入力原本/正確なargv/cwd/環境/exit/stdout/stderr/期待値/HTML原本/実測/全画像/閲覧結果/通信/ソース箇所を対応付ける。VERIFICATION.mdとCLI/CI文字証拠を保存・標準添付し、画像閲覧枚数・内容・結果を明記する。PMに画像・圧縮ファイルの閲覧を求めない。
- 追加試験の狙ったRED→最小実装GREEN、追加と全既存pytestの実件数/環境/コマンド/exit、README例の実CLI結果を記録する。既存試験削除・回避、未実施・未閲覧・未報告CIを成功扱いしない。OpenSpec task 2.2の独立品質はフェーズ検証へ明示引継ぎする。
- `docs/wordfreq-min-count-verification.md` は汎用のraw/画像/通信の方法だけ参照する。旧scope/head/件数/CLI/台帳/短い一時pathの人の例外は今回へ流用しない。
- PLANの検証はBuilder・品質が実在する試験/検証ファイルから標準実行する。新しい検証ファイルが必要なら同taskまたは先行taskで作成を明記する。計画中に未作成コマンドを試さず、インライン実行・ヒアドキュメント・無検査no-opを使わない。

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable — shadcn・第三者registry・外部packageを導入しない |

検証を通すためにも製品CSS/DOM/文言を変更しない。依存・CI・サービス・対話操作・新スタイルの追加なし。

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS
- [ ] Dimension 2 Visuals: PASS
- [ ] Dimension 3 Color: PASS
- [ ] Dimension 4 Typography: PASS
- [ ] Dimension 5 Spacing: PASS
- [ ] Dimension 6 Registry Safety: PASS
- [ ] Dimension 7 Inventory Provenance: PASS

**Approval:** pending — researcher作成のdraft。親工程の独立gsd-ui-checkerと承認後の公式UI-consideration probeを待つ。製品・ブラウザ受入の完了を意味しない。
