# Phase 06: README min-count three example - Research

**Researched:** 2026-11-24（terminal `date -I`）
**Domain:** README局所追記、既存CLIの3形式直接実行、独立品質への文字証拠配送
**Confidence:** MEDIUM（ソース読取りに基づく計画調査。製品CLI・試験本体は未実行）

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** READMEの「wordfreq の実行」に `python -m wordfreq input.txt --min-count 3` の例1つを追加。既存例・説明・末尾の検証A行・改行を保持する。READMEへ検証用3例を追加しない。必要な局所説明のみ可。追加前に当該例が無いことを確認する（REQ-25、OpenSpec1.1）。
- **D-02:** 同一UTF-8実ファイルinput.txt・閾値3で例そのものの既定textと `--format json` / `--format html` だけを加えた形式を各自実行。top等で条件を変えない。3以上と3未満の語を含める（REQ-26、1.2）。
- **D-03:** 各実exit0・stderr、閾値ちょうど/超の保持と未満の除外、語・回数・回数降順/同数初出順を照合。text count-tab-word/末尾改行、JSON配列word/count、HTML静的UTF-8/3列表/1始まり順位/basename/min-countとtop前総数を既存契約と照合。既存API/公開形式は変更しない。
- **D-04:** Builderと品質はそれぞれ実行主体・作業場所・検証head・入力パスと全文・完全なコマンド・実exit/stdout/stderr・期待値との照合を `_bmad-output/initiative-r-5f8197e8/` 内の文字原本へ保存。stdoutを他形式から合成しない。未実行・未確認・不一致・原本欠落を成功にしない（REQ-27、1.2/2.1）。
- **D-05:** 品質が同条件を独立再実行し、全git差分で製品変更がREADMEのみか確認。VERIFICATION.mdとCLI証拠文書を標準添付しPMがread_fileで判定できる形にする。画像やzipをPMへ要求しない。画像不要なら0枚と理由、画像を用いた場合は品質が実閲覧した枚数・内容・結果を文字記録。Builderは独立品質未実施を明記してhandoffする（2.1）。
- **D-06:** コード・設定・依存・公開入出力・試験ファイル・新fixture・検証ツール追加禁止。BMAD/OpenSpec/計画/検証文字文書は工程成果として区別。既存CLI/既存試験を使い、不一致でコード修正へ勝手に拡大しない。新UI設計/Architecture不要だがhtml出力確認は必須。
- **D-07:** specsは公式skip_specs:true経路でskipped。proposal/tasksを承認した。specを捏造しない。受入後のsync/archiveは最終化工程であり、このPLANには含めない。
- **D-08:** 各PLAN最大3tasks。同じ依頼branch argonauts/r-5f8197e8へ番号順に直列積上げ。taskの終了時点で検証入力とコマンドが使えること、phase検証時に先行PLAN含む全成果があること。独立PLANは他PLAN成果の有無にかかわらず検証可能。fails_whenは対象の誤動作を失敗として観測する条件を書く。未作成の検証スクリプトを計画中に試さない。security/nyquist/plan_check/pattern_mapperは開始値維持。

### Claude's Discretion
入力内容と一時準備方法、既存CLI/試験での照合手順、文字証拠の分割とPLAN分割のみ。入力は工程証拠用で製品fixtureとしない。新試験・補助スクリプト追加や製品改修は裁量に含めない。

### Deferred Ideas (OUT OF SCOPE)
コード/試験/依存/CI/UI変更、過去phase修復、sync/archive、マージ、学習公開。今は計画のみで製品コマンドは実行しない。
</user_constraints>

## Summary

READMEの既存コードブロックへ指定コマンドを1行挿入するだけにする。現行ブロックには閾値2のJSON例があるが閾値3の指定例はない。既存説明は既に閾値・順序・総数・エラーを説明しているため、説明の追加も原則不要。末尾の `検証A: v1.12 の通しの確かめ（2026-11-22）` は保持する。[VERIFIED: README.md:5-35]

