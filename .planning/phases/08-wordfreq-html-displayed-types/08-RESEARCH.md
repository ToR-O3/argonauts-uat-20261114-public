# Phase 08: wordfreq HTML displayed types — Research

**Researched:** 2026-11-26（セッション日付）
**Domain:** Python標準ライブラリ製CLIの静的HTML、固定出力回帰、独立ブラウザ証拠
**Confidence:** LOW（公式confidence seamの未分類local providerに対する保守値。下記のソース読取りによる確認と、実行未確認を区別する）

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- D-01: HTML table metadata shows `表示 N 種類` next to existing total occurrences. N is len(final pairs), after existing Unicode extraction/casefold, min/max filtering and top. Empty/no-token/all-excluded => 0; original total occurrences remains sum(original counts).
- D-02: Preserve text/json bytes, formatter API, basename-only path handling, initial-occurrence ties, escapes, no scripts/external resources/network, current light palette and table. No dependency, CI, permissions, external sending, migrations or unrelated refactoring.
- D-03: Approved HTML compatibility exception is only displayed-N addition and minimum layout adjustment. Old Phase4 D-06/D-07 and Phase7 D-04/REQ-26 are historic snapshots; do not overwrite those CONTEXT files, sealed baselines, or their past evidence. For current assertions use separate expected output or explicit narrowly-scoped transformation; never blanket ignore HTML. Text/json and security checks stay strict. Past snapshot-only scope gates are not current product acceptance gates.
- D-04: Ingest BLOCKERS 2 in .planning/INGEST-CONFLICTS.md are approved changes, not unresolved product decisions. E.7/F.3 therefore selects official phase.add new Phase8, not merge overwrite or reopening completed phases. Attach conflict report for PM review. Historical stale verification remains separate.
- D-05: Test first RED then production minimum GREEN, expand edge regression, run all pytest. Include ordinary, explicit/large/default top (12 candidates => 10), min/max intersections, empty/no-token/all-excluded, Unicode aggregation and exact text/json regressions. README HTML description gains exactly one relevant line, existing unrelated content retained.
- D-06: Independently quality-run CLI, full pytest and real browser at 1280×900 and 320×900 DPR1, verify adjacent count above table, long words/basename readable without overlap/clipping/overflow, escape and no network attempts. The old request's image exemption does not apply. Quality records actual image count/content/results in plain VERIFICATION.md and CLI/CI evidence, attaches plain originals for PM read_file; PM need not open images or archives. Unperformed/pending checks must not be claimed passed.

### Claude's Discretion
Use existing metadata typography, separators and spacing; only minimum local layout change if actual render requires it. Test helper naming and separate current expected fixtures follow repository conventions.

### Specifics
Preserve original totals for beta4/zoo3/apple2/pear2/single1 => 12; min2/max3/top1 displays one type. Single logical metadata row with total and count at both widths; long basename may wrap separately without hiding text. OpenSpec tasks1.1 tests,1.2 implementation/README,2.1 independent acceptance need explicit PLAN mapping. Plans execute serially on the same request branch.

### Deferred Ideas (OUT OF SCOPE)
No future features. No global repair of prior phase metrics or snapshot gates.
</user_constraints>

## Summary

**推奨:** `format_html(pairs, basename, total)` の最終 `pairs` だけから `len(pairs)` を求め、既存totalの独立leafを保持した局所行に文言を追加する。選択・引数・入力取得は変更しない。公開署名は `def format_html(pairs: list[tuple[str, int]], basename: str, total: int) -> str:`、現行のmetadataは `<div class="total-value">`。これを維持すれば既存のmetadata抽出への影響を小さくできる。[VERIFIED: wordfreq/formatters.py:22-38,108-118]

製品変更より回帰整合と独立検証の計画が重要。既存の全pytestには「現在のCLIを封印前HTML bytesと直接比較する試験」と「古い証拠の完全性を検査する試験」が混在する。前者のみ承認差分を明示した今回期待値へ接続し、後者の原本・旧scopeは保持する。今回ブラウザdriverはまだ存在が確認できず、Phase7 driverの `review-session` はブラウザを起動しない。これを品質受入コマンドとして転用してはいけない。[VERIFIED: tests/test_cli.py:796-817,1017-1029; tests/test_max_count_verifier.py:167-178,272-296; tools/verify_wordfreq_max_count.py:549-553]

