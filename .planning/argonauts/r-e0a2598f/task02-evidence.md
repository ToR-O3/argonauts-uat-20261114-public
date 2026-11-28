# 08-03-02 実測と対象の区別

実装はBuilderの引渡し準備のみ。品質の起動・予約・独立判定・OpenSpec3.2完了はしていません。

- `python3 -m unittest discover -s .planning/argonauts/r-e0a2598f -p test_quality_handoff.py -v` RED: exit1、19 testsの対象アサーション失敗。loadable fail-closed skeletonは実際にexit2/implementation_pendingを返し、valid pending packageの期待exit0に失敗。checker-red.txt原本、checker-red.jsonを公式 `gsd_run check tdd-red-evidence ... --raw` に渡しexit0/RED_EVIDENCE_OK。missing-command/import/setup失敗をREDに使っていません。
- 同コマンドGREEN: exit0、19 tests/OK、checker-green.txt原本。欠落/空/権限なし原本（rootでもmode0を拒否）、誤digest、command/argv/input/environment/stdout/stderr/exit/expected-vs-actual/参照欠落、AC欠落、形式不正/不存在/stale対象、scope path欠落/変更、26edge/14UI/2禁止/traceの欠落・重複・source改変・偽green、品質義務/Q6配送・手順欠落、早すぎるquality pass/3.2チェックをそれぞれ名前付きで拒否。未来のVERIFICATION/quality-evidenceなしの正常系も成功。
- `python3 .planning/argonauts/r-e0a2598f/prepare-handoff.py`: exit0、実原本から148 execution recordsを作成（歴史/候補64組×2、実除外18、回帰2）。fixtureの実行結果を製品原本に流用していません。
- `python3 .planning/argonauts/r-e0a2598f/check_quality_handoff.py --repo-root . --handoff .planning/argonauts/r-e0a2598f/quality-handoff.json`: exit0/HANDOFF_READY_ONLY、scoped_files19/edges26/ui14/prohibitions2、quality_statusとopenspec_3_2はpending。対象はd30dd316ae6b73dcf10376ce9bd75cfc134b0c2c。scopeはtracked wordfreq/**,tests/**,README.md,pyproject.toml全件、各Git bytesとworktree bytes/digestを照合。
- `python3 .planning/argonauts/r-e0a2598f/check-real-controls.py`: exit0、actual packageの隔離コピーは成功、actual linked cli-captures.jsonを削除したコピーはexit2/original_missing、実在するが古いbaseline headへ変えたコピーはexit2/target_stale、Q6配送義務を削除したコピーはexit2/obligation:Q6。real-package-controls.jsonおよびreal-control-*.txtは実stderr/stdout/argv/exitの原本。現物のpackageや原本には変異を入れていません。
- `python3 .planning/argonauts/r-e0a2598f/run-regressions.py`: exit0。内部の指定除外コマンド `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude`: exit0、452 passed/358 deselected/18.58s。内部の全件 `uv run --extra dev python -m pytest -q`: exit0、1154 passed/188.74s。*-final-stdout.txt/*-final-stderr.txtとregression-executions.jsonはそのままの出力。stderrは既存uv requires-python警告のみ。pytest自体の失敗/警告なし。task01の188.61s全件実行とは別の最終実行です。

## 初期の内容対象と報告head

report-only commitに自己hashを埋めることはできないため、target_headは最新のscope変更commitを固定します。checkerは `git log -1 HEAD -- wordfreq tests README.md pyproject.toml` と照合し、scope全パスのGit/現在bytesが一致する場合のみ報告だけの子孫を許します。判定の出力にtarget_headと現在のreporting_headを両方出し、品質は必ず新たにexact HEADを解決し独立に実行します。これは計画の「初期target/source manifest」「報告をmanifestから外して自己参照を避ける」に対応します。報告headが違っても独立品質の合格を再利用できるという意味ではありません。

全後続品質義務Q1..Q6はPLANのMandatory later independent quality節の原文を省略せずJSON/Markdownへ転記し、毎回原本から比較。公式GSD検証経路とOpenSpec verify Skillの実在パス/digestを参照だけに保存しました。5 concurrency backstopはhuman_needed/insufficient_spec、禁止2件はflagged-unverified、全UIはpending-independent-qualityで保持。画像閲覧0、geometry/可読性/実通信の観測なし。過去の合格、Builderの現在の成功、fixture検査、将来の独立品質は混ぜていません。