受入の本体は既存試験の改変ではなく、Builderと品質それぞれによる同じ実入力の3回実行と文字照合。既存試験は形式・min-count契約の回帰確認として併用するが、新例そのものの実行証拠には代用しない。品質実行をBuilderのPLAN内で自己認定しない。[VERIFIED: openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md:5-10]

**Primary recommendation:** 1つのPLAN・最大3tasks（READMEの局所追記、Builderの直接検証＋回帰、文字原本と独立品質handoff）を推奨。独立品質は別の実行主体が同じ手順を実施する工程と明記する。以下の新しい入力・証拠ファイル名・コマンド例は設計提案であり既存ファイルの存在や実行成功を示さない。

## Project Constraints (from HERMES.md)

`HERMES.md` と `.hermes/HERMES.md` は read_file がともに File not found を返した。`.hermes/skills/` と `.agents/skills/` も検索対象パスが存在しなかった（本セッションのツール観測）。追加のproject-local指示は発見していない。固定のbranch/カード入力を優先し、この調査ではgit/kanban操作をしない。[VERIFIED: user task context]

設定の `"nyquist_validation": true`、`"plan_check": true`、`"pattern_mapper": true`、`"security_enforcement": true` は変更しない。`"agent_skills": {}`。[VERIFIED: .planning/config.json:21-63]

公式launcher経由の `gsd_run query init.phase-op 6` は phase_found=true、phase_number="06"、has_context=true、has_plans=false を返した。graphify statusはdisabledで、今回有効化しない。STATEの過去完了表示はPhase6追加を否定する根拠にせず、過去phase修復を計画しない。[VERIFIED: official GSD CLI session output; .planning/STATE.md:93-101]

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|---|---|---|
| REQ-25 | README.mdの「wordfreq の実行」に `python -m wordfreq input.txt --min-count 3` の実行例を1つ追加する。既存例・説明・末尾の検証A行と改行を保持し、例1つと必要な局所説明だけの差分にする。利用者向け変更はREADME.mdのみでコード・設定・依存・公開入出力・試験ファイルの追加変更を禁止する。 | 既存ブロックを読んで不在確認後、指定行のみ挿入。差分全文・元READMEとの比較。 |
| REQ-26 | 同一UTF-8実ファイル・閾値3で、追加例そのものの既定textと形式指定だけを加えたjson/htmlを実際に実行する。3以上と3未満の語を含め、exit0・stderr・保持/除外・語/回数/初出順、textのタブ、JSON配列word/count、HTML3列表/順位/basename/min-countとtop前総数を既存契約と照合する。 | 下記の提案入力、3実CLI、既存test_cli/test_formatters、直接文字照合。 |
| REQ-27 | Builderと独立品質がそれぞれ実行した作業場所・検証head・入力パスと全文・完全なコマンド・実exit/stdout/stderr・期待値との照合をinitiative配下の文字原本に記録する。品質は全git差分のscopeを確認しVERIFICATION.md等へ対応付け、原本を添付する。PMはread_fileで判断でき、画像・圧縮物を開く必要がない。画像があれば閲覧枚数/内容/結果を記録する。未実行・未確認・不一致は合格としない。コード修正へ無断拡大しない。 | 実行主体別fresh evidence root、原本索引、実行単位のexit保存、独立品質で全差分照合。 |
</phase_requirements>

上表のDescriptionは要件原文。[VERIFIED: .planning/REQUIREMENTS.md:92-94] OpenSpec対応は1.1→REQ-25、1.2→REQ-26/27、2.1→REQ-27。[VERIFIED: openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md:5-10]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| 指定例の掲載 | Documentation / Static | — | 製品差分はREADMEのみ（D-01/D-06）。 |
| UTF-8取得・正規化・閾値・順位 | CLI / local processing | — | 既存処理を呼び出すだけ。コードは触らない。 |
| text/json/html生成 | CLI formatter | stdout capture | それぞれ実CLIのstdoutを独立保存。 |
| 検証・scope・受渡し | Engineering evidence | 独立品質 / PM | 文字原本と判定を分離し、実行主体も分離。 |