**調査境界:** 製品変更・pytest試験実行・ブラウザ起動・Kanban・commit/pushは行っていない。公式 `query init.phase-op 8` はphase_found=true、phase_number="08"、plan_count=0を返した。graphifyはdisabled。`.planning/STATE.md` の旧集計を今回状態判定に代用しない。[VERIFIED: official GSD CLI output in this session; .planning/STATE.md:1-17,91-95]

## Architectural Responsibility Map

| Capability | Primary tier | Secondary tier | 計画上の責任 |
|---|---|---|---|
| 抽出・casefold・閾値・top | CLI処理 | — | 既存経路を保持 |
| 表示N・total・静的escape | Python整形 | — | 最終pairsから純粋整形 |
| 横配置・折返し・可読性 | Browser/static CSS | Python生成HTML | DOM順でなく実描画で確認 |
| 固定bytes・封印原本 | pytest/検証補助 | — | currentとlegacyの期待値を区別 |
| 独立CLI・画像閲覧・証拠配送 | 品質工程 | PM受入 | Builder自己採取を独立合格にしない |

根拠: `counts = count_words(iter_tokens(text))` → `total = sum(counts.values())` →包含ANDの別Counter→ `pairs = top_words(selected_counts, args.top)` → `output = format_html(pairs, basename, total)`。この順序と全形式の共有pairsは既に実装されている。[VERIFIED: wordfreq/__main__.py:35-50]

<phase_requirements>
## Phase Requirements

| ID | 要求（REQUIREMENTS.mdの要約） | Research Support |
|---|---|---|
| REQ-29 | 最終行数の「表示 N 種類」を総数横へ。通常/top/閾値/空/Unicode、元総数維持 | formatterのlenとliteral matrix、共通パイプラインを変更しない |
| REQ-30 | text/json全バイト不変、HTML限定差分、封印保全、安全性、両幅可読 | 下記旧比較接点・strict allow-list・current browser計測の不足を計画化 |
| REQ-31 | 先行RED/GREEN・全pytest・README1行、品質独立実行、文字証拠添付 | serial task mappingとValidation Architecture、PM配送gate |

出典: `.planning/REQUIREMENTS.md:110-112` の `REQ-29` / `REQ-30` / `REQ-31`。表示例・手順は承認済みPRDとUI-SPECを優先し、古い免除を継承しない。[VERIFIED: .planning/REQUIREMENTS.md:106-118; .planning/phases/08-wordfreq-html-displayed-types/08-UI-SPEC.md:130-138]
</phase_requirements>

## Standard Stack

| Component | 確認済みversion/契約 | 使用方針 |
|---|---|---|
| 製品 | `version = "0.1.0"`, `dependencies = []` | 標準ライブラリのみ、install不要 |
| 開発依存 | `dev = ["pytest"]` | 新依存を足さない |
| 既存CI | `python-version: "3.12"`, `python -m pytest` | workflowを変更しない |
| ローカル検証interpreter | `/usr/bin/python3 --version` → Python 3.12.15 | 既設3.12を明示 |
| ローカルpytest | 下記prefix + `-m pytest --version` → pytest 9.0.3 | bare pytestを使わない |
| ローカルbrowser | `/usr/bin/chromium-browser --version` → Chromium 156.0.8078.73 | version取得のみ、起動可否は未確認 |

[VERIFIED: pyproject.toml:5-16; .github/workflows/pytest.yml:9-18; terminal version outputs in this session]

共通検証prefixは `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3`。bare `pytest --version` は `ModuleNotFoundError: No module named 'pytest'` で失敗したが、このprefixでは9.0.3が取得できた。環境不備を製品REDと記録しない。Playwright/websocketsのimport・起動・画像閲覧能力は未確認。古い短い `/tmp/aw-*` 許可は旧依頼限定であり、今回のTMPDIR制約を解除しない。[VERIFIED: terminal outputs; docs/wordfreq-min-count-verification.md:39-43]

追加外部packageなし。registry調査・package legitimacy auditは適用外。最新packageへの更新を目的にしない。

