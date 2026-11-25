---
phase: 07-wordfreq-max-count
verified: 2026-11-25T14:11:21Z
status: passed
score: 10/10 must-haves verified
covered_files:
  - ".planning/argonauts/r-d4bcda40/quality/final-01/manifest.json"
  - ".planning/argonauts/r-d4bcda40/quality/final-01/suite.json"
  - ".planning/phases/07-wordfreq-max-count/07-01-PLAN.md"
  - ".planning/phases/07-wordfreq-max-count/07-01-SUMMARY.md"
  - ".planning/phases/07-wordfreq-max-count/07-02-PLAN.md"
  - ".planning/phases/07-wordfreq-max-count/07-02-SUMMARY.md"
  - ".planning/phases/07-wordfreq-max-count/07-03-PLAN.md"
  - ".planning/phases/07-wordfreq-max-count/07-03-SUMMARY.md"
  - "README.md"
  - "docs/wordfreq-max-count-verification.md"
  - "tests/test_cli.py"
  - "tests/test_max_count_verifier.py"
  - "tools/verify_wordfreq_max_count.py"
  - "wordfreq/__main__.py"
covered_digest: "v4:sha256:84509774a77a17e32ba67e7318aea083783a2ff5cb7bf5269905c418c9909f4f"
behavior_unverified: 0
overrides_applied: 0
---

# Phase 7: wordfreq max-count Verification Report

**Phase Goal:** 承認済み依頼r-d4bcda40の整数--max-countを全3形式へ追加し、包含上限とminの積集合をtop前に適用する。省略互換・元Counter/HTML総数・安全性を保ち、追加/既存試験と独立CLI/HTML検証の読める証拠で全受入条件を追跡できる。
**Verified:** 2026-11-25T14:11:21Z (target head b4e9037892f01582554a96df2389c9e0458d7c35)
**Status:** passed
**Re-verification:** No — initial verification

## Requester decision applied (scope of acceptance)

依頼者判断（2026-11-25 21:22 JST、t_87068596、human `default`）:「この依頼の受入条件に、画面の画像の比較は入っていません。…変更前後の画像の取得と比較は省いてください。html の出力は、試験で中身（出す単語と回数）を確かめれば足ります。ほかの受入条件と品質の独立した確認はそのままにしてください。」

