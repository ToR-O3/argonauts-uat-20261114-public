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

## 5. 01-05 follow-up — 2026-11-17（現在の状態）

上記 §1〜4 は 01-04 実測時点の履歴であり、削除・上書きしない。現在は **人の設定対応済み / 独立品質 CI 検証待ち**。workflow の新設を再度人へ依頼する段階ではない。

- **人対応済み（入力出所: fix-1 / カード）:** CI 対象 CPython **3.12** の選択と workflow 追加。commit `5c9d8fa37939fc5d011b0f2469fb3cd074c4b3f2`。
- **Builder の Git 読取り証拠（実行証拠ではない）:** `git show 5c9d8fa37939fc5d011b0f2469fb3cd074c4b3f2 -- .github/workflows/pytest.yml` と現行原本を照合。name/job `pytest`、`ubuntu-latest`、`actions/checkout@v4`、`actions/setup-python@v5` の `python-version: "3.12"`、`push` の `argonauts/**` と `pull_request`、`permissions: contents: read`、`python -m pip install pytest`、`python -m pytest` を確認。人commitから現行HEADへの同workflow差分は空（exit 0）。不一致なし。ただし Git 上の存在は Actions の成功を証明しない。
- **人報告のみ（Builder / architect は独立未検証）:** 上記歴史的commitに対して run `44017344659`（`pull_request`）、`44017344584`（`push`）が completed/success、43 passed。PR実行の実際のmerge SHAとの関連付けも品質が独立確認する。これらは後続の文書commitを含む最新headの成功証拠ではない。

### Task 1 のローカル証拠（CI とは別）

開始時点 snapshot は計画head `24391acbad9170e37fbc7cd24eda5f45a3beeb39`。以後の文書commitは別headとなる。既存環境で事前に全43件成功を確認後、Task 1 文書追記時点でも `python -m pytest` を実行する。終了時の実測は下の追記欄に記録する。新規コード・テスト・依存・workflow変更はない。文書の正確性はpytestでは検証されず、Builderが出所と差分を別途照合する。

Task 1 終了時実測（2026-11-17T04:59:31Z、ローカルのみ）:

```text
python --version
Python 3.14.9
python -m pytest
platform linux -- Python 3.14.9, pytest-9.2.0, pluggy-1.7.0
collected 43 items
tests/test_aggregator.py ....                                            [  9%]
tests/test_cli.py .....................                                  [ 58%]
tests/test_formatters.py ....                                            [ 67%]
tests/test_sources.py .....                                              [ 79%]
tests/test_sources_boundary.py ...                                       [ 86%]
tests/test_tokenizer.py ......                                           [100%]
43 passed in 1.11s
```

終了コード0、failed/error/skipped 0、全43件欠落なし。`git diff --check` exit 0。差分は両文書への追記のみで過去測定・過去未完チェックを保持。人対応済み・人報告・品質未検証を原本と照合した。CI版3.12の実行証拠ではない。

### 残余 gate と失敗経路

REQ-07 は **Pending**、元の `01-VERIFICATION.md` は **gaps_found** のまま。OpenSpec task 3.3 の既存チェックは有無確認と引継ぎ準備の完了であり、CI合格ではない。

品質は自分のレビュー境界で最新の依頼branch headを解決し、手元HEADと照合してローカル全試験を独立実行する。それとは別に、対象headに結びつく Actions workflow/job/event、CPython 3.12 setupログ、実際のpytest全43件成功・failed 0・exit 0を有限回の読取りで確認する。不足、pending、権限拒否、ログ不可、head不一致、失敗、skip、Python不一致、0件なら未達を保持して結果を返し、待たない。workflow不一致や修正の必要は人対応へ戻し、Botはworkflow・権限・依存を変更せず、dispatchやpollingもしない。

Task 2 の明示出力: [ci-handoff.md](../../argonauts/t_0d6af354/ci-handoff.md)（Task 1 終了時は作成予定、Task 2 で作成）。同一カードの品質レビュー後、後続のフェーズ検証が全先行PLANも再検証する。BuilderはREQ-07 checkbox、VERIFICATION判定、phase完了を更新しない。
