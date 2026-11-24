# Phase 08 Builder CLI — original text evidence

## Authority / identity

- Request r-d78495de, task t_6cbb9153, PLAN 08-01 only, full flow; Task1 → Task2 sequential.
- Latest reception judgement: 2026-11-25T06:53+09:00.
- 原文: 検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。
- Expected repository (card): ToR-O3/argonauts-uat-20261114-public; base branch v112-a; origin https://github.com/ToR-O3/argonauts-uat-20261114-public.git matched by git remote -v. Delivery branch argonauts/r-d78495de; local branch wt/t_6cbb9153. All commands run at this card worktree root.
- EDIT_BASE=e18a818a6cc2f6cc37e7f320998c0f6c005e91da (fixed before README edit; not moving HEAD).
- Start: 2026-11-24T23:04:22Z. Initial git status --porcelain: empty; reflog branch: Created from HEAD. Standard checkout aligned to origin/argonauts/r-d78495de. Fetch and base merge exit0 / Already up to date. Workflow difference empty. GH authentication available (credential values not retained).
- Official execute-plan read from active profile gsd-core/workflows/execute-plan.md; card referenced generic home path absent, PLAN execution_context supplied the real installed profile path. Official runtime launcher sourced in same terminal as gsd_run. init.execute-phase 8: one runnable incomplete 08-01-PLAN.md, no summaries. STATE Current Position Phase8, Current Plan1, Total1, Ready to execute matched selected plan. begin-phase --phase 8 --name 'README min-count example' --plans 1 returned phase8/plan_count1 and updated execution state. Inline Pattern C (2 tasks <= threshold3), SEQUENTIAL=true by card marker; no child executor/next PLAN.

## Task1 RED — natural absence, not command failure

Before editing, read_file README.md full 35 lines/4696 bytes and git show e18a818a6cc2f6cc37e7f320998c0f6c005e91da:README.md full output were read. git diff HEAD -- README.md empty; tracked eol i/lf w/lf. Commands returned exit0, stderr empty. Usage lines 9–15 contained basic input.txt, min-count2/json and html examples, but no `python -m wordfreq input.txt --min-count 3`. Therefore REQ-28 content FAIL before edit. This is manual direct-reading failure, not fabricated nonzero exit or missing environment. Existing final line was 検証A: v1.12 の通しの確かめ（2026-11-22）.

## Task1 GREEN — direct reading

Inserted exactly `python -m wordfreq input.txt --min-count 3` after the basic invocation inside the existing sh fence. Read_file full resulting README: 36 lines/4739 bytes, requested line11; old min-count2/json, top/json, html examples still present in order; all option explanations and last line36 retained. Full unified40 patch read: one added line only, no removed line, no EOF-newline marker or mode change. numstat `1\t0\tREADME.md`; eol remains i/lf w/lf. diff --check empty, exit0. Display success is not the content judgement; full originals and patch support Builder REQ-28 GREEN. No new verifier/test, product invocation, dependency/config/tool/code changes. Existing text/json/html execution is excluded, not pending.

The following command transcript retains actual full stdout plus raw exit. Unless specifically shown, stderr was empty in terminal result (error=null). Git display exit0 never by itself means acceptance. Initial original remains reproducible at fixed EDIT_BASE; the full patch includes unchanged README context.

## Task1 actual verification transcript

```text
$ git diff --no-ext-diff --no-textconv --unified=40 e18a818a6cc2f6cc37e7f320998c0f6c005e91da -- README.md
diff --git a/README.md b/README.md
index 0961498..55a5aba 100644
--- a/README.md
+++ b/README.md
@@ -1,35 +1,36 @@
 # argonauts-uat public
 
 Argonauts v1.10 acceptance test repository.
 
 ## wordfreq の実行
 
 リポジトリ直下で、UTF-8 の実ファイルを指定します。Python の標準ライブラリだけで動き、インストールや Web サーバーは不要です。
 
 ```sh
 python -m wordfreq input.txt