## Architecture Patterns

```text
UTF-8 file → Unicode extraction/casefold → original Counter → original total
                                                  ↓
                                        min/max inclusive AND
                                                  ↓
                                      stable frequency order → top
                                                  ↓
                                             final pairs
                          ┌───────────────────────┼───────────────────┐
                      text bytes              JSON bytes      HTML(total + len(pairs))
                                                                  ↓
                                                  local browser at both widths
```

既存実装は `if count >= args.min_count and (args.max_count is None or count <= args.max_count)`。`--top`の既定は `default=10`、`--min-count`は `default=1`、`--max-count`は `default=None`。ここへ新処理を入れない。[VERIFIED: wordfreq/__main__.py:13-19,35-50]

### 最小DOM/CSS設計

- total leafは `div.total-value` のまま、独立した表示件数leafと共通の局所wrapperを置くことを推奨する（新class名は未決の実装裁量）。既存のHTML parserはdivを許容する一方spanは許可集合にない。span採用は不要なallow-list拡大になる。[VERIFIED: tests/test_formatters.py:94-109; tools/verify_wordfreq_html.py:67-89]
- 新wrapperだけ局所flex/inline行、8px gap。totalのaccent、新文言のbody色・16px/400/1.5を保持する。受入両幅で同じ行にし、basenameは別区画で折返す。固定高・clip・ellipsis・縮小を導入しない。[VERIFIED: .planning/phases/08-wordfreq-html-displayed-types/08-UI-SPEC.md:44-59,63-87]
- 新wrapperの親へtotalと新文言を混ぜ、`.total-value`自身のtextを `7 表示 3 種類` に変えない。独立totalの厳密期待値を維持するためである。[VERIFIED: tests/test_cli.py:425-441; tests/test_formatters.py:148-150]

## Regression Contact Map — 必ずPLANで扱う接点

| 実在する接点 | 新表示の影響 / 必要な対処 |
|---|---|
| `tests/test_formatters.py:94-133` | class allow-listへ実装した局所classだけ明示追加。タグ/属性/URL禁止は維持 |
| 同:218-262 | CSS辞書の完全一致。局所新規ruleのみ追加し、既存宣言・禁止patternを維持 |
| `tests/test_cli.py:201-239,425-441` | `CLIHTML`はfilename/totalのみ収集。新表示の別抽出・構造検査を追加し、既存values期待値を不必要に拡張しない |
| 同:796-817 | `test_min_count_saved_default_bytes` は封印HTMLと現CLIを直接比較。HTMLだけ今回期待値へ明示変換、text/jsonは元bytesのまま |
| 同:1017-1029 | `test_max_count_saved_bytes` も同様。省略/大上限/明示min1すべてを維持 |
| `tests/test_max_count_verifier.py:98-110` | `collected_capture`は現CLIを呼ぶ。`validate_scope`のmockはscopeだけであり、旧HTML bytes比較は残る |
| `tools/verify_wordfreq_max_count.py:354-408,411-460` | 現CLI fixture採取は旧oracleとbytes比較するため影響。新期待値への限定接続が必要。保存済みcaptureのvalidationと混同しない |
| `tests/test_max_count_verifier.py:167-178,272-296` | 保存済みcapture/baseline/REDのintegrityを保持。過去原本を新headへ付替えない |
| `tools/verify_wordfreq_max_count.py:463-494` | 旧scopeはformatter変更を許さずREADME hashも固定。今回受入gateとして実行しない。cold fixtureの旧scope判別力は残す |
| `tools/verify_wordfreq_min_count.py:560-575` | 旧comparisonsはbytes/raw/images完全一致。今回は表示追加のためこの旧受入コマンドの無改変転用不可 |

[VERIFIED: 上表の各ソース行。新実装に対する失敗はコード読取りによる予測であり未実行]

### 固定期待値の推奨

