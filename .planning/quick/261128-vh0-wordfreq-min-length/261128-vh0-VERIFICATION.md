---
phase: quick-261128-vh0-wordfreq-min-length
verified: 2026-11-28T14:53:04Z
status: passed
score: 6/6 must-haves verified
verification_scope: builder-responsibility-only
head: c7634579f9966f8718c16d9e88ffa5d47a9b7409
behavior_unverified: 0
overrides_applied: 0
human_verification: []
independent_quality: pending
browser_verification: pending
acceptance_status: pending
re_verification:
  previous_status: human_needed
  previous_score: 5/6
  gaps_closed: ["PM承認の責任分離後、第6must-haveのBuilder証拠と品質pending引継ぎを実証"]
  gaps_remaining: []
  regressions: []
decision_coverage:
  honored: 0
  total: 0
  not_honored: []
covered_files: [".planning/argonauts/r-a7606d74/baseline/index.json", ".planning/argonauts/r-a7606d74/baseline/input.txt", ".planning/argonauts/r-a7606d74/builder/EVIDENCE.md", ".planning/argonauts/r-a7606d74/builder/final-cli-index.json", ".planning/argonauts/r-a7606d74/builder/responsibility-resume/min-length.exit", ".planning/argonauts/r-a7606d74/builder/responsibility-resume/min-length.stderr", ".planning/argonauts/r-a7606d74/builder/responsibility-resume/min-length.stdout", ".planning/argonauts/r-a7606d74/builder/resume-fixture/all.exit", ".planning/argonauts/r-a7606d74/builder/resume-fixture/all.stderr", ".planning/argonauts/r-a7606d74/builder/resume-fixture/all.stdout", ".planning/quick/261128-vh0-wordfreq-min-length/261128-vh0-PLAN.md", ".planning/quick/261128-vh0-wordfreq-min-length/261128-vh0-SUMMARY.md", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/responsibility-spot.exit", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/responsibility-spot.stderr", ".planning/quick/261128-vh0-wordfreq-min-length/verifier/responsibility-spot.stdout", "README.md", "openspec/changes/r-a7606d74-light/tasks.md", "pyproject.toml", "tests/fixtures/max_count_scope/__main__.py", "tests/test_cli.py", "tests/test_max_count_verifier.py", "wordfreq/__main__.py", "wordfreq/aggregator.py", "wordfreq/formatters.py", "wordfreq/sources.py", "wordfreq/tokenizer.py"]
covered_digest: "v4:sha256:9c84fa12aa902720333dffc8359f3e902c088ea6878b81ffa4b2c77b34973916"
---

# Quick 261128-vh0 Builder担当範囲 再検証原本

**passedはBuilder担当範囲のみ。製品最終受入はpending。**

PM t_8b54614f comment246承認後のPLAN/SUMMARY全文、実コード・試験・原本を読み、既存Quick step6.5を再検証した。VerifierはBuilderプロファイル内gsd-verifierであり独立qualityではない。現PLANは独立品質の実施そのものではなく、必須条件をpendingで引き継ぐことを第6must-have/Task 3のBuilder完了条件としている。要求の免除・品質合格・overrideではない。

旧human_needed原本は `.planning/argonauts/r-a7606d74/builder/responsibility-resume/261128-vh0-VERIFICATION.before-pm-responsibility-split.md` に保持。更新前VERIFICATIONとのcmp一致を確認し、保存先は未変更。通常ROADMAP phaseではなくQuickの承認済み契約を対象とした。

## Observable Truths

| # | 現PLAN must-have（要旨） | 判定 | 実証 |
|---|---|---|---|
| 1 | 正整数、既定1、casefold後Unicode lenの包含境界 | VERIFIED | main:18–22,35–36,42–47、tokenizer:18。実CLI unicode試験はß→ss、CJK/数字/下線、N1/2/3/巨大Nをliteral期待pairsに照合。今回fresh成功。 |
| 2 | 不正値全形式を入力前exit2、stdout空、開いたstdinを読まない | VERIFIED | parser type=intと入力前の `<1`。invalid_before_readはspy呼出し0と実CLI不存在入力優先を検査。invalid_open_stdinはEOF未送信・stdin未closeでwait(timeout=3)により終了を確認。今回両試験fresh成功。 |
| 3 | 長さ/頻度ANDはtop前、降順・同数初出順・元total保持 | VERIFIED | main:42–58の元counts/total→items順新Counter→top_words→共通pairs、aggregator:17のstable sort後slice。composition144は頻度条件に依存しない長さtop前判別と独立不適格語を含む。internal_orderのCounter/identity/metadata assertは今回fresh成功。 |
| 4 | 省略/明示1の変更前bytes互換、空/全除外/入力失敗保持 | VERIFIED | test_cli:1265–1275で旧24caseのexit/stdout/stderr hexに両呼出しを比較。1418–1462で空表現と有効Nのmissing/directory/decode/実EACCESを値assert。対象263成功原本確認、baseline再生成なし。 |
| 5 | help全説明、README/依存/CI/抽出/正規化/HTML外観非変更 | VERIFIED | help試験1359–1366はファイルなしexit0/stderr空と全説明句を要求。初期HEADから非対象製品/README/pyproject/.github/過去verifier差分なし。外観コード非変更の証拠であり実描画受入は別pending。 |
| 6 | Builder対象/全pytest成功、不変baseline/README、CLI原本対応、品質pending引継ぎ | VERIFIED | responsibility-resume263、resume-fixture1311、既存CLI913のstdout/stderr/exitを直接確認。git差分・checksum、raw索引/HTMLサンプル、PLAN quality_acceptance/SUMMARY/OpenSpec tasksのpending保持を確認。 |

