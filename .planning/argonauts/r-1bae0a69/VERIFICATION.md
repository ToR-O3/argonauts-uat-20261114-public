# 確認の記録 r-1bae0a69（light・手順版1.14）

- 依頼: wordfreq に --min-length N を追加（既定1、--help、試験、README.md 不変）
- 対象: ToR-O3/argonauts-uat-20261114-public#50（OPEN・draft・同じrepo）
- 試験したhead: 05ac9a143215cddeb755d4e5ebdf58035f366935（HEAD = origin/argonauts/r-1bae0a69 = PR headRefOid）
- 基準: origin/v112-b c6b701b
- 依頼者の判断コメント: 受付に無し（CI失敗コメントは旧head 55fa8af・e0681a8のもの）
- 確認者: argonauts-uat-quality（カード t_8c56e252）、2026-11-28

## 範囲
製品の変更：wordfreq/__main__.py（+3）、tests/test_cli.py、tests/test_max_count_verifier.py、tests/fixtures/max-count-scope/（PM判断 t_481cc860 で認めた過去試験用の固定コピー）、tests/fixtures/min-length-default.html。工程の文書：.planning・openspec・_bmad-output の下（判定の対象外）。
危険なパス：触れていない（.github/・pyproject.toml・lockファイル等の変更なし）。README.md・tools/ は基準と差分なし。

## GSD Quick と OpenSpec
- `gsd_run query verification.status .planning/quick/261128-jaf-wordfreq-min-length-option` → status: passed
- STATE.md の Quick 表に 261128-jaf（Verified）あり
- `openspec validate r-1bae0a69-light --strict` → valid
- `openspec instructions apply --change r-1bae0a69-light --json` → all_done、tasks 3/3
- OpenSpec verify：ADDED 要求 ML-1〜3 は wordfreq/__main__.py の引数と `len(word) >= args.min_length` 条件、tests/test_cli.py の試験に対応。design.md は light で任意（Not applicable）。CRITICAL・WARNING なし。

## 受入条件ごとの結果
1. N未満を除外・Nちょうどは残す：入力 `a bb ccc bb` に --min-length 2 → `2 bb / 1 ccc`（a除外、bb残る）、N=3 → `1 ccc`、N=4 json → `[]`、すべて exit0。`ß ss a` に N=2 → `2 ss`（casefold後の長さ）。合格
2. 既定1で従来の動作：同じ入力で省略と --min-length 1 が同一出力。基準 v112-b の wordfreq と text/json/html の出力をバイト比較し一致（cmp）。合格
3. --help に説明：`--min-length N  Exclude words shorter than N characters after casefold (default: 1)`。合格
4. 試験の追加と回帰：min_length 試験 29件成功、全件 1080件成功（失敗0、Python 3.12、240秒）。CI（pytest、push・pull_request）は対象headで success。合格
5. README.md 不変：`git diff --quiet origin/v112-b HEAD -- README.md` 差分なし。合格

## 再試験のコマンド（作業場所のルートで実行）
再試験: uv run --no-project --python 3.12 --with pytest python -m pytest -q -k min_length -p no:cacheprovider
再試験: uv run --no-project --python 3.12 --with pytest python -m pytest -q -p no:cacheprovider
再試験: python3.12 -m wordfreq <入力 a bb ccc bb> --min-length 2
再試験: python3.12 -m wordfreq --help
再試験: git diff --quiet origin/v112-b HEAD -- README.md

## 判定
合格（verdict: passed）。画像の確認は無し（CLIのみ）。

## 学び
- 既定互換の確認は、変更後の省略と明示1の比較だけでなく、基準branchの実装を git archive で取り出して出力をバイト比較すると独立に確かめられる。
- 提案（必須ではない）：.planning の Quick 配下に試験補助スクリプト record_red.py・capture_outputs.py が残っている。
