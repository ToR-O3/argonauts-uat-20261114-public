---
phase: 01-wordfreq-cli
verified: 2026-11-17T04:21:00Z
status: gaps_found
score: 4/5 must-haves verified
covered_files:
  - ".planning/phases/01-wordfreq-cli/01-01-PLAN.md"
  - ".planning/phases/01-wordfreq-cli/01-01-SUMMARY.md"
  - ".planning/phases/01-wordfreq-cli/01-02-PLAN.md"
  - ".planning/phases/01-wordfreq-cli/01-02-SUMMARY.md"
  - ".planning/phases/01-wordfreq-cli/01-03-PLAN.md"
  - ".planning/phases/01-wordfreq-cli/01-03-SUMMARY.md"
  - ".planning/phases/01-wordfreq-cli/01-04-PLAN.md"
  - ".planning/phases/01-wordfreq-cli/01-04-SUMMARY.md"
  - "pyproject.toml"
  - "tests/test_aggregator.py"
  - "tests/test_cli.py"
  - "tests/test_formatters.py"
  - "tests/test_sources.py"
  - "tests/test_sources_boundary.py"
  - "tests/test_tokenizer.py"
  - "wordfreq/__init__.py"
  - "wordfreq/__main__.py"
  - "wordfreq/aggregator.py"
  - "wordfreq/formatters.py"
  - "wordfreq/sources.py"
  - "wordfreq/tokenizer.py"
covered_digest: "v4:sha256:a7d65e57dd9985af73c5bb3e09c1468ac8712b0acebc593771e02b9e535957b0"
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "pytest 試験一式（全 FR のエッジケース含む）がリポジトリ CI の pytest ジョブで通る（ROADMAP Success Criterion 5 / REQ-07 / OpenSpec Scenario「CI で pytest が通る」）"
    status: failed
    reason: "リポジトリに CI の pytest ジョブが存在しない。`gh api repos/ToR-O3/argonauts-uat-20261114-public/actions/workflows` は total_count=0、`git ls-files .github` は空。対象 head 0cd4673bb75d78e465aa84c8dd31e8ff810a44b8 の CI 成功証拠が無い。ローカル `python -m pytest` 43 passed（exit 0）は CI 成功の代替にならない。REQUIREMENTS.md でも REQ-07 は Pending。"
    artifacts:
      - path: ".github/workflows/"
        issue: "存在しない（pytest を実行する CI workflow / job が未定義）。workflow 変更は Bot 権限外"
      - path: ".planning/phases/01-wordfreq-cli/01-USER-SETUP.md"
        issue: "人の対応チェックリストが Status: Incomplete のまま"
    missing:
      - "人が対象 CPython 3 の版を確定し、依頼branch argonauts/r-5a3b8a3f に `python -m pytest` を実行する CI workflow（例: .github/workflows/）の pytest job を 1 本追加する"
      - "対象 head での CI run 成功（failed 0・exit 0、skipped 不可）の証拠: run・job 名・head SHA・Python 版・ログ"
---

# Phase 1: wordfreq CLI 検証報告

**Phase Goal:** ユーザーは `python -m wordfreq <file>` で、決定論的な並び順と出力形式、exit code 規約を持つ単語頻度集計を stdlib-only の CLI として実行できる
**Verified:** 2026-11-17T04:21:00Z
**Status:** gaps_found
**Re-verification:** No — 初回検証（既存 VERIFICATION.md なし）
**対象 HEAD:** `0cd4673bb75d78e465aa84c8dd31e8ff810a44b8`（worktree `wt/t_3dc4a405`、追跡ファイルの未コミット変更なし）

## Goal Achievement

### Observable Truths

