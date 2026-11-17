# Phase 02: wordfreq HTML output — Research

**Researched:** 2026-11-17
**Domain:** stdlib Python CLI / static local HTML / existing Chromium CDP evidence
**Confidence:** HIGH for repository facts and browser launch/discovery; LOW for not-yet-exercised evidence harness. Product acceptance is NOT verified.

<user_constraints>
## User Constraints (from CONTEXT.md)

Source: [VERIFIED: 02-CONTEXT.md:17–35,53–55]. The following decisions, discretion and deferred scope are copied verbatim.

### Locked approved decisions

D-01: 全形式の同数順はcasefold後正規化語の初出順。頻度降順は維持しsort後top。旧REQ-04/D-2/phase1 D-10と語昇順の試験・CONCEPTSは今回の明示互換性変更で置換。text/json構造に順位やmetadataを追加しない。
D-02: HTMLは明るい背景、順位・単語・回数3列。scope=col。top後1始まり表示行連番。同数でも連番、top1は順位1の1行、空入力は総数0・3見出し・データ0行。Q-1〜4は回答済み、再質問しない。
D-03: 表前metadataはbasenameのみをリンクにせず文字表示。総数はtop前の全正規化トークン出現回数総和。Zoo apple zoo APPLE betaはtop1でも総数5・1/zoo/2。ディレクトリ非露出。
D-04: 純粋HTML formatterは選択済みpairs・basename・totalを受け取り、入力を読まず再sortしない。1回の集計から全形式へ配線。既存入力取得境界/Unicode抽出/casefold/exit0,1,2は維持。
D-05: doctype/UTF8 charset/viewport・inline CSSの単一文書、JS/外部asset不要。1回escapeし、& < > quotes/entity風文字/空白/LF/CR/CRLFの元文字列をDOMでも保持。HTML parserの改行正規化に対処する。入力読取り層のuniversal newlineは変更しない。
D-06: 320/375 mobile CSS viewportと1280 desktopで3列・200文字連続語・長い日本語名・空表を欠落/重なり/横overflowなく表示。悪意ある実ファイル名がtag/script/eventにならず外部request0を実ブラウザで確認。
D-07: 品質がCLI生成HTMLをローカルで独立再実行できる経路を計画に具体化。実HTML、画像、DOM/text/layout、network、ブラウザ名/版、viewport、対象head・生成条件を保存。手段不足は未検証として人へ返し、静的検査で代替合格しない。
D-08: 全pytest/CLI既存回帰・入力バイト不変・入力境界を維持。別ファイルへのUTF8保存、共有時の語/名前露出、同一パスredirectがCLI起動前に入力を消す注意を説明し、無害なデータで例を実行。
D-09: CI/依存追加変更、生成日時、テーマ切替、Webサーバ/アップロード/配信、対話sort/graphは範囲外。既存browser手段のみ。既存設定security/nyquist/plan_check/pattern_mapperを無効化しない。
D-10: 同じ依頼branchへ複数PLANを直列に積む。各PLAN3task以下。各task終了時に検証ファイルが存在し、その時点でテスト可能。先行PLANが必要ならdepends_onに明示し、phase検証は全成果を含むbranchで行う。独立PLANは他成果の有無に依存せず検証可能にする。誤動作は既存検証で失敗観測できるようfails_whenを記述する。
D-11: FR-1/3/HTML-4回帰は全形式で通常/空/記号のみ/Unicode、既定top10/正整数top/語種数超過、不正top0以下/非整数、不正format、ファイル個数0/2以上、不存在/読取不能/UTF8不正を含む。正常exit0/stderr空、環境exit1と使い方exit2はstderrエラー/stdout空。HTML正常stdoutにログ/別文書なし。既存textはcount TAB word LF、jsonはword/count配列（空[]）、空textは出力なし。casefold統合後初出・頻度優先・複数seedは各形式内のバイト一致を検証する。

### Claude's Discretion

CSS/余白/書体/配色の具体値は承認された02-UI-SPECに従う。関数名・試験構成・既存browser手段の選択はresearchで現環境に根拠付ける。範囲や既定値の変更は裁量外。

### Deferred Ideas (OUT OF SCOPE)

stdin/URL、形態素解析、サーバ/配信/upload、対話sort/graph、生成日時、テーマ切替、依存/CI変更は追加しない。archiveは最終化工程。
</user_constraints>

## Summary

[VERIFIED: wordfreq/aggregator.py:6–13; wordfreq/__main__.py:24–32; wordfreq/formatters.py:5–13] Existing aggregation already returns `Counter(tokens)` but selection uses `key=lambda wc: (-wc[1], wc[0])`. Replace only the secondary ordering contract, retain the Counter, select once, and feed pure formatters. Existing text `f"{count}\t{word}\n"` and JSON `json.dumps(items, ensure_ascii=True) + "\n"` must remain structurally unchanged. HTML adds basename and pre-top total only to its own formatter.

[VERIFIED: research terminal/browser discovery, 2026-11-17] A usable **existing browser bootstrap and WebSocket endpoint** were found without installing anything: Chromium `156.0.8078.73`, Node `v24.21.0`, local CDP discovery, live protocol method inventory, and an HTTP `101 WebSocket Protocol Handshake`. The first browser launch failed because the absolute profile scratch TMPDIR made Chromium's singleton socket path too long. Launching with **cwd=profile scratch and child TMPDIR=.** succeeded, without `--no-sandbox`. This is not a completed Node CDP client or file-HTML evidence run; the Builder must create and execute that file-backed harness, and quality must rerun it independently.