**6/6 Builder truths VERIFIED、behavior_unverified=0、override=0。** 前回の独立受入未実施自体は解消していない。現PLANの責任分離に基づきBuilder契約のみをpassedとする。

## Artifacts / Wiring / Data Flow

公式 `query verify.artifacts <PLAN>`: **all_passed=true、4/4**。main/test_cli/baseline index/inputを実内容まで確認。captureは明示環境変数、既存index上書き拒否、製品min-length未追加guardがあり、通常試験は再生成しない。

公式 `query verify.key-links <PLAN>`: **all_verified=false、0/4**、全て `Target not referenced in source`。自動結果は成功へ読み替えない。Python相対importと分割path構成を手読みにより追跡し、以下を実行証拠で補完した。

| Link | 手動根拠 | 最終状態 |
|---|---|---|
| main→tokenizer | `.tokenizer import iter_tokens`、`count_words(iter_tokens(text))`、casefold済みキーのlen。fresh実CLI Unicode成功。 | WIRED / FLOWING |
| main→aggregator | imports→元counts→items順AND新Counter→stable sort→top。fresh internal_orderで非変更/順序をassert。 | WIRED / FLOWING |
| main→formatters | 同一pairsを3形式へ、HTMLに選択前total。FileSource実入力由来で静的mockではない。internal_orderとCLI原本で補完。 | WIRED / FLOWING |
| test_cli→baseline | ROOT/baseline + index.jsonの動的path、旧hex bytesとの比較。 | WIRED / 固定旧oracle |

## Behavioral Evidence

全pytest環境prefix: `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`。

| 区分 | 実pytest引数 | 実測・原本 |
|---|---|---|
| Builder fresh対象 | `tests/test_cli.py -k min_length -q -p no:cacheprovider` | 263 passed, 650 deselected in 8.18s、exit0、stderr空。`builder/responsibility-resume/min-length.{stdout,stderr,exit}` |
| Builder既存CLI | `tests/test_cli.py -q --junitxml=.../logs/final-cli.xml` | 913 passed in 70.54s、exit0、stderr空。`builder/logs/final-cli.{stdout,stderr,exit}` |
| Builder既存全suite | `-q --junitxml=.../resume-fixture/all.xml` | 1311 passed in 213.95s、exit0、stderr空。`builder/resume-fixture/all.{stdout,stderr,exit}` |
| 今回verifier fresh spot | `tests/test_cli.py::test_min_length_unicode tests/test_cli.py::test_min_length_internal_order tests/test_cli.py::test_min_length_invalid_before_read tests/test_cli.py::test_min_length_invalid_open_stdin -q -p no:cacheprovider` | **54 passed in 1.75s、exit0、stderr空**。本Quick `verifier/responsibility-spot.{stdout,stderr,exit}` |

既存結果は今回read_fileで直接確認した。全suiteは今回再実行していない。spotは独立qualityの実行ではない。PLAN/SUMMARYに独立shell probe宣言なし。実在pytest nodeidから検証した。

### Scope / Immutable Originals

- 現HEAD `c7634579f9966f8718c16d9e88ffa5d47a9b7409`。全suite成功HEAD `1d3a99abbb7d3166c168e1acf43db3bf52856459` → 現HEADのREADME/wordfreq/tests/pyproject/.github/過去verifierはgit diff --exit-code成功。現在の同対象working/staged差分もなし。CLI原本HEAD `50786d64208241ddb285784a03fc9cae3e9c4147` → 現HEADのwordfreq/test_cliも差分なし。
- 初期HEAD `6aae84890f8ddbd17e186b9a4732df6dd92d2976` → 現HEADのREADME/非対象製品/依存/CI/過去verifier差分なし。READMEはworking/stagedと履歴の両方で非変更。
- baseline indexは初期HEAD、product_diff_hex空、jqでcases24。index SHA-256 `2ec8db3041583a2defb94279315a6dd71876a0ae781c678877d69a6f00fb1de0`、input SHA-256 `36862295d293157114143e3e825e6df8a037fe7ed25c04cd7c39cc84cb78eaa4`、既存source-hashesと一致。再生成なし。
- 過去fixtureは承認出典commit `31953e1c3f1bd0b5da09484f079f0027976ec737` のmainと同梱fixtureのSHA-256がともに `9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba`。scope_repoのcopy元局所変更を読み、承認hash/既存assertの緩和ではないことを確認。