この判断はPLAN/UI-SPEC/REQ-27/ROADMAP SC5のブラウザ画像・画像閲覧・raw Range/幾何・通信観測・canaryの文言より優先する。これらは **受入対象外（N/A by decision）・未実施** として記録し、合格扱いにも gap / human_verification にもしない（下表「N/A by requester decision」）。score の分母からも除外した。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| - | ----- | ------ | -------- |
| 1 | SC1 / E01-E03,E05,E06: `--max-count` は type=int・省略None、0/負数/+2/02/±10**100/`=-1` を正確なintで受理。両端包含、min併用、指定順独立、Unicode合算、同数初出順、選択後11種類以上で既定top10/明示3/99が全3形式で固定期待値と一致 | ✓ VERIFIED | `wordfreq/__main__.py:18` `add_argument("--max-count", type=int, default=None)`; L37-39 `count >= min AND (max is None or count <= max)`. tests/test_cli.py `test_max_count_parser`(L837), `_parser_equals_negative`, `_help`, `_selection`(L858-886: max2/max1/min2max2/min2max3/max2top1/zoo3元12/Straße・日本語/Zoo apple tie/zoo-apple 5回初出順/eligible12種類top省略10・3・99, reverse順×3形式)。本検証で `-k "max_count and not discrimination"` 277 passed exit0 |
| 2 | SC2 / E07,E08 / 07-02 truth: 正常入力のmax0/負数/min>max/全除外/空/抽出0語はexit0既存空形式。有効maxでmissing/directory/decode/permissionはexit1（入力取得を短絡しない）。max欠落/abc/1.5とmin0/top0併用は入力取得前exit2・stdout空・stderr通知・Tracebackなし | ✓ VERIFIED | `test_max_count_empty`(L889-908)、`test_max_count_input_failure`(L941-965, permissionは実PermissionErrorを先にassert・finally復元)、`test_max_count_invalid_before_read`(L911-938, read_text spy未呼出し＋実subprocess)。ソース順序: parse/検証(L25-29)→read(L31)→選択(L37)でmin/max関係エラーなし。品質直接CLI: missing/directory exit1、abc/1.5/欠落 exit2（不存在ファイルでも）、min0/top0併用 exit2 |
| 3 | SC3 / E09,E10 / spy truth: 元Counterと元total（HTML総数）はmin/max/top前、topへはmin/max適用済みの別Counter、全formatterへ同一pairs。三条件min2/max3/top1でzoo3・元総数12 | ✓ VERIFIED | L35 counts→L36 `total = sum(counts.values())`→L37-39 別Counter→L40 `top_words(selected_counts, args.top)`→L46/48/50 同じ`pairs`。`test_max_count_internal_order`(L968-1000): top入力 `is not original`・項目順[(zoo,3),(apple,2),(pear,2)]、formatter `pairs is selected[0]`、HTML metadata ("input.txt",12)、元Counter値/順序不変。品質capture `triple-html/stdout.html` に `total-value 12`・`zoo` のみ |
| 4 | E04: 空/空白/記号入力と単語1つで有効maxの空/1行を区別、text空/json `[]`+LF/html0行・固定空文言・元total0（または正total） | ✓ VERIFIED | `test_max_count_empty` パラメータ ("one",1,0,1)/("",1,2,0)/(" \t\r\n",…,0)/("!?,.;: --",…,0)/全除外 total5、HTML `td`0件・空文言完全一致・`assert_static_document`; `test_max_count_selection` ("one",1,1,3)→1行 |
| 5 | 省略互換: 製品変更前に封印したoracleと、max省略/10**100/明示min1の全形式stdout/stderr/exitがバイト一致 | ✓ VERIFIED | `.planning/argonauts/r-d4bcda40/baseline/index.json`（verify.artifacts passed）; `test_max_count_saved_bytes` 39 case × {省略, `--max-count 10**100`, `--min-count 1`} を保存bytesと照合（L1017-1029）、変更後同士比較で代替していない |
| 6 | E11: 既存stateless read-only一回CLIを保持（入力/作業面へ書かない） | ✓ VERIFIED | `test_max_count_read_only`(L1032-1056): cold git copyでmax2全形式後の入力bytes・ディレクトリ・`git status --porcelain` 不変 |
| 7 | SC4 / E12: 先行RED→最小GREEN、追加と全既存pytestが実件数>0・失敗0・exit0。依存/CI/無関係製品変更なし | ✓ VERIFIED | builder/07-01/red/result.json: 製品編集前 276 tests / 213 failures / exit1; green 276/0/exit0; mutations 7/0。品質full suite at b4e9037 (`quality/final-01/suite.json`): tests 1048, failures 0, errors 0, skipped 0, exit 0。CI pytest at b4e9037: Actions 45626948539 (pull_request) / 45626937818 (push) success（品質提供の記録）。`git diff --stat 8efbfaa HEAD`: 製品は `wordfreq/__main__.py` +3/-1 のみ、他は README/tests/tools/docs。pyproject/.github/他wordfreqモジュール無変更 |
| 8 | SC4 / E14,E15 (REQ-28): README に指定例1つ（入力・期待JSON付き）と整数全域/省略上限なし/包含/min併用/0負数逆転は正常空/max調整/HTML総数はmin/max/top前を説明。実CLIでexit0・stdout固定JSON+LF・stderr空 | ✓ VERIFIED | README.md L22,26,27,36-48,55; 末尾「検証B」行維持。`test_max_count_readme_example`(L1171-) が出現1回・入力・期待・説明文言・旧例保持をassertし実subprocessを実行（277 passed内）。品質の一時cwd実行: exit0、stdout `[{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]`+LF、stderr空 |
| 9 | HTML出力の内容契約（UI05-09, UI11 と UI02/04/12/14 の全文保持側）: 共通pairsを既存3列/1始まり連番/basename/元totalで表示、0/1/多行で同一構造、空は固定文言、loading/補足UIなし、長語/長basename/CR全文保持・静的（script/外部参照なし） | ✓ VERIFIED | `assert_output_bytes`(html)＋`test_max_count_empty`の`assert_static_document`; `formatters`無変更（diffに含まれず）; 品質capture HTML46件（long/large-long/cr/hostile/unicode/empty等）は manifest のliteral pairs/total と一致と品質報告、本検証でも triple-html に script/http 0件を確認 |
| 10 | SC5 / E13 (REQ-27 の残る範囲): 品質が対象headで独立にCLI/HTML内容を再生成し、入力/argv/exit/stdout/stderr/HTML原本をAC/REQへ追跡可能 | ✓ VERIFIED | `quality/final-01/manifest.json`: head b4e9037…、provenance profile `argonauts-uat-quality` / role `quality`、cases 138（各 input/argv/stdout.bin/stderr.bin、HTMLは stdout.html）、`ac_index`あり、`browser: "not run: t_87068596/default/1795609328"`, images 0, synthetic false。max2-text stdout `2 alpha / 1 gamma / 1 delta`、triple-json `[{"word": "zoo", "count": 3}]` を本検証で読取り確認 |

