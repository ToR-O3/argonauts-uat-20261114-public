# Phase 1: CI pytest gap — REQ-07

## 1. CI ジョブの実測

- 対象: `ToR-O3/argonauts-uat-20261114-public`、依頼branch `argonauts/r-5a3b8a3f`。
- 検査時の HEAD: `2f16d5ca33ff051c68883148a4b18558c8be8d45`（前 PLAN の品質合格 head）。base `origin/main` は取込み済み。
- 実測日時: 2026-11-17T04:14:31Z の検証開始後。
- `git ls-files -- '.github/**' '.gitlab-ci*' '.circleci/**' '.buildkite/**' '.azure-pipelines/**' 'azure-pipelines*' 'Jenkinsfile*' '.travis.yml' 'bitbucket-pipelines.yml' 'appveyor.yml' '.woodpecker*' '.drone*'`: 出力なし、終了コード 0。
- `git ls-tree -r --name-only origin/main -- .github .gitlab-ci.yml .circleci .buildkite azure-pipelines.yml Jenkinsfile .travis.yml`: 出力なし、終了コード 0。
- `git ls-files` の全追跡ファイルも確認。CI 設定定義は見つからなかった。
- `gh api repos/ToR-O3/argonauts-uat-20261114-public/actions/workflows --jq '{total_count, workflows: [.workflows[] | {name,path,state}]}'`: `{"total_count":0,"workflows":[]}`、終了コード 0。

結論: 調べた依頼branch・base の追跡設定と GitHub Actions 登録には pytest ジョブがない。未登録の外部 CI まで不在と断定するものではない。

## 2. ローカル全試験の証拠

repo 直下で既存の導入済み環境を使用（新規インストールなし）:

```text
python --version
Python 3.14.9
python -m pytest
platform linux -- Python 3.14.9, pytest-9.2.0, pluggy-1.7.0
collected 43 items
43 passed in 1.06s
```

終了コード 0、failed 0。内訳は aggregator 4、CLI 21、formatters 4、sources 5、sources_boundary 3、tokenizer 6。これはローカルでの結果であり CI の成功ではない。

## 3. block 判定と未達条件

REQ-07 の「リポジトリ CI の pytest ジョブで通る」は未充足。workflow の追加・変更は Bot の権限外であり、人による CI ジョブ追加と対象 head での実行証拠が必要。

OpenSpec task 3.3 の完了は「有無確認と block 判定の準備」の完了だけを示す。REQ-07 の CI 合格、phase の受入、CI 設定の作成は意味しない。本 PLAN はこの引継ぎ記録を作る工程であり、同じカードの品質レビューと後続フェーズ検証へ未達を渡す。`phase.complete` は実行しない。

## 4. 人への依頼と再検証

1. 人が対象の CPython 3 の版を確定し、依頼branch に CI ジョブを 1 本追加する（例: `.github/workflows/`）。Bot への workflow 権限追加は不要。
2. repo 直下で pytest 開発依存を導入し、`python -m pytest` を実行する。ランタイム依存を追加しない。
3. この依頼の対象 head で実行し、CI run・job 名・Python 版・head SHA・終了コード 0 と全試験成功のログを提示する。失敗や skipped を成功扱いしない。
4. 品質が後続フェーズ検証で設定・実行ログを再確認するまで REQ-07 の CI 部分は未検証のままとする。

手順のチェックリスト: [01-USER-SETUP.md](./01-USER-SETUP.md)。

## 前 PLAN からの観察事項（未修正）

01-03 の品質合格時に持ち越された、読み取り専用試験の継承 `GIT_*`（特に `GIT_INDEX_FILE`）とグローバル Git 設定の隔離、非 UTF-8 stdout の観察はこの文書タスクでは修正しない。フェーズ検証へ渡す。コード・テストファイルは本 PLAN では変更していない。
