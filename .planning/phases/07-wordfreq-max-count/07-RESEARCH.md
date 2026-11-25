# Phase 7: wordfreq max-count — Research

**Researched:** 2026-11-25（依頼コンテキストの日付）
**Domain:** Python stdlib CLI、頻度帯の共通選択、互換性・独立HTML検証
**Confidence:** HIGH（読了した承認仕様と現行ソースの対応）。外部docsの取得providerの機械判定はLOW、ブラウザ実行可否は未検証。

<user_constraints>
## User Constraints (from CONTEXT.md)

以下は `07-CONTEXT.md:15–27,51–53` の原文。仕様・制約の引用であり、この調査で実行済みという意味ではない。

### Locked requirements (PRD全体を決定として扱う)
- D-01 / REQ-23 / MAX-1: argparse type=int相当、default=Noneの--max-count N。0/負整数/+2/02/大整数/--max-count=-1を受理。ファイルなしhelpはexit0、stderr空、--max-count MAX_COUNT表示。abc/1.5/値欠落は入力取得より先にexit2、stdout空、stderr通知、Tracebackなし。
- D-02 / REQ-24 / MAX-1/FR-2/FR-4/MC-1: 正規化・casefold後の元Counterから count>=min_count AND (max_count is None OR count<=max_count) を選択して既存topへ渡す。引数順独立、両端包含、max1、min=max、min>maxを含める。元Counter・HTML元総数の算出を変更しない。全formatterで同じpairs。top入力spy/Counter不変/shared pairsで内部順序も検証。
- D-03 / REQ-25 / MAX-2/MC-2: max0/負数/min>max/全除外/空/空白/記号入力は正常空結果exit0・stderr空。text空/json []+改行1つ/html既存3列/0行/空文言/basename/元総数。空集合でも入力取得短絡なし。有効maxと不存在/ディレクトリ/読込拒否/不正UTF-8はexit1・stdout空、stderr通知。不正min0/top0併用は入力前exit2。min/max関係エラー・max正値制限を追加しない。
- D-04 / REQ-26 / MAX-2/HTML-2: 上限未指定・大上限・明示min1を変更前固定の期待バイト列/exit/stderrと照合する。新コード2呼出し同士の比較のみは不可。既存期待値は書換えない。top10/明示top、Unicode、同数初出順、basename/UTF-8/escape/静的安全性/formatter API/text/json構造/HTML CSS/見た目/空文言不変。
- D-05 / REQ-27 / MAX-3/tasks1.1/1.2/2.1: Builderが先行試験の狙ったREDを記録してから最小実装GREEN、追加と全既存pytest成功を環境/コマンド/件数/exit付きで保存。既存試験削除・回避なし。beta4/zoo3/apple2/pear2/single1のmin2/max3/top1はzoo3のみ・元総数12。選択後11種類以上のtop10、不正min/topとmax0/負数も検証。
- D-06 / REQ-28 / MAX-3/tasks1.3: README例1つは python -m wordfreq input.txt --min-count 2 --max-count 3 --format json、入力 beta beta beta alpha gamma alpha delta、期待JSON [{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]+改行、exit0・stderr空。例を実CLIで再現するpytest。直接関連説明として整数全域/省略上限なし/包含/min併用/逆転等の正常空結果/maxを上げるか省略する全除外案内/HTML総数はmax前を記す。
- D-07 / REQ-27 / tasks2.2: 品質が対象headからCLIを独立生成し、省略互換/包含/min併用/全除外/元総数を確認。HTMLは既存義務どおり通常幅1280x900・狭幅320x900 DPR1でブラウザ確認し、入力/argv/exit/stdout/stderr/HTML原本/実測/画像の実閲覧/失敗含む通信試行を追跡可能に残す。VERIFICATION.mdとCLI/CI文字証拠を添付しAC別結果と画像閲覧枚数/内容/結果を明記。PMに画像や圧縮ファイル閲覧を求めず、未実施・未報告CIを成功扱いしない。OpenSpec2.2の独立検証実施はフェーズ検証へ明示引継ぎ。
- D-08 / scope: 製品変更はwordfreq/__main__.py・関連CLI試験・READMEのみを基本とし、必要な試験fixture/検証文書を計画する。依存/CI/新入力元/新サービス/見た目/無関係機能/全体リファクタなし。要件を通すためsecurity_enforcement/nyquist_validation/plan_check/pattern_mapperを無効化しない。

### Claude's Discretion
- 局所変数名、pytestケースの分け方、既存試験helperの再利用、fixtureと品質証拠の最小構成。受入条件を削らない。
- PLANは各3 task以内で同じ依頼branchへ直列に積み上げる。各タスク終了時とフェーズ検証時に、その時点の同一branchの成果で検証可能にする。未作成コマンドを計画中に走らせず、作成する検証ファイルは同じtaskまたは先行taskに明記。独立PLANは他PLAN成果なしでも検証できる。automatedは標準実行方法とし外側cd/grepを足さず、fails_whenは観測する失敗を書く。

### Deferred Ideas
依存/CI更新、機能拡張、新入力元、UI再設計、過去phaseの検証修復は対象外。未決事項なし。
</user_constraints>

## Summary

実装点は既存CLIの引数登録と共通選択の二箇所に限定できる。現行順序は `counts = count_words(iter_tokens(text))` → `total = sum(counts.values())` → 別Counterの下限選択 → `pairs = top_words(selected_counts, args.top)` → formatter分岐。上限をこの選択条件へANDで加え、`None` を明示判定する。抽出・順位付け・formatterを変更しないのが承認designに一致する。 [VERIFIED: wordfreq/__main__.py:13–54; openspec/changes/r-d4bcda40-max-count/design.md:19–26]

計画上の主なリスクはコード量でなく証拠設計である。変更前固定bytes、狙ったREDとGREEN、top入力spy、元Counter不変、品質本人による対象headの独立CLI/ブラウザ証拠を別々に確保する。旧min-count用driverはrequest・scope・ケース・引数が専用で、そのまま実行してmax-count受入を満たすものではない。 [VERIFIED: .planning/argonauts/r-d4bcda40-prd.md:198–210; tools/verify_wordfreq_min_count.py:18–20,145–163,414–450,490–521]

**Primary recommendation:** 最初の製品編集前に固定oracleと採取手順を成立させ、実CLIの小さいtracerのRED→最小GREENを先頭に置き、残りの判別ケースとREADMEを同一branchへ直列に積む。独立品質の実施をフェーズ検証の必須gateとして明示する（この文書はPLANでも受入証拠でもない）。 [VERIFIED: 07-CONTEXT.md:20–27; .planning/argonauts/r-d4bcda40-prd.md:203–210]

## Architectural Responsibility Map

| Capability | Primary tier | Secondary tier | Rationale / evidence |
|---|---|---|---|
| 整数受理・help・使い方exit | CLI composition | argparse | parserと既存正値検証が入力より前。`wordfreq/__main__.py:13–30` |
| 入力取得・decode失敗 | Source boundary | CLI exit mapping | UTF-8読込みと例外変換、CLIがexit決定。`wordfreq/sources.py:13–22`; `__main__.py:29–33` |
| min/max選択・元total | CLI composition | Counter | 集計後・順位付け前の既存共通点。`__main__.py:34–38` |
| 回数降順・同数初出・top | Aggregator | — | `top_words`は回数のみの安定ソート。`wordfreq/aggregator.py:11–17` |
| HTMLのescape・構造・見た目 | Pure formatter / static document | CLI basename/total | `format_html(pairs, basename, total)`を保持。`wordfreq/formatters.py:17–127` |
| 可読性・通信観測・証拠帰属 | Independent quality | Browser tooling | 単体試験で代用しない。PRD:91–93,210 |

各行は読了済みソースによる責任境界。新しいfrontend/API/DB tierは追加しない。 [VERIFIED: 上表の各ソース; openspec/changes/r-d4bcda40-max-count/design.md:9–17]

## Project Constraints (from HERMES.md)

`HERMES.md` と `.hermes/HERMES.md` はどちらもread_fileがFile not found。`.hermes/skills/` と `.agents/skills/` も探索でPath not found。したがって読めるプロジェクト固有指示は確認できず、ここに架空の規約を追加しない。公式 `query agent-skills gsd-phase-researcher --skills-only` の出力は空、configの原文は `"agent_skills": {}`。 [VERIFIED: 本調査read_file/search_files/公式CLI結果; .planning/config.json:63–64]

本依頼の追加制約：読取りはread_file、抽出はjq、GSD判定は公式CLI。inlineスクリプト・ヒアドキュメントなし。未作成検証は研究/計画中に実行しない。実装・PLAN作成・commit/push・kanbanは本調査では行わない。 [VERIFIED: 委任依頼本文]

## Phase Requirements

<phase_requirements>
| ID | Description（REQUIREMENTS.mdの対応） | Research support |
|---|---|---|
| REQ-23 | type=int相当、省略None、整数全域/help、欠落/非整数pre-I/O exit2 | parser登録点、read spy＋実CLI、整数表記matrix |
| REQ-24 | 正規化後min AND任意max→既存top、全形式/初出順/Unicode/既定10、Counter不変/shared pairs | 既存選択点、top spy、独立固定pairs、選択後11種類以上 |
| REQ-25 | 正常空集合exit0、入力失敗exit1、不正min/top pre-I/O exit2、関係エラーなし | 空結果/入力失敗/使い方を直交したmatrixで検証 |
| REQ-26 | 変更前固定bytes、省略/大上限互換、元total12とAPI/安全性/見た目/範囲保持 | 旧保存oracleの位置、新baselineの不足分、formatter無変更とscope diff |
| REQ-27 | 先行RED→GREEN、全pytest記録、独立CLI/両幅browser/実画像/通信/文字証拠 | Validation Architectureの責任分離とフェーズgate |
| REQ-28 | README指定1例の入力/JSON/exit再現、直接関連説明だけ | 既存README試験型を再利用、本文整合と実CLI双方をassert |
</phase_requirements>

要件ID/契約の原文は `"REQ-23"` から `"REQ-28"`。上表は要約でありPRD全scenarioを置換しない。 [VERIFIED: .planning/REQUIREMENTS.md:88–102; .planning/argonauts/r-d4bcda40-prd.md:38–195]

## Standard Stack

| Component | Version / observed state | Use |
|---|---|---|
| Product | `"version = \"0.1.0\""`, `"dependencies = []"` | ローカルrepo内のwordfreqのみ。同名PyPI packageを導入しない |
| Python stdlib | `/usr/bin/python3 --version` → `Python 3.12.15` | argparse/Counter/既存I/O・formatter経路 |
| Tests | 指定PYTHONPATH下で `pytest 9.0.3` | 既存pytest + subprocess + monkeypatch + HTMLParser |
| Browser executable | `/usr/bin/chromium-browser --version` → `Chromium 156.0.8078.73 Built from source for Red Hat Enterprise Linux release 10.2 (Coughlan)` | 後工程の独立HTML検証用。起動成功はまだ未確認 |

製品設定の原文は `name = "wordfreq"`, `version = "0.1.0"`, `dependencies = []`, `dev = ["pytest"]`。stdlibのため追加install/registry調査は不要、既存dev依存の版を上げない。 [VERIFIED: pyproject.toml:5–12; 本調査terminalのversion出力]

**重要な環境差:** PATH上の `python`/`python3` は `Python 3.14.9` だが `python -m pytest --version` は `No module named pytest`。既存runbookの環境指定 `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest --version` は `pytest 9.0.3` を返した。pytestの標準実行コマンドはこの既存環境へ固定する。これは版横断互換保証ではない。 [VERIFIED: 本調査terminal出力; docs/wordfreq-min-count-verification.md:14,18–19]

## Architecture Patterns

### Data flow

```text
argv ─→ argparse/help/usage validation ─→ usage error: stderr / exit2
                      │ valid
                      ▼
UTF-8 file ─→ FileSource ─→ input/decode error: stderr / exit1
                      │ text
                      ▼
Unicode extraction → casefold → original Counter → original total retained
                                      │
                                      ▼
                         min AND optional inclusive max
                                      │ new ordered Counter
                                      ▼
                   descending count / stable ties → top → shared pairs
                                                         ├→ text
                                                         ├→ JSON
original basename + original total ───────────────────────└→ static HTML
```

上図は現行経路へ承認済み上限条件だけを加える推薦であり、実装済み図ではない。根拠は `iter_tokens` の原文 `return (token.casefold() for token in tokenizer(text))`、CLIの選択点、designのAND条件。 [VERIFIED: wordfreq/tokenizer.py:14–18; wordfreq/__main__.py:22–54; openspec/changes/r-d4bcda40-max-count/design.md:21–25]

### Component responsibilities / minimal touch surface

- `wordfreq/__main__.py`：parserと既存selectionのみが基本の製品編集箇所。`--top` の `default=10`、`--min-count` の `default=1` は維持。 [VERIFIED: wordfreq/__main__.py:13–18; PRD:28,204]
- `tests/test_cli.py`：既存helperの原文名は `run_cli`, `CLIHTML`, `run_cli_bytes`, `assert_output_bytes`。bytes subprocessでUTF-8/newlineを確認し、HTML構造はparserで確認する。新ケースは追加し、旧期待値を改変しない。 [VERIFIED: tests/test_cli.py:16–20,201–239,418–441,796–817; PRD:203]
- `README.md`：上限説明、既存のfilter順序・総数説明の直接関連更新、新例1つ。旧min例を消さない（既存試験が文字列を要求）。既存末尾の検証B行を無関係に削除・改変しない。 [VERIFIED: README.md:13,21–37; tests/test_cli.py:672–682; PRD:205]
- tokenizer/aggregator/sources/formattersは参照・回帰検証対象であって変更対象ではない。既存API原文は `def top_words(counts: Counter[str], n: int) -> list[tuple[str, int]]:`、`def format_html(pairs: list[tuple[str, int]], basename: str, total: int) -> str:`。 [VERIFIED: wordfreq/aggregator.py:11–17; wordfreq/formatters.py:22–26; PRD:28]

### Baseline/oracle separation

既存 `test_min_count_saved_default_bytes` は保存stdoutをread_bytesして、未指定/明示min1を比較する。原文 `root = ROOT / ".planning/argonauts/r-e476c11d/baseline"` と `capture_root = Path(index["root"])` により履歴絶対pathを現worktreeへメモリ写像する。この方式を理解して保存原本を利用し、旧原本のhead/rootを書き換えない。 [VERIFIED: tests/test_cli.py:796–817]

旧indexの原文は `"request": "r-e476c11d"`, `"head": "789cc17267fb4cfeea24111797c3d934c542ce6a"`。jqで抽出したcaseは既定text、text/json/html、空/空白/記号HTML、longの既定/12/99、injection、CR basename。旧原本は既存byte oracleの参考であり、Phase7の変更前画像・現head独立品質の代用ではない。特に既存min>1の呼出し互換や全形式の空結果の不足は、最初の製品変更前に今回の固定bytes/exit/stderr/argv/環境と期待pairsを補う。 [VERIFIED: .planning/argonauts/r-e476c11d/baseline/index.json:2–20,63–87; 本調査jq抽出結果; PRD:80–82,185–195,203]

推薦する採取契約：既存保存原本を不変で参照し、不足ケースだけ今回専用のfresh rootへ採取する。入力原本、basename、argv、cwd、実interpreter/version、環境、対象head、stdout/stderr bytes、exit、固定期待値と対応を一緒に記録する。baseline採取時点ではmaxは未実装なので、通常の既存argvで採取し、実装後の大上限/省略/明示min1を同じ固定oracleへ比較する。画像の同条件比較が必要なケースは製品編集前に同じbrowser/フォント/両幅で採取する。新しい記録ファイル・採取スクリプトの名前とCLIはplannerが作成taskに明記する（ここでは存在すると仮定しない）。 [VERIFIED: PRD:80–93,185–187,203; 07-CONTEXT.md:19,22,27]

### Quality tooling: reuse mechanisms, not old request acceptance

旧driver原文は `REQUEST = "r-e476c11d"`, `BASE = "9eb1e694aafc6cd29f0f7d2a29382764bc1627fb"`, `WIDTHS = (1280, 320)`。preflightは過去task commit名を要求し、case_argvはmin/topだけを構築、scopeは旧依頼名とPhase4 pathを許可する。従って旧CLIをそのままPLANのmax-count合格コマンドに記すのは不正確。 [VERIFIED: tools/verify_wordfreq_min_count.py:18–20,145–163,444–450,490–502]

推薦：旧raw Range/通信観測/画像台帳の方法を読み、max-count専用の最小fixture・検証記録・必要な検証ファイルを計画する。旧driverの一般化、独立サービス、既存min-count verifier改造は本機能の前提にしない。作成する検証ファイルは同じtaskまたは先行taskで明記し、そのファイルの実在後にのみ標準CLIを実行する。旧runbookの短い一時pathへの人の例外は今回へ移植しない。 [VERIFIED: 07-CONTEXT.md:23,27,43; docs/wordfreq-min-count-verification.md:39–43; 07-UI-SPEC.md:180–192（読取り時draft）]

## Don't Hand-Roll

| Problem | Don't build | Use instead / evidence |
|---|---|---|
| 整数構文・help・usage | 独自正規表現parser、max専用positive型 | 既存argparseの `type=int`。design:21 |
| 順位付け・tie復元 | 新ソート、set、語の昇順 | 既存 `top_words` と元Counter順。aggregator:11–17 |
| HTML empty/safety | max用HTMLや空理由別copy、独自escape | 無変更の `format_html`。formatters:17–37 |
| pytest起動環境 | installやpyproject/CI更新 | 検出した既存CPython3.12 + PYTHONPATH環境 |
| 独立受入 | Builderのcaptureを品質acceptedとする自動台帳 | 品質自身のCLI/実閲覧/通信原本と文字報告。PRD:91–93,210 |

上表の採否は承認scopeと読了済みソースに基づく推薦。 [VERIFIED: openspec/changes/r-d4bcda40-max-count/design.md:19–26; PRD:28,85,210]

## Common Pitfalls

1. **0を未指定扱いするtruthiness。** `if max_count` / `max_count or ...` はmax0を落とす。`is None` と `<=` を明記した境界試験を置く。 [VERIFIED: design.md:21–22; PRD:54–55,64–66]
2. **minの正値制約をコピー。** max0/負数/min>maxは正常空集合であり引数エラーではない。逆にmin0/top0はmax0併用でも読込み前exit2。 [VERIFIED: PRD:38–39,72–78]
3. **top後filter。** max2/top1でalpha2を出す入力を置く。最高頻度beta3を最初にtopすると空になり誤りを識別できる。内部spyも別に必須。 [VERIFIED: PRD:113–115; design.md:22,24]
4. **選択Counterからtotalを再計算。** 三条件ケースのzoo3表示と元12、全除外で正の元total、抽出0語で0を別々に固定する。 [VERIFIED: PRD:64–70,155–157]
5. **初出順を旧語昇順へ戻す。** 旧学習の昇順記載は不採用。zoo→appleのtieを固定し、選択Counterの項目順までassertする。 [VERIFIED: CONCEPTS.md:49–55; .planning/argonauts/r-d4bcda40-learnings.md:19–21; aggregator.py:17]
6. **変更後2呼出しだけの互換比較。** 省略と大上限が同じ誤出力でも通る。変更前固定oracleと比較し、期待値再生成を禁止する。 [VERIFIED: PRD:80–82,203]
7. **permission試験の偽成立。** 既存試験はchmodの意図だけでなく同一実効ユーザーでPermissionErrorを確認する。root実行で失敗した場合、skipやmockだけへ置換しない。本調査 `id -u` は `1000`。 [VERIFIED: tests/test_cli.py:503–527,647–669; 本調査terminal]
8. **構造試験成功を可読性/無通信に読み替える。** 全画像実閲覧、raw未補正、失敗要求を含む観測を品質の別gateとする。旧件数・画像・head・承認を流用しない。 [VERIFIED: CONCEPTS.md:53–59; PRD:91–93,210; docs/wordfreq-min-count-verification.md:63–86]

## Code Examples

ここは現行コード/承認designの引用であって実装差分ではない。

### Existing seam and API

```python
# wordfreq/__main__.py:34–38（現行原文）
counts = count_words(iter_tokens(text))
total = sum(counts.values())
selected_counts = Counter({word: count for word, count in counts.items()
                           if count >= args.min_count})
pairs = top_words(selected_counts, args.top)
```

[VERIFIED: wordfreq/__main__.py:34–38]

承認済み条件の原文：`count >= min_count` かつ `max_count is None or count <= max_count`。同じ選択点へ追加し、元totalとtop/APIを保持する。新しい変数名・新検証ファイルpathは現物値でないので、実在として引用しない。 [VERIFIED: openspec/changes/r-d4bcda40-max-count/design.md:22–24]

### Existing test idiom to extend

既存parser試験は `build_parser().parse_args(...)`、pre-I/O試験は `FileSource.read_text` のspyと実subprocessを併用する。内部試験では `top_spy` が別Counter/項目順をassertし、`formatter_spy` が `pairs is selected[0]` をassert、最後に元Counterの値と順序の不変をassertしている。この型へ上限による高頻度語除外を追加する。 [VERIFIED: tests/test_cli.py:611–644,759–793]

README試験は既存の `test_min_count_help_and_readme_example` 型を使う。新例は原文 `python -m wordfreq input.txt --min-count 2 --max-count 3 --format json`、入力 `beta beta beta alpha gamma alpha delta`、stdout `[{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]` と末尾改行1つ。README文字列の存在確認だけでなく実subprocessのexit/stdout/stderrをassertする。 [VERIFIED: tests/test_cli.py:672–682; PRD:87–89,205]

## Validation Architecture

### Test Framework

| Property | Value |
|---|---|
| Framework | 既存pytest。検出版 `pytest 9.0.3`、CPython `3.12.15` |
| Config | pyprojectはpackage/dependencies設定。pytest専用設定追加は不要 |
| Standard environment | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3` |
| Existing focused command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -q -x` |
| Existing full-suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/ -q` |
| Existing API/safety regression command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_aggregator.py tests/test_formatters.py tests/test_sources_boundary.py -q` |

設定とコマンド慣例の根拠は `pyproject.toml:1–15`、`docs/wordfreq-min-count-verification.md:17–22`、読了した既存 `tests/test_cli.py`。上記は実在ファイルへの標準実行形式であり、本調査はpytest本体の `--version` のみ確認した。テスト実行・件数・所要時間・合格はまだ主張しない。 [VERIFIED: 当該ファイル; 本調査terminal]

### Phase Requirements → Test Map

各コマンドはrepo rootで実行。max用ケースは**これから追加**する。`-k max_count` は推薦する命名/選択契約であり現時点で存在するtest名ではない。新ケース作成前に実行しない。表のファイルは既存、maxカバレッジはWave0 gap。

| Req ID | Behavior / test type | Automated command after cases exist | File exists? |
|---|---|---|---|
| REQ-23 | parser default None、0/負数/+2/02/大整数/equals表記、fileなしhelp、abc/1.5/欠落pre-I/O spy＋全形式実CLI / unit+CLI | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k max_count -q -x` | ✅ file / ❌ max cases |
| REQ-24 | 両端包含/min=max、AND、指定順、Unicode、tie、top前、高top/既定10、top入力/Counter/shared pairs / unit+CLI | 同上（追加するmax_count群を選択） | ✅ file / ❌ max cases |
| REQ-25 | max0/負数/逆転/全除外/空/空白/記号、全形式bytes/HTML元total、4入力失敗、min0/top0 pre-I/O / CLI+spy | 同上 | ✅ file / ❌ max cases |
| REQ-26 | 保存oracle比較、省略/大max/明示min1、元total12、API/静的安全性 / regression | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py tests/test_aggregator.py tests/test_formatters.py tests/test_sources_boundary.py -q` | ✅ files+旧oracle / ❌ 不足oracle+max比較 |
| REQ-27 | 先行RED/GREEN、追加群・全既存suiteとJUnit/exit記録 / regression+independent acceptance | full-suite command（下記ログ契約付き） | ✅ suite / ❌ 今回の記録・独立品質原本 |
| REQ-28 | README例1つ/直接関連説明/掲載入力/期待JSON/実CLI exit0 stderr空 / doc+CLI | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k max_count -q -x` | ✅ file / ❌ README max例test |

推薦する個別selectorはplannerが最終test名を決め、同taskまたは先行taskで作成してから使う。上表の同一コマンドだけでは細かい行の充足を証明しないため、JUnit testcase名・入力/期待値とREQの対応表を残す。0 collected、必須caseのskip、想定外ERRORをGREENとしない。 [VERIFIED: PRD:203–210; 07-CONTEXT.md:27; docs/wordfreq-min-count-verification.md:22]

### Discriminating fixed-case matrix

以下は承認仕様由来の期待値であって測定結果ではない。全3形式で同じpairsを照合し、HTMLでは常に元totalを別assertする。 [VERIFIED: PRD:41–82,113–157,183–195]

| Input / intent | Options | Literal expected pairs / total |
|---|---|---|
| 通常入力 beta3 alpha2 gamma1 delta1 | max2 / max1 | alpha2,gamma1,delta1 / gamma1,delta1、元7 |
| 上下端/AND | min2 max2 / min2 max3、順交換 | alpha2 / beta3,alpha2、元7 |
| top後filterを検出 | max2 top1 | alpha2、元7 |
| 三条件で別々の語が落ちる | beta4,zoo3,apple2,pear2,single1; min2 max3 top1 | zoo3、元12 |
| 正常空 | max0 / max-1 / min3 max2 | 空pairs、元7 |
| 正規化後判定 | Straße STRASSE 日本語 日本語; max1 / min2 max2 | 空 / strasse2,日本語2、元4 |
| tie/top境界 | Zoo apple APPLE zoo banana; min2 max2 top1 / top2 | zoo2 / zoo2,apple2、元5 |
| 選択後11種類以上 | 高頻度の不適格語を先頭に置き、その後の適格語を固定列挙 | 既定は適格先頭10種類、大topは適格全種類。期待値は製品から生成しない |
| 入力なし/抽出0 | 空 / 空白 / 記号、有効max | text空、JSON `[]`+LF、HTML0行/元0/既存copy |
| 入力失敗 | max0/負数/逆転と不存在/dir/permission/decode | exit1、stdout空、stderr非空、Tracebackなし |
| usage | max欠落/abc/1.5、またはmax0/負数+min0/top0 | read spy未呼出し、exit2、stdout空、stderr非空 |

### Sampling Rate and RED/GREEN evidence

- **最初の製品編集前:** oracle保存/不足分採取と同条件画像を先に成立させる。その後、最初のtracerの新試験を実在ファイルへ作成し、未実装maxの狙った失敗を保存する。import失敗/pytest欠落/0 collectedは機能のREDではない。
- **Per task:** そのtaskの実在node selectorまたは追加群のfocused command。tracer以降も識別対象の失敗方向を明記し、包含・AND・filter順・元totalを別assertで区別する。GREEN後は既存回帰も実施。
- **Per wave / phase gate:** 全既存suiteを無削除・無回避で実行し、追加群と全suiteの環境/argv/cwd/対象head/実件数/exit/stdout/stderrを保存する。必要ならpytest標準 `--junitxml` を今回fresh evidence root内のファイルへ指定する（root作成taskを先行させる）。
- **Latency:** まだ測定していないため「30秒以内」とは記さない。unit/内部spyを最短feedbackにし、CLI matrixは必要な直交caseへ絞り、全suite/ブラウザは別gateにする。Builderが各stageの実測時間を記録する。
- **Phase acceptance:** full suite GREENに加えて品質本人の独立CLI/HTML実施が必要。OpenSpec task2.2をフェーズ検証へ明示引継ぎし、Builder captureを独立合格にしない。

[VERIFIED: PRD:203–210; 07-CONTEXT.md:20–27; docs/wordfreq-min-count-verification.md:22,63–100]

### Wave 0 Gaps / prerequisites for executable plans

- [ ] 変更前oracleの不足分を確認・固定する実在採取ファイル、入力/期待値/argv/env/bytes/exit/stderr索引。旧原本を上書きしない。
- [ ] `tests/test_cli.py` 内のmax_count追加ケース：parser/CLI/内部spy/互換bytes/README例。命名とnode selectorをPLANに一致させる。
- [ ] max受入用の最小検証ファイル/記録runbook：品質が自分でCLI/HTMLを生成し、元headと原本を追跡できること。新しいfile/CLIを想像で呼ばない。
- [ ] 同条件の変更前HTML表示と両幅画像。画像閲覧手段・raw読取り・通信観測・既存browser依存のimport/起動能力を、製品編集より前に確認する。
- [ ] 今回のVERIFICATION.md/CLI・CI文字証拠の出力先、AC/REQ索引、実画像閲覧台帳と標準添付への引継ぎを決める。
- [ ] Framework installは不要：既存3.12環境のpytest版取得成功。新依存導入で解決しない。

これらは推薦する後工程の作成/検証要件であり、この調査では新テスト/採取script/PLANを作成も実行もしていない。 [VERIFIED: 委任範囲; PRD:203–210]

### Independent quality / browser evidence gate

品質本人は対象headからfresh rootへCLIを再生成し、少なくとも省略互換・包含・min併用・top・全除外・元totalをAC/REQへ対応付ける。HTMLは1280×900と320×900 CSS px、DPR1、同browser/フォント/描画条件で確認し、全full/必要tileを実寸以上または全域panで開く。生の文字Range/祖先overflow/box/隣接非重複を補正せず残し、横収まり・clipなし・全文可読を判断する（自身elementの厳格縦包含だけを必須にしない）。 [VERIFIED: PRD:91–93,210; .planning/REQUIREMENTS.md:39,92; docs/wordfreq-min-count-verification.md:63–86]

通信はopen前から終了までのrequest/failed request/navigation/popupを含めて記録し、初回file文書と外部試行を分ける。成功response0や遮断だけで無通信にしない。画像実閲覧枚数・各画像の確認内容/結果、入力/argv/cwd/env/exit/stdout/stderr/HTML/raw/network原本と対象head、現ソース順序確認を文字報告へ索引化する。PMにはVERIFICATION.mdとCLI/CI文字証拠を標準添付し、画像/圧縮物の閲覧を要求しない。未報告CIは未確認と明記し、CI更新や待機機構を追加しない。 [VERIFIED: PRD:210; 07-CONTEXT.md:22; docs/wordfreq-min-count-verification.md:84–91,124]

## Security Domain

configの原文は `"security_enforcement": true`, `"security_asvs_level": 1`, `"nyquist_validation": true`, `"plan_check": true`, `"pattern_mapper": true`。いずれも無効化せず、既存CLI/static HTMLへ適用可能な項目を扱う。 [VERIFIED: .planning/config.json:21–25,43–50]

| ASVS category | Applies | Control / phase validation |
|---|---|---|
| V2 Authentication | No | 認証機能/サービス追加なし |
| V3 Session Management | No | 製品は自己完結CLI/static document。品質用browser sessionとは区別 |
| V4 Access Control | Scoped | 入力権限失敗の通知exit1を保持。特権化/permission回避なし |
| V5 Input Validation / output encoding | Yes | argparse int、pre-I/O usage検証、basename限定、既存escape/CR保護/UTF-8、無通信/静的HTML |
| V6 Cryptography | No product feature | 秘密・暗号機能を追加しない。証拠同一性hashは既存標準手段で確認 |

これは本phaseへの適用整理でありASVS全準拠の宣言ではない。入力境界/escape/static-documentの実装根拠は以下。 [VERIFIED: wordfreq/sources.py:17–22; wordfreq/__main__.py:23–33,39–53; wordfreq/formatters.py:17–19,22–127; design.md:15–17]

| Threat / regression | STRIDE | Mitigation |
|---|---|---|
| basename/動的値をmarkupとして解釈 | Tampering / information disclosure | 既存quote=True escapeを無変更、hostile basename回帰 |
| HTMLへdirectory漏洩 | Information disclosure | basename化と全HTML path不在assert |
| max0で読込み失敗を隠す | Tampering | 入力取得を常に実行しInputError→exit1保持 |
| 外部resource/失敗通信を見逃す | Information disclosure | 既存static allow-listと独立browser全試行観測 |
| 旧head証拠やBuilder自己承認 | Repudiation / evidence integrity | head/実施者/原本/文字索引と独立品質gate |

[VERIFIED: tests/test_cli.py:481–527; CONCEPTS.md:5–15,53–55; PRD:72–74,91–93,210]

## State of the Art / Scope Reconciliation

- 現行契約は回数降順・同数初出順。REQ-04の歴史的語昇順より、REQ-11/現aggregator/今回承認specを優先する。古いscenario名「同回数ワードは単語の昇順」でも期待値はzoo→apple。 [VERIFIED: .planning/REQUIREMENTS.md:20,34–38; PRD:117–126; aggregator.py:11–17]
- 公式 `query init.phase-op 7` は `"phase_found": true`, `"phase_number": "07"`, `"phase_name": "wordfreq max-count"`, `"has_plans": false`, `"plan_count": 0`。STATEの `current_phase: 5` / `status: completed` は今回の完了判定ではない。ROADMAPはPhase7とREQ-23..28を明記する。 [VERIFIED: 本調査公式CLI結果; .planning/STATE.md:3–8,91–99; .planning/ROADMAP.md:140–156]
- `graphify status` は `"disabled": true`。graphを有効化したり架空の関係を補わず、直接ソースで調査した。 [VERIFIED: 本調査公式CLI結果]
- 読取り時の `07-UI-SPEC.md` は `status: draft` / `Approval: pending`。既存HTML保持の設計資料として参照したがchecker承認を主張しない。 [VERIFIED: .planning/phases/07-wordfreq-max-count/07-UI-SPEC.md:1–8,206–216]

## Environment Availability

| Dependency / capability | Observation | Planning consequence |
|---|---|---|
| 既存CPython3.12 + pytest | version取得成功 | 既存環境で標準実行。PATH python3.14をpytestへ流用しない |
| Chromium executable | command/version取得成功 | browser起動/全画像閲覧/通信収集の成功までは未確認 |
| Native permission test user | `id -u` → `1000` | 後工程で実拒否を確認する。rootでの偽成立を避ける |
| ctx7 | `command -v ctx7` は出力なし | installせず公式docsへ直接fallback |
| 独立品質profile・画像閲覧・添付能力 | 本subagentは未実行/未確認 | 品質担当がpreflight。不能なら受入gapとする |

[VERIFIED: 本調査terminal; docs/wordfreq-min-count-verification.md:9–15; PRD:210]

## Assumptions Log

採用した製品判断に `[ASSUMED]` はない。要件・実装境界は読了済み仕様/現物へ結び付けた。新規検証ファイル名・将来件数・browser成功・CI成功・品質acceptedは推測せず、未作成/未実施と明記している。外部API説明は下記の取得限界を越えて断定しない。

## Open Questions

1. **仕様の未決事項はない。** 実装方式は承認designで固定されている。 [VERIFIED: 07-CONTEXT.md:51–53; design.md:19–26]
2. **品質能力の実行確認は後工程。** Browser executable存在と旧runbookだけでは全画像閲覧/通信観測可能性を保証できない。計画には製品変更前の能力gateと不足時の停止/報告を含める。 [VERIFIED: 本調査version結果; docs/wordfreq-min-count-verification.md:14–15]
3. **pytest所要時間/全suite件数は未測定。** 今回は研究のみで、既存/提案テストは実行していない。Builderが実数を記録し品質が対象headで再確認する。 [VERIFIED: 本調査実行範囲; PRD:209–210]

## Sources

### Primary: opened repository sources

- 承認原本 `.planning/argonauts/r-d4bcda40-prd.md:1–215`（proposal + 全spec scenario + tasks）、`openspec/changes/r-d4bcda40-max-count/design.md:1–38`。
- `.planning/phases/07-wordfreq-max-count/07-CONTEXT.md:1–54`、`.planning/REQUIREMENTS.md:84–102`、`.planning/ROADMAP.md:140–156`、`.planning/STATE.md:1–122`、`.planning/config.json:1–82`。
- `wordfreq/__main__.py:1–58`、`aggregator.py:1–17`、`tokenizer.py:1–18`、`sources.py:1–22`、`formatters.py:1–127`、`tests/test_cli.py:1–819`、`pyproject.toml:1–15`、`README.md:1–37`、`CONCEPTS.md:1–59`。
- `.planning/argonauts/r-d4bcda40-learnings.md:1–55`、`docs/wordfreq-min-count-verification.md:1–126`、旧baseline index先頭とjqケース抽出、旧driverのrequest/preflight/argv/scope定義。
- `07-UI-SPEC.md:1–216` は読取り時draft。独立承認/実行済み証拠としては採用しない。

### Official documentation: fallback lookup, not package installation

- [Python 3.12 argparse](https://docs.python.org/3.12/library/argparse.html)：ArgumentParser/add_argument/parse_args、自動help/usageのAPI参照。 [CITED: docs.python.org/3.12/library/argparse.html]
- [Python 3.12 collections](https://docs.python.org/3.12/library/collections.html)：Counterがdict subclassであること。 [CITED: docs.python.org/3.12/library/collections.html]
- [Python Sorting HOWTO](https://docs.python.org/3.12/howto/sorting.html)：sortedが新listを返すこと。tieの現行実装契約はrepoソースで確認した。 [CITED: docs.python.org/3.12/howto/sorting.html; VERIFIED: wordfreq/aggregator.py:11–17]

公式research-plan seamはdocs providerにcontext7を返したが、このsessionにはContext7 toolとctx7 executableがなく、web_extractで公式docsへ直接fallbackした。取得ページtitleはPython 3.12.16 documentation、実行interpreterは3.12.15（同一patch版とは主張しない）。extractが返した本文は導入部分に限定されたため、負数/全整数表記/安定性の細部をその抽出だけで検証済みにしていない。機械判定 `query classify-confidence --provider webfetch` は `"confidence": "LOW"`、cross-checkフラグを付けてもLOWだったため、research-storeにもLOWで保存した。repoに直接定義された判断と外部providerのconfidenceを混同しない。 [VERIFIED: 本調査公式CLI/web_extract/terminal結果]

## Metadata

- **Standard stack:** HIGH — repo設定と実version取得。版横断互換性や最新package版の推測なし。
- **Architecture:** HIGH — 現行compositionと承認designを両方読了。
- **Pitfalls / validation design:** HIGH — PRDのscenario、既存試験helper/spy/保存bytes経路、旧driverの専用制約を照合。
- **External docs provider:** LOW — 公式seamの実判定を保持。製品契約はそれに依存せず承認specと現物で確定。
- **Research validity:** この承認仕様と現行ソースが変わるまで。head変更時は行番号/CLI/品質対象を再解決する。
- **Actions intentionally not performed:** 実装、PLAN作成、新試験/pytest実行、baseline採取、browser起動/画像閲覧、品質受入、CI合格判定、commit/push/kanban。研究文書の完成は製品・Phase7の完成ではない。