1. HTMLの旧固定bytesを入力とし、旧total断片と局所CSSの**完全一致かつ出現1回**を要求する明示的変換をテスト側に用意する。差替え後の全文bytesで比較し、行/順序/escape/残りCSSを一切無視しない。Nは独立literal期待pairsの長さを使用し、製品formatterを期待値生成に呼ばない。
2. 変換対象が見つからなければfail closed。HTML全削除、空白一括正規化、metadata全無視、regexの広いDOTALL除去をしない。別のcurrent固定fixtureを置く選択でもよいが、旧原本との許可差分を明示する。
3. current CLIを生成する旧max-verifier fixtureにも同じ限定比較接続が必要。必要なら**現行CLI比較だけ**の明示的adapter接点を補助コードへ追加し、legacy既定validator/封印照合は変更しない。これが補助ファイルへ波及する場合はPLANのfiles_modifiedと理由に明記する。旧scope allow-list/hashを現在に書き換える解法は採用しない。
4. 全pytestをgreenにするため `-k not legacy` / skip / xfail を最終commandへ足さない。先行REDは新表示assertionを対象に採り、compatibility調整を理由に新機能REDを飛ばさない。

根拠: 承認された例外は「今回用期待値または許可差分を明示した変換」であり、封印変更・HTML blanket ignoreを許可していない。[VERIFIED: .planning/phases/08-wordfreq-html-displayed-types/08-CONTEXT.md:15-20; openspec/changes/r-6ae2cbf2-html-displayed-types/design.md:15-24]

## Sealed Evidence Inventory

- Phase4 indexは `"verdict": "baseline-sealed"`、`"head": "789cc17267fb4cfeea24111797c3d934c542ce6a"`。jqでcases長12を確認。生成箇所は旧driverの `source = folder / "private-source-directory" / case["basename"]` / `stdout, stderr = folder / "stdout.bin", folder / "stderr.bin"` / `html = folder / "stdout.html"`。絶対rootを履歴として保持し、相対参照だけで現在worktreeへ解決する。[VERIFIED: .planning/argonauts/r-e476c11d/baseline/index.json:2-16; tools/verify_wordfreq_min_count.py:84-113; jq output]
- Phase7の定義は `BASELINE = Path('.planning/argonauts/r-d4bcda40/baseline')`、保存は `save_json(output/'provenance.json', provenance)`、`seal(output, index)`。index先頭をreadし、jqで `cli_cases:39, views:0, images:0` を確認した。旧画像なしは今回の免除ではない。[VERIFIED: tools/verify_wordfreq_max_count.py:21-23,158-203; .planning/argonauts/r-d4bcda40/baseline/index.json:1-11; jq output]
- 今回はindex参照・定義・主要接点の存在を読んだだけで、全artifact checksumの完全性は実行未確認。Builder/品質の保存済みintegrity試験で確認する。原本を再採取しない。

## Code Examples / Literal Oracles

既存の部品呼出しは `format_html(pairs, basename, total)`、件数計算の承認式は `len(pairs)`。新署名・新集計部品は不要。[VERIFIED: openspec/changes/r-6ae2cbf2-html-displayed-types/design.md:15]

| 入力 / 条件 | 独立期待pairs | total / N |
|---|---|---|
| `beta beta beta alpha gamma alpha delta`, max2 | alpha2, gamma1, delta1 | 7 / 3 |
| 同 max2/top1 | alpha2 | 7 / 1 |
| 同 max2/top99 | alpha2, gamma1, delta1 | 7 / 3 |
| beta4/zoo3/apple2/pear2/single1, min2/max3/top1 | zoo3 | 12 / 1 |
| 同条件の両端: 通常入力min2/max2 | alpha2 | 7 / 1 |
| 選択後12候補、top省略 / top99 | 初出順の先頭10 / 全12 | 元total維持 / 10・12 |
| 空 / 空白 / 記号のみ | 空 | 0 / 0 |
| 通常入力max0 / max-1 / min3,max2 / min4 | 空 | 7 / 0 |
| `Straße STRASSE`, min2/max2 | strasse2 | 2 / 1 |

[VERIFIED: .planning/argonauts/r-6ae2cbf2-prd.md:34-66,87-120,136-142; tests/test_cli.py:860-875; .planning/phases/08-wordfreq-html-displayed-types/08-UI-SPEC.md:121-124]

N=top、N=sum(display counts)、N=original種類数という誤実装をそれぞれ落とすケースを置く。formatter単体は未ソートpairsをそのまま出す性質、引数不変、空で見出しのみ、hostile値・CRの一度escapeを維持する。[VERIFIED: tests/test_formatters.py:136-214]

