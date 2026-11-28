# 確認の記録 r-1bae0a69（light・手順版1.14）— 訂正版

この記録は、元の確認（カード t_8c56e252、試験したhead 05ac9a1）の記録の訂正である。元の記録の再試験の行に説明用の入力の表記が残り、そのまま実行できなかったため、全ての再試験の行を、入力の用意を含めてクリーンな作業場所からそのまま実行できるコマンドに直し、現在の依頼branchで全行を実行し直した。最終化はこの記録を最新の合格確認として参照する。

- 依頼: wordfreq に --min-length N を追加（既定1、--help、試験、README.md 不変）
- 対象: ToR-O3/argonauts-uat-20261114-public#50
- 試験したhead: c8b5ce88660e8532b42dc9d3e71857490fea02dd（= origin/argonauts/r-1bae0a69、取得直後）
- 基準: origin/v112-b c6b701b（依頼branchに取込み済み、workflowの変更なし）
- 製品・試験のコード: 05ac9a1 から c8b5ce8 までの差分は .planning・openspec（archiveへの移動 R100 と正本の更新）・docs/solutions だけで、wordfreq/・tests/ は同一
- 依頼者の判断コメント: 受付に無し
- 確認者: argonauts-uat-quality（カード t_504d8113）、2026-11-28

## 範囲
製品の変更：wordfreq/__main__.py（+3）、tests/test_cli.py、tests/test_max_count_verifier.py、tests/fixtures/max-count-scope/（PMが認めた過去試験用の固定コピー）、tests/fixtures/min-length-default.html。工程の文書：.planning・openspec・_bmad-output・docs/solutions の下（判定の対象外）。危険なパス：触れていない。README.md・tools/ は基準と差分なし。

## GSD Quick と OpenSpec
- Quick原本 .planning/quick/261128-jaf-wordfreq-min-length-option を再利用（新しいQuickは起動していない）。
- `gsd_run query verification.status <Quick原本>`：c8b5ce8 では `stale`。理由として示された対象は openspec/changes/r-1bae0a69-light/ の spec.md・tasks.md（最終化の準備で archive/2026-11-28-r-1bae0a69-light/ へ内容同一で移動）と tests/fixtures/max-count-scope/README.md（blob a491cb6 で 05ac9a1 と同一）。試験したコードの 05ac9a1 では同じ照会が `passed`。判定に使うコードと試験は変わっていないため、Quickの検証結果はこのheadでも有効と判断し、受入条件は下で直接再試験した。
- OpenSpec：`openspec list --json` で未完の変更なし。ARCHIVE-RESULT.json は change r-1bae0a69-light、archivedAs 2026-11-28-r-1bae0a69-light、specsUpdated true、added 3。`openspec validate --specs` は 2 passed・0 failed（exit 0）。`--strict` では wordfreq-cli が警告で失敗するが、警告は既存の要求（D-3、FR-5・FR-6、FR-7・FR-8）で、今回追加の ML-1〜3 は SHALL/MUST を含む（正本の基準からの差分は ML-1〜3 の追加だけ）。
- verify：ML-1（N未満の除外・境界・casefold後の長さ・併用）は `len(word) >= args.min_length` と test_min_length_boundary/casefold/unicode/composition/tie_order、ML-2（既定互換・空結果・HTML元総数）は default=1 と test_min_length_default_fixed（固定期待値）・test_min_length_empty、ML-3（help・試験・README不変）は help引数と test_min_length_help・下の再試験に対応。CRITICAL・WARNINGなし。

## 受入条件ごとの結果（c8b5ce8 で実行、作業場所のルート）
1. N未満を除外・Nちょうどは残す：`a bb ccc bb` に N=2 → stdout `2\tbb` `1\tccc`、exit 0（a除外、bb残る）。N=3 → `1\tccc` exit 0。N=4 json → `[]` exit 0。`ß ss a` に N=2 → `2\tss` exit 0。`a bb` に N=3 json → `[]` exit 0。合格
2. 既定1で従来互換：省略と `--min-length 1` の出力が一致（diff exit 0）。基準 origin/v112-b の実装を別のgit worktreeに取り出し、text/json/html の出力が一致（diff exit 0、worktreeは削除済み）。合格
3. --help に説明：`--min-length N        Exclude words shorter than N characters after casefold (default: 1)`、exit 0。合格
4. 追加試験と既存試験：min_length 29 passed（1051 deselected、exit 0）。全件 1080 passed（失敗0・skip0、213.70秒、exit 0、Python 3.12）。合格
5. README.md 不変：`git diff --quiet origin/v112-b HEAD -- README.md` exit 0。合格

## 再試験のコマンド（作業場所のルートで、bashで実行。入力は各コマンド内で用意する）
再試験: uv run --no-project --python 3.12 --with pytest python -m pytest -q -k min_length -p no:cacheprovider
再試験: uv run --no-project --python 3.12 --with pytest python -m pytest -q -p no:cacheprovider
再試験: printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --min-length 2; echo "exit=$?"
再試験: printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --min-length 3; echo "exit=$?"; printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --min-length 4 --format json; echo "exit=$?"
再試験: printf 'ß ss a\n' | python3.12 -m wordfreq /dev/stdin --min-length 2; echo "exit=$?"; printf 'a bb\n' | python3.12 -m wordfreq /dev/stdin --min-length 3 --format json; echo "exit=$?"
再試験: diff <(printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin) <(printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --min-length 1); echo "exit=$?"
再試験: B="$TMPDIR/r-1bae0a69-base" && git worktree add -q --detach "$B" origin/v112-b && diff <(printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --format text) <(cd "$B" && printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --format text) && diff <(printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --format json) <(cd "$B" && printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --format json) && diff <(printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --format html) <(cd "$B" && printf 'a bb ccc bb\n' | python3.12 -m wordfreq /dev/stdin --format html); rc=$?; git worktree remove --force "$B"; echo "exit=$rc"
再試験: python3.12 -m wordfreq --help; echo "exit=$?"
再試験: git diff --quiet origin/v112-b HEAD -- README.md; echo "exit=$?"

## 判定
合格（verdict: passed）。画像の確認は無し（CLIのみ）。品質の印と自動マージの予約はこの確認では行わない（最終化のレビューで行う）。

## 学び
- 再試験の行には入力の用意まで含める。ファイル引数のCLIは `printf ... | <cli> /dev/stdin` で、一時ファイルなしにそのまま再現できる。
- OpenSpecのarchiveで変更の場所が移ると、GSD Quickの検証は内容が同じでも stale になる。最終化後の確認では、試験したコードのheadでの照会と移動の内容同一を合わせて記録する。