既存フローは `FileSource` → `iter_tokens` → `count_words` → 元総数 → 閾値適用 → `top_words` → 形式分岐 → stdout。コードには `default=10`、`default=1`、`choices=["text", "json", "html"], default="text"`、`if count >= args.min_count`、`sys.exit(0)` がある。[VERIFIED: wordfreq/__main__.py:13-54] 集計順位は `sorted(counts.items(), key=lambda wc: -wc[1])[:n]`。[VERIFIED: wordfreq/aggregator.py:11-17]

## Standard Stack

| Component | Existing version / contract | Use |
|---|---|---|
| ローカル製品 | `name = "wordfreq"`, `version = "0.1.0"`, `dependencies = []` | READMEどおり `python -m wordfreq`。外部の同名パッケージをinstallしない。 |
| 既存試験 | `dev = ["pytest"]` | 既存ファイルだけを回す。 |
| text/json整形 | `f"{count}\t{word}\n"`、`json.dumps(items, ensure_ascii=True) + "\n"` | 末尾改行まで照合。 |
| 標準ツール | jq / cmp / diff / od / iconv | JSON抽出・比較・byte補助確認。追加ツール作成なし。 |

製品・試験宣言の出典：[VERIFIED: pyproject.toml:5-14]。整形の原文出典：[VERIFIED: wordfreq/formatters.py:6-14]。標準ツールはcommand -vで存在確認済み（本セッション）。新規導入はないためregistry更新調査・package install・Package Legitimacy Auditは対象外。

## Environment Availability

- 本セッションの `python --version` は `Python 3.14.9`、`/usr/bin/python3 --version` は `Python 3.12.15` を返した。PATH上のpythonと過去の試験用Pythonを混同しない。[VERIFIED: terminal environment probes]
- `pytest --version` の環境照会は `ModuleNotFoundError: No module named 'pytest'`。pytestの試験実行・collectionはしていない。PATH上のpytestをそのままPLANに採用してはいけない。[VERIFIED: terminal environment probe]
- 既存runbookは `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` を使う。[VERIFIED: docs/wordfreq-min-count-verification.md:14-19; .planning/argonauts/t_8a90bad6-init-plan.json:58-90] そのpytestファイルはread_fileで読め、版宣言は `__version__ = version = '9.0.3'`。[VERIFIED: /home/Yuki/.local/lib/python3.12/site-packages/_pytest/_version.py:21-22] この経路の実行可否は後続Builderの実コマンドで検証する。存在だけを成功扱いしない。
- jq/cmp/diff/od/iconv/teeおよびuvはcommand -vで発見。uvによるinstallは推奨しない。上記既存環境が動かない場合は環境blockを記録し、依存追加や試験修正で救済しない。[VERIFIED: terminal environment probes; 06-CONTEXT.md:19-21]

## Architecture Patterns

### 1. 最小文書差分

既存ブロックの最初の通常実行行の直後に指定行を挿入する。末尾に例を足さない。既存閾値2例の置換も不可。編集前にread_fileで全文と不在を確認、編集後にread_fileと差分で指定例1回・既存全内容保持を照合する（単に文字列があるだけでは不足）。現在のREADMEの改行byteはterminalのodでLF、末尾もLFであることを観測した。[VERIFIED: README.md:9-15,35; terminal `od -An -tx1 README.md`]

### 2. 同一入力と独立した3 stdout

以下の**提案の検証入力1つだけ**を採用する（製品fixtureでなく後続がwrite_fileで作る工程一時入力）。末尾LFを含むUTF-8。数値期待は**計画値であり、実行結果ではない**：

```text
Zoo apple APPLE zoo banana hello HELLO hello Hello zoo apple banana once
```

改善版の計画期待：hello=4、zoo=3、apple=3、banana=2、once=1。表示はhello4 → zoo3 → apple3。zooとappleは語昇順と逆の初出順なので回帰を検出できる。元総数13、表示回数和10（terminal `expr 4 + 3 + 3 + 2 + 1` →13、`expr 4 + 3 + 3` →10で計算確認）。閾値の「超」「ちょうど」「未満」を同じ入力で判定できる。入力と期待値は研究提案であり新しい既存契約ではない。