**Score:** 10/10 truths verified (0 present, behavior-unverified)

### N/A by requester decision (not performed, not counted as passed)

| Item | Source | Disposition |
| ---- | ------ | ----------- |
| 変更前/変更後HTMLの1280×900・320×900 DPR1ブラウザ画像の取得・比較・全画像実閲覧、閲覧枚数台帳 | 07-01 truth1（画像部分）, 07-03 品質truth, REQ-27, ROADMAP SC5, REQ-26「見た目」 | 未実施。依頼者判断で受入対象外。capture manifest `images: 0`, browser "not run" |
| UI01/02/03/04/10/12/13/14 の幾何（横収まり・clip・非重複・raw Range） | 07-03 must_haves | 未実施（N/A）。内容側（全文保持）はTruth 9で検証 |
| 通信観測・canary（外部試行/failed/navigation/popup） | 07-03 must_haves, T-07-08 | 未実施（N/A）。HTMLが静的で外部参照を含まないことは自動試験で確認 |
| key link `tools/verify_wordfreq_max_count.py → tools/verify_wordfreq_html.py`（ブラウザ汎用機構の利用） | 07-01/07-03 key_links | ブラウザ経路を削除した判断に従い未配線は意図どおり（N/A）。maxツールは stdlib＋HTMLParser で内容検証 |

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `wordfreq/__main__.py` | `--max-count` 登録と包含AND共通選択のみ | ✓ VERIFIED | verify.artifacts passed; diff +3/-1 |
| `tests/test_cli.py` | max_count 追加群 | ✓ VERIFIED | tracer/parser/help/selection/empty/invalid_before_read/input_failure/internal_order/hashseed/saved_bytes/read_only/discrimination/empty_exit_discrimination/readme_example |
| `tests/test_max_count_verifier.py` | browser_free/saved_*/evidence_contract/scope_contract | ✓ VERIFIED | exists, passed; full suite内で成功 |
| `tools/verify_wordfreq_max_count.py` | baseline/capture/review-session/finalize/validate | ✓ VERIFIED | exists; 品質 final-01 capture を生成 |
| `docs/wordfreq-max-count-verification.md` | 独立品質手順 | ✓ VERIFIED | exists; verify.key-links: test→docs, docs→tool verified |
| `README.md` | 指定例1つと関連説明 | ✓ VERIFIED | readme_example test |
| `.planning/argonauts/r-d4bcda40/baseline/index.json` | 変更前oracle | ✓ VERIFIED | saved_bytes 39 case |