+python -m wordfreq input.txt --min-count 3
 python -m wordfreq input.txt --min-count 2 --top 1 --format json
 python -m wordfreq input.txt --top 2 --format json
 python -m wordfreq input.txt --format html
 python -m wordfreq input.txt --format html > result.html
 ```
 
 HTML はロケールや `PYTHONIOENCODING` に依存せず UTF-8 バイト列を標準出力へ書きます。保存時はバイト列をそのままリダイレクトしてください（シェル側で文字コードを変換しないでください）。ファイル名の表示は basename のバイト列を実行環境のファイルシステム文字コードで読み、その文字コードで復号できないバイトだけを置換文字 `�` にします。入力ファイルの読み込みに使うパス自体は変更しません。保存した `result.html` はローカルのブラウザで開けます。HTML は内包 CSS のみの静的文書で、スクリプト・外部フォント・画像・リンク・対話操作はありません。
 
 - `--min-count N` は1以上の整数、既定は1。不正値・値欠落は入力読込み前に stderr と exit2 で知らせます。
 - `--top N` は1以上の整数、既定は10。種類数が N 未満なら全件を表示します。
 - `--format text|json|html` の既定は text。text は `<count>\t<word>\n`、JSON は `word` と整数 `count` の配列に末尾改行1つです。空入力は text が空、JSON が `[]` と改行、HTML が見出し3列・データ0行・総数0です。
 - Unicode の単語文字の連続を抽出し、casefold した語を数えます。日本語の形態素解析は行いません。
 - 全形式で min-count 未満を除外し、回数降順に並べ、同数時は**正規化後の初出順**を保ってから top を適用します。両値は独立で、指定順による違いはありません。これは以前の「同数は語の昇順」からの意図した互換性変更です。`Zoo apple APPLE zoo banana` は min-count2 で zoo2 / apple2、さらに top1 で zoo2 になります。全件除外されたら min-count を下げてください。
 - HTML の表は順位・単語・回数で、順位は表示行の1始まり連番です。表の上にファイルの basename のみと **min-count / top 前の総出現回数**を表示します。総数は表示行の和や種類数ではありません。ディレクトリ情報は HTML に埋め込みません。ただし入力本文中の語と basename 自体は表示されるため、共有前に内容を確認してください。
 - ファイル名と語はテキストとして一度だけ HTML escape し、属性・CSS・URL には使いません。明るい背景固定で、長い語・名前は連続空白・改行・タブを保持して折り返す設計です。
 - 読込み・UTF-8 decode 失敗は stderr と exit1、不正 top・format・引数個数は stderr と exit2。エラー時は stdout を空にし、エラー用 HTML は出しません。
 
 ## 部品の契約と検証状況
 
 `count_words` が正規化済みトークン列から作る Counter の挿入順は初出順です。`top_words(counts, n)` に直接渡す場合も、この挿入順を保つことが前提です。回数だけの安定ソート後に制限し、入力は変更しません。
 
 `format_html(pairs, basename, total)` は渡された順序を保つ純粋な文字列整形部品です。呼出し側が basename と min-count / top 前の総数を渡します。整形部品は再読込み・集計・ソート・標準出力への書込みをしません。既存 text/json の部品の引数と形式は変更しません。
 
 自動試験は集計・実CLI・HTMLParser、安全性、証拠欠落の拒否を検査します。[ブラウザ検証手順](docs/wordfreq-html-verification.md)に、通常幅1280×900と狭幅320×900 CSS px・DPR1での再生成、live review-session、全画像とrawRangeの実閲覧台帳、通信試行・head/scopeの再照合、finalize後の最終verdict確認を記載しています。品質担当は自分のfresh rootで対象headから独立再生成します。ツール完成やcapture成功は独立品質・phase受入の完了ではなく、そのgateは実行までpendingです。CSS・幾何・画像の存在だけで可読性や無通信の合格とはしません。
 検証A: v1.12 の通しの確かめ（2026-11-22）
raw exit=0
$ git diff --numstat e18a818a6cc2f6cc37e7f320998c0f6c005e91da -- README.md
1	0	README.md
raw exit=0
$ git diff --check e18a818a6cc2f6cc37e7f320998c0f6c005e91da -- README.md
raw exit=0
```

## Task2 committed scope and originals (pre-D.5)

Task1 commit/tracer: fc3d7362d6e88487222565a4c16d1d9ab0a6cadb. After this commit, re-ran unified40 EDIT_BASE→HEAD, numstat and diff --check; all exit0/stderr empty, full patch still one specified line only, numstat1/0. Task1 criteria content PASS, tracer feedback confirmed before Task2. README full read from Task1 remains the Task2 starting file (unchanged).