契約根拠は `count\tword\n`、`{"word": <str>, "count": <int>}`、`text|json|html`、初出順、元総数：[VERIFIED: openspec/specs/wordfreq-cli/spec.md:51-64,81-90,114-138,176-208]。

### 3. 原本は文字ファイル、受入は別文書

出力先は承認された `_bmad-output/initiative-r-5f8197e8/`。[VERIFIED: 06-CONTEXT.md:17] この配下に実行主体別のfresh root（例：`verification/builder/<実run>/` と `verification/quality/<実run>/`）を提案する。新runごとに別rootを作り、過去原本を上書きしない。これは工程文書・生の文字証拠であり新検証ツールではない。

各rootへ入力原本、text stdout、JSON stdout、HTML stdout、各stderr（空もファイルとして保持）、各exit、実行記録Markdown、既存試験stdout/stderr/exit、差分原本、チェック結果索引を置く。HTMLもread_fileで全文を読める原本のまま置く。タブは見た目でなくodの `09`、LFは `0a` で補助照合し、その出力も文字証拠にすることを推奨する。

## Don't Hand-Roll

| Problem | Don't Build | Use Instead |
|---|---|---|
| CLI結果の捕捉 | Python/Node-inline、補助shell script、新検証ファイル | 直接CLIのリダイレクトと直後のexit記録 |
| JSON解析 | 自前parseまたはJSONから他stdoutを合成 | jqで実JSON原本を解析し独立した計画期待と照合 |
| HTML構造と静的性 | 新しいHTML validator / browser pipeline | 既存test_formatters＋実HTMLの全文読取り |
| 読める証拠配送 | 画像・tar・zip中心の引渡し | Markdown索引＋生のstdout/stderr/exit原本 |
| 独立品質 | Builderがroleラベルだけ変えて再実行 | 品質本人が別rootで同条件を実行 |

これらの禁止・配送制約は承認範囲に基づく。[VERIFIED: 06-CONTEXT.md:17-24; openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md:5-10]

## Code Examples

以下は**後続Builder・品質用の提案手順**。この調査では実行していない。新スクリプトは保存しない。`E` は各自が選定した実行主体別fresh evidence rootの絶対パスに設定し、完全展開したコマンドも実行記録へ記載する。準備ファイルはwrite_fileで作成する。

1. 作業場所は各自の対象headのrepo root。対象head・実行者・実task/run・cwd・Python版・環境を記録。`input.txt` が既存なら上書きせず停止し、衝突のない準備方法を確認する。repo rootの `input.txt` は今回だけの工程一時ファイルとし、改善版入力をwrite_fileで作成、同じ内容を証拠rootにも保存する。3回の間は変更せず、後でcmpする。製品fixtureとして追加しない。
2. 実行は次の3つだけ。textに明示formatを足さず、topも変えない。各コマンドのすぐ次の操作で `$?` をexitファイルに保存する。証拠用のリダイレクトはCLIの引数ではない。set -eで非0時の記録を飛ばさない環境で個別に実施する。

```sh
python -m wordfreq input.txt --min-count 3 > "$E/text.stdout.txt" 2> "$E/text.stderr.txt"
printf '%s\n' "$?" > "$E/text.exit.txt"
python -m wordfreq input.txt --min-count 3 --format json > "$E/json.stdout.json" 2> "$E/json.stderr.txt"
printf '%s\n' "$?" > "$E/json.exit.txt"
python -m wordfreq input.txt --min-count 3 --format html > "$E/html.stdout.html" 2> "$E/html.stderr.txt"
printf '%s\n' "$?" > "$E/html.exit.txt"
```

上記は既存CLI引数の組合せであり、将来の証拠ファイル名は提案値。CLIの根拠原文は `parser.add_argument("filename")`、`parser.add_argument("--min-count", type=int, default=1)`、`parser.add_argument("--format", choices=["text", "json", "html"], default="text")`。[VERIFIED: wordfreq/__main__.py:15-18]

3. textの独立した期待ファイルは `4\thello\n3\tzoo\n3\tapple\n` を実TAB/LFでwrite_fileし、cmpでbyte比較する。実stdoutはread_fileでも読み、odでTAB/LFを確認する。JSONの独立期待は次の配列。jqは実JSONを正規化して期待との比較に使い、stdout原本は置換しない。

