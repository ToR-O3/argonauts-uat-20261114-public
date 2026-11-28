# Quick 261128-jaf — Builder実測証拠

## 結論と対象状態

**再開後: Task 1/2/3完了。全回帰1080 passed / exit0。独立品質・PM受入・CIは未確認。**

以下の初回記録は失敗履歴として保持する。最新状態・出典・再実行結果は末尾「Task 3再開」を正本とする。VERIFICATION.mdは過去のgaps_foundのまま変更せず、親の再判定対象。

- workspace: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-b/.worktrees/t_23cd547e`
- 開始HEAD: `7ba06e8e757fb86f93ca6a63b13bdc8110df2777`
- 最終検証HEAD: `075ac7f06869b1dd400c2f365e29aac5b6936df8`
- Task 1 commit: `9dc83cb592a84b8dbbc9b7abfc9cb368d5f2f48e`
- Task 2 commit: `075ac7f06869b1dd400c2f365e29aac5b6936df8`
- 最終dirty状態: `?? .planning/quick/`のみ。製品・試験・tasksの未commit変更なし。
- 開始時には `.planning/quick/` と今回の `openspec/changes/r-1bae0a69-light/tasks.md` がuntracked。tasksは実施済み1.1/1.2だけチェックして各task commitへ含めた。1.3は未チェック。
- READMEはHEAD/worktree、index、開始HEAD→最終HEADの3比較とも0 bytes。`readme-head.diff`, `readme-index.diff`, `readme-plan.diff`。
- `git diff --check`: exit0 (`diff-check.log`)。
- 製品変更は `wordfreq/__main__.py` の3行追加のみ。tokenizer/aggregator/formatters、依存設定、README、既存証拠原本、STATE、ROADMAPは未変更。

## 実行環境と再実行方法

既定 `python3`: Python 3.14.9、`python3 -m pytest --version` は `No module named pytest`、exit1。
PATHの `pytest` も `/usr/bin/python3` を使い同じくpytest不在。`/usr/bin/python3.12 -m pytest --version` も利用不可。
既存のuv cache環境を読取り確認し、次の既設環境を再利用した。install・依存追加・環境作成なし。

```sh
export PY=/home/Yuki/.cache/uv/archive-v0/93Y_xVGwEKUhHy-t/bin/python
export Q=.planning/quick/261128-jaf-wordfreq-min-length-option
unset PYTEST_ADDOPTS
"$PY" --version
"$PY" -m pytest --version
# Python 3.14.7 / pytest 9.2.0
"$PY" -m pytest tests/test_cli.py -k min_length -q --basetemp="$TMPDIR/quick-261128-jaf-final-targeted"
"$PY" -m pytest tests -q --basetemp="$TMPDIR/quick-261128-jaf-regression"
```

TMPDIRはactive Builder profileの管理scratch:
`/home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/cache/scratch`。
新規変異はpytest tmp_path内のcold copyのみ。追加worktree・branch変更なし。
公式GSD判定は指定launcherをsourceして `gsd_run query state.load`, `query agent-skills gsd-executor --skills-only`, `query git.base-branch --is-protected`, `check tdd-red-evidence` を使用。保護branch判定false、configured skillsなし。phase advance/completeとSTATE更新は実施していない。

### 開始時の実行失敗を含む全記録

最初のbaselineは `PYTEST_ADDOPTS="--basetemp=$TMPDIR/quick-261128-jaf-pytest"` をexportしたため、既存の子pytestにも親ディレクトリが継承され、子pytestがexit4になった。結果は **17 failed, 1031 passed / exit1 / 206.77s** (`baseline.log`, `baseline.exit`)。製品不具合の証拠ではなく実行環境設定の失敗であり、合格扱いしていない。

製品編集前に `unset PYTEST_ADDOPTS` し、basetempをトップレベルコマンド引数だけに移して同じ全試験を実行:
`"$PY" -m pytest tests -q --basetemp="$TMPDIR/quick-261128-jaf-baseline"`
→ **1048 passed / exit0 / 246.37s** (`baseline-corrected.log`, `baseline-corrected.exit`)。
以後はこの修正済み起動方法。既存試験コードは変更していない。

## TDDの実順序

以下のコマンドは全てrepo rootで実在するtests/test_cli.pyへ実行。`"$PY" -m pytest tests/test_cli.py`を共通prefixとする。追加coverageが既に通る場合はREDと呼んでいない。

|順序|selector / 追加引数|実測|原本|
|---|---|---|---|
|1|`-k 'min_length_default_fixed and omitted' -q`|3 passed, 653 deselected / exit0 / 0.27s、製品編集前|default-before.log|
|2|`-k min_length_tracer -q -s --junitxml="$Q/tracer-unwired.xml"`|1 failed, 656 deselected / pytest exit1、CLI exit2|tracer-unwired.log/xml|
|3|引数type=int/default=1のみ追加後、`-k min_length_tracer -q -s --junitxml="$Q/tracer-selection-red.xml"`|1 failed, 656 deselected / pytest exit1、CLI exit0だがaが残る|tracer-selection-red.log/xml|
|4|長さ条件追加後、`-k min_length_tracer -q -s`|1 passed, 656 deselected / exit0 / 0.08s|tracer-green.log|
|5|全形式境界追加、`-k 'min_length_default_fixed or min_length_tracer or min_length_boundary' -q`|10 passed, 650 deselected / exit0 / 0.53s|task1.log|
|6|casefold追加後、`-k min_length_casefold -q`|3 passed, 660 deselected / exit0|casefold.log|
|7|Unicode追加後、`-k min_length_unicode -q`|3 passed, 663 deselected / exit0|unicode.log|
|8|合成追加後、`-k min_length_composition -q`|3 passed, 666 deselected / exit0|composition.log|
|9|同頻度初出順追加後、`-k min_length_tie_order -q`|3 passed, 669 deselected / exit0|tie-order.log|
|10|空状態追加後、`-k min_length_empty -q`|3 passed, 672 deselected / exit0|empty.log|
|11|help試験追加後、`-k min_length_help -q --junitxml="$Q/help-red.xml"`|1 failed, 675 deselected / exit1 / 0.22s|help-red.log/xml|
|12|metavarとhelp追加後、`-k min_length_help -q`|1 passed, 675 deselected / exit0 / 0.13s|help-green.log|
|13|変異試験追加後、`-k min_length_discrimination -q -s --basetemp="$TMPDIR/quick-261128-jaf-discrimination"`|3 passed, 676 deselected / exit0 / 2.08s|discrimination.log|
|14|`-k min_length -q --basetemp="$TMPDIR/quick-261128-jaf-targeted"`|29 passed, 650 deselected / exit0 / 2.73s|task2.log|
|15|最終HEADで `-k min_length -q --basetemp="$TMPDIR/quick-261128-jaf-final-targeted"`|29 passed, 650 deselected / exit0 / 2.70s|final-targeted.log|

固定HTMLは未変更CLIから `default-before.html` を取得・read_fileで読取り、完全なliteral fixture `tests/fixtures/min-length-default.html` を製品変更前に保存。cmp exit0。以後fixture再生成なし。text/jsonは固定バイトliteral。省略・明示1は別paramで各固定原本に比較している。

未配線REDのCLI出力は `(2, b'', b'usage: ... unrecognized arguments: --min-length 2\n')`。これは境界比較の証拠ではない。
選択欠落REDは `(0, b'2\tbb\n1\ta\n1\tccc\n', b'')`。期待は `b'2\tbb\n1\tccc\n'`。GREENはこの期待に一致。
help REDは `--min-length N` 欠落のassertionで失敗。help GREENで選択肢・N文字未満除外・default:1を確認。

### 公式RED分類と手順上の制約

`record_red.py`は実際のJUnit XMLを変更せずJSONへ格納する補助。`tracer-selection-red.json`, `help-red.json` にcommand/exit/expected/actual/semanticAssessmentがある。
両方の `gsd_run check tdd-red-evidence ... --raw` は **RED_EVIDENCE_OK / tests1, fail1, report_errors空** (`tracer-selection-red-verdict.json`, `help-red-verdict.json`)。
Task 1の機械分類はGREEN後に実施しており、事前認可としては主張しない。実行時のREDはXMLとconsoleへ保存済みで、その場で観測してから実装した。helpはGREEN前に機械分類済み。
ユーザー指定のtask単位atomic commitに従い、独立したRED-only commitは作っていない。一般GSD TDDのRED専用commit規則との差異としてSUMMARYにも明記する。workflow.tdd_modeはfalse。

## 境界判別力 — 初期REDとは独立

`test_min_length_discrimination`はcontrol / ignore-length / exclusiveの3コピーを別tmp_pathへ作成。実装seam `and len(word) >= args.min_length` の一致箇所数1をassert。子pytestは `-k min_length_boundary` のみ、JUnitを解析。

- control: **child exit0, 3 passed**。
- ignore-length (`and True`): **child exit1, 3 failed**。N未満のaが残り、全形式の期待値比較でAssertionError。
- exclusive (`>`): **child exit1, 3 failed**。Nちょうどのbbが消え、全形式の期待値比較でAssertionError。
- 各childのtests=3, errors=0, skipped=0をassert。失敗はassert_output_bytes内と確認。未知引数exit2、collection/import/syntaxエラーや0件を検出成功と数えていない。
- 外側pytest: **3 passed / exit0**。`discrimination.log`に実際の子出力全文。
- 最終全回帰でも既存max-count変異試験は成功。既存seamは未変更。

## 入出力と要求対応

`"$PY" "$Q/capture_outputs.py"` を最終HEADで実行し、**25 real CLI subprocess outputs**を保存した。これは合成応答でなく実際のCLI出力。`actual-outputs.json`に入力、argv、exit、完全stdout/stderr、`outputs/<case>/<format>.stdout`に未変更バイト列。helpも同JSONへ保存。全呼出しexit0・stderr空を実測assert。

|要求 / Spec|試験・入力（各text/json/html）|固定期待と実測照合|
|---|---|---|
|ML-FR-1 / ML-1|boundary: `a bb ccc bb`, N2|bb:2, ccc:1、aなし。HTML total4|
|ML-FR-1 / ML-1|casefold: `ß ss a`, N2|ss:2のみ、HTML total3|
|ML-FR-1 / ML-1|unicode: `日 日本 日本語 _ 12`, N2|日本:1,日本語:1,12:1、HTML total5|
|ML-FR-2 / ML-2|default/explicit-one: `a bb ccc bb`|固定text `2\tbb\n1\ta\n1\tccc\n`、固定JSON bb/a/ccc、固定完全HTML、total4、stderr空・exit0|
|ML-FR-2 / ML-1/2|composition: `a a a bb cc bb cc dddd`, N2,min2,max2,top1|bb:2のみ、HTML total8|
|ML-FR-2 / ML-1|tie: `a zz aa zz aa`, N2,top1|zz:2（辞書順aaではない）、HTML total5|
|ML-FR-1/2 / ML-2|empty: `a bb`, N3|text空、json `[]\n`、HTMLデータ行0・既存空メッセージ・total2|
|ML-FR-3 / ML-3|filenameなし `--help`|`--min-length N`, `Exclude words shorter than N characters after casefold (default: 1)`、exit0、stderr空。README差分0|
|ML-FR-4 / ML-3|全追加・全既存pytest|追加29成功。全回帰は下記1件失敗のため未達|

## 全回帰の未解消blocker

最終HEADで実行:

```sh
"$PY" -m pytest tests -q --basetemp="$TMPDIR/quick-261128-jaf-regression"
```

**1 failed, 1076 passed in 248.70s / exit1、skipなし** (`regression.log`, `regression.exit`)。
失敗: `tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only`。

`scope_repo` fixtureは現在の製品をcold copyするが、`tools/verify_wordfreq_max_count.py:487-492`は過去max-count受入用CLIの固定SHA-256だけを承認する。そのため正当なmin-length追加を含む現在のCLIは `ValueError: unapproved product/README change: wordfreq/__main__.py` になる。
旧固定SHAは `9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba`、今回CLIの実測SHAは `76d94464a947552d8036d1848440acca1c6975424c966bf37a8d5ed702cba246`。
この1件は修正済み開始baselineでは成功しており、今回変更と無関係な既存失敗とは扱っていない。

単独再現も実施:
`"$PY" -m pytest tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only -q --basetemp="$TMPDIR/quick-261128-jaf-blocker"`
→ **1 failed / exit1** (`blocker-reproduction.log`)。

過去の検証原本・固定承認ハッシュを書き換えたり、試験をskipして全回帰成功を装うことはしていない。親へ、過去製品を使うscope fixtureの分離などの修正範囲を判断するよう引継ぐ。今回のTask 3の「全回帰失敗なし」は未達なので1.3をチェックせず、Task 3完了commitも作らない。

## 未実施・未確認

- 全回帰成功、Task 3完了、要求ML-FR-4の全面達成は未確認（上記失敗あり）。
- 独立品質の再実行・受入、PMの原本読取り、CI結果は未実施。
- STATE更新、通常phase advance/complete、push/PR/merge/kanban操作はユーザー指定により未実施。
- README/既存原本/依存変更なし。SUMMARY/EVIDENCE/ログ/補助スクリプトはcommitしていない。

## Task 3再開 — PM承認済みfixture分離と全回帰

### 対象と修正範囲

- 再開開始HEAD: `e0681a88729290f8cdc24ee1596781bd0330f91f`、branch `wt/t_23cd547e`、SEQUENTIAL=true。同じworkspaceのみ。開始dirtyは親が変更したPLANのみ。
- PM承認 `t_481cc860` / 元カードコメント208をPLAN Task 3から読取り。追加Quickなし。
- RED commit: `c51d7fa`。GREEN/Task 3 commit: `d8ed666d7bc73e60c52f29c4c7fde3a22b7838d5`。
- 全回帰実行時HEADはRED commitで、fixture修正・固定データ・CLI拒否paramは未commit。全回帰成功後にOpenSpec 1.3をチェックし、同じ検証済みコードをGREEN commitへ保存。製品は再開開始から無変更。
- 修正: `scope_repo`のPRODUCT全6ファイルとREADMEのみを固定歴史fixtureからコピー。test_cli.pyとpyproject.tomlは従来どおり現在の入力。固定fixture rootは`__file__`由来で現行ROOTに依存しない。
- 新規試験2件は一時的な偽current checkoutのCLI/READMEへmarkerを追記し、fixtureが取り込まないこととclean scope成功を検査する。実製品・READMEは編集しない。
- 既存append-only成功、7種damage拒否を保持。追加CLI改変拒否1件も成功。skip/xfail・assert削除・hash緩和なし。検証器・過去原本・固定hashは無変更。

### 出典の実測

出典commit: `27d359409c585cbb923b42aef3298cf6dfc28094`。
`git show <commit>:<path>` のstdoutバイト列を `tests/fixtures/max-count-scope/<path>` に保存。現行出力から期待値を生成していない。
全7ファイルのsourceバイト列とfixtureを再度 `git show ... | cmp - ...` で比較し全一致 (`resume-source-match.log`)。各SHA-256は `resume-source-hashes.txt` およびfixtureの`PROVENANCE.md`に記載。

- 出典path `wordfreq/__main__.py`: `9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba`。
- 出典path `README.md`: `5a0ca56634033c569765f1c3002962b15357b45821cbfd1245b86862a54aeb3a`。
- 上記は変更していない `validate_scope` の固定承認hashと完全一致。新規fixtureは過去証拠原本の置換ではなく、historical scope unit testだけの入力。

### 実コマンドと順序

共通環境（各pytestへ個別のbasetemp引数、exportによる子pytest衝突なし）:

```sh
export SEQUENTIAL=true PYTHONDONTWRITEBYTECODE=1
unset PYTEST_ADDOPTS
export PY=/home/Yuki/.cache/uv/archive-v0/93Y_xVGwEKUhHy-t/bin/python
export Q=.planning/quick/261128-jaf-wordfreq-min-length-option
```

Python 3.14.7 / pytest 9.2.0を再確認。installなし。下表の各コマンドは `"$PY" -m pytest` に続く引数であり、consoleは同名.logへstdout/stderr両方を保存、実exitは同名.exitへ保存した。

|順序|引数|実測|ログstem|
|---|---|---|---|
|1 既存失敗再現|`tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only -q --basetemp="$TMPDIR/quick-jaf-resume-repro"`|1 failed / exit1 / 0.11s、固定hash不一致のValueError|resume-repro|
|2 新規独立性RED、修正前|`tests/test_max_count_verifier.py -k scope_fixture_independent -q --basetemp="$TMPDIR/quick-jaf-resume-red" --junitxml="$Q/resume-fixture-red.xml"`|2 failed, 54 deselected / exit1 / 0.15s。両方ともmarkerを取り込む意図したassertion失敗|resume-fixture-red|
|3 fixture修正後|`tests/test_max_count_verifier.py -q --basetemp="$TMPDIR/quick-jaf-resume-scope"`|56 passed / exit0 / 10.38s|resume-scope-green|
|4 min_length追加試験|`tests/test_cli.py -k min_length -q --basetemp="$TMPDIR/quick-jaf-resume-min-length"`|29 passed, 650 deselected / exit0 / 3.17s|resume-min-length|
|5 CLI拒否param追加後|`tests/test_max_count_verifier.py -q --basetemp="$TMPDIR/quick-jaf-resume-scope-final"`|57 passed / exit0 / 10.33s|resume-scope-final|
|6 全tests|`tests -q --basetemp="$TMPDIR/quick-jaf-resume-full"`|1080 passed / exit0 / 291.70s、fail/error/skipなし|resume-regression|

RED XMLをjqの`--rawfile`で無改変のままrecord JSONへ格納した。公式launcherを各GSDコマンドでsourceし、`gsd_run check tdd-red-evidence "$Q/resume-fixture-red.json" --raw` を**GREEN編集前**に実行。`resume-fixture-red-verdict.json` は **RED_EVIDENCE_OK / tests2, fail2, report_errors=[]**。logを読取り、対象assertionが動作しfixture/load/syntax失敗でないことを確認後RED-only commit、その後fixture修正。CLI拒否paramは既存拒否挙動のcoverage GREENであり新たなREDとは呼ばない。refactorなし。初回Task 1分類がGREEN後だった事実は上記履歴を保持し、今回の事前分類で遡って適合したとは主張しない。

### 最終範囲確認と引継ぎ

- GREEN後HEADは `resume-final-head.txt`。コードcommit前後とも`git diff --check` exit0 (`resume-diff-check.log/.exit`)。
- READMEのHEAD/worktreeとindex比較は0 bytes (`resume-readme-head.diff`, `resume-readme-index.diff`)。
- 再開開始→最終HEADの製品、README、検証器、過去原本、STATE、ROADMAP、VERIFICATION差分も0 bytes (`resume-protected.diff`)。
- 追加は独立性2件＋CLI拒否1件で、元1077件から全1080件へ。以前の1076pass/1failは削除・上書きせず保存。
- OpenSpec 1.3は全回帰exit0を読取り確認した後のみ完了。Task名・順序変更なし。
- コード・fixture・OpenSpecはcommit済み。親のPLAN、今回SUMMARY/EVIDENCE、resume-*ログはdocs担当の親へ未commitで引継ぐ。STATE完了一覧・ROADMAP・VERIFICATIONは編集していない。
- ML-FR-4 / ML-3のBuilder全回帰条件を今回満たした。独立品質の再実行、verifier再判定、PM受入、CIは未確認であり別工程。旧VERIFICATIONのgaps_foundを本Builderが書き換えていない。