Source matching: card fixed repository/base v112-a and git remote get-url origin = https://github.com/ToR-O3/argonauts-uat-20261114-public.git. `git fetch origin refs/heads/v112-a:refs/remotes/origin/v112-a` exit0, empty stdout/stderr. `git rev-parse --verify 'origin/v112-a^{commit}'` = cf407aaa6babebc0a21cf6370530d321b8a615e1 (BASE); HEAD_SHA = fc3d7362d6e88487222565a4c16d1d9ab0a6cadb. Both verified commit objects; `git merge-base` = cf407aaa6babebc0a21cf6370530d321b8a615e1. Local v112-a = c6b701bfdc1af9c39f9b8421336e881e5cda6ee4, DIFFERENT from fetched base, not used or modified. All identity commands exit0/stderr empty. This is pre-D.5 branch observation, NOT final PR validation. No origin/main fallback.

### Classification and separate verdicts

- Every status/path is retained below without filtering. README.md is the requested product document. `.planning/INGEST-CONFLICTS.md`, REQUIREMENTS/ROADMAP/STATE/state.json are workflow input/state; `.planning/argonauts/` are approved source, manifest, learning and planner checks; `.planning/intel/` are ingestion classifications/context; `.planning/phases/08-*` are PLAN/context/research/patterns/validation and Builder text record. All remain changes and make condition2 unmet; directory names do not exempt them.
- Every `_bmad-output/initiative-r-d78495de/` path below is an upstream specification/review/template/memlog artifact (including brief HTML, not product HTML). Every `openspec/changes/r-d78495de-readme-min-count/` path below is workflow proposal/design/task/schema input. They are not new product code, but are still outside the permitted final README-only list. No other product path appeared against the fetched v112-a base.
- REQ-28/OpenSpec1.1: Builder content GREEN from fixed EDIT_BASE/branch base originals, full README and complete patch: one requested example added in the existing fence; all existing content/final line preserved. Standard attachment still pending at this recording point; actual IDs/hash checks go in transition metadata after upload, not invented here.
- REQ-29/OpenSpec2.1: UNMET / provisional before D.5. Full name-status/name-only lists below match, nonempty but include all those non-README paths. Builder handoff done is NOT independent quality, PM acceptance, final PR success or phase completion. OpenSpec2.1 stays unchecked.
- Uncommitted paths at transcript: .planning/STATE.md and .planning/state.json (official begin-phase), plus this .planning/phases/08-readme-min-count-example/08-BUILDER-CLI.md (its own recording update). Cached list and untracked list empty. SUMMARY will be created later and explicitly committed; subsequent official state/roadmap changes and SUMMARY must be re-observed at delivery head. These are not hidden in the committed snapshot.
- Images generated/viewed: 0. README original/patch text verification only; no UI change. Product CLI / text,json,html executions and product input/output/exit-code evidence: not performed, excluded by current judgement, NOT pending.
- Three unresolved probes E1 boundary/E2 precision/E3 unclassified and two descriptorless prohibitions (publication is not execution proof; intermediate/self-review is not independent final approval) remain flagged-unverified. No product runtime requirements added and no flags silently resolved.

### Required downstream handoff (not performed by Builder)

1. Independent quality must obtain its own README originals, patch and complete unfiltered lists from its observed head; confirm expected repo and base v112-a/fetch, record full base/head/merge-base and local-reference difference, separate working/index/untracked lists. Save/push/standard-attach 08-QUALITY-CLI.md and 08-VERIFICATION.md, with two separate condition results and images0/reason. Until final scope is restricted, REQ-29 remains unmet/provisional.
2. PM/finalization must read official team D.5 and perform its specified-file-only procedure ONLY after full originals (PLAN, SUMMARY, Builder evidence, quality evidence) are saved, pushed, standard-attached and verified. No individual process-file deletion or improvised history cleanup. Engineering roots: .planning, openspec, _bmad-output, .compound-engineering, docs/solutions.
3. After D.5, independent quality must re-fetch actual PR identity, base branch v112-a, complete base/head SHAs; verify objects/merge-base; obtain `git diff --no-ext-diff --no-textconv --no-relative --name-status "${BASE}...${HEAD_SHA}"` and same --name-only WITHOUT any path restriction; obtain both `git show "${MERGE_BASE}:README.md"`, `git show "${HEAD_SHA}:README.md"`, full `git diff --no-ext-diff --no-textconv --unified=40 "${BASE}...${HEAD_SHA}" -- README.md` and `git diff --check "${BASE}...${HEAD_SHA}"`. Empty list, missing README, any non-README path (including workflow), missing/duplicate/wrong example or damaged old content FAILS the corresponding condition; incomplete output/wrong SHA means unverifiable, never PASS. Changed base/head requires new observations. Do not reuse this intermediate head as final proof.
4. Quality standard-attaches those final text originals; PM reads the actual originals with read_file. Builder self-confirmation is not the independent judgement. All these downstream steps, finalization and PM read are pending, not claimed executed. Next phase null; this request is Phase8 only (global ROADMAP phase_count6).