ROADMAP Success Criteria 1〜5 を契約とし、各 PLAN の must_haves.truths は該当 SC の詳細として統合した（範囲は縮小していない）。

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `python -m wordfreq <file>` が回数降順（同数は正規化後単語昇順）で表示、`--top N`（既定 10、1 以上）で件数変更、N 未満なら全件 | ✓ VERIFIED | `aggregator.top_words` は `sorted(..., key=(-count, word))[:n]`（most_common 不使用）。実行: tie.txt → `5 apple / 5 zoo / 1 b` exit 0。tests/test_cli.py `test_default_text_normalizes_sorts_and_limits_to_ten`・`test_top_three_*`・`test_top_one_is_smallest_allowed_limit`・`test_top_three_outputs_all_when_fewer_words_exist`、test_aggregator.py の apple/zoo 試験が全スイート中で passed |
| 2 | `--format text|json`。text は `<count>\t<word>` 1 語 1 行、json は `{"word","count"}` 配列で `json.loads` 可読、0 件は json `[]` / text 出力なし | ✓ VERIFIED | `formatters.format_text`/`format_json`（ensure_ascii=True + `\n`）。実行: case.txt json → `[{"word": "hello", "count": 3}, {"word": "world", "count": 2}]`、empty.txt json → `[]` exit 0。test_formatters.py 4 件・test_cli.py `test_json_is_machine_readable_*`・`test_empty_file_is_success`（text/json）passed |
| 3 | 異常系: 不存在・開けない・UTF-8 失敗 → stderr + exit 1、引数個数・`--top`・`--format` 不正 → stderr + exit 2、空ファイル exit 0、出力は決定論的 | ✓ VERIFIED | `__main__.main` が `InputError` のみ捕捉して exit 1、`args.top < 1` は `parser.error`（exit 2）。実行: bad.txt exit 1・stdout 0 bytes・stderr 1 行、不存在 exit 1、`--top 0` / `--format xml` / ファイル 2 個 exit 2。PYTHONHASHSEED=1 と 777 で README.md 出力 md5 一致（`aa4e705e…`）。test_cli.py の exit code 系 12 件 passed |
| 4 | tokenizer / aggregator / sources / formatters が部品分離され、各部品の単体試験と、集計経路が `TextSource` 境界を介してのみテキストを受け取る境界越し試験が存在。入力元拡張の構成判断が design.md に記録済み | ✓ VERIFIED | 4 モジュールは互いを import せず `__main__` のみが合成（`from .aggregator/.formatters/.sources/.tokenizer`）。`sources.TextSource(Protocol)`・`FileSource`・`InputError`。test_sources_boundary.py（spy で calls==[]、FakeSource 二重化、境界通過 1 回）3 件 passed。design.md D-A/D-B に StdinSource・URL を `sources.py` の実装追加で足す判断を記録（注: ROADMAP SC4 本文の「足りないことが」は REQUIREMENTS REQ-06「足りる」の誤記と判断し、REQ-06 の文言で判定） |
| 5 | pytest 試験一式がリポジトリ CI の pytest ジョブで通り、ランタイム依存は標準ライブラリのみ | ✗ FAILED | 後半（stdlib-only）は充足: `pyproject.toml` `dependencies = []`、pytest は `dev` extra のみ、wordfreq/ の import は argparse/sys/json/re/collections/typing のみ。前半（CI）は未充足: Actions workflows total_count=0、`git ls-files .github` 空、CI run 証拠なし。ローカル 43 passed は CI 成功ではない |

**Score:** 4/5 truths verified（0 present, behavior-unverified）

### Required Artifacts

`gsd-tools query verify.artifacts` は 4 PLAN とも `total: 0`（artifacts が `{path, provides}` 形でなく文字列配列のため検査器が項目を認識しない）を返したため、手動で 3 レベル確認した。

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `wordfreq/__init__.py` | パッケージマーカー | ✓ VERIFIED | docstring のみ（意図どおり） |
| `wordfreq/tokenizer.py` | `\w+` 抽出 + casefold、注入点 | ✓ VERIFIED | 18 行。`_WORD_RE`・`default_tokenizer`・`iter_tokens(tokenizer=...)`。`__main__` から使用 |
| `wordfreq/aggregator.py` | count_words / top_words | ✓ VERIFIED | Counter + 決定論ソート。`__main__`・境界試験から使用 |
| `wordfreq/sources.py` | InputError / TextSource / FileSource | ✓ VERIFIED | `(OSError, UnicodeDecodeError)` → `InputError`。`__main__` から使用 |
| `wordfreq/formatters.py` | format_text / format_json | ✓ VERIFIED | 純関数。`__main__` から使用 |
| `wordfreq/__main__.py` | argparse + 合成 + exit 0/1/2 | ✓ VERIFIED | 実 CLI 実行で全分岐確認 |
| `pyproject.toml` | 最小形・依存ゼロ | ✓ VERIFIED | setuptools、`dependencies = []`、`dev = ["pytest"]` |
| `tests/test_*.py`（6 本） | 部品単体・境界越し・CLI 試験 | ✓ VERIFIED | 43 件 collected / passed |
| `.planning/phases/01-wordfreq-cli/01-CI-GAP.md` | CI 実測・block 判定記録 | ✓ VERIFIED | 4 項目（実測・ローカル証拠・block 判定・人への依頼）を記載 |
| `.github/workflows/`（CI pytest job） | REQ-07 の CI 実行 | ✗ MISSING | 未作成（Bot 権限外、人の対応待ち） |