README追加文は承認どおり `HTMLでは総出現回数の横に「表示 N 種類」を示し、Nは絞込み・top適用後の表示語種類数で、空結果は0です。`。既存HTML説明付近へ1行追加し、既存末尾 `検証B: v1.12 の通しの確かめ（2026-11-22）` と既存JSON例を保持する。[VERIFIED: .planning/phases/08-wordfreq-html-displayed-types/08-UI-SPEC.md:107-111; README.md:19-28,31-58; tests/test_cli.py:1171-1198]

## Independent Browser Verification Architecture

既存collectorの再利用可能な下層は `collect_view(browser, case, width, output, live=None)`。新contextはheight900/DPR1、実CLI stdoutのfile URLを開き、raw・実fonts・full/tile・networkを保存する。`live`指定時は観測contextを閉じず残す。旧高層scope/request/AC/finalizeを無変更で今回へ流用しない。[VERIFIED: tools/verify_wordfreq_html.py:586-671]

**不足:** geometry JSのtarget selectorは `main,h1,.metadata,.metadata-item,.label,.filename-value,.total-value,table,caption,thead,tbody,tr,th,td,.empty-message`。新件数leafがこの集合外なら文字単位Rangeが取得されない。`dom_errors`も現状basename/total/rows/headersだけでNや横配置を検証しない。新表示専用の測定・期待値・隣接位置assertionを加える必要がある。共有JSを拡張する場合、過去rawの検査を新必須fieldで壊さず、current collectorだけ新要素を必須化する。[VERIFIED: tools/wordfreq_html_geometry.js:28-67; tools/verify_wordfreq_html.py:556-583]

PLANに以下の独立gateを明示する（ここでは実施しない）:

1. 品質の実profile・対象head・clean execution surfaceを確認し、新規rootへ自身の入力からCLIを生成する。Builderの生成HTMLを独立実行の代わりにしない。
2. 通常 / max2-top1 / 既定10 / 空・全除外 / 長basename・長語 / escape候補を **1280×900と320×900 DPR1** で描画。totalと新Nが共通区画、total左・新N右、同じ表示行かつ表より上であることをrawと画像で確認する。縦scrollは許可、横overflow/clip/重複は不可。
3. 新表示・全既存textのRangeを未補正で保存。全祖先clip、隣接text非重複、実fontとCSSを確認。自身elementの厳格な縦包含だけで不合格にしない。fullとtileの描画条件を揃える。全full/全tileおよび比較対象画像を実閲覧し、実数・内容・結果を台帳へ残す。
4. 同条件の変更前原本を別rootへ保全し、表示追加とその局所レイアウト以外の変更がないことを比較する。過去封印を上書きしない。Phase7は画像0なので「そこに比較画像がある」と仮定しない。必要な今回変更前画像は製品編集前の別採取taskとして配置する。
5. open前から最終flushまでrequest/failed/navigation/popup等の試行を観測し、成功response0を無通信と同一視しない。観測の判別力canaryも別の検証生成物として扱う。製品にscript/外部resourceを追加しない。
6. 品質本人が全pytest・現ソースのfilter→top→shared pairsを確認。head更新後はfresh evidenceを取り、前head結果を付替えない。画像閲覧不能/ブラウザ起動不能はblock/gapであり、旧Phase7の免除を採用しない。

根拠: [VERIFIED: .planning/phases/08-wordfreq-html-displayed-types/08-UI-SPEC.md:130-138; docs/wordfreq-html-verification.md:54-60,105-125; .planning/argonauts/r-6ae2cbf2-learnings.md:31-47,66-71]

## Validation Architecture

### Test Framework