```text
$ git diff --no-ext-diff --no-textconv --no-relative --name-status cf407aaa6babebc0a21cf6370530d321b8a615e1...fc3d7362d6e88487222565a4c16d1d9ab0a6cadb
M	.planning/INGEST-CONFLICTS.md
M	.planning/REQUIREMENTS.md
M	.planning/ROADMAP.md
M	.planning/STATE.md
A	.planning/argonauts/r-d78495de-learnings.md
A	.planning/argonauts/r-d78495de-manifest.yaml
A	.planning/argonauts/r-d78495de-prd.md
A	.planning/argonauts/t_19c23e10/PLAN-CHECK.md
A	.planning/argonauts/t_19c23e10/api-coverage.json
A	.planning/argonauts/t_19c23e10/gap-analysis.json
A	.planning/argonauts/t_19c23e10/verify-command-paths.json
A	.planning/argonauts/t_19c23e10/verify-failure-directions.json
M	.planning/intel/SYNTHESIS.md
A	.planning/intel/classifications/brief-readme-min-count-3-065f1da5.json
A	.planning/intel/classifications/prd-readme-min-count-3-0ae126e9.json
A	.planning/intel/classifications/proposal-5fd092e7.json
A	.planning/intel/classifications/r-d78495de/brief-readme-min-count-3-065f1da5.json
A	.planning/intel/classifications/r-d78495de/prd-readme-min-count-3-0ae126e9.json
A	.planning/intel/classifications/r-d78495de/proposal-5fd092e7.json
A	.planning/intel/classifications/r-d78495de/tasks-a4097a09.json
A	.planning/intel/classifications/tasks-a4097a09.json
M	.planning/intel/constraints.md
M	.planning/intel/context.md
M	.planning/intel/decisions.md
M	.planning/intel/requirements.md
A	.planning/phases/08-readme-min-count-example/.gitkeep
A	.planning/phases/08-readme-min-count-example/08-01-PLAN.md
A	.planning/phases/08-readme-min-count-example/08-BUILDER-CLI.md
A	.planning/phases/08-readme-min-count-example/08-CONTEXT.md
A	.planning/phases/08-readme-min-count-example/08-PATTERNS.md
A	.planning/phases/08-readme-min-count-example/08-RESEARCH.md
A	.planning/phases/08-readme-min-count-example/08-VALIDATION.md
M	.planning/state.json
M	README.md
A	_bmad-output/initiative-r-d78495de/brief/.memlog.md
A	_bmad-output/initiative-r-d78495de/brief/.template.md
A	_bmad-output/initiative-r-d78495de/brief/brief-readme-min-count-3.html
A	_bmad-output/initiative-r-d78495de/brief/brief-readme-min-count-3.md
A	_bmad-output/initiative-r-d78495de/brief/review-fresh-reader.md
A	_bmad-output/initiative-r-d78495de/brief/review-prose.md
A	_bmad-output/initiative-r-d78495de/brief/review-reconciliation.md
A	_bmad-output/initiative-r-d78495de/brief/review-rubric.md
A	_bmad-output/initiative-r-d78495de/brief/review-structure.md
A	_bmad-output/initiative-r-d78495de/brief/review-update.md
A	_bmad-output/initiative-r-d78495de/initiative-r-d78495de.md
A	_bmad-output/initiative-r-d78495de/prd/.memlog.md
A	_bmad-output/initiative-r-d78495de/prd/.template.md
A	_bmad-output/initiative-r-d78495de/prd/prd-readme-min-count-3.md
A	_bmad-output/initiative-r-d78495de/prd/review-fresh-reader.md
A	_bmad-output/initiative-r-d78495de/prd/review-prose.md
A	_bmad-output/initiative-r-d78495de/prd/review-reconciliation.md
A	_bmad-output/initiative-r-d78495de/prd/review-rubric.md
A	_bmad-output/initiative-r-d78495de/prd/review-structure.md
A	_bmad-output/initiative-r-d78495de/prd/review-update.md
A	_bmad-output/initiative-r-d78495de/review-current.md
A	_bmad-output/initiative-r-d78495de/review-independent.md
A	openspec/changes/r-d78495de-readme-min-count/.openspec.yaml
A	openspec/changes/r-d78495de-readme-min-count/design.md
A	openspec/changes/r-d78495de-readme-min-count/proposal.md
A	openspec/changes/r-d78495de-readme-min-count/tasks.md
raw exit=0
$ git diff --no-ext-diff --no-textconv --no-relative --name-only cf407aaa6babebc0a21cf6370530d321b8a615e1...fc3d7362d6e88487222565a4c16d1d9ab0a6cadb
.planning/INGEST-CONFLICTS.md
.planning/REQUIREMENTS.md
.planning/ROADMAP.md
.planning/STATE.md
.planning/argonauts/r-d78495de-learnings.md
.planning/argonauts/r-d78495de-manifest.yaml
.planning/argonauts/r-d78495de-prd.md
.planning/argonauts/t_19c23e10/PLAN-CHECK.md
.planning/argonauts/t_19c23e10/api-coverage.json
.planning/argonauts/t_19c23e10/gap-analysis.json
.planning/argonauts/t_19c23e10/verify-command-paths.json
.planning/argonauts/t_19c23e10/verify-failure-directions.json
.planning/intel/SYNTHESIS.md
.planning/intel/classifications/brief-readme-min-count-3-065f1da5.json
.planning/intel/classifications/prd-readme-min-count-3-0ae126e9.json
.planning/intel/classifications/proposal-5fd092e7.json
.planning/intel/classifications/r-d78495de/brief-readme-min-count-3-065f1da5.json
.planning/intel/classifications/r-d78495de/prd-readme-min-count-3-0ae126e9.json
.planning/intel/classifications/r-d78495de/proposal-5fd092e7.json
.planning/intel/classifications/r-d78495de/tasks-a4097a09.json
.planning/intel/classifications/tasks-a4097a09.json
.planning/intel/constraints.md
.planning/intel/context.md
.planning/intel/decisions.md
.planning/intel/requirements.md
.planning/phases/08-readme-min-count-example/.gitkeep
.planning/phases/08-readme-min-count-example/08-01-PLAN.md
.planning/phases/08-readme-min-count-example/08-BUILDER-CLI.md
.planning/phases/08-readme-min-count-example/08-CONTEXT.md
.planning/phases/08-readme-min-count-example/08-PATTERNS.md
.planning/phases/08-readme-min-count-example/08-RESEARCH.md
.planning/phases/08-readme-min-count-example/08-VALIDATION.md
.planning/state.json
README.md
_bmad-output/initiative-r-d78495de/brief/.memlog.md
_bmad-output/initiative-r-d78495de/brief/.template.md
_bmad-output/initiative-r-d78495de/brief/brief-readme-min-count-3.html
_bmad-output/initiative-r-d78495de/brief/brief-readme-min-count-3.md
_bmad-output/initiative-r-d78495de/brief/review-fresh-reader.md
_bmad-output/initiative-r-d78495de/brief/review-prose.md
_bmad-output/initiative-r-d78495de/brief/review-reconciliation.md
_bmad-output/initiative-r-d78495de/brief/review-rubric.md
_bmad-output/initiative-r-d78495de/brief/review-structure.md
_bmad-output/initiative-r-d78495de/brief/review-update.md
_bmad-output/initiative-r-d78495de/initiative-r-d78495de.md
_bmad-output/initiative-r-d78495de/prd/.memlog.md
_bmad-output/initiative-r-d78495de/prd/.template.md
_bmad-output/initiative-r-d78495de/prd/prd-readme-min-count-3.md
_bmad-output/initiative-r-d78495de/prd/review-fresh-reader.md
_bmad-output/initiative-r-d78495de/prd/review-prose.md
_bmad-output/initiative-r-d78495de/prd/review-reconciliation.md
_bmad-output/initiative-r-d78495de/prd/review-rubric.md
_bmad-output/initiative-r-d78495de/prd/review-structure.md
_bmad-output/initiative-r-d78495de/prd/review-update.md
_bmad-output/initiative-r-d78495de/review-current.md
_bmad-output/initiative-r-d78495de/review-independent.md
openspec/changes/r-d78495de-readme-min-count/.openspec.yaml
openspec/changes/r-d78495de-readme-min-count/design.md
openspec/changes/r-d78495de-readme-min-count/proposal.md
openspec/changes/r-d78495de-readme-min-count/tasks.md
raw exit=0
$ git show cf407aaa6babebc0a21cf6370530d321b8a615e1:README.md
# argonauts-uat public

Argonauts v1.10 acceptance test repository.

## wordfreq の実行

リポジトリ直下で、UTF-8 の実ファイルを指定します。Python の標準ライブラリだけで動き、インストールや Web サーバーは不要です。

```sh
python -m wordfreq input.txt
python -m wordfreq input.txt --min-count 2 --top 1 --format json
python -m wordfreq input.txt --top 2 --format json
python -m wordfreq input.txt --format html
python -m wordfreq input.txt --format html > result.html
```

HTML はロケールや `PYTHONIOENCODING` に依存せず UTF-8 バイト列を標準出力へ書きます。保存時はバイト列をそのままリダイレクトしてください（シェル側で文字コードを変換しないでください）。ファイル名の表示は basename のバイト列を実行環境のファイルシステム文字コードで読み、その文字コードで復号できないバイトだけを置換文字 `�` にします。入力ファイルの読み込みに使うパス自体は変更しません。保存した `result.html` はローカルのブラウザで開けます。HTML は内包 CSS のみの静的文書で、スクリプト・外部フォント・画像・リンク・対話操作はありません。

- `--min-count N` は1以上の整数、既定は1。不正値・値欠落は入力読込み前に stderr と exit2 で知らせます。
- `--top N` は1以上の整数、既定は10。種類数が N 未満なら全件を表示します。
- `--format text|json|html` の既定は text。text は `<count>\t<word>\n`、JSON は `word` と整数 `count` の配列に末尾改行1つです。空入力は text が空、JSON が `[]` と改行、HTML が見出し3列・データ0行・総数0です。
- Unicode の単語文字の連続を抽出し、casefold した語を数えます。日本語の形態素解析は行いません。
- 全形式で min-count 未満を除外し、回数降順に並べ、同数時は**正規化後の初出順**を保ってから top を適用します。両値は独立で、指定順による違いはありません。これは以前の「同数は語の昇順」からの意図した互換性変更です。`Zoo apple APPLE zoo banana` は min-count2 で zoo2 / apple2、さらに top1 で zoo2 になります。全件除外されたら min-count を下げてください。
- HTML の表は順位・単語・回数で、順位は表示行の1始まり連番です。表の上にファイルの basename のみと **min-count / top 前の総出現回数**を表示します。総数は表示行の和や種類数ではありません。ディレクトリ情報は HTML に埋め込みません。ただし入力本文中の語と basename 自体は表示されるため、共有前に内容を確認してください。
- ファイル名と語はテキストとして一度だけ HTML escape し、属性・CSS・URL には使いません。明るい背景固定で、長い語・名前は連続空白・改行・タブを保持して折り返す設計です。
- 読込み・UTF-8 decode 失敗は stderr と exit1、不正 top・format・引数個数は stderr と exit2。エラー時は stdout を空にし、エラー用 HTML は出しません。

## 部品の契約と検証状況

`count_words` が正規化済みトークン列から作る Counter の挿入順は初出順です。`top_words(counts, n)` に直接渡す場合も、この挿入順を保つことが前提です。回数だけの安定ソート後に制限し、入力は変更しません。

`format_html(pairs, basename, total)` は渡された順序を保つ純粋な文字列整形部品です。呼出し側が basename と min-count / top 前の総数を渡します。整形部品は再読込み・集計・ソート・標準出力への書込みをしません。既存 text/json の部品の引数と形式は変更しません。

自動試験は集計・実CLI・HTMLParser、安全性、証拠欠落の拒否を検査します。[ブラウザ検証手順](docs/wordfreq-html-verification.md)に、通常幅1280×900と狭幅320×900 CSS px・DPR1での再生成、live review-session、全画像とrawRangeの実閲覧台帳、通信試行・head/scopeの再照合、finalize後の最終verdict確認を記載しています。品質担当は自分のfresh rootで対象headから独立再生成します。ツール完成やcapture成功は独立品質・phase受入の完了ではなく、そのgateは実行までpendingです。CSS・幾何・画像の存在だけで可読性や無通信の合格とはしません。
検証A: v1.12 の通しの確かめ（2026-11-22）

raw exit=0
$ git show fc3d7362d6e88487222565a4c16d1d9ab0a6cadb:README.md
# argonauts-uat public

Argonauts v1.10 acceptance test repository.

## wordfreq の実行

リポジトリ直下で、UTF-8 の実ファイルを指定します。Python の標準ライブラリだけで動き、インストールや Web サーバーは不要です。

```sh
python -m wordfreq input.txt
python -m wordfreq input.txt --min-count 3
python -m wordfreq input.txt --min-count 2 --top 1 --format json
python -m wordfreq input.txt --top 2 --format json
python -m wordfreq input.txt --format html
python -m wordfreq input.txt --format html > result.html
```

HTML はロケールや `PYTHONIOENCODING` に依存せず UTF-8 バイト列を標準出力へ書きます。保存時はバイト列をそのままリダイレクトしてください（シェル側で文字コードを変換しないでください）。ファイル名の表示は basename のバイト列を実行環境のファイルシステム文字コードで読み、その文字コードで復号できないバイトだけを置換文字 `�` にします。入力ファイルの読み込みに使うパス自体は変更しません。保存した `result.html` はローカルのブラウザで開けます。HTML は内包 CSS のみの静的文書で、スクリプト・外部フォント・画像・リンク・対話操作はありません。

- `--min-count N` は1以上の整数、既定は1。不正値・値欠落は入力読込み前に stderr と exit2 で知らせます。
- `--top N` は1以上の整数、既定は10。種類数が N 未満なら全件を表示します。
- `--format text|json|html` の既定は text。text は `<count>\t<word>\n`、JSON は `word` と整数 `count` の配列に末尾改行1つです。空入力は text が空、JSON が `[]` と改行、HTML が見出し3列・データ0行・総数0です。
- Unicode の単語文字の連続を抽出し、casefold した語を数えます。日本語の形態素解析は行いません。
- 全形式で min-count 未満を除外し、回数降順に並べ、同数時は**正規化後の初出順**を保ってから top を適用します。両値は独立で、指定順による違いはありません。これは以前の「同数は語の昇順」からの意図した互換性変更です。`Zoo apple APPLE zoo banana` は min-count2 で zoo2 / apple2、さらに top1 で zoo2 になります。全件除外されたら min-count を下げてください。
- HTML の表は順位・単語・回数で、順位は表示行の1始まり連番です。表の上にファイルの basename のみと **min-count / top 前の総出現回数**を表示します。総数は表示行の和や種類数ではありません。ディレクトリ情報は HTML に埋め込みません。ただし入力本文中の語と basename 自体は表示されるため、共有前に内容を確認してください。
- ファイル名と語はテキストとして一度だけ HTML escape し、属性・CSS・URL には使いません。明るい背景固定で、長い語・名前は連続空白・改行・タブを保持して折り返す設計です。
- 読込み・UTF-8 decode 失敗は stderr と exit1、不正 top・format・引数個数は stderr と exit2。エラー時は stdout を空にし、エラー用 HTML は出しません。

## 部品の契約と検証状況

`count_words` が正規化済みトークン列から作る Counter の挿入順は初出順です。`top_words(counts, n)` に直接渡す場合も、この挿入順を保つことが前提です。回数だけの安定ソート後に制限し、入力は変更しません。

`format_html(pairs, basename, total)` は渡された順序を保つ純粋な文字列整形部品です。呼出し側が basename と min-count / top 前の総数を渡します。整形部品は再読込み・集計・ソート・標準出力への書込みをしません。既存 text/json の部品の引数と形式は変更しません。

自動試験は集計・実CLI・HTMLParser、安全性、証拠欠落の拒否を検査します。[ブラウザ検証手順](docs/wordfreq-html-verification.md)に、通常幅1280×900と狭幅320×900 CSS px・DPR1での再生成、live review-session、全画像とrawRangeの実閲覧台帳、通信試行・head/scopeの再照合、finalize後の最終verdict確認を記載しています。品質担当は自分のfresh rootで対象headから独立再生成します。ツール完成やcapture成功は独立品質・phase受入の完了ではなく、そのgateは実行までpendingです。CSS・幾何・画像の存在だけで可読性や無通信の合格とはしません。
検証A: v1.12 の通しの確かめ（2026-11-22）

raw exit=0
$ git diff --no-ext-diff --no-textconv --unified=40 cf407aaa6babebc0a21cf6370530d321b8a615e1...fc3d7362d6e88487222565a4c16d1d9ab0a6cadb -- README.md
diff --git a/README.md b/README.md
index 0961498..55a5aba 100644
--- a/README.md
+++ b/README.md
@@ -1,35 +1,36 @@
 # argonauts-uat public
 
 Argonauts v1.10 acceptance test repository.
 
 ## wordfreq の実行
 
 リポジトリ直下で、UTF-8 の実ファイルを指定します。Python の標準ライブラリだけで動き、インストールや Web サーバーは不要です。
 
 ```sh
 python -m wordfreq input.txt