`gsd_run query verify.artifacts`: 07-01 5/5, 07-02 2/2, 07-03 3/3 all_passed (exit 0).

### Key Link Verification

`verify.key-links` は字句参照のみを見るため 07-01 0/3, 07-02 1/3, 07-03 2/3（exit1）。手動確認:

| From | To | Via | Status | Details |
| ---- | -- | --- | ------ | ------- |
| wordfreq/__main__.py | wordfreq/aggregator.py | counts→total→AND別Counter→top_words | ✓ WIRED | L7 `from .aggregator import count_words, top_words`（相対importのためCLIは未検出）; L35-40 |
| tests/test_cli.py | baseline/index.json | saved bytes | ✓ WIRED | L1019 `ROOT / ".planning/argonauts/r-d4bcda40/baseline"` |
| tests/test_cli.py | wordfreq/sources.py | read_text spy | ✓ WIRED | L921-928 `monkeypatch.setattr(FileSource, "read_text", spy)` |
| tests/test_cli.py | README.md | 固定assert＋実subprocess | ✓ WIRED | CLI verified |
| docs → tool, test_max_count_verifier → docs | | | ✓ WIRED | CLI verified |
| tools/verify_wordfreq_max_count.py | tools/verify_wordfreq_html.py | browser汎用機構 | N/A by decision | 上表参照 |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| `__main__.main` → formatters | `pairs` | FileSource.read_text→iter_tokens→count_words→選択Counter→top_words | Yes（実CLI出力で確認） | ✓ FLOWING |
| `format_html` total | `total` | `sum(counts.values())`（選択前） | Yes（triple 12、通常7） | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| max_count 追加群（変異判別を除く） | `env PYTHONPATH=… /usr/bin/python3 -m pytest tests/test_cli.py -k "max_count and not discrimination" -q -p no:cacheprovider` | 277 passed, exit 0, 10.01s | ✓ PASS |
| 全suite（品質実行・再実行せず読取り） | `quality/final-01/suite.json` | 1048 tests, 0 failures/errors/skipped, exit0, head b4e9037 | ✓ PASS |
| 独立CLI max2 text | `quality/final-01/max2-text/stdout.bin` | `2\talpha\n1\tgamma\n1\tdelta` | ✓ PASS |
| 三条件 json/html | `triple-json/stdout.bin`, `triple-html/stdout.html` | `[{"word": "zoo", "count": 3}]`; html total 12, zoo のみ, script/http 0 | ✓ PASS |

### Probe Execution

| Probe | Command | Result | Status |
| ----- | ------- | ------ | ------ |
| — | — | phaseに `probe-*.sh` 宣言なし | SKIPPED (none declared) |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ----------- | ----------- | ------ | -------- |
| REQ-23 | 07-01,02,03 | type=int/省略None、0/負/+2/02/大整数受理、help、欠落/非整数は入力前exit2 | ✓ SATISFIED | Truth 1, 2 |
| REQ-24 | 07-01,02,03 | min AND max包含の共通選択→top、全形式、順独立、Unicode、11種類以上top10、spy/Counter不変/共通pairs | ✓ SATISFIED | Truth 1, 3 |
| REQ-25 | 07-01,02,03 | 正常空exit0、有効maxで入力失敗exit1、min0/top0併用exit2、関係エラーなし | ✓ SATISFIED | Truth 2, 4 |
| REQ-26 | 07-01,02,03 | 省略/大上限の固定bytes一致、元Counter/総数12、各種保持、CI/依存/無関係変更なし | ✓ SATISFIED（「見た目」の画像比較は判断によりN/A） | Truth 3, 5, 6, 7, 9 |
| REQ-27 | 07-01,02,03 | RED→GREEN・全pytest記録、品質の対象head独立CLI/HTML内容検証と原本追跡、文字証拠 | ✓ SATISFIED（ブラウザ/画像/通信は判断によりN/A・未実施。文字証拠の標準添付とPM読取りは本報告後の品質工程） | Truth 7, 10 |
| REQ-28 | 07-02 | README例1つ＋説明、実CLI exit0/stdout/stderr | ✓ SATISFIED | Truth 8 |

