# wordfreq --max-count：品質のCLI・CIの証拠（フェーズ検証 7）

- 確認者: profile argonauts-uat-quality、カード t_dc0281b7、run 135
- 確認した対象head: b4e9037892f01582554a96df2389c9e0458d7c35（origin/argonauts/r-d4bcda40 と PR ToR-O3/argonauts-uat-20261114-public#24 の headRefOid が同じ。PRはOPEN・draft・同じrepo）
- この文書を保存したcommitは、確認した対象とは別のcommit（`.planning/` だけを変える報告のcommit）。
- 実行環境: /usr/bin/python3（CPython 3.12.15）、pytest 9.0.3、PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages、LANG=C.UTF-8、PYTHONHASHSEED=0、cwd=カードのworktree。新しいinstallはしていない。
- 依頼者の判断（2026-11-25 21:22 JST、t_87068596、作者 default）: 画面の画像の取得と比較は受入条件に入らない。HTMLは中身（単語と回数）を試験で確かめれば足りる。ほかの受入条件と品質の独立した確認はそのまま。
  → ブラウザは起動していない。実際に見た画像は0枚。Range・geometry・通信の観測・canaryもしていない。これらは「未実施」であり、合格とは書かない。

## 1. runbookのCLI（docs/wordfreq-max-count-verification.md）
| 手順 | 正確なargv | exit | 結果 |
|---|---|---|---|
| review-session | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_max_count.py --mode review-session --role quality --output-dir .planning/argonauts/r-d4bcda40/quality/final-01 --baseline-dir .planning/argonauts/r-d4bcda40/baseline` | 0 | 138ケース・全suite。213秒。manifest.json の SHA-256 は 8b77fbca…27e3d |
| validate | 同じ形で `--mode validate`（output-dir・baseline-dir は同じ） | 0 | 固定baselineのバイト列と照合した |
| finalize | `... --mode finalize --role quality --output-dir …/final-01 --baseline-dir …/baseline --review-ledger .planning/argonauts/r-d4bcda40/quality/reviews-01.json` | 0 | verdict quality-content-reviewed、ledger の SHA-256 は 594f36f2…46ebc。finalize の後も manifest の SHA-256 は変わっていないことを読み戻した |
baselineは取り直していない（固定root `.planning/argonauts/r-d4bcda40/baseline`、変更前のhead 8efbfaa）。

## 2. 実際に読んだケース（入力 `beta beta beta alpha gamma alpha delta`。別の入力のものは別に書く）
原本は `final-01/<id>/input/`、`stdout.bin`、`stderr.bin`、`stdout.html`。stderrはすべて0バイト、exitはすべて0。
| id | オプション | stdout |
|---|---|---|
| max1-text | --max-count 1 | `1 gamma` `1 delta` |
| max2-text / -json / -html | --max-count 2 | alpha2, gamma1, delta1（HTMLは同じ3行で、総数は7） |
| min2max2-text | --min-count 2 --max-count 2 | `2 alpha` |
| min2max3-text と -reverse-text | min2 max3 と、順序を入れ替えたもの | どちらも beta3, alpha2 |
| top1-text | --max-count 2 --top 1 | `2 alpha` |
| zero-text / negative-json / inverted-text | max0 / `--max-count=-1` / min3 max2 | 空 / `[]`+LF / 空 |
| triple-text/json/html（入力 beta×4 zoo×3 apple×2 pear×2 single） | min2 max3 top1 | zoo3。HTMLの総数は12（フィルタ前） |
| many-text / many-all-text（選択後12種類） | max2 / max2 top99 | 10行 / 12行 |
| tie2-text（`Zoo apple APPLE zoo banana`） | min2 max2 top2 | zoo2, apple2（初出順） |
| unicode-empty / unicode-selected（`Straße STRASSE 日本語 日本語`） | max1 / min2 max2 | 空 / strasse2, 日本語2 |
| large-* と default-*・explicit-min-*・min-top-* | 上限を省略したものと --max-count 1000000 | 変更前の固定バイト列と一致（validate exit0） |
| max2-html, hostile-html | — | `<script` と `http` を含まない |

## 3. 品質が直接実行したCLI（入力ファイルは scratch/qcli.lFrC/input.txt。内容は上と同じ）
| argv（`/usr/bin/python3 -m wordfreq` の後） | exit | stdout | stderr |
|---|---|---|---|
| `input.txt --min-count 2 --max-count 3 --format json`（READMEの例。cwd は一時ディレクトリ、PYTHONPATH はrepo） | 0 | `[{"word": "beta", "count": 3}, {"word": "alpha", "count": 2}]`+LF | 空 |
| `<input>` | 0 | beta3 alpha2 gamma1 delta1 | 空 |
| `<input> --max-count 2 --format json` | 0 | alpha2, gamma1, delta1 のJSON | 空 |
| `<input> --max-count +2 --format text` / `--max-count 02` | 0 | alpha2 gamma1 delta1 | 空 |
| `<missing.txt> --max-count 2` | 1 | 空 | `…missing.txt: [Errno 2] No such file or directory…` |
| `<dir> --max-count 0` | 1 | 空 | `[Errno 21] Is a directory` |
| `<input> --max-count abc` / `<missing> --max-count abc` | 2 / 2 | 空 | usage と `invalid int value: 'abc'`（ファイルが無くても先に2で終わる） |
| `<input> --max-count`（値なし） | 2 | 空 | `expected one argument` |
| `<missing> --max-count 1.5` | 2 | 空 | `invalid int value: '1.5'` |
| `<missing> --min-count 0 --max-count 3` | 2 | 空 | `--min-count must be >= 1` |
| `<missing> --top 0 --max-count -1` | 2 | 空 | `--top must be >= 1` |
| `--help` | 0 | `--max-count MAX_COUNT` を含む | 空 |
ソースの順序（read_file wordfreq/__main__.py、SHA-256 9a5e38d9…9eba）: 35行目 元のCounter → 36行目 元の総数 → 37〜39行目 AND で選ぶ → 40行目 top_words → 46〜50行目 同じ pairs を3つのformatterへ渡す。

## 4. 試験
- 全suite（review-session の中）: `/usr/bin/python3 -m pytest tests/ -q --junitxml=…/final-01/suite.xml` → 1048 passed、failures/errors/skipped 0、exit 0、208.42秒（30秒を超えるので遅い。速いとは書かない）。原本は suite.json、suite.xml、suite.stdout.txt。
- 一部だけの実行（Nyquist・security の監査が実行）: `pytest tests/test_cli.py -k max_count -q` は292 passed（exit0）、`pytest tests/test_max_count_verifier.py -q` は54 passed（exit0）。
- RED/GREEN: builder/07-01 の原本。製品を変える前の先行REDは276件中213件が失敗（exit1）、GREENは276件（exit0）。実装した後の変異REDを、先行REDの代わりにはしていない。

## 5. CI（対象head b4e9037 について1回だけ読んだ。待たない。Checks API は使わない）
- 必須の一覧（`gh api --paginate repos/ToR-O3/argonauts-uat-20261114-public/rules/branches/v112-b`）: `argonauts/quality`、`pytest`
- Actions: run 45626948539（pull_request）は completed/success、job pytest も success。run 45626937818（push）は completed/success、job pytest も success。どちらの head_sha も b4e9037。
- commit status: なし。`argonauts/quality` は、フェーズ検証では付けない（最終確認で付ける）。
- 受付に残っている「CI失敗：pytest head a2bb383」は古いheadのもの。今のheadの最新は success。

## 6. 範囲（工程の文書は .planning, openspec, _bmad-output, .compound-engineering, docs/solutions。判定の対象外）
製品の変更: wordfreq/__main__.py（+3/-1）、README.md、tests/test_cli.py（追記だけ）、tests/test_max_count_verifier.py、tools/verify_wordfreq_max_count.py、docs/wordfreq-max-count-verification.md。危険なパスには触れていない（.github/、pyproject.toml、lock、依存はどれも変わっていない）。