### CLI原本と文字記録

`builder/EVIDENCE.md` はFR/SC/LEN・command・期待値・ログ対応を保持。そこに残る旧全suite失敗は履歴であり、SUMMARY resume節とresume-fixture成功原本が解決後証拠。

`builder/final-cli-index.json` はjqで262 records、test/input/argv/head/environment/exit/expected pairs/total/record_pathを持つ。サンプル `final-head-raw/005606a49bd44d37b740568babf12db4/cli.json` とstdout.htmlを直接読み、min-length3/min-count2/max-count2/top2、zoo2→apple2、元total8、basename selection.txtとの対応を確認。全262 rawを個別読了したとは主張しない。HTMLソース読取りはブラウザ実閲覧ではない。Spy-only/EOF未送信stdinはpytest内assertとレポートへ対応。

## Requirements / Test Quality / Anti-Patterns

| 要求 | Builder判定 | 最終品質受入 |
|---|---|---|
| FR-1/LEN-1/SC-1 | Unicode・境界・casefold・正整数を確認 | 独立quality待ち |
| LEN-2/SC-4 | 入力前spy/開いたstdin、有効N入力失敗/help確認 | 独立quality待ち |
| FR-2/SC-2 | 不変旧bytesへ省略/明示1比較 | 独立quality待ち |
| FR-3/LEN-3/SC-3 | AND/top前/初出順/元total/空表現確認 | 独立quality/HTML待ち |
| FR-4 | ファイルなしhelp全説明確認 | 独立quality待ち |
| FR-5/LEN-4/SC-5 | Builder試験成功、不変性、原本対応、pending引継ぎ確認 | **pending（要求全体の最終受入未完）** |

min-length領域はactive、literal値/bytes/順序/identity/metadata/実CLI終了結果をassert。内部spyのみでtokenizer統合を証明せず実CLIで補完。baselineは旧互換oracleであり、新機能の期待値を同じ実装から生成する循環ではない。今回追加領域にskip/disabledやTBD/FIXME/XXX/TODO/HACK/PLACEHOLDERなし。既存POSIX filename skipifは今回追加ではない。空表現は契約でありstubではない。新規blocking anti-patternを認めなかった。

### Decision Coverage

公式 `query check.decision-coverage-verify`: **No CONTEXT.md - nothing to check.** skipped=true、total=0、honored=0、not_honored=[]。agent-skills --skills-onlyは空、project HERMES.md/.agents skills/.hermes skillsなし。

### Advisory (New Scope, Unevidenced)

None。旧未完受入を新規製品欠陥や解消済み品質項目へ読み替えていない。

## Builder Human Verification Required

なし（human_verification=[]）。現PLAN human-checkはBuilderによる原本・不変性・対応確認と品質pending引継ぎであり、それを実証した。以下は別担当の必須品質受入として保持し、Builderのpassedを製品受入に転用しない。

## 必須品質受入 / 製品最終受入 — pending

**未実施・未合格。本verifierは独立品質役ではなくブラウザ/画像を実閲覧していない。**

1. 独立qualityが最終HEAD・環境を記録し、自分のfresh quality rootで対象pytestと全pytestを実行する。Builder原本/本spotを流用して独立実行完了にしない。command/件数/exitと入力・argv・stdout/stderr・文字記録を対応付ける。
2. HTMLの省略/明示1互換、絞込み、全除外、元総数を1280×900と320×900、DPR1、zoom100%で実ブラウザ閲覧する。全画像/必要tileを実際に開き、raw/画像/実閲覧を対応付け、可読性・行/順位・元総数・空状態・見出しを文字記録する。安全性/UTF-8/basename/親path非漏洩/静的HTML契約を維持する。

PLAN quality_acceptance、SUMMARY pending字段/末尾、OpenSpec tasks非checkbox品質区画は未完を保持。FR-5/LEN-4/SC-5最終受入、independent_quality/browser_verification/acceptance_statusはpending。既存3 taskのBuilder完了と独立受入を循環させない。

## Integrity / Handoff

公式verification.fingerprintのcovered_files/covered_digestをそのまま転記。PLAN/SUMMARYは自動追加、report自身は除外。今回作成/変更は本VERIFICATIONとverifier/responsibility-spot.{stdout,stderr,exit}のみ。旧human_needed保存先は未変更。製品/試験/PLAN/SUMMARY/OpenSpec/STATE/ROADMAP編集、commit/push/PR/branch/worktree/Kanban操作なし。

_Verifier: Hermes / official gsd-verifier（Builder担当範囲）_