全PLANの `requirements` は REQ-23..28 で、REQUIREMENTS.md の Phase 7 対応表（REQ-23..28）と一致。ORPHANED なし。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| （変更ファイル全体） | — | TBD/FIXME/XXX | — | 該当なし |
| tests / tools | — | 07-REVIEW.md warning 2 / info 4（検証ツール・試験の堅牢性） | ℹ️ Info | 製品挙動に影響なし |

### Human Verification Required

None. 依頼者判断により画像比較・画像閲覧は受入対象外。品質による文字証拠（本書・CLI/CI証拠）の標準添付とPMの read_file 読取りは本検証後に品質が行う工程であり、受入の人手確認項目ではない（07-SECURITY.md T-07-10 はこの添付まで非blocking open）。

### Gaps Summary

なし。製品変更は `--max-count` 登録と包含AND条件の3行のみで、元Counter/元総数を選択前に保持し、選択後Counterをtopへ渡し、同じpairsを全formatterへ渡す。先行RED（276中213失敗）→GREEN、全1048試験成功、CI pytest成功、品質の対象head独立CLI/HTML内容capture（138 case）で全受入条件を追跡できる。ブラウザ画像・幾何・通信観測は依頼者判断で未実施（合格扱いではない）。

### 品質の独立確認（受入条件ごと。カード t_dc0281b7 run 135、profile argonauts-uat-quality、head b4e9037）

| 受入条件 | REQ | 判定 | 品質が実行して確かめたこと（原本） |
|---|---|---|---|
| AC1 整数のオプション、省略時は上限なし | REQ-23, REQ-26 | 合格 | help に表示される。+2・02・=-1 を受け付ける。上限を省略したときと 1000000 を指定したときは、変更前の固定バイト列と一致（validate exit0） |
| AC2 指定した値以下だけ（境界の値を含む） | REQ-24, REQ-25 | 合格 | max2→alpha2/gamma1/delta1、max1→gamma1/delta1。max0・負数・逆転の区間は空でexit0。HTMLの総数は7のまま |
| AC3 --min-count と併用 | REQ-24, REQ-25, REQ-26 | 合格 | min2max2→alpha2。min2max3 は指定順を入れ替えても beta3/alpha2。三条件では zoo3 で総数12。top は選んだ後に効く（10件/12件） |
| AC4 追加した試験と既存の試験が通る | REQ-27 | 合格 | 全suite 1048 passed、exit0、208秒。必須CIの pytest は push・pull_request とも success |
| AC5 README の例1つを再現 | REQ-28 | 合格 | 一時cwdで実行し、exit0、期待どおりのJSON+LF、stderr空 |
| AC6 範囲（無関係な変更・依存・CIの変更なし） | REQ-26, REQ-27 | 合格 | 製品の変更は __main__.py の2か所、README、試験、検証の道具、手順書だけ。危険なパスには触れていない |

- 実際に見た画像: 0枚（依頼者の判断 2026-11-25 21:22 で、画像の取得と比較は受入条件から外れた。未実施で、合格扱いはしていない）
- 入力・正確なargv・exit・stdout・stderr・CIの詳細は `.planning/argonauts/r-d4bcda40/quality/cli-ci-proof.md` にある。ケースの原本は `quality/final-01/`、台帳は `quality/reviews-01.json`（finalize exit0）。
- OpenSpec の verify: `.planning/argonauts/t_dc0281b7/openspec-verify.md`（CRITICAL 0。tasks 2.2 の内容はこのrunで済んだ。印は最終化で付ける）

---

_Verified: 2026-11-25T14:11:21Z_
_Verifier: Claude (gsd-verifier)_
