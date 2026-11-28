# 08-03 品質差戻しの修正記録

## 変えたこと

浅い取得でも、除外未指定時の出力を固定過去版と比較できるよう、試験用のGitオブジェクトを同梱しました。製品、依存、CI設定、通信処理は変更していません。

判断日時: 2026-11-28T14:45:42.849521+00:00
参照した依頼者原文: 「提案のまま進めてください（1〜5 すべて提案どおり）。」

## 原因と修正

品質が示したGitHub Actions run 46173111182の実ログを `gh run view 46173111182 --log-failed` で確認。1090 passed / 64 setup errors、固定過去版への `git ls-tree` がexit128でした。既存workflowはcheckout既定のdepth1。全履歴のある手元での成功では検出できませんでした。

修正前に `test_exclude_baseline_available_in_offline_shallow_checkout` を追加し実行。実depth1の複製で固定commitが欠落することを確認してから、同じ `git ls-tree` exit128で失敗しました（shallow-red.txt）。

固定commit `79d83ba14dd59d289d2ecd3e33c85e8de437972e` の実Gitから、commit・root tree・wordfreq tree・6blobの計9objectを `git cat-file` で取得。tests/fixtures/exclude-baseline-git-objects.json（12691bytes）にraw bytesをbase64で保存しました。取得元を候補ソースやCLI出力で代用していません。

試験は専用一時Git databaseにhash-objectで書き、返された全object IDを照合。固定commitからroot tree、wordfreq tree、各blobへGitの参照をたどって原本を抽出します。変更したblobのIDも再計算する攻撃でも、固定commitにつながる親treeは変えられません。依頼checkoutのGit databaseへは書かず、fetchしません。欠落・改変は失敗、skip/fallbackはありません。既存64比較のinterpreter/argv/env/input path/隔離module rootとstdout生bytes/status/stderrの比較は維持。

内容commit: 526b89cec8d6b7c440b5716ee6319aec2f68f479。

## 実行した確認

| コマンド | 実測 |
|---|---|
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_baseline_available_in_offline_shallow_checkout （修正前） | exit1、浅い取得の固定commit欠落で再現。shallow-red.txt |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_baseline or exclude_immutability or exclude_docs' | exit0、79 passed / 736 deselected、14.66s。shallow-green-final.txt |
| uv run --extra dev python .planning/argonauts/t_354e296c/verify-shallow-ci.py | exit0、depth1・固定commitなし・origin切断の隔離checkoutで既存 `python -m pytest` を実行。1159 passed、190.74s。shallow-suite.jsonとstdout/stderr原本 |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude | exit0、457 passed / 358 deselected、21.95s。exclude-repair-green.txt |
| python3 -m unittest discover -s .planning/argonauts/r-e0a2598f -p test_quality_handoff.py -v | exit0、19 tests OK、6.142s。handoff-tests-repair.txt |

新しい5件は実shallowの回帰1件と、基準file欠落/blob欠落/blob改変/blob改変後再hashの4件。全既存1154件を保持しました。64過去版比較も実行され、skipはありません。隔離checkoutで固定commitが無いことは全件実行後も確認しています。CPython3.12.15/pytest9.2.0で実行。GitHub自身の新head CI成功は、この手元の実測と区別します。

## 引渡しの限界

公式GSD readback: current phase8/current plan3/total3/status verifying、verification.status=missing。既存SUMMARYは保持して追記、state.advance-planやphase.completeは再実行しません。OpenSpec3.2、独立フェーズ検証、26edge/14UI/2禁止の独立判定、画像確認は未実施です。

今回の必須差戻しはCIの基準欠落だけを修正しました。記録のみのWR-01（形の崩れたhandoffのexit1/traceback）、WR-02（工程試験のprofile依存）、IN-01〜05は変更せず後続の判断材料として保持しています。これらを直した／独立品質合格とは主張しません。以前の実測原本は過去の対象に対する履歴として保持し、新しいtarget manifestと本修正原本を追加して区別します。