### Key Link Verification

`gsd-tools query verify.key-links` は全リンクで「Target not referenced in source」を返した。これは検査器がファイルパス文字列（例 `wordfreq/tokenizer.py`）をソース内に探すためで、Python の import 表記（`from .tokenizer`／`from wordfreq.tokenizer`）を照合できない。実ソースで手動確認した結果:

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| tests/test_tokenizer.py | wordfreq/tokenizer.py | import | ✓ WIRED | `from wordfreq.tokenizer import iter_tokens` 等、6 試験 passed |
| tests/test_sources.py | wordfreq/sources.py | FileSource / InputError | ✓ WIRED | `from wordfreq.sources import FileSource, InputError` |
| wordfreq/formatters.py | wordfreq/aggregator.py | pairs 型契約 | ✓ WIRED | `__main__` で `top_words(...)` の戻り値を `format_*` に直接渡す |
| wordfreq/__main__.py | wordfreq/sources.py | `FileSource(args.filename).read_text()` → exit 1 | ✓ WIRED | 25〜28 行 |
| wordfreq/__main__.py | wordfreq/tokenizer.py | `top_words(count_words(iter_tokens(text)), args.top)` | ✓ WIRED | 29 行 |
| wordfreq/__main__.py | wordfreq/formatters.py | `sys.stdout.write(format_json/format_text)` | ✓ WIRED | 30〜31 行 |
| 01-CI-GAP.md | tests/ | ローカル全スイート結果 | ✓ WIRED | 43 passed・内訳を記載 |
| tests/（pytest） | リポジトリ CI | CI pytest job | ✗ NOT_WIRED | CI workflow 不在 |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `__main__.main` stdout | `pairs` → `output` | `FileSource(args.filename).read_text()`（実ファイル） | Yes（入力ごとに異なる集計を実測） | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 全試験スイート（1 回のみ実行） | `python -m pytest -q -p no:cacheprovider` | 43 passed in 0.98s, exit 0（Python 3.14.9） | ✓ PASS |
| 同数タイブレーク | `python -m wordfreq tie.txt` | `5 apple / 5 zoo / 1 b`, exit 0 | ✓ PASS |
| casefold + json | `python -m wordfreq --format json case.txt` | `[{"word": "hello", "count": 3}, {"word": "world", "count": 2}]`, exit 0 | ✓ PASS |
| 空ファイル json | `python -m wordfreq --format json empty.txt` | `[]`, exit 0 | ✓ PASS |
| UTF-8 デコード失敗 | `python -m wordfreq bad.txt` | exit 1, stdout 0 bytes, stderr 1 行 | ✓ PASS |
| 不存在ファイル | `python -m wordfreq nope.txt` | exit 1 | ✓ PASS |
| 使い方エラー | `--top 0` / `--format xml` / ファイル 2 個 | exit 2 / 2 / 2 | ✓ PASS |
| 決定論 | PYTHONHASHSEED=1 と 777 で `python -m wordfreq README.md` | md5 一致 | ✓ PASS |
| CI pytest job の存在 | `gh api .../actions/workflows --jq '{total_count}'`、`git ls-files .github` | `{"total_count":0}`、出力なし | ✗ FAIL |

品質担当の独立証拠（`.planning/argonauts/t_3dc4a405/cli-evidence.md`・`openspec-verify.md`）とも全項目で一致した。

### Probe Execution

| Probe | Command | Result | Status |
|-------|---------|--------|--------|
| — | — | PLAN/SUMMARY に probe 宣言なし、`scripts/*/tests/probe-*.sh` なし | 該当なし |

### Requirements Coverage