**Primary recommendation [RECOMMENDATION]:** Implement one vertical CLI HTML slice with the shared ordering change and relevant tests; then extend full regression/security coverage; then create an opt-in stdlib-only Node/CDP evidence harness. Same request branch, explicit serial dependencies, no more than three tasks per PLAN. Do not install Playwright or alter CI.

## Architectural Responsibility Map

[RECOMMENDATION, grounded in openspec/changes/r-5c041156-wordfreq-html/design.md:22–44]

| Capability | Primary tier | Secondary tier | Responsibility |
|---|---|---|---|
| UTF-8 input and environment errors | CLI/input boundary | filesystem | Read once through FileSource; preserve existing exits |
| Unicode extraction and normalization | domain/tokenizer | — | Existing Unicode word extraction followed by casefold |
| Frequency, first-seen ties, top | domain/aggregator | CLI composition | Preserve insertion order, stable frequency sort, then slice |
| Basename and full total | CLI composition | — | Derive before formatting, never expose directory |
| Safe semantic report | Python output formatter | static browser document | Serialize text once, inline fixed CSS, no acquisition/re-sort |
| Responsive rendering | browser layout | static HTML/CSS | Approved UI tokens and semantic three-column table |
| Evidence | development-only harness | local Chromium | file URL navigation, DOM/layout/screenshots/network, not product runtime |

## Project Constraints (from HERMES.md)

[VERIFIED: read_file HERMES.md and .hermes/HERMES.md returned not_found; project file discovery] No project HERMES file or project SKILL.md was found in the inspected worktree. Official `query agent-skills gsd-phase-researcher --skills-only` returned an empty block. There are no additional project directives to copy here.

[VERIFIED: .planning/config.json:21–50] Preserve `"nyquist_validation": true`, `"plan_check": true`, `"pattern_mapper": true`, `"security_enforcement": true`, and `"security_asvs_level": 1`. Config parallelization does not override the card's serial-PLAN decision. `commit_docs` is enabled in config, but this research assignment does not authorize commit/push/Kanban changes.

[VERIFIED: official query init.phase-op 2] Phase `"02"`, `"wordfreq HTML output"` exists; initial query returned `has_research:false`, `has_context:true`, `has_plans:false`, `plan_count:0`. Official `graphify status` returned `disabled:true`; no graph setting was changed. STATE's older Phase 1 completion text is history, not authority to skip Phase 2.

<phase_requirements>
## Phase Requirements

[VERIFIED: .planning/REQUIREMENTS.md:36–41] Current IDs and descriptions:

| ID | Description | Research support |
|---|---|---|
| REQ-09 | AC1 — `--format html` は単一の自己完結UTF-8 HTML文書をstdoutへ出す。既定text、text/json構造・終了値は維持し、HTMLのメタデータや順位を既存形式へ足さない。 | Pure formatter, explicit CLI branch, unchanged text/json APIs |
| REQ-10 | AC2 — 表前に入力basenameのみをリンクでなく文字表示し、top前の全正規化トークン出現数総和を表示。Zoo apple zoo APPLE betaのtop1は総数5・1/zoo/2、空入力は総数0。 | Retain counts, compute total before slice; Path.name at CLI |
| REQ-11 | AC3 — 明るい背景・順位/単語/回数3列・scope=col。順位はtop後の1始まり連番。同数でも連番、空表は見出しのみ。320/375/1280pxで200文字語と長い日本語名を欠落/重なり/横overflowなしで読める。実ブラウザ画像・DOM/layout・network・名前/版・viewportと実HTMLを証跡化する。 | Approved UI contract + live Chromium/CDP bootstrap + planned evidence matrix |
| REQ-12 | AC4 — text/json/htmlすべて回数降順、同数はcasefold後の正規化語の初出順、sort後top。Unicode/casefold・頻度優先・top境界・複数hashseedの決定論を試験する。旧語昇順を明示的に置換する。 | Counter order, stable sort, old assertion/doc inventory, multi-seed subprocesses |
| REQ-13 | AC5 — 純粋formatterで1回escapeし、特殊文字/エンティティ風文字/空白/CR/CRLFの元文字列をDOMでも保持。悪意ある実ファイル名が要素/script/イベントとして実行されず、JS/外部assetなし・外部request0を実測する。 | html.escape then CR references; direct formatter and real-name CLI fixtures; pre-navigation monitoring |
| REQ-14 | AC6 — 全pytest・既存CLI/入力境界/エラー/入力不変回帰を維持。stdlib-only、CI・依存変更禁止。別ファイルへのUTF-8保存・共有時の露出・同一パスへのリダイレクト禁止を説明する。ブラウザ手段不足は未検証として人へ返す。 | Existing cached pytest environment, all-format regression, opt-in browser gate, independent rerun and documentation |
</phase_requirements>

## Standard Stack