```json
[{"word":"hello","count":4},{"word":"zoo","count":3},{"word":"apple","count":3}]
```

```sh
jq -e '. == [{"word":"hello","count":4},{"word":"zoo","count":3},{"word":"apple","count":3}]' "$E/json.stdout.json"
od -An -tx1 "$E/text.stdout.txt"
od -An -tx1 "$E/json.stdout.json"
iconv -f UTF-8 -t UTF-8 "$E/html.stdout.html" > /dev/null
```

jq比較は実JSONの配列・キー/値/型・順序・余計な要素を検査し、末尾LFの契約は別途odで照合する。iconvのexitだけでHTML構造合格としない。HTMLはread_fileで全文を読み、次を判定表に明記する：

- `<!doctype html>`、`<meta charset="utf-8">`、内包styleのみ、script/外部参照なし。
- 見出し `順位` / `単語` / `回数`、データ行は順位1 hello4、順位2 zoo3、順位3 apple3だけ。
- 表より前にbasename `input.txt`、元総数13。表示和10・種類数3ではない。実cwdや入力ディレクトリがtitle/属性等へ漏れていないこと。
- banana/onceのデータ行なし、各実exit=0、各実stderr空。入力は実行前後cmpで不変。

HTML固定の文字契約は `class="rank"`、`class="word"`、`class="count"`、`<meta charset="utf-8">`、`class="filename-value"`、`class="total-value"`、`順位`、`単語`、`回数`。[VERIFIED: wordfreq/formatters.py:28-43,108-122] 新入力についての結果判定は後続の実原本読取りで行う。

4. 実行記録には期待値列と実測列を分け、比較コマンドの実exit・一致/不一致・原本パスを付す。空stderrも原本パス＋0 byteで追跡する。完全なstdoutはリンク先原本に置き、省略表示や他形式からの生成で代用しない。作業用input.txtの削除は証拠コピーと不変照合後、今回作った一時入力だけに限定する。
5. 後続の品質は対象headと依頼基点の全git差分を確認（commit済み差分だけでなくstaged/unstaged/untrackedも含む）、製品READMEと工程文書を分類する。基点をHEAD直前だと決め付けない。README以外の製品変更、新試験・設定・ツール追加があれば不合格。研究担当はgit操作を実施していない。

## Validation Architecture

### Test Framework

| Property | Value |
|---|---|
| Framework | 既存pytest。読取りで確認した既存3.12用版宣言は9.0.3。PATH上pytestはimport失敗。 |
| Config file | pyproject.tomlには製品/開発依存宣言。新設定追加なし。 |
| Quick run command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k 'min_count_selection or min_count_help_and_readme_example' -x` |
| Full suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` |
| Source existence | tests/test_cli.py、tests/test_formatters.pyを本セッションでread_file済み。実行時間・件数・成功は未測定。 |

