# 確認 r-a7606d74（light・手順版1.14）

- 依頼: wordfreq に `--min-length N` を追加（既定1、N未満を除外、--help・試験、README.md不変）
- 依頼者の判断（2026-11-28T13:23:21.058370+00:00）: casefold後の文字数、Nは1以上の整数だけ
- PR: ToR-O3/argonauts-uat-20261114-public#52（OPEN・draft・同じrepo）
- 試験した対象head: `6ce25c6bfbe3fc8282ec994017f5e27b8a052c90`（ローカルHEAD・origin/argonauts/r-a7606d74・PRのheadRefOidが一致）
- 基準 origin/v112-b `27d3594` はheadに含まれる（baseの取込み不要）
- 環境: python3.12（/usr/bin）、pytest 9.0.3（PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages）。CIは python 3.12 + `python -m pytest`

## 範囲
製品の変更：wordfreq/__main__.py（+8行）、試験 tests/test_cli.py・tests/test_max_count_verifier.py・tests/fixtures/max_count_scope/__main__.py。工程の文書：50件（判定の対象外）。全54ファイル。危険なパス・.github/workflows・README.md の変更なし。

## 公式の検証結果
- GSD `gsd_run query verification.status .planning/quick/261128-vh0-wordfreq-min-length` → `status: stale`。原因は覆域の `.planning/argonauts/r-a7606d74/builder/final-cli-index.json` がbranchに無い（Builderのローカルの記録ファイルで未commit）。製品・試験ファイルの変更ではない。Quick原本 VERIFICATION.md のfrontmatterは `status: passed`（Builder担当範囲、head c763457。以後の差分は工程文書だけ）。製品の判定は下の独立の再試験で行った。
- OpenSpec `status --change r-a7606d74-light --json` → isComplete true（proposal/specs/design/tasks done）
- OpenSpec `instructions apply --change r-a7606d74-light --json` → progress 3/3、remaining 0
- OpenSpec `validate r-a7606d74-light --strict` → `Change 'r-a7606d74-light' is valid`（exit 0）
- openspec-verify: Completeness 3/3 tasks・ADDED要求4件（LEN-1〜4）、Correctness 4/4（__main__.py 18–22・35–36・46 と試験で各シナリオ確認）、Coherence 設計どおり（元Counter/総数を保持し選択条件にANDで追加）。CRITICAL/WARNING なし。

## 受入条件ごとの確認（head 6ce25c6）
1. N未満を除外し境界Nを保持：`a bb ccc bb` で N=2 → `2 bb`,`1 ccc`（aは除外、bbは残る）text/json とも exit0。N=3 → `1 ccc`。casefold：`ß SS a 日本語 12 __` で N=2 → ss2・日本語1・12 1・__1、N=3 → 日本語1。不正値 0・-1・x・1.5・値なし → exit2、stdout 0バイト、stderrに使い方エラー。**合格**
2. 既定1で従来互換：基準 v112-b の別worktreeと同じ入力で、省略時・`--min-length 1` の出力が text(49B)/json(280B)/html(2989B) すべてバイト一致（cmp）。**合格**
3. --help に説明：`--min-length MIN_LENGTH  minimum length N (positive integer): Unicode code points after casefold; exclude words shorter than N; include N or more (default: 1)`、exit0。**合格**
4. 追加・回帰試験：対象263 passed、全体1311 passed（exit 0）。**合格**
5. README.md 不変：`git diff --quiet origin/v112-b HEAD -- README.md` 成功。**合格**
6. HTML（仕様LEN-4の画面確認）：`a bb ccc bb a a dd` を N=2 でHTML出力し、Hermes標準ブラウザーで1280×900・320×900（DPR1）表示。両幅で scrollWidth=clientWidth（横はみ出し無し）、行は 1 bb 2 / 2 ccc 1 / 3 dd 1、総出現回数は絞込み前の7。N=9（全除外）では0行と空の案内文、総数7。品質が目で見た画像は1枚（ui-empty-1280.png：ファイル名・総数7・見出し帯・案内行を確認。日本語の字形はブラウザー環境のフォント不足で空白表示、DOMの文字は正しい）。他の2幅の確認はDOMの計測値による。**合格**

## 再試験
再試験: PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages python3.12 -m pytest tests/test_cli.py -k min_length -q -p no:cacheprovider
結果: 263 passed, 650 deselected in 8.46s（exit 0）
再試験: PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages python3.12 -m pytest -q -p no:cacheprovider
結果: 1311 passed in 211.90s（exit 0）
再試験: printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --min-length 2
結果: `2	bb` / `1	ccc`（exit 0）
再試験: printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --min-length 3
結果: `1	ccc`
再試験: printf 'ß SS a 日本語 12 __\n' | python3.12 -m wordfreq /dev/stdin --min-length 3
結果: `1	日本語`
再試験: printf 'a\n' | python3.12 -m wordfreq /dev/stdin --min-length=0
結果: exit 2、stdout空、`wordfreq: error: --min-length must be >= 1`
再試験: python3.12 -m wordfreq --help
結果: exit 0、--min-length の説明あり

## 判定
verdict: passed。必須の指摘なし。
記録（提案）: GSDのQuick検証が、branchに無いBuilderのローカル記録を覆域に含むため stale と出る。最終化の前に覆域の扱いを整えると公式の状態がそろう。baseline/index.json に実行環境の環境変数一式が入っている（前回レビューの提案と同じ）。

## 学び
GSDの検証の覆域にcommitしない記録ファイルを入れると、製品が変わらなくても stale になる。覆域はbranchにある原本だけにする。