| Component | Observed version/contract | Use |
|---|---|---|
| Python runtime | Local active `3.14.9`; cached test environment `3.12.15` | Product stays stdlib-only; use existing cached Python for pytest |
| CI Python | `python-version: "3.12"` | Existing CI is unchanged [VERIFIED: .github/workflows/pytest.yml:14–18] |
| Existing test tool | `pytest 9.2.0` in cached environment | No install needed; plain pytest/current Python currently fail import |
| HTML serialization | stdlib html.escape | Text-node escaping only [CITED: https://docs.python.org/3/library/html.html#html.escape] |
| Collection/sort | Counter and sorted | Preserve first encounter order and sort stability [CITED: https://docs.python.org/3.12/library/collections.html#collections.Counter; https://docs.python.org/3.12/howto/sorting.html#sort-stability-and-complex-sorts] |
| Browser | Local Chromium `156.0.8078.73` | Existing headless engine; no download [VERIFIED: version and live /json/version] |
| Development harness | Node `v24.21.0`, native WebSocket/fetch, node:fs/node:child_process/node:url | No npm package required [VERIFIED: node --version; CITED: https://nodejs.org/download/release/v24.21.0/docs/api/globals.json] |

[VERIFIED: pyproject.toml:8–11] `dependencies = []` and `dev = ["pytest"]`. **Installation: none. Package Legitimacy Audit: not applicable; no external package is added.** Node/browser tooling is validation-only, not a Python runtime dependency.

## Architecture Patterns

### Data flow

```text
CLI args → validate → FileSource.read_text → iter_tokens → Counter
   │ input/usage error → stderr + existing exit 1/2
   └ success → stable count-desc sort → top-selected pairs
                 │ retained Counter → full total
                 │ original input argument → basename
                 ├ text(pairs) → stdout
                 ├ json(pairs) → stdout
                 └ html(pairs, basename, total) → stdout → distinct UTF-8 file
                                                        → local browser file URL
                                                        → independent evidence
```

[RECOMMENDATION, design.md:24–34] Retain a single counts object in CLI instead of nesting count_words inside top_words. `top_words` remains the only ordering authority. `format_html(pairs, *, filename, total_count)` is the approved signature shape, not an existing function [VERIFIED: design.md:28, quote: `format_html(pairs, *, filename, total_count)`]. Compute basename using the execution OS's Path semantics without resolve. Sum all counts, not selected pairs or distinct keys. Enumerate already selected rows for display rank.

[VERIFIED: 02-UI-SPEC.md:83–114] Fixed title/h1 is `wordfreq 集計結果`; labels are `入力ファイル:` and `総出現数:`; columns are `順位` / `単語` / `回数`; fixed aria-label is `単語の出現頻度`. Apply the approved contract verbatim: max-width `960px`, padding `24px`/`16px`, table fixed `20%`/`60%`/`20%`, cell padding `8px`, `white-space: pre-wrap; overflow-wrap: anywhere; word-break: normal`. Keep labels and values in separate elements. No indentation whitespace inside dynamic value elements. No clipping, horizontal scroll wrapper, display:block table cards, or font shrinking. UI-SPEC already defines all colors, typography and margins; do not redesign.

### Component change inventory

[VERIFIED: opened current files in this session]

| Existing source | Finding and planned change |
|---|---|
| wordfreq/aggregator.py:11–13 | Docstring says `descending count, then ascending word`; change to stable count-only selection |
| wordfreq/__main__.py:13–15,29–31 | Choices currently `["text", "json"]`; add HTML branch, preserve existing default and writes |
| wordfreq/formatters.py:1–13 | Pure text/json functions; add HTML and one text escape boundary |
| tests/test_aggregator.py:17–33 | Old alphabetic expectations, including top1 apple; replace with first-seen expectations |
| tests/test_cli.py:22–60 | Default text, top3 and JSON old alphabetic order all require intentional updates |
| tests/test_cli.py:137–180 | Empty and cold-copy worktree/input checks currently cover text/json or default text; expand all formats without weakening baseline staging |
| tests/test_sources_boundary.py:7–42 | Existing acquisition separation and once-only boundary; retain, extend CLI composition spy where needed |
| wordfreq/sources.py:17–22 | `open(self._path, "r", encoding="utf-8")`; do not change newline acquisition behavior |
| wordfreq/tokenizer.py:6,14–18 | `r"\w+"` and `token.casefold()`; preserve |
| CONCEPTS.md:45–47 | Old codepoint ascending contract; synchronize glossary with intentional replacement |
| README.md:1–3 | Only repository identification exists; add actual safe CLI HTML usage and compatibility notice |

### Recommended sequential plan boundaries

[RECOMMENDATION] Each PLAN has at most three tasks, on the same branch. Use explicit depends_on for every follow-on plan. Avoid a formatter-only horizontal plan before a CLI slice.

1. **Vertical tracer:** test-first shared first-seen selection and update existing old-order expectations/CONCEPTS; pure HTML formatter + CLI wiring with smoke/metadata/empty/safety tests; run existing unit/CLI suite on completed slice. Include actual tests in each task that first changes behavior; never reference a later task's absent verifier.
2. **Regression/security expansion:** all-format input/top/error/Unicode/hashseed and once-only composition tests; direct formatter whitespace/escape/CR tests and fixture preparation; README safe usage and input-byte preservation test. Depends on tracer.
3. **Browser evidence:** create reusable file-backed harness and opt-in pytest integration with deterministic fixtures; execute Builder evidence and fix failures without loosening assertions; quality rerun handoff with evidence index and current target head. Depends on all previous outputs. A quality gate is not satisfied by writing the handoff.

Each task's fails_when must identify observable wrong behavior: apple winning a zoo-first tie, total equaling selected count, basename mismatch after browser parsing, any injected element/dialog, any unexpected resource request, overlap/scroll overflow, or input-byte change. Gate checks run from files already created in that task or earlier tasks.

## Don't Hand-Roll

[RECOMMENDATION, grounded in cited Python/Node docs and approved design]

| Problem | Do not build | Use instead |
|---|---|---|
| Counting and encounter order | Parallel position map, sets, lexical tie fallback | Existing Counter insertion order |
| Ordering | Per-format sort or custom comparison engine | Stable sorted by negative count, slice last |
| Escaping | Replace ampersands/brackets manually or escape template twice | html.escape once, then CR reference substitution |
| Filename privacy | String splitting or resolve/absolute path display | Path.name in CLI |
| Browser transport | WebSocket frame implementation | Existing Node native WebSocket |
| Responsive report | Framework, CSS library, browser-side JS | Approved inline CSS and semantic table |
| Evidence | Static parser posing as browser, invented screenshots/logs | Live Chromium CDP and actual file document |

## Code Examples

These are **proposed implementation patterns, not files created or commands run in this research**. Names/signature come from opened design.md:24–34; stdlib APIs from cited documentation.

```python
# Shared selection: retain Counter insertion order for equal counts.
return sorted(counts.items(), key=lambda pair: -pair[1])[:n]

# Text-node serialization only, not HTML attributes or CSS.
from html import escape
safe_text = escape(value, quote=True).replace("\r", "&#13;")
```

[CITED: https://html.spec.whatwg.org/multipage/parsing.html#preprocessing-the-input-stream; VERIFIED: 02-UI-SPEC.md:110–115] Raw CR/CRLF is normalized during HTML parsing. Escape first, convert CR second, and never escape the resulting `&#13;` again. A source literal `&amp;` must become serialized ampersand text that decodes back to the original literal, not to a different character. Browser textContent comparison must be exact, without trim or newline normalization. Direct formatter inputs can contain characters that tokenizer normally removes; they are necessary boundary tests, not tokenization changes.

## Environment Availability

[VERIFIED: discovery terminal and read_file results in this session]

| Dependency | Availability | Actual finding / required action |
|---|---|---|
| Active Python / plain pytest | Unusable for pytest currently | `python3 -m pytest`: `No module named pytest`; plain pytest launcher also ModuleNotFoundError |
| Existing cached Python + pytest | Available | `/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python --version` → `Python 3.12.15`; same executable `-m pytest --version` → `pytest 9.2.0` |
| playwright executable | Broken | `/home/Yuki/.local/bin/playwright --version` → `ModuleNotFoundError: No module named 'playwright'`; do not use/install |
| Chromium wrapper | Local execution | readlink resolves `/usr/bin/chromium-browser` to `/usr/lib64/chromium-browser/chromium-browser.sh`; wrapper reads local `/etc/chromium/chromium.conf` and execs sibling binary, not remote/container dispatch [VERIFIED: wrapper:8–10,35–51] |
| Chromium headless/CDP | Launch/discovery/handshake available | Successful launch and endpoints below; product navigation/evidence not executed |
| Node | Available | `v24.21.0`; official exact-version globals JSON says native WebSocket is no longer experimental since `v22.4.0` |
| curl / jq | Available and exercised | Discovery, live method/parameter extraction, HTTP upgrade |
| Context7 MCP / ctx7 CLI | Not available in this tool set/PATH | Research-plan selected context7; used official docs through web_extract/curl instead; no install |

### Browser discovery: actual execution, not just version

[VERIFIED: browser process logs and read_file of generated DevToolsActivePort] First launch used absolute scratch TMPDIR and exited `134` with:

```text
FATAL:chrome/browser/process_singleton_posix.cc:315] Socket path too long:
.../cache/scratch/org.chromium.Chromium.xzruRr/SingletonSocket.
```

Second launch used the existing profile scratch directory as cwd, `env TMPDIR=.` for the browser child, the following arguments, and a distinct user-data-dir under that scratch directory:

```text
/usr/bin/chromium-browser --headless --disable-gpu --no-first-run
  --no-default-browser-check --disable-background-networking
  --remote-debugging-address=127.0.0.1 --remote-debugging-port=0
  --user-data-dir=<absolute-profile-scratch>/phase02-cdp-short about:blank
```

[VERIFIED: live discovery] Chromium printed `DevTools listening on ws://127.0.0.1:44729/devtools/browser/583e1d4c-60a3-499e-857f-cbfece7e674f`. The generated DevToolsActivePort contained port `44729` and that browser path. `/json/version` returned `"Browser": "Chrome/156.0.8078.73"`, `"Protocol-Version": "1.3"`, `"File-Path-Style": "posix"`. `/json/list` showed a page target `about:blank` as well as browser_ui targets. **Select only the intended page target**, not the first arbitrary entry.

[VERIFIED: live /json/protocol extraction with jq] Advertised commands include `Network.enable`, `Page.enable`, `Page.navigate`, `Page.captureScreenshot`, `Runtime.enable`, `Runtime.evaluate`, `Emulation.setDeviceMetricsOverride`. Width/height/deviceScaleFactor/mobile are required emulation parameters. Screenshot has format/fromSurface/captureBeyondViewport options.

[VERIFIED: curl WebSocket upgrade] GET to the discovered browser WebSocket path with Upgrade/Connection/Version/Key headers returned:

```text
HTTP/1.1 101 WebSocket Protocol Handshake
Upgrade: WebSocket
Connection: Upgrade
```

The curl connection intentionally ended by its 2-second timeout (`exit 28`); it sent no CDP JSON. This proves endpoint upgrade, **not** Node WebSocket message exchange, screenshot capture, file URL navigation, network instrumentation, or product acceptance. No wildcard remote origin flag, no sandbox disabling, no HTML-serving server, no upload was used. The debug HTTP endpoint is browser instrumentation, not report serving.

## Existing-browser evidence execution design

[RECOMMENDATION, supported by local discovery and CITED: https://chromedevtools.github.io/devtools-protocol/] Create a small development-only `.mjs` file using native WebSocket; do not add npm metadata/packages. CDP is high-privilege and its official docs warn of compatibility changes: pin evidence to the observed browser version, inspect its live protocol, fail clearly on missing methods, and keep the endpoint loopback-only. The harness itself is not yet present or tested.

### Builder files and entrypoint contracts (all NEW/proposed)

- `tests/conftest.py`: register `--real-browser` boolean and `--browser-evidence-dir` path; register a real_browser marker and skip marked tests unless explicitly enabled. Do not modify pyproject or CI for marker configuration. When opted in, unavailable browser/Node is a test failure/blocker, never a skip/pass.
- `tests/test_html_browser.py`: pytest-owned fixture generation and subprocess CLI calls; exact expected JSON manifest; invoke Node via its file path, with bounded timeout; check actual output/index and preserve results.
- `tests/browser/wordfreq_html_evidence.mjs`: launch Chromium in unique scratch cwd, child TMPDIR=.; native fetch discovery and WebSocket transport, incrementing command IDs/pending promises/events/error handling; CDP evidence operations; finally close browser/socket and terminate its process if needed. No shell command string, eval CLI, or dependency import.
- `tests/test_html_output.py`: pure HTML/CLI contract regression. It may instead be split across existing formatter and CLI modules if planner updates commands consistently.
- Evidence output beneath the approved `.planning/phases/02-wordfreq-html-output/evidence/`, with separate `builder/` and `quality/` run subdirectories, not overwriting each other. This directory is deliberately not created during research [VERIFIED: planned parent path in 02-UI-SPEC.md:138].

### Fixture matrix (generate from a real test file, not inline scripts)

[RECOMMENDATION, approved scenarios: spec.md:48–155; UI-SPEC:132–142]

| Case | Generation / expected oracle | Browser widths |
|---|---|---|
| Normal | CLI input `one one one two two three`; three ranked rows | 320 / 375 / 1280 |
| Ties | CLI `Zoo apple zoo APPLE beta`; zoo then apple then beta | 320 / 375 / 1280 |
| Top1 | Same input, top1; total5, only 1/zoo/2 | 320 / 375 / 1280 |
| Empty / symbols | CLI zero-byte file and punctuation-only file; total0, three headers, zero rows | 320 / 375 / 1280 |
| Long | CLI file with a 200-character ASCII word and long Japanese basename | 320 / 375 / 1280 |
| Real malicious names | CLI actual filesystem names containing tag/event/entity/quotes; exact basename and normal input words | 320 / 375 / 1280 |
| Real whitespace names | CLI actual Japanese basename with spaces, tab, LF, CR, CRLF; exact DOM text | 320 / 375 / 1280 |
| Direct formatter boundary | Test file imports formatter; words and filename include special chars, entity-looking text, spaces/tab/LF/CR/CRLF, leading/trailing whitespace | 320 / 375 / 1280 |

Use harmless synthetic content, not private user input. Long Japanese basename must fit the filesystem's byte-length limit; recommend 40 Japanese characters plus `.txt`, not 200 Japanese characters. The 200-character requirement is for a **word**, not a basename. Actual filenames must be a single basename: **no `/` or NUL**. Do not write a test that secretly creates path components such as `</script>` or `https://...` inside a filename.

Concrete proposed real-basename payloads include `<img src=x onerror=alert(1)> &amp;.txt`, `<svg onload=alert(2)>.txt`, and a separate name containing quotes and `<script>` text; none uses slash. Full closing-tag payloads belong in direct formatter inputs, where slash is legal. Write CLI fixture content and read filenames through filesystem APIs, never through interpolated shell commands. Store expected name as JSON with control-character escaping. Before running malicious cases, prepare no fake passing log or screenshot.

### Required CDP sequence

[RECOMMENDATION, API availability verified above; behavior still to be exercised]

1. Generate UTF-8 HTML through actual CLI stdout bytes into a **different** path; save exit/stderr, options, input bytes or hash, expected values, head and dirty-state/diff attribution. Direct-formatter documents must be labeled separately, never passed off as CLI-generated evidence.
2. Launch fresh Chromium, cwd within active profile scratch, TMPDIR=. and unique profile. Read its generated debug port; discover/select page about:blank. Do not reuse a user's existing profile/browser session. Connect native WebSocket and await open with a deadline.
3. Install event listeners **before** commands/navigation. Await acknowledgments of Network.enable, Page.enable and Runtime.enable. Subscribe to requestWillBeSent/responseReceived/loadingFailed/loadingFinished, console/errors and javascriptDialogOpening. Close and fail on dialog after recording it, rather than hanging. Keep page JS execution enabled: disabling scripts or injecting a protective CSP would conceal an escaping bug.
4. Set width 320/375 with mobile=true; 1280 with mobile=false; planned height 900 and deviceScaleFactor=1 explicitly. Record requested metrics plus actual innerWidth/innerHeight/devicePixelRatio. Include screen dimensions if needed, and fail if actual CSS viewport differs. Use file URL conversion, not manual URL concatenation, for spaces/control characters.
5. Navigate only after monitoring is active; wait for the right frame/load event and document completion, with timeout and failed-navigation detection. Capture main file request and completion as **positive evidence that monitoring was active**. Reconcile requested URL/frame with observed file request. If Chromium does not expose those events as expected, report monitoring unverified or use a separate local positive-control fixture with a known local resource; do not treat an empty event list as success. No external positive-control request or report server.
6. Compare DOM textContent exactly with manifest strings; compare rows, headers, scope=col, total, basename, rank sequence, no links/dynamic attributes/elements/script. Also inventory event-handler attributes and unexpected resource tags. Record dialogs/console/errors and any changed execution marker when relevant. The harness's observer JavaScript is validation code, not product JS.
7. Save document/body/table scrollWidth/clientWidth and bounding rects for main/h1/metadata/table/headers/cells. Assert no document horizontal scrolling, table/cells fit their allocations, adjacent cells do not overlap, and blocks appear in order without overlap. Check metadata bounding width plus each text range/client rect for wrapped text containment where necessary. Compare full original text and styles; never trim, insert break characters, or allow hidden/clip/ellipsis to fake fit. Vertical scrolling is allowed. Check approved light colors and contrast at least 4.5:1 with a test-file implementation of the standard contrast calculation; include computed style values.
8. Capture real PNGs for each case/viewport; include full-page image or scroll captures for tall long-word content, not just a clipped first viewport. Save DOM/measurement JSON, raw network event JSON, main-file events, external request classification/count and **unexpected additional local resource** count. External requests and unexpected local resources must both be zero. Record browser version, viewport height/scale, CLI generation conditions and target head in the index.
9. Rerun from CLI generation through observation for quality, into a separate output directory. Re-resolve target head immediately before report; if it changed, rerun or mark evidence stale. Close browser and remove scratch processes. Missing screenshot/DOM/network/version/head evidence is a failed gate, not a static-test substitute.

## Common Pitfalls

[VERIFIED: existing code/tests and UI contract; mitigations are recommendations]

- **Old order appears in more than the aggregator.** tests/test_cli.py:28,36,54–57 and CONCEPTS:47 assert old lexical behavior. Update intentionally; never delete regression coverage to make new order green.
- **A Counter equality assertion ignores ordering.** Add ordered pairs/keys expectations and CLI bytes for first-seen ties, frequency precedence, top boundary and casefold collisions.
- **Total computed after top.** Retain Counter and derive its sum before selection; top1 example detects the mistake.
- **CR passes a Python parser but fails the real browser.** Static parser/string tests are not browser newline normalization proof. Preserve CR references and compare literal DOM strings.
- **HTML safety appears covered because tokenizer removes symbols.** Test pure formatter directly and malicious real basename through CLI/browser; both boundaries are mandatory.
- **Network instrumentation starts late or records nothing.** Register listeners and enable domains before navigation; require positive main-file observation and zero unexpected resources.
- **Remote debugging socket is too long.** Use short relative TMPDIR under actual scratch cwd; no system-temp diversion, package install, blanket sandbox/origin relaxation.
- **Plain pytest points at the wrong Python.** Use the discovered existing cached interpreter. Do not auto-install pytest/playwright or use uv download wrappers.
- **State hygiene regression is weakened.** Preserve cold copy, copy .gitignore, git init/add baseline, environment cleanup and full untracked status comparison [VERIFIED: tests/test_cli.py:152–180]. Extend to HTML with output outside input/repo fixture rather than excluding generated files from assertions.
- **False unreadable-file test.** A directory already exercises OSError; add actual permission-denied coverage with environment-aware setup or a FileSource read fault test, not a chmod fixture that silently succeeds under a privileged account. Do not skip all error assertions.
- **Evidence contaminates its own target.** Capture product/test head before generated output; record dirty state and distinguish evidence/report commit from verified target. Do not copy old 43-passed results into this phase [VERIFIED: learnings.md:33–41].

## Validation Architecture

[VERIFIED: .planning/config.json:25] Nyquist validation is explicitly enabled. All commands below are **planned Builder/quality commands**, not executions performed during planning. New files/options must exist before their command is used. Only framework version discovery was run here; no pytest acceptance suite was run.

### Test Framework

| Property | Value |
|---|---|
| Framework | Existing pytest 9.2.0, cached CPython 3.12.15; CI Python 3.12 remains unchanged |
| Existing config | pyproject.toml contains packaging only; no pytest config [VERIFIED: pyproject.toml:1–14] |
| Interpreter | `PYTEST_PYTHON=/home/Yuki/workspace/argonauts-uat-20261116/home/.cache/uv/archive-v0/OrlfUBJ6ZvJ3-CXj/bin/python` |
| Quick existing regression | `"$PYTEST_PYTHON" -m pytest tests/test_aggregator.py tests/test_formatters.py tests/test_cli.py -q` |
| Expanded quick | `"$PYTEST_PYTHON" -m pytest tests/test_html_output.py tests/test_aggregator.py tests/test_cli.py -q` — only after NEW file exists |
| Full default suite | `"$PYTEST_PYTHON" -m pytest -q` — browser tests explicitly opt-in through NEW --real-browser flag, skipped by default |
| Real browser gate | `"$PYTEST_PYTHON" -m pytest tests/test_html_browser.py --real-browser --browser-evidence-dir=.planning/phases/02-wordfreq-html-output/evidence/builder -q` — only after NEW files/options exist |
| Independent quality | Same opt-in command with `evidence/quality`, actual current target head recorded separately |

### Phase Requirements → Test Map

All paths labelled NEW below are recommendations, not existing artifacts or claims of completed tests. Existing files are source-read in this session.

| Req ID | Behavior | Type | Planned command | File exists? |
|---|---|---|---|---|
| REQ-09 | Complete single HTML; default text; unchanged JSON shape; exit/stdout/stderr | unit + CLI | `"$PYTEST_PYTHON" -m pytest tests/test_formatters.py tests/test_cli.py tests/test_html_output.py -q` | First two yes; HTML file NEW |
| REQ-10 | Basename only, total before top, total0 empty | formatter + CLI | `"$PYTEST_PYTHON" -m pytest tests/test_html_output.py -q` | NEW |
| REQ-11 | Semantic 3 columns/ranks, responsive long/empty at all widths | unit + real browser | `"$PYTEST_PYTHON" -m pytest tests/test_html_browser.py --real-browser --browser-evidence-dir=.planning/phases/02-wordfreq-html-output/evidence/builder -q` | NEW; images/layout must be reviewed |
| REQ-12 | Stable normalized first-seen ties, casefold, priority/top, seeds | aggregation + CLI | `"$PYTEST_PYTHON" -m pytest tests/test_aggregator.py tests/test_cli.py -q` | Yes; extend/update assertions |
| REQ-13 | Escape once, CR/CRLF exact DOM, malicious filenames, no resources/execution | unit + real browser | HTML output quick command AND browser gate above | NEW |
| REQ-14 | Full matrix, input/worktree/boundary preserved, safe documentation example | regression + documented usage + independent browser | `"$PYTEST_PYTHON" -m pytest -q` AND independent quality browser command | Existing suite yes; browser extension NEW |

[RECOMMENDATION] Quick unit/CLI sampling should aim below 30 seconds and use bounded subprocess timeouts; actual timing is not measured in research. Browser matrix is a separate bounded gate and may exceed 30 seconds; never cut viewports/scenarios just to claim a fast gate. Multiple seeds can be checked inside the CLI test using subprocess env, e.g. 1 and 777, comparing **bytes within each format** (not text vs JSON vs HTML). Parameterize normal/empty/symbols/Unicode, default10/top1/topN/overlarge, invalid top0/negative/noninteger, invalid format, zero/multiple files, missing/unreadable/invalid UTF8. Preserve output and error contracts exactly.

### Sampling Rate

- Per task commit: execute appropriate quick tests from already-existing verification files; record command/interpreter/exit. Tests and implementation must be together by task completion.
- Per serial PLAN completion: full default suite; does not certify skipped browser tests.
- At browser PLAN/phase gate: explicit opt-in complete matrix, full default suite, evidence completeness and visual review; independent quality repeats CLI generation and browser measurement.
- Failing browser bootstrap, missing expected file events, unavailable Node native WebSocket, missing fonts/tofu, or incomplete evidence: REQ-11/13 and relevant REQ-14 acceptance remain unverified. Return gap; do not install or change CI.

### Wave 0 Gaps

- [ ] NEW HTML contract/regression tests and whole all-format matrix.
- [ ] NEW opt-in conftest options/marker, browser test file, file-backed Node harness and manifest contract.
- [ ] NEW fixtures for valid malicious filenames, exact control characters, long word/name, top/empty cases.
- [ ] NEW generated evidence/index and reproducible quality instructions (creation is implementation, not research).
- [ ] Framework installation: **none**. Existing cached pytest environment was found and its version command succeeds. If that cache is unavailable to a later agent, stop for environment assistance instead of installing dependencies under this scope.

## Security Domain

[VERIFIED: .planning/config.json:49–51] Security enabled, ASVS level 1, high findings block. Use stack-applicable controls, not an authentication/server checklist as a reason to add services.

| ASVS category (project template nomenclature) | Applies | Control |
|---|---|---|
| V2 Authentication | No | Offline read-only static document, no accounts |
| V3 Session Management | No | No sessions or cookies in product |
| V4 Access Control | Local boundary only | Basename privacy, no filesystem link/navigation exposed |
| V5 Input Validation / output encoding | Yes | argparse, existing UTF-8 boundary, one HTML text encoding boundary; no dynamic attributes/CSS/URLs |
| V6 Cryptography | No product crypto | Stdlib hashes only if used for evidence integrity; no custom crypto |

[RECOMMENDATION, threat model grounded in approved HTML-2/HTML-4] XSS/HTML injection (tampering): encode at formatter, confirm exact DOM and no event/script effects. Information disclosure: basename only, synthetic fixtures, document that stored words/name remain visible when shared. Unexpected communication: no external references; observe before navigation; classify extra local resources as failures too. Input destruction: document distinct output paths, verify bytes, never demonstrate same-path destructive redirection. Debugger exposure: loopback only, fresh scratch profile, close process; never public-bind CDP.

## Runtime State Inventory

[VERIFIED: design.md:55–57] This is an additive static formatter plus an explicit ordering-contract replacement; design says data migration/service deployment is unnecessary. No identifiers/services are renamed. Repository-local state affected: code expectations, CONCEPTS and usage documentation. No external stored data, live service config, OS registrations or secret keys are to be migrated in this scope. Only temporary browser profile/build evidence is created by future validation; no installer or system registration is needed. This is scope analysis, not an audit of unrelated user systems.

## State of the Art

[CITED: Python Counter/sorting docs; Chrome headless docs; exact Node globals JSON] Counter remembers insertion order; stable sorting is sufficient. Unified Chromium headless uses the real browser engine; no alternate download is necessary. Node's native WebSocket removes the need for npm ws/Playwright dependencies here. Direct CDP compatibility is not guaranteed by its upstream docs, so validate methods against the live browser and preserve versioned evidence. The old lexical tie rule is **superseded project behavior**, not a Python deprecation.

## Assumptions Log / Open Questions

| Item | Status / risk / disposition |
|---|---|
| Node native WebSocket client plus file evidence harness | [ASSUMED] End-to-end harness compatibility is not executed in research. Official native API plus live HTTP101/method discovery establish a grounded route, not an acceptance result. Builder must exercise actual file-backed client; failure becomes BLOCKED/unverified without install. |
| Browser layout, zero requests and CR fidelity | Not claimed as facts. Explicit future acceptance checks; cannot be inferred from docs or static code. |
| Performance/timing | Not benchmarked; proposed timeouts/sampling targets are recommendations, not measured results. |

No product-scope/user-design question remains; no repeat of Q-1–4. Environment discovery resolves the broken default pytest path with an existing compatible cached interpreter. Browser bootstrap is no longer version-only, but actual product evidence is deliberately deferred to implementation and independent quality as required. UI-SPEC frontmatter says `status: approved`; its trailing old pending/checklist wording is inconsistent [VERIFIED: UI-SPEC:1–5,150–160]. Follow approved contract and tell the planner/parent about the stale footer; do not reopen UI design or silently edit it during this research.

## Sources and Research Method

### Primary repository / live environment

All repository sources cited with line ranges were opened with read_file in this session: CONTEXT, REQUIREMENTS, STATE, UI-SPEC, learnings, current source/tests, design/spec, config, CONCEPTS, README, pyproject, existing CI and .gitignore. Discrete values above are quoted next to their citations. Proposed new paths are explicitly NEW, not verified source-of-truth artifacts.

Actual tool observations: official GSD init/graphify/agent-skills/research-plan/classify-confidence, Python/pytest/Chromium/Node version commands; wrapper/config reads; Chromium launch attempts; DevToolsActivePort read; curl discovery/protocol/HTTP101; exact-version Node globals.json parsed with jq. Browser was opened only on about:blank for discovery, not on product/generated HTML. No implementation, tests, validation scripts or evidence fixtures were created/run during planning.

### Official documentation (CITED)

- https://docs.python.org/3.12/library/collections.html#collections.Counter — insertion order.
- https://docs.python.org/3.12/howto/sorting.html#sort-stability-and-complex-sorts — stable sorting.
- https://docs.python.org/3/library/html.html#html.escape — standard HTML escaping; generic docs redirect to newer docs, use only documented established escape behavior, not an inferred version support claim.
- https://html.spec.whatwg.org/multipage/parsing.html#preprocessing-the-input-stream — HTML input/newline parsing; approved UI contract independently requires CR references and exact browser proof.
- https://developer.chrome.com/docs/chromium/headless — real headless Chromium execution; retrieved page reports updated 2024-10-21.
- https://nodejs.org/download/release/v24.21.0/docs/api/globals.json — exact installed-version native WebSocket declaration, including stable-since metadata.
- https://chromedevtools.github.io/devtools-protocol/ and Page/Network/Emulation references — automation transport and APIs; supplement with the actual live /json/protocol to avoid tip-of-tree mismatch.

### GSD seam provenance

[VERIFIED: official CLI output] research-plan returned keys `e822c91d53a1f6fb91173105a8a30c577423c97546f323c7cba9899b7999e818` and `f9383970e6502445407ee859c801709e99b4ab4b0c5b9806e580d7fc119e2602`, both requesting context7. Context7/ctx7 unavailable; authoritative direct fetch was used instead, without installation. `query classify-confidence --provider webfetch` and with `--verified` both returned `LOW`; `context7` returned `MEDIUM` but was not the provider actually used. Accordingly official-doc digests were cached through research-store as provider webfetch/confidence LOW, not relabeled as Context7/HIGH. Local repository/runtime observations remain explicitly distinguished from documentation-derived design and unexecuted harness assumptions.

## Metadata

- Repository/runtime factual confidence: HIGH for observed content, launch and endpoint discovery only.
- Standard stack recommendation: established stdlib APIs plus exact existing tool inventory; no new dependencies.
- Evidence-harness end-to-end confidence: LOW until Builder runs actual file-backed implementation; never described here as verified screenshots/DOM/network.
- Research validity: recheck browser/runtime/cache paths before implementation; no product behavior/pytest result was asserted by this research.
- Output scope: this RESEARCH.md plus profile-local research cache/scratch discovery artifacts. A reusable discovery lesson was staged in the active profile's skill approval queue (not yet saved). No product/dependency/CI change, no commit/push/Kanban action. Discovery Chromium was terminated after inspection.