上記環境経路の根拠：[VERIFIED: docs/wordfreq-min-count-verification.md:14-22]。既存test名の原文は `test_min_count_help_and_readme_example`、`test_min_count_selection`、`test_min_count_empty_total`、`test_min_count_selection_hashseed`、`test_min_count_selection_preserves_counter_and_shared_pairs`。[VERIFIED: tests/test_cli.py:672-793] `test_min_count_help_and_readme_example` が確認する掲載例は `python -m wordfreq input.txt --min-count 2 --top 1 --format json` であり、新しい閾値3例の掲載検査ではない。[VERIFIED: tests/test_cli.py:672-682]

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command / inspection | File Exists? |
|---|---|---|---|---|
| REQ-25 | 新例1つ、既存全文/末尾/改行保持、README以外の製品差分なし | 文書/scope直接検査 | read_file README＋全差分照合。既存補助：`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py::test_min_count_help_and_readme_example -x` | Yes（掲載新例自体は人/agent直接照合） |
| REQ-26 | 例そのものの3実CLI、閾値境界・順序・形式 | integration + direct CLI | 上のQuick run＋3形式の直接コマンド/原本照合 | Yes（既存test_cli） |
| REQ-26 | text/JSON構造、HTML3列表・静的UTF-8・元総数 | unit + raw inspection | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_formatters.py -x` ＋実HTML全文 | Yes |
| REQ-27 | 実行主体/cwd/head/入力/exit/stdout/stderr/期待比較と独立品質 | evidence audit / manual-only | read_file両主体の索引・全原本・VERIFICATION.md、品質の全差分分類 | 新test不要。本人性と独立実行はpytestで代替不可 |

### Sampling Rate

- **Per task commit:** task終了時点に存在する入力・原本・READMEを直接照合し、製品編集taskはQuick runを実行。未作成の検証ファイルを呼ばない。
- **Per wave merge:** 既存Full suite commandと対象3形式の原本照合。全試験の実件数・skip・exitを記録。成功未確認をgreenと書かない。
- **Phase gate:** Builder結果＋独立品質の同条件再実行・scope・証拠監査が揃ってから受入判断へ。full suiteに既存履歴由来の失敗があれば本件成功として隠さず、過去phase修復へ拡張せず報告する。
- 30秒以内などの所要時間はこの調査では測定していない。後続が実測を残す。

### Wave 0 Gaps

**新規検証ファイル追加はなし。** 既存試験で既存契約を確認し、新例の掲載・3実CLI・文字原本の完全性は直接照合する。これを「既存自動試験だけで全受入が自動化済み」とは書かない。環境上のgapはPATHのpytest不整合であり、既存3.12経路を後続で実行確認する。新fixture、新conftest、新検証スクリプト、framework installのWave0 taskを作らない。[VERIFIED: 06-CONTEXT.md:19-24]

## Common Pitfalls

1. **閾値2の既存掲載testがgreenなら新例も検証済み、とする。** 新例の不在→追加1回の直接照合と、既定textの指定コマンド実行を別に必要とする。[VERIFIED: tests/test_cli.py:672-682; tasks.md:5-6]
2. **同数語の期待を語昇順にする。** 正規化後初出順が現契約。提案入力はzoo→appleの同数で検出する。[VERIFIED: openspec/specs/wordfreq-cli/spec.md:81-90]
3. **HTML総数を表示和にする。** `total = sum(counts.values())` は閾値より前。今回の計画値は13で、表示和10ではない。[VERIFIED: wordfreq/__main__.py:34-44]
4. **stdoutをtee/パイプに流して最後のコマンドのexitを記録する。** 直接リダイレクトし直後のCLI exitを保存する。これは提案する証拠捕捉パターン。
5. **既存browser検証driverを今回の新ツールとして拡張する。** 今回は見た目変更なし。UI gate入力はfrontend=trueでもhasFrontendEvidence=false/block=false、新UI設計不要（依頼固定入力）。HTML文字照合は省略しない。画像は0枚とその理由を明記する。[VERIFIED: user task context; proposal.md:25]
6. **Builder再実行を独立品質と書く／原本配送前にacceptedにする。** Builderの引渡し時点では独立品質pending。品質が自分の原本とVERIFICATION.mdを標準添付する。[VERIFIED: 06-CONTEXT.md:17-18]

## Security Domain

security_enforcementは維持。今回は新エンドポイント・auth・保存サービスを導入しない。次表は本phaseへの適用判定であり、製品全体のASVS認証主張ではない。[VERIFIED: proposal.md:17-25; .planning/config.json:49-51]

| ASVS Category | Applies | Existing control / verification |
|---|---|---|
| V2 Authentication | No new surface | ローカルCLIと文書のみ。認証追加なし。 |
| V3 Session Management | No new surface | セッション機能追加なし。 |
| V4 Access Control | Limited | 自分の入力だけ準備し、既存input.txt/他主体の原本を上書きしない。 |
| V5 Input Validation | Yes, existing behavior | 既存parserの `if args.min_count < 1` と `parser.error("--min-count must be >= 1")` を変更せず、全形式の既存試験を使う。 |
| V6 Cryptography | No new use | 新暗号・秘密情報を導入しない。 |
| Output encoding / injection | Yes, existing behavior | `escape(value, quote=True).replace("\r", "&#13;")`、静的HTMLの既存試験を維持。 |

入力検査とescapeの根拠：[VERIFIED: wordfreq/__main__.py:25-28; wordfreq/formatters.py:17-19]。静的性の既存検査は `assert_static_document` が許可タグ/属性とCSS外部参照を検査する。[VERIFIED: tests/test_formatters.py:94-133]

| Threat pattern | STRIDE | Mitigation for this phase |
|---|---|---|
| 別head/他主体stdoutを実測と偽認 | Spoofing / Repudiation | 主体・実cwd・head・argvと原本を一対一で記録。独立品質が再実行。 |
| HTMLへパス/秘密が混入 | Information disclosure | 無害な入力のみ、basename限定と全文HTMLを照合。 |
| 既存入力/原本の上書き | Tampering | fresh rootと存在衝突時停止、入力の前後cmp。 |

以上は計画上の安全対策で、実施済みという主張ではない。

## State of the Art

このphaseは新技術導入でなく既存契約の文書補足。旧語昇順の履歴に戻さず、現在の初出順を確認する。過去の大規模browser baseline/capture/finalize工程は本件へコピーしない。[VERIFIED: openspec/specs/wordfreq-cli/spec.md:81-90; 06-CONTEXT.md:9,19,45]

## Assumptions Log

未確認事項は既存3.12 pytest経路の現在の実行可否、試験件数/所要時間/成否、後続の実行head・証拠root、実出力。これらを成功と仮定していない。提案入力・期待値・新しい証拠名は設計値であり、既存ファイル発見を主張していない。新たな製品仕様についての仮定はない。

## Open Questions

スコープ/受入条件の未決事項なし。実行段階の確認点は既存pytest環境のみ。使えなければ無断installやコード改修をせずblockを報告する。独立品質は本研究・Builder完了では実施済みにならない。

## Sources

### Primary: opened this session
- `06-CONTEXT.md:9-45` — 固定判断・工程範囲。
- `.planning/REQUIREMENTS.md:88-100` — REQ-25/26/27。
- `.planning/STATE.md:93-101` — Phase6追加と過去phase範囲外。
- `.planning/config.json:21-63` — gate維持・agent_skills空。
- `README.md:5-35` — 既存例・出力説明・末尾行。
- `openspec/changes/r-5f8197e8-readme-min-count-three/{proposal,tasks}.md` — 1.1/1.2/2.1。
- `openspec/specs/wordfreq-cli/spec.md:51-90,114-138,176-223` — 既存形式・順序・元総数・閾値。
- `wordfreq/__main__.py:13-54`, `wordfreq/aggregator.py:11-17`, `wordfreq/formatters.py:6-127` — 現処理と固定HTML。
- `tests/test_cli.py:425-441,672-817`, `tests/test_formatters.py:9-48,94-175` — 既存検査と限界。
- `docs/wordfreq-min-count-verification.md:14-22` — 既存pytest環境コマンド。
- `pyproject.toml:5-14` — 既存製品/開発依存宣言。

### Tool observations
- 公式launcher経由 init.phase-op 6、graphify status、classify-confidence。classify-confidenceはcontext7/refでMEDIUM、未知provider officialでLOWを返した。外部providerによる新規library調査は不要（既存repoだけの文書phase）として行わず、provider由来のHIGHを装わない。
- terminal runtime/tool availability、date、od、expr。製品CLI・pytest本体/collection・git/kanbanは未実行。pytestへの呼出しは版照会のみでimport失敗を記録した。

## Metadata

- Standard stack confidence: MEDIUM — 既存宣言と試験環境ファイルを読取り、実行可否は後続確認。
- Architecture confidence: MEDIUM — 処理ソース・現契約・承認範囲を相互照合。新構成導入なし。
- Pitfalls confidence: MEDIUM — 現testが閾値2例を検査する点、PATHのpytest失敗、初出順と元総数のソースを確認。
- Validity: repoの現契約・承認範囲が変わるまで。実行headと環境は後続で再確認。
