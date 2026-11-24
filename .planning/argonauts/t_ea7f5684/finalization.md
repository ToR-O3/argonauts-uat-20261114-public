# 最終化の確認（Builder）

対象: r-774f3cd6 / ToR-O3/argonauts-uat-20261114-public#15 / argonauts/r-774f3cd6。
開始head: b0f7291d759d923a1d1b9f055db1661572a47c82。最終headは同カードのrequest_review metadataに記録する。

## 判断と範囲

受付の最新原文、日時 2026-11-24T15:29:52.610474+00:00: 「(a) 4項目とも pass とする。」
仕様判断 2026-11-24T13:00:38.567271+00:00: 「②を選ぶ。description を新設してよい。連結元の文字列は「argonauts-uat public」、完成値は「argonauts-uat public (UAT)」とする。」
受入t_ce851077のapprovedを親の完了引継ぎで確認。指定連結元は観測旧値ではない。
危険なパスpyproject.tomlへの変更のため受付lightよりfullを優先。最終品質・報告にもこの理由を保持する。
元PLANのREQ-23 edge/unresolved・transparencyを改変しない。人のUAT1/2 passを参照。
報告後gateのexit1/INDEX_SCOPE（他24 PASS）は人のUAT3 passで既知工程pathとして受入済み。成功へ置換せず、hash固定registryを再固定しない。最終化の新しいarchive/sync/本記録の差分はこの記録で別途確認する。

## 実行結果

- originは固定repoと一致、依頼branch最新headへ合わせた。`git fetch origin`成功。`.planning`存在。baseのworkflow差分なし、`git merge --no-edit origin/v112-b`はAlready up to date。
- `openspec archive r-774f3cd6-pyproject-uat --json`: exit1、archive_confirmation_required（1 specの同期確認のみ）。
- `openspec archive r-774f3cd6-pyproject-uat --yes --json`: exit0、archivedAs=2026-11-25-r-774f3cd6-pyproject-uat、specsUpdated=true、added4/modified0/removed0/renamed0。
- archiveの全5原本（.openspec.yaml/design/proposal/tasks/specs/package-metadata/spec.md）を開始HEADの原本と`git show | cmp`で比較し全件exit0。旧active changeディレクトリ不存在をtestで確認。同期仕様はopenspec/specs/package-metadata/spec.md。製品は編集していない。
- `openspec validate --all --json`: exit0、3 spec passed/0 failed。package-metadata issues=[]。既存wordfreq-cliにRFC2119表現WARNING3（今回変更せず）。
- `gh pr ready argonauts/r-774f3cd6`成功、同branchのPR再読でOPEN/isDraft=false/head=b0f7291…/number15を確認。その後に最終commit/pushを行う。
- `python3 -B .planning/argonauts/r-774f3cd6/test_verify_description.py -v`: exit0、18 tests、3.301s、OK。
- `python3 -B .planning/argonauts/r-774f3cd6/verify_description.py content --baseline b34cba0d008923e7f5267ce52d5403492ea53925 --candidate pyproject.toml`: exit0、11条件すべてPASS、failures=[]。TOML全体解析、完成値完全一致、description除去後の構造・許可1行除去後のraw bytes不変を確認。
- `uv run --offline --no-project --with pytest python -B -m pytest -q -p no:cacheprovider`: exit0、702 passed in 203.68s。依存/製品試験/CIは変更せず、既存キャッシュを使用したBuilder実行であり独立品質結果ではない。
- `git diff --exit-code b0f7291… -- pyproject.toml`: exit0。`git diff --check`: exit0。
- `sha256sum pyproject.toml`: 540df8d5bf689fd037f73e336faa5ea05aa809699635472f47dd414dc3afb7e0（固定製品hashと一致）。
- baseline b34cba0…から開始HEADの全製品差分はM pyproject.tomlのみ。最終化の変更はopenspec/と本工程記録のみ。

## 品質へ渡す注意

最終headで内容・製品不変・archive/sync・本記録を独立確認する。旧registryのrepository gateはarchive等の新工程pathも未登録として失敗し得るため、実測exitと失敗IDをそのまま報告し製品不合格・成功のどちらにも偽装しない。最終化の工程pathを固定registryへ追加する判断は行っていない。
PRの案内はBuilder下書き。品質が全件diff・必須CI（待たず1回）・危険判定・smart方針の予約/取消しを独立判断し、最終headの印を付ける。Builderは予約・印・承認・マージを実行しない。