PLAN frontmatter の requirements 和集合は REQ-01〜REQ-08 の 8 件で、REQUIREMENTS.md の Phase 1 割当 8 件と一致（ORPHANED なし）。

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| REQ-01 | 01-02, 01-03 | ファイル 1 個・UTF-8 読み、exit 1/2、空ファイル exit 0 | ✓ SATISFIED | Truth 1・3、test_sources.py・test_cli.py、実 CLI |
| REQ-02 | 01-03 | `--top N` 既定 10・1 以上・N 未満は全件 | ✓ SATISFIED | Truth 1・3 |
| REQ-03 | 01-02, 01-03 | `--format text|json`、0 件時の出力、不正は exit 2 | ✓ SATISFIED | Truth 2・3 |
| REQ-04 | 01-02 | 回数降順・同数は単語昇順・決定論 | ✓ SATISFIED | Truth 1・3、PYTHONHASHSEED 比較 |
| REQ-05 | 01-01, 01-02 | 切り出し・正規化と集計・整形の部品分離、単体試験 | ✓ SATISFIED | Truth 4、test_tokenizer.py 6 件ほか |
| REQ-06 | 01-02, 01-03 | 入力取得境界と境界越し試験、design.md 記録 | ✓ SATISFIED | Truth 4、test_sources_boundary.py、design.md D-B |
| REQ-07 | 01-01, 01-03, 01-04 | pytest 試験が**リポジトリ CI の pytest ジョブで通る** | ✗ BLOCKED | 試験内容・ローカル緑は充足だが CI job 不在・CI 成功証拠なし。REQUIREMENTS.md も Pending。01-04-SUMMARY の `requirements-completed: [REQ-07]` は転記であり達成宣言ではないと同 SUMMARY 自身が明記 |
| REQ-08 | 01-03 | ランタイム依存は stdlib のみ、pyproject 最小 | ✓ SATISFIED | `dependencies = []`、import 走査で非 stdlib なし |

### Prohibitions（must_haves.prohibitions、judgment tier・flagged）

自律検証のため以下は **非権威の LLM 判定** であり、`unverified-prohibition — human review recommended` として記録する（gaps_found のため status に影響しない）。

| Plan | Prohibition | LLM 判定（非権威） | 根拠 |
|------|-------------|--------------------|------|
| 01-01 | トークン列・順序がハッシュ乱数化や挿入順で変わらない | 違反なし | 正規表現 findall の入力順、ソートは明示キー。PYTHONHASHSEED 1/777 で出力一致 |
| 01-02 | 入力取得・出力整形がファイルを新規作成・変更しない | 違反なし | `open(..., "r")` のみ、formatters は文字列を返すだけ。test_cli.py 読み取り専用試験 passed、実行後の `git status` に追跡変更なし |
| 01-03 | stdout に結果以外（ログ・traceback 等）を流さない | 違反なし | エラーは `print(..., file=sys.stderr)` と argparse の stderr。bad.txt 実行で stdout 0 bytes |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| wordfreq/・tests/・pyproject.toml | — | TBD/FIXME/XXX/TODO/HACK/placeholder | — | 該当なし |
| tests/test_cli.py | 152〜180 | 読み取り専用回帰試験が継承 `GIT_*`（`GIT_INDEX_FILE` 等）とグローバル Git 設定を隔離しない | ⚠️ Warning | 特定の Git 環境下で試験が誤動作し得る。ゴール達成は妨げない（01-03 品質からの持越し） |
| （観察） | — | 非 UTF-8 stdout（例 `LANG=C` で日本語出力）時の挙動が未観察 | ℹ️ Info | spec 範囲外の環境依存。ゴール外 |
| .planning/ROADMAP.md | 27 | SC4 の「足りないことが」は REQ-06「足りる」と矛盾する誤記と見られる | ℹ️ Info | 判定は REQ-06 の文言で実施 |

### Human Verification Required

なし（CI 部分は自動で不在を確認できたため human_needed ではなく gap として扱う）。

### Deferred Items

なし（ROADMAP は Phase 1 のみで、後続 phase に CI を扱う項目がない）。

### Gaps Summary

実装（CLI・部品分離・入力境界・決定論出力・exit code 規約・stdlib-only）は実コードと実行で確認でき、ローカルの pytest 43 件もすべて通った。未達は 1 点のみ: **REQ-07 / Success Criterion 5 の「リポジトリ CI の pytest ジョブで通る」**。リポジトリに CI workflow が 1 本も無く（Actions total_count=0、`.github` 未追跡）、対象 head の CI 成功証拠が存在しない。workflow 追加は Bot 権限外のため、人が 01-USER-SETUP.md に従って pytest job を追加し、依頼branch の対象 head で成功 run を得たうえで再検証する必要がある。コード修正では解消しない、人の対応が必要な gap である。

---

_Verified: 2026-11-17T04:21:00Z_
_Verifier: Claude (gsd-verifier)_