| Property | Value |
|---|---|
| Framework | 既設pytest 9.0.3 / CPython3.12.15（version取得のみ） |
| Config | `pyproject.toml`にpytest設定節なし。既存testsを直接指定 |
| Quick run | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_formatters.py -q` |
| Focused integration | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_formatters.py tests/test_cli.py -q` |
| Full suite | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest -q` |

上記は存在を読んだファイルへの**後続実行用**command。調査では実行していない。Quickの30秒内完了も未測定で、Builderが実測する。Nyquistは `"nyquist_validation": true`。[VERIFIED: .planning/config.json:21-25; pyproject.toml:1-16; tests/test_formatters.py:1-262; tests/test_cli.py:1-19]

### Phase Requirements → Test Map

| Req ID | Behavior | Test type | 実在ファイルに対するcommand（共通prefixを前置） | File exists? |
|---|---|---|---|---|
| REQ-29 | N/total/最終行、0/1/3/10/12、閾値/Unicode | unit + CLI | `-m pytest tests/test_formatters.py tests/test_cli.py -q` | yes、N assertionはWave0追加 |
| REQ-30 | fixed text/json、HTML限定変換、escape/API | regression | `-m pytest tests/test_cli.py tests/test_formatters.py tests/test_max_count_verifier.py tests/test_min_count_verifier.py -q` | yes、current互換adapter不足 |
| REQ-30 | 両幅隣接/長語/無通信/全画像実閲覧 | real-browser + human inspection | 今回用公開CLIは未作成。既存旧CLIをそのまま採用しない | gap、まず検証ファイル作成・読取り |
| REQ-31 | README1行/先行RED/GREEN/全件/独立証拠 | regression + process | `-m pytest -q` とREADME diff原本、品質文字証拠 | suite実在、追加assertion/報告は未作成 |

### Sampling Rate

- 各task: formatter quick + 変更対象のfocused tests。新RED対象の正確selectorは試験追加後に実在を確認して確定する。0 collectedをRED/GREENとしない。
- 各wave: full pytest（除外・skip追加なし）。失敗を「legacyだから」と無言で落とさない。
- Phase gate: 品質独立full pytest + current CLI + 両幅全画像実閲覧 + 文字証拠配送。ローカルgreenをCI成功に置換しない。

### Wave 0 Gaps / Recommended Serial Task Boundaries

1. **比較原本・検証seam準備:** 製品編集前の今回用CLI/同条件ブラウザ比較原本を保全。封印integrity、旧current比較接点の限定adapter、今回用browser実行ファイル/手順/negative検査を準備する。旧driverのコピー全改修ではなく必要下層だけ再利用する。新ファイル名・CLI flagは未確定であり、この調査から架空commandをPLANへ転記しない。
2. **OpenSpec1.1:** 既存2試験ファイルへN・配置構造・literal row count・exact text/jsonを先に追加。未変更製品で新表示欠如のassertion REDを保存する。環境/collection errorはREDではない。新試験ファイル実在確認後にPLANの実行commandを固定する。
3. **OpenSpec1.2:** formatter局所GREEN、CSS/class期待値の局所整合、README承認文1行。focusedとfull pytestを実行し実件数・exit・環境・ログ/JUnitを残す。製品候補はformatterだけでCLI変更は不要。
4. **OpenSpec2.1:** 品質実profileから新headを独立CLI/全pytest/両幅browser/全画像実閲覧。VERIFICATION.mdとCLI/CI文字証拠、PM読取りまでのhandoffを別責任で完了する。

依存順は同一依頼branchで直列。Phase7のno-browser runbookや旧snapshot専用scopeをcurrent acceptanceへ持ち込まない。[VERIFIED: openspec/changes/r-6ae2cbf2-html-displayed-types/tasks.md:3-10; 08-CONTEXT.md:36-41; tools/verify_wordfreq_max_count.py:549-553]

## Evidence Delivery Contract

品質報告はREQ-29/30/31別に、検証head・実profile/task/run・cwd/interpreter/env・入力原本・正確argv・exit/stdout/stderr・literal期待値・HTML原本・browser/version/viewport/DPR・raw/network・画像pathと**実閲覧枚数/内容/判定**・RED/GREENと全suite実数を対応付ける。CIは同じheadの既存状態を有限回読み、未報告/pendingはそのまま記録し、待機loop・workflow編集をしない。[VERIFIED: .planning/REQUIREMENTS.md:110-112; .planning/phases/08-wordfreq-html-displayed-types/08-UI-SPEC.md:137; .planning/argonauts/r-6ae2cbf2-learnings.md:31-47]

`VERIFICATION.md` とCLI/CI文字証拠を標準添付し、受取側がread_fileで本文・原本を読めることを確認する。索引JSON・profileローカル絶対path・archiveだけでは配送完了でない。保存/添付成功/PM原本読取りを分ける。PMに画像や圧縮物の閲覧を求めないが、品質本人の全画像閲覧は省略しない。承認済み衝突報告もPMへ渡す。[VERIFIED: 08-CONTEXT.md:17-20; .planning/argonauts/r-6ae2cbf2-learnings.md:40-47,69-71]

## Don't Hand-Roll / Common Pitfalls

- **Nの再集計禁止:** formatterでtokenize/filter/topを作り直さない。最終pairsのlenを使う。
- **動的HTMLの独自escape禁止:** `_html_text`の `escape(value, quote=True).replace("\r", "&#13;")` を維持。class/CSS/URLへ入力を流さない。[VERIFIED: wordfreq/formatters.py:17-19,28-32,108-115]
- **構造=横配置ではない:** parser試験は位置の十分条件でない。実ブラウザを必須にする。
- **CSS全書換え禁止:** exact CSS試験の辞書から局所rule以外を削らない。white-space/break-spaces、長語/filename wrapping、明るいpalette、列幅を継承する。[VERIFIED: tests/test_formatters.py:218-262]
- **legacy成功の付替え禁止:** 完了済みscope/RED/画像免除はその依頼の履歴。今回の追加試験と独立合格の代替にしない。

## Security Domain

設定は `"security_enforcement": true`、`"security_asvs_level": 1`。[VERIFIED: .planning/config.json:49-51]

| ASVS area | Applies | Current control / planning consequence |
|---|---|---|
| V2 Authentication / V3 Sessions / V4 Access Control | 製品機能として対象外 | CLIから完成静的HTMLを出すだけ。認証/権限機構を追加しない |
| V5 Input Validation / output encoding | yes | 既存argparseと一度escape、独立text leaf、static allow-list、UTF-8・basename維持 |
| V6 Cryptography | 新暗号機能は対象外 | 証拠SHAは改変照合用であり可読性や独立合格の代替にしない |

脅威はbasename/語からのmarkup injection、入力pathの漏洩、CSS/URL/script経由の外部試行、証拠原本の置換。既存hostile/CR/encoding回帰とcurrent browser観測を維持する。これは適用領域の計画分類でありASVS認証の完了主張ではない。[VERIFIED: tests/test_formatters.py:136-195; tests/test_cli.py:357-415,490-500; tools/verify_wordfreq_html.py:67-89; 08-UI-SPEC.md:135-137]

## Open Questions / Environment Risks

製品判断の未決事項はない。以下は実行準備の未検証gapであり、利用者へ仕様を再質問する理由ではない。

- browser版は取得できるが、起動・Playwright/websockets・画像閲覧能力は未実証。Phase7では起動不能の履歴がある。今回免除なしなので品質が能力確認し、不能なら正直にblockする。
- 今回用browser公開CLI/検証ファイルとcurrent互換adapterは未作成。PLANは実在ファイルを根拠にcommandを確定する前提を守る必要がある。
- full suite所要時間/現在の成功件数/CI結論は未確認。調査で実行していないため見積値を成功証拠にしない。

## Sources / Metadata

一次資料は本セッションでread_fileした現行製品・tests・tools、承認CONTEXT/UI-SPEC/PRD/OpenSpec、封印indexの冒頭、既存CIである。数値抽出はjq、GSD判定は公式launcher後のgsd_runを使用した。外部API・package調査が必要になる変更ではないためWeb research-plan seamは使用していない。

公式 `query classify-confidence --provider filesystem --verified` は `confidence: LOW`（local/official/curatedも未分類LOW）を返した。ソース自体の直接確認をWeb文献のconfidenceへ偽装しないため全体ラベルはLOWとし、各事実にはreadした根拠を明示した。実行未確認は上記のとおり区別する。

**Assumptions Log:** 新DOM class名、新検証ファイル名/CLIは未定の提案であり実在識別子として主張していない。実装影響の失敗予測は読取りベースであり、pytest実行結果ではない。

**Validity:** formatter/tests/tools/承認契約が変更された時点で関連箇所を再読する。履歴STATE集計やstale検証のグローバル修復は対象外。