+python -m wordfreq input.txt --min-count 3
 python -m wordfreq input.txt --min-count 2 --top 1 --format json
 python -m wordfreq input.txt --top 2 --format json
 python -m wordfreq input.txt --format html
 python -m wordfreq input.txt --format html > result.html
 ```
 
 HTML はロケールや `PYTHONIOENCODING` に依存せず UTF-8 バイト列を標準出力へ書きます。保存時はバイト列をそのままリダイレクトしてください（シェル側で文字コードを変換しないでください）。ファイル名の表示は basename のバイト列を実行環境のファイルシステム文字コードで読み、その文字コードで復号できないバイトだけを置換文字 `�` にします。入力ファイルの読み込みに使うパス自体は変更しません。保存した `result.html` はローカルのブラウザで開けます。HTML は内包 CSS のみの静的文書で、スクリプト・外部フォント・画像・リンク・対話操作はありません。
 
 - `--min-count N` は1以上の整数、既定は1。不正値・値欠落は入力読込み前に stderr と exit2 で知らせます。
 - `--top N` は1以上の整数、既定は10。種類数が N 未満なら全件を表示します。
 - `--format text|json|html` の既定は text。text は `<count>\t<word>\n`、JSON は `word` と整数 `count` の配列に末尾改行1つです。空入力は text が空、JSON が `[]` と改行、HTML が見出し3列・データ0行・総数0です。
 - Unicode の単語文字の連続を抽出し、casefold した語を数えます。日本語の形態素解析は行いません。
 - 全形式で min-count 未満を除外し、回数降順に並べ、同数時は**正規化後の初出順**を保ってから top を適用します。両値は独立で、指定順による違いはありません。これは以前の「同数は語の昇順」からの意図した互換性変更です。`Zoo apple APPLE zoo banana` は min-count2 で zoo2 / apple2、さらに top1 で zoo2 になります。全件除外されたら min-count を下げてください。
 - HTML の表は順位・単語・回数で、順位は表示行の1始まり連番です。表の上にファイルの basename のみと **min-count / top 前の総出現回数**を表示します。総数は表示行の和や種類数ではありません。ディレクトリ情報は HTML に埋め込みません。ただし入力本文中の語と basename 自体は表示されるため、共有前に内容を確認してください。
 - ファイル名と語はテキストとして一度だけ HTML escape し、属性・CSS・URL には使いません。明るい背景固定で、長い語・名前は連続空白・改行・タブを保持して折り返す設計です。
 - 読込み・UTF-8 decode 失敗は stderr と exit1、不正 top・format・引数個数は stderr と exit2。エラー時は stdout を空にし、エラー用 HTML は出しません。
 
 ## 部品の契約と検証状況
 
 `count_words` が正規化済みトークン列から作る Counter の挿入順は初出順です。`top_words(counts, n)` に直接渡す場合も、この挿入順を保つことが前提です。回数だけの安定ソート後に制限し、入力は変更しません。
 
 `format_html(pairs, basename, total)` は渡された順序を保つ純粋な文字列整形部品です。呼出し側が basename と min-count / top 前の総数を渡します。整形部品は再読込み・集計・ソート・標準出力への書込みをしません。既存 text/json の部品の引数と形式は変更しません。
 
 自動試験は集計・実CLI・HTMLParser、安全性、証拠欠落の拒否を検査します。[ブラウザ検証手順](docs/wordfreq-html-verification.md)に、通常幅1280×900と狭幅320×900 CSS px・DPR1での再生成、live review-session、全画像とrawRangeの実閲覧台帳、通信試行・head/scopeの再照合、finalize後の最終verdict確認を記載しています。品質担当は自分のfresh rootで対象headから独立再生成します。ツール完成やcapture成功は独立品質・phase受入の完了ではなく、そのgateは実行までpendingです。CSS・幾何・画像の存在だけで可読性や無通信の合格とはしません。
 検証A: v1.12 の通しの確かめ（2026-11-22）
raw exit=0
$ git status --short
 M .planning/STATE.md
 M .planning/phases/08-readme-min-count-example/08-BUILDER-CLI.md
 M .planning/state.json
raw exit=0
$ git diff --name-status
M	.planning/STATE.md
M	.planning/phases/08-readme-min-count-example/08-BUILDER-CLI.md
M	.planning/state.json
raw exit=0
$ git diff --cached --name-status
raw exit=0
$ git ls-files --others --exclude-standard
raw exit=0
```
