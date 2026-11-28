---
title: "子pytestを起動する回帰試験ではbasetempを親コマンドだけに渡す"
date: 2026-11-28
category: best-practices
module: "wordfreq 回帰試験の起動環境"
problem_type: test_failure
component: testing_framework
severity: medium
symptoms:
  - "未変更製品のbaselineで子pytestがexit4になり、17件の試験が失敗した"
root_cause: test_isolation
resolution_type: environment_setup
tags: [pytest, basetemp, subprocess, environment, baseline]
---

# 子pytestを起動する回帰試験ではbasetempを親コマンドだけに渡す

## Problem

wordfreqの回帰試験には、一時コピー内でさらにpytestを起動して判別力を確かめるものがある。親用の一時ディレクトリ設定まで環境変数で継承すると、製品を変えていないbaselineでも試験基盤が失敗し、製品の回帰と取り違える。

## Symptoms

PR #50（記録時点でOPEN）の実装前baselineでは、`PYTEST_ADDOPTS`に`--basetemp`を設定してexportした実行が17 failed / 1031 passed / exit1になった。子pytestのエラーは次の通りだった。

```text
argument --basetemp: basetemp must not be empty, the current working directory or any parent directory of it
config source: via PYTEST_ADDOPTS
```

原本は `.planning/quick/261128-jaf-wordfreq-min-length-option/baseline.log`、起動方法と修正結果は同ディレクトリの `261128-jaf-EVIDENCE.md` の「開始時の実行失敗を含む全記録」にある。

## What Didn't Work

scratchの使用先を親子まとめて固定しようと、親の`--basetemp`を`PYTEST_ADDOPTS`にexportした。子の作業場所が親の一時ディレクトリ配下にある実行では、その継承値がpytestの引数検査で拒否された。これは製品の不具合を検出したREDではない。

## Solution

今回混入させた`PYTEST_ADDOPTS`を解除し、`--basetemp`はトップレベルのコマンド引数だけに渡した。以下は、pytestを利用できるPython環境でリポジトリのルートから実行する例である。`TMPDIR`には作業場所の外にある管理scratchを使う。

```sh
unset PYTEST_ADDOPTS
python -m pytest tests -q --basetemp="$TMPDIR/wordfreq-parent-pytest"
```

この起動方法に直した同じ実装前baselineは1048 passed / exit0だった。原本は `.planning/quick/261128-jaf-wordfreq-min-length-option/baseline-corrected.log`。製品編集前に成功を確認してから機能の実装へ進んだ。

## Why This Works

親コマンドの引数は子プロセスの環境変数にはならない。子pytestにはその子の一時領域を選ばせ、親の作業ディレクトリや削除対象を共有させない。この失敗は試験の起動環境に起因し、CLIの集計ロジックを変える必要はなかった。

現行の `tests/test_cli.py` の最小文字数の判別力試験も、子の環境から`PYTEST_ADDOPTS`を除去している。ただし、その局所対策だけで他の子pytestを含む全試験の起動環境まで保護できるわけではない。

## Prevention

- 入れ子のpytestを含む試験を回すときは、親専用の一時領域を環境変数でexportせず、親の引数として渡す。子pytestのexit4は引数・環境の問題かを先に確認し、製品の回帰と分けて記録する。
- 他の必要な`PYTEST_ADDOPTS`がある環境では、無条件に全設定を捨てるのではなく、親専用の`--basetemp`を取り除く。上の`unset`は今回追加した設定を解除した例である。
- この注意は無関係な子試験の失敗を一括で無視する理由にはならない。起動方法を直したbaselineと、変更後の全回帰をそれぞれ成功させる。

## Related Issues

- 実装前baselineの起動失敗と復旧は `.planning/quick/261128-jaf-wordfreq-min-length-option/261128-jaf-SUMMARY.md` の「Test execution and blocker」にも記録されている。
- 製品変更後の独立確認は `.planning/argonauts/r-1bae0a69/VERIFICATION.md` を参照。ここに記載した1048件は実装前baselineであり、変更後の試験件数とは区別する。
